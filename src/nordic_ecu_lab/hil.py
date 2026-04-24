from __future__ import annotations

from dataclasses import dataclass
from time import monotonic, sleep

from nordic_ecu_lab.ecu import BodyControlEcu
from nordic_ecu_lab.protocol import DiagnosticRequest, DiagnosticResponse, NegativeResponseCode


class HilTimeoutError(TimeoutError):
    pass


@dataclass
class HilController:
    ecu: BodyControlEcu
    timeout_s: float = 0.05
    poll_interval_s: float = 0.001

    def send(self, service: str, **payload: object) -> DiagnosticResponse:
        deadline = monotonic() + self.timeout_s
        request = DiagnosticRequest(service=service, payload=payload)

        while monotonic() < deadline:
            response = self.ecu.handle(request)
            if response is not None:
                return response
            sleep(self.poll_interval_s)

        raise HilTimeoutError(f"ECU did not respond to {service!r}")

    def inject_fault(self, fault: str) -> None:
        if fault == "undervoltage":
            self.ecu.set_input("voltage_v", 8.4)
        elif fault == "overtemperature":
            self.ecu.set_input("temperature_c", 102.0)
        elif fault == "stuck_driver_door":
            self.ecu.set_input("driver_door_open", True)
        elif fault == "communication_timeout":
            self.ecu.set_responsive(False)
        else:
            raise ValueError(f"unknown fault: {fault}")

    def recover_fault(self, fault: str) -> None:
        if fault == "undervoltage":
            self.ecu.set_input("voltage_v", 12.2)
        elif fault == "overtemperature":
            self.ecu.set_input("temperature_c", 35.0)
        elif fault == "stuck_driver_door":
            self.ecu.set_input("driver_door_open", False)
        elif fault == "communication_timeout":
            self.ecu.set_responsive(True)
        else:
            raise ValueError(f"unknown fault: {fault}")

    def safe_send(self, service: str, **payload: object) -> DiagnosticResponse:
        try:
            return self.send(service, **payload)
        except HilTimeoutError:
            return DiagnosticResponse.reject(
                service, NegativeResponseCode.TIMEOUT, message="harness timeout"
            )
