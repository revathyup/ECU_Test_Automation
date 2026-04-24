from __future__ import annotations

from dataclasses import dataclass, field

from nordic_ecu_lab.protocol import (
    BusEvent,
    DiagnosticRequest,
    DiagnosticResponse,
    NegativeResponseCode,
    Session,
)


@dataclass
class BodyControlEcu:
    software_version: str = "BCM-SE-0.1.0"
    session: Session = Session.DEFAULT
    voltage_v: float = 12.4
    temperature_c: float = 28.0
    ignition_on: bool = False
    driver_door_open: bool = False
    welcome_light_ms: int = 5000
    _dtcs: set[str] = field(default_factory=set)
    _bus_events: list[BusEvent] = field(default_factory=list)
    _responsive: bool = True

    def handle(self, request: DiagnosticRequest) -> DiagnosticResponse | None:
        self._evaluate_faults()
        if not self._responsive:
            return None

        payload = request.payload or {}
        service = request.service

        if service == "session_control":
            return self._session_control(str(payload.get("session", "")))
        if service == "read_version":
            return DiagnosticResponse.ok(service, software_version=self.software_version)
        if service == "read_dtc":
            return DiagnosticResponse.ok(service, dtcs=sorted(self._dtcs))
        if service == "clear_dtc":
            self._dtcs.clear()
            self._evaluate_faults()
            return DiagnosticResponse.ok(service, remaining_dtcs=sorted(self._dtcs))
        if service == "write_config":
            return self._write_config(payload)
        if service == "read_signals":
            return DiagnosticResponse.ok(service, **self.signals)
        if service == "soft_reset":
            self.session = Session.DEFAULT
            self._evaluate_faults()
            return DiagnosticResponse.ok(service, reset="soft")

        return DiagnosticResponse.reject(service, NegativeResponseCode.UNKNOWN_COMMAND)

    @property
    def signals(self) -> dict[str, int | float | bool]:
        return {
            "voltage_v": round(self.voltage_v, 2),
            "temperature_c": round(self.temperature_c, 1),
            "ignition_on": self.ignition_on,
            "driver_door_open": self.driver_door_open,
            "welcome_light_ms": self.welcome_light_ms,
        }

    def set_input(self, name: str, value: float | bool) -> None:
        if not hasattr(self, name):
            raise ValueError(f"unknown ECU input: {name}")
        setattr(self, name, value)
        self._evaluate_faults()
        self._publish_signal_update(name)

    def set_responsive(self, responsive: bool) -> None:
        self._responsive = responsive

    def pop_bus_events(self) -> list[BusEvent]:
        events = list(self._bus_events)
        self._bus_events.clear()
        return events

    def _session_control(self, requested: str) -> DiagnosticResponse:
        if requested == Session.EXTENDED.value:
            self.session = Session.EXTENDED
            return DiagnosticResponse.ok("session_control", session=self.session.value)
        if requested == Session.DEFAULT.value:
            self.session = Session.DEFAULT
            return DiagnosticResponse.ok("session_control", session=self.session.value)
        return DiagnosticResponse.reject(
            "session_control", NegativeResponseCode.REQUEST_OUT_OF_RANGE
        )

    def _write_config(self, payload: dict[str, object]) -> DiagnosticResponse:
        if self.session is not Session.EXTENDED:
            return DiagnosticResponse.reject(
                "write_config", NegativeResponseCode.SECURITY_ACCESS_DENIED
            )

        value = int(payload.get("welcome_light_ms", self.welcome_light_ms))
        if not 1000 <= value <= 30000:
            return DiagnosticResponse.reject(
                "write_config", NegativeResponseCode.REQUEST_OUT_OF_RANGE
            )

        self.welcome_light_ms = value
        self._publish_signal_update("welcome_light_ms")
        return DiagnosticResponse.ok("write_config", welcome_light_ms=value)

    def _evaluate_faults(self) -> None:
        if self.voltage_v < 9.0:
            self._dtcs.add("B1325_UNDERVOLTAGE")
        elif "B1325_UNDERVOLTAGE" in self._dtcs:
            self._dtcs.remove("B1325_UNDERVOLTAGE")

        if self.temperature_c > 95.0:
            self._dtcs.add("B1001_OVERTEMPERATURE")
        elif "B1001_OVERTEMPERATURE" in self._dtcs:
            self._dtcs.remove("B1001_OVERTEMPERATURE")

    def _publish_signal_update(self, changed_signal: str) -> None:
        self._bus_events.append(
            BusEvent(
                arbitration_id=0x321,
                name="BCM_STATUS",
                signals={"changed": changed_signal, **self.signals},
            )
        )
