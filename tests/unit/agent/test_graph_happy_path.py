"""The review step on its main path — FR-013, FR-015, FR-018, FR-021; research R-13, R-14, R-16."""

from __future__ import annotations

import json

from langchain_core.messages import ToolMessage

from agentic_review.core.findings.schema import SCHEMA_VERSION
from tests.unit.agent.conftest import CONTEXT, PortFactory
from tests.support.scripted_chat_model import ai_reply, finding_call, invalid_json_call


def test_two_valid_calls_become_two_findings(make_port: PortFactory) -> None:
    calls = [finding_call(severity="important"), finding_call(severity="nit", startLine=3, endLine=5)]
    port, model = make_port([ai_reply(calls, usage=(1200, 80))])
    outcome = port.review(CONTEXT)

    assert model.call_count == 1
    assert [f.id for f in outcome.findings] == ["f-1", "f-2"]
    assert [f.severity for f in outcome.findings] == ["important", "nit"]
    assert all(f.turn_index == 0 and f.schema_version == SCHEMA_VERSION for f in outcome.findings)
    assert all(len(f.fingerprint) == 12 for f in outcome.findings)
    assert outcome.completion_status == "emitted" and outcome.degradations == ()
    assert (outcome.tool_calls_total, outcome.tool_calls_emission, outcome.tool_calls_investigation) == (2, 2, 0)
    assert outcome.repair_turns == 0
    assert (outcome.tokens_in, outcome.tokens_out) == (1200, 80)
    assert outcome.model == "meta/llama-3.3-70b-instruct" and outcome.provider == "integrate.api.nvidia.com"

    observations = [m for m in port.last_transcript if isinstance(m, ToolMessage)]
    assert [m.tool_call_id for m in observations] == [c["id"] for c in calls]
    assert [json.loads(m.content) for m in observations] == [
        {"status": "ok", "reason": None, "content": "accepted as f-1"},
        {"status": "ok", "reason": None, "content": "accepted as f-2"},
    ]


def test_prose_is_discarded_and_no_call_is_recorded(make_port: PortFactory) -> None:
    prose = 'I found one issue: {"file": "src/app.ts", "startLine": 1, "endLine": 1, "severity": "blocking"}'
    port, _ = make_port([ai_reply(content=prose)])
    outcome = port.review(CONTEXT)
    assert outcome.findings == ()
    assert outcome.completion_status == "no-tool-call"
    assert [(d.source, d.code) for d in outcome.degradations] == [("CF-6", "no-tool-call")]
    assert outcome.tool_calls_total == 0


def test_tokens_are_none_when_not_reported(make_port: PortFactory) -> None:
    port, _ = make_port([ai_reply([finding_call()])])
    outcome = port.review(CONTEXT)
    assert (outcome.tokens_in, outcome.tokens_out) == (None, None)


def test_rejected_and_invalid_json_calls_get_error_observations(make_port: PortFactory) -> None:
    calls = [finding_call(), finding_call(file="src/nope.ts")]
    bad_json = invalid_json_call()
    port, _ = make_port([ai_reply(calls, invalid_tool_calls=[bad_json]), ai_reply()])
    outcome = port.review(CONTEXT)

    assert [f.id for f in outcome.findings] == ["f-1"]
    assert outcome.tool_calls_total == 3 and outcome.tool_calls_emission == 3
    by_id = {m.tool_call_id: json.loads(m.content) for m in port.last_transcript if isinstance(m, ToolMessage)}
    assert by_id[calls[1]["id"]]["status"] == "error"
    assert by_id[calls[1]["id"]]["reason"].startswith("file: 'src/nope.ts' was not part of this review")
    assert by_id[bad_json["id"]] == {"status": "error", "reason": "arguments: not valid JSON", "content": None}
