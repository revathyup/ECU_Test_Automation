from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class Session(str, Enum):
    DEFAULT = "default"
    EXTENDED = "extended"


class NegativeResponseCode(str, Enum):
    CONDITIONS_NOT_CORRECT = "conditions_not_correct"
    REQUEST_OUT_OF_RANGE = "request_out_of_range"
    SECURITY_ACCESS_DENIED = "security_access_denied"
    TIMEOUT = "timeout"
    UNKNOWN_COMMAND = "unknown_command"


@dataclass(frozen=True)
class DiagnosticRequest:
    service: str
    payload: dict[str, Any] | None = None


@dataclass(frozen=True)
class DiagnosticResponse:
    positive: bool
    service: str
    payload: dict[str, Any]
    code: NegativeResponseCode | None = None

    @classmethod
    def ok(cls, service: str, **payload: Any) -> "DiagnosticResponse":
        return cls(True, service, payload)

    @classmethod
    def reject(
        cls, service: str, code: NegativeResponseCode, **payload: Any
    ) -> "DiagnosticResponse":
        return cls(False, service, payload, code)


@dataclass(frozen=True)
class BusEvent:
    arbitration_id: int
    name: str
    signals: dict[str, int | float | str | bool]
