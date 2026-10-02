from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


STATUSES = {
    "PASS", "FAIL_TECHNICAL", "NOT_EVALUABLE", "NOT_APPLICABLE",
    "INSPECTION_ERROR", "HUMAN_REVIEW_REQUIRED",
}


@dataclass(frozen=True)
class Finding:
    finding_id: str
    rule_id: str
    rule_version: str
    authority: str
    requirement_id: str | None
    source_file: str
    object_type: str | None
    object_id: str | None
    locator: str
    observed: Any
    expected: Any
    status: str
    severity: str
    evidence: dict[str, Any] = field(default_factory=dict)
    recommendation: str = ""
    provenance: str = ""

    def __post_init__(self) -> None:
        if self.status not in STATUSES:
            raise ValueError(f"Unsupported finding status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
