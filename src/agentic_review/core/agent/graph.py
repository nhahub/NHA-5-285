"""The review step's graph (research R-12, R-14, data-model §5).

``call_model`` sends the conversation; ``process_calls`` validates each tool call in order and answers every call with
exactly one structured observation. No checkpointer: state is built fresh for every review (FR-5.1).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, TypedDict

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.runnables import Runnable
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agentic_review.core.agent.accounting import CallAccounting
from agentic_review.core.assembly.prompt import user_message
from agentic_review.core.findings.model import ToolObservation
from agentic_review.core.findings.port import ReviewContext
from agentic_review.core.findings.report import CompletionStatus, Degradation
from agentic_review.core.findings.validation import Accepted, Rejected, invalid_json_rejection, validate_call

NO_TOOL_CALL_DETAIL = (
    "The model replied without calling emit_finding. With emit_finding as its only tool, this build cannot tell a "
    "change with nothing to report from a model that did not use the finding tool."
)


@dataclass
class ReviewRun:
    context: ReviewContext
    messages: list[BaseMessage]
    accounting: CallAccounting = field(default_factory=CallAccounting)
    turn_index: int = 0
    calls_by_turn: list[int] = field(default_factory=list)
    rejected_by_turn: list[int] = field(default_factory=list)
    degradations: list[Degradation] = field(default_factory=list)


class ReviewState(TypedDict):
    run: ReviewRun


def build_graph(bound_model: Runnable[Any, BaseMessage] | BaseChatModel) -> CompiledStateGraph:
    def call_model(state: ReviewState) -> ReviewState:
        run = state["run"]
        reply = bound_model.invoke(run.messages)
        if not isinstance(reply, AIMessage):
            reply = AIMessage(content=str(getattr(reply, "content", "")))
        run.messages.append(reply)
        run.accounting.add_usage(reply.usage_metadata)
        return {"run": run}

    def process_calls(state: ReviewState) -> ReviewState:
        run = state["run"]
        reply = run.messages[-1]
        assert isinstance(reply, AIMessage)
        calls = 0
        rejected = 0
        for call in reply.tool_calls:
            calls += 1
            run.accounting.count_emission_call()
            result = validate_call(call["name"], call["args"], run.context.material)
            if isinstance(result, Accepted):
                finding = run.accounting.accept(result.draft, turn_index=run.turn_index)
                observation = ToolObservation(status="ok", content=f"accepted as {finding.id}")
            else:
                rejected += 1
                observation = ToolObservation(status="error", reason=result.reason)
            run.messages.append(_observation_message(observation, call.get("id")))
        for invalid in reply.invalid_tool_calls:
            calls += 1
            rejected += 1
            run.accounting.count_emission_call()
            observation = ToolObservation(status="error", reason=invalid_json_rejection().reason)
            run.messages.append(_observation_message(observation, invalid.get("id")))
        run.calls_by_turn.append(calls)
        run.rejected_by_turn.append(rejected)
        return {"run": run}

    graph = StateGraph(ReviewState)
    graph.add_node("call_model", call_model)
    graph.add_node("process_calls", process_calls)
    graph.set_entry_point("call_model")
    graph.add_edge("call_model", "process_calls")
    graph.add_edge("process_calls", END)
    return graph.compile()


def _observation_message(observation: ToolObservation, call_id: str | None) -> ToolMessage:
    return ToolMessage(content=json.dumps(observation.model_dump(mode="json")), tool_call_id=call_id or "")


def start_run(context: ReviewContext) -> ReviewRun:
    return ReviewRun(
        context=context,
        messages=[
            SystemMessage(content=context.instructions),
            HumanMessage(content=user_message(context.material_statement, context.diff_section)),
        ],
    )


def finish(run: ReviewRun) -> tuple[CompletionStatus, list[Degradation]]:
    """Completion status and degradations at END (research R-16, R-17)."""
    degradations = list(run.degradations)
    accepted = len(run.accounting.findings)
    if run.calls_by_turn and run.calls_by_turn[0] == 0:
        degradations.append(Degradation(source="CF-6", code="no-tool-call", detail=NO_TOOL_CALL_DETAIL))
        return "no-tool-call", degradations
    rejected = sum(run.rejected_by_turn)
    if rejected:
        degradations.append(
            Degradation(
                source="CF-6",
                code="invalid-model-output",
                detail=f"{rejected} emit_finding call(s) could not be validated; {accepted} finding(s) were accepted.",
            )
        )
        if accepted == 0:
            return "invalid-model-output", degradations
    return "emitted", degradations
