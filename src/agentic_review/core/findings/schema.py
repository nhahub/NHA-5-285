"""Schema generation — the tool schema and the report schema both derive from the Pydantic models (research R-11, R-22)."""

from __future__ import annotations

import copy
from typing import Any

from agentic_review.core.findings.model import FindingDraft
from agentic_review.core.findings.report import ReviewReport

SCHEMA_VERSION = "1.0"
"""Hand-set, never derived from the package version: a patch release must not renumber the schema (02 §4)."""

TOOL_NAME = "emit_finding"
TOOL_DESCRIPTION = "Report one review finding. This is the ONLY way a finding is recorded; prose is discarded."

REPORT_SCHEMA_ID = f"https://agentic-review.invalid/schemas/review-report/{SCHEMA_VERSION}.json"
REPORT_SCHEMA_DESCRIPTION = (
    f"agentic-review review report, schema version {SCHEMA_VERSION}. "
    "Consumers must ignore unknown fields: minor versions add fields without changing existing ones."
)


def inline_refs(schema: dict[str, Any]) -> dict[str, Any]:
    """Resolve every ``$ref`` against ``$defs``, then drop ``$defs``, ``title`` noise and null defaults.

    Some OpenAI-compatible backends fail on ``$ref`` inside tool parameters, so the tool schema is sent inlined.
    """
    defs = schema.get("$defs", {})

    def walk(node: Any, *, is_properties: bool = False) -> Any:
        if isinstance(node, list):
            return [walk(item) for item in node]
        if not isinstance(node, dict):
            return node
        if is_properties:
            return {name: walk(value) for name, value in node.items()}
        if "$ref" in node:
            target = node["$ref"].removeprefix("#/$defs/")
            merged = {**copy.deepcopy(defs[target]), **{k: v for k, v in node.items() if k != "$ref"}}
            return walk(merged)
        result: dict[str, Any] = {}
        for key, value in node.items():
            if key in ("$defs", "title"):
                continue
            if key == "default" and value is None:
                continue
            if key == "discriminator" and isinstance(value, dict):
                # The mapping points at $defs entries that no longer exist; the const `kind` of each arm remains.
                result[key] = {"propertyName": value["propertyName"]}
                continue
            result[key] = walk(value, is_properties=key == "properties")
        return result

    return walk(schema)


def tool_schema() -> dict[str, Any]:
    return inline_refs(FindingDraft.model_json_schema(by_alias=True))


def report_schema() -> dict[str, Any]:
    generated = ReviewReport.model_json_schema(by_alias=True, mode="serialization")
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": REPORT_SCHEMA_ID,
        **generated,
        "description": REPORT_SCHEMA_DESCRIPTION,
    }
