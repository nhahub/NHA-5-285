"""The finding model — what the model may emit, and what the system accepts (data-model §3, FR-014).

``FindingDraft`` is the single definition behind the ``emit_finding`` tool schema, the ``findings`` section of the
report schema, and call validation (SRS §5: one definition, not two).
"""

from __future__ import annotations

from typing import Annotated, Any, ClassVar, Literal

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer,
    model_validator,
)
from pydantic.alias_generators import to_camel
from pydantic.json_schema import SkipJsonSchema
from pydantic_core import PydanticCustomError

Severity = Literal["blocking", "important", "nit"]
Category = Literal[
    "correctness",
    "error-handling",
    "interface-contract",
    "test-evidence",
    "security",
    "performance",
    "maintainability",
]


def _optional_str(value: Any) -> Any:
    # Checked before the `str | None` union, so a bad value yields one error at the field, not one per union branch.
    if value is not None and not isinstance(value, str):
        raise PydanticCustomError("string_type", "Input should be a valid string")
    return value


def _optional_non_negative_int(value: Any) -> Any:
    if value is None:
        return value
    if isinstance(value, bool) or not isinstance(value, int):
        raise PydanticCustomError("int_type", "Input should be a valid integer")
    if value < 0:
        raise PydanticCustomError("greater_than_equal", "Input should be greater than or equal to 0")
    return value


class WireModel(BaseModel):
    """camelCase on the wire, snake_case in Python; optional fields listed in ``_omit_when_none`` are left out."""

    model_config = ConfigDict(
        extra="forbid",
        alias_generator=to_camel,
        validate_by_name=True,
        validate_by_alias=True,
        frozen=True,
    )

    _omit_when_none: ClassVar[frozenset[str]] = frozenset()

    @model_serializer(mode="wrap")
    def _omit_absent(self, handler: SerializerFunctionWrapHandler):  # noqa: ANN202 - no annotation keeps the model schema
        data = handler(self)
        if isinstance(data, dict) and self._omit_when_none:
            for name in self._omit_when_none:
                for key in (name, to_camel(name)):
                    if key in data and data[key] is None:
                        del data[key]
        return data


class CheckEvidence(WireModel):
    _omit_when_none = frozenset({"failing_test"})

    kind: Literal["check"]
    check_id: Literal["tests", "typecheck"]
    failing_test: Annotated[str | SkipJsonSchema[None], BeforeValidator(_optional_str)] = None


class ContextEvidence(WireModel):
    kind: Literal["context"]
    file: Annotated[str, Field(min_length=1)]
    start_line: Annotated[int, Field(ge=1)]
    end_line: Annotated[int, Field(ge=1)]


class DiffEvidence(WireModel):
    _omit_when_none = frozenset({"hunk_index"})

    kind: Literal["diff"]
    file: Annotated[str, Field(min_length=1)]
    hunk_index: Annotated[
        int | SkipJsonSchema[None],
        BeforeValidator(_optional_non_negative_int),
        Field(json_schema_extra={"minimum": 0}),
    ] = None


class UnverifiedEvidence(WireModel):
    kind: Literal["unverified"]
    reason: Annotated[str, Field(min_length=1)]


EvidenceRef = Annotated[
    CheckEvidence | ContextEvidence | DiffEvidence | UnverifiedEvidence,
    Field(discriminator="kind"),
]


class FindingDraft(WireModel):
    """Exactly what the model may emit through ``emit_finding`` (contracts/emit-finding.md)."""

    _omit_when_none = frozenset({"rule_id"})

    file: Annotated[str, Field(min_length=1)]
    start_line: Annotated[int, Field(ge=1)]
    end_line: Annotated[int, Field(ge=1)]
    severity: Severity
    category: Category
    rationale: Annotated[str, Field(min_length=1)]
    rule_id: Annotated[str | SkipJsonSchema[None], BeforeValidator(_optional_str)] = None
    evidence: EvidenceRef

    @field_validator("rationale")
    @classmethod
    def _rationale_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise PydanticCustomError("blank", "must contain text other than whitespace")
        return value

    @model_validator(mode="after")
    def _end_not_before_start(self) -> FindingDraft:
        if self.end_line < self.start_line:
            raise PydanticCustomError("end_before_start", "must be greater than or equal to startLine")
        return self


class Finding(FindingDraft):
    """A draft the system accepted, plus the fields the model cannot set (data-model §3)."""

    # Report consumers must ignore unknown fields, so the published finding does not forbid them.
    model_config = ConfigDict(extra="ignore")

    id: str
    schema_version: str
    turn_index: Annotated[int, Field(ge=0)]
    fingerprint: Annotated[str, Field(pattern=r"^[0-9a-f]{12}$")]


class ToolObservation(WireModel):
    """The structured result handed back to the model for every tool call (FR-015 / FR-5.9)."""

    status: Literal["ok", "error", "denied"]
    reason: str | None = None
    content: str | None = None

    @model_validator(mode="after")
    def _reason_when_not_ok(self) -> ToolObservation:
        if self.status != "ok" and not self.reason:
            raise ValueError("reason is required when status is not ok")
        return self
