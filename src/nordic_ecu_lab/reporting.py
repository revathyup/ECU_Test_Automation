from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TestEvidence:
    requirement_id: str
    verdict: str
    note: str


def requirement_marker(requirement_id: str) -> str:
    if not requirement_id.startswith("REQ-"):
        raise ValueError("requirement IDs must start with REQ-")
    return requirement_id
