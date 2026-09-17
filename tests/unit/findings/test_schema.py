"""One definition, not two (SRS §5): the tool schema and the report schema are generated — research R-11, R-22."""

from __future__ import annotations

import json
from typing import Any

from jsonschema import Draft202012Validator

from agentic_review.core.findings.model import FindingDraft
from agentic_review.core.findings.schema import SCHEMA_VERSION, inline_refs, report_schema, tool_schema

ALL_DEGRADATION_CODES = {
    "no-index",
    "unresolvable-imports",
    "parse-error",
    "budget-exhausted",
    "checks-unrunnable",
    "execution-timed-out",
    "provider-error",
    "invalid-model-output",
    "no-tool-call",
    "tool-budget-exhausted",
}


def _keys(node: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            found.add(key)
            found |= _keys(value)
    elif isinstance(node, list):
        for item in node:
            found |= _keys(item)
    return found


def test_inline_refs_leaves_no_refs_defs_or_titles() -> None:
    keys = _keys(tool_schema())
    assert not keys & {"$ref", "$defs", "title"}


def test_tool_schema_is_the_transform_of_the_model_schema() -> None:
    assert tool_schema() == inline_refs(FindingDraft.model_json_schema(by_alias=True))


def test_tool_schema_matches_the_contract() -> None:
    schema = tool_schema()
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {"file", "startLine", "endLine", "severity", "category", "rationale", "evidence"}
    assert schema["properties"]["severity"]["enum"] == ["blocking", "important", "nit"]
    assert len(schema["properties"]["category"]["enum"]) == 7
    assert schema["properties"]["ruleId"] == {"type": "string"}
    arms = schema["properties"]["evidence"]["oneOf"]
    assert sorted(arm["properties"]["kind"]["const"] for arm in arms) == ["check", "context", "diff", "unverified"]
    assert all(arm["additionalProperties"] is False for arm in arms)
    Draft202012Validator.check_schema(schema)


def test_report_schema_is_versioned_and_valid() -> None:
    schema = report_schema()
    Draft202012Validator.check_schema(schema)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert SCHEMA_VERSION == "1.0" and "1.0" in schema["$id"]
    assert "ignore unknown fields" in schema["description"]
    assert "degradations" in schema["required"]


def test_report_schema_empty_sections_and_null_depths() -> None:
    schema = report_schema()
    defs = schema["$defs"]
    assert schema["properties"]["context"]["maxItems"] == 0
    assert defs["EvidenceRecord"]["properties"]["checks"]["maxItems"] == 0
    depth = defs["RunMetadata"]["properties"]["requestedDepth"]
    assert {"type": "null"} in depth["anyOf"]
    assert "not gathered" in depth["description"]


def test_report_schema_lists_every_degradation_code() -> None:
    text = json.dumps(report_schema())
    code_schema = report_schema()["$defs"]["Degradation"]["properties"]["code"]
    assert set(code_schema["enum"]) == ALL_DEGRADATION_CODES
    assert "credential" not in text.lower() and "apikey" not in text.lower()
