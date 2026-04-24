from __future__ import annotations

import pytest

from nordic_ecu_lab.protocol import NegativeResponseCode


@pytest.mark.req("REQ-DIAG-001")
def test_extended_session_unlocks_config_write(hil):
    session = hil.send("session_control", session="extended")
    response = hil.send("write_config", welcome_light_ms=8000)

    assert session.positive
    assert response.positive
    assert response.payload["welcome_light_ms"] == 8000


@pytest.mark.req("REQ-DIAG-002")
def test_config_write_is_rejected_in_default_session(hil):
    response = hil.send("write_config", welcome_light_ms=8000)

    assert not response.positive
    assert response.code is NegativeResponseCode.SECURITY_ACCESS_DENIED


@pytest.mark.req("REQ-SIG-001")
def test_signal_change_generates_bus_event(ecu, hil):
    hil.send("session_control", session="extended")
    hil.send("write_config", welcome_light_ms=12000)

    events = ecu.pop_bus_events()

    assert events
    assert events[-1].name == "BCM_STATUS"
    assert events[-1].signals["changed"] == "welcome_light_ms"
    assert events[-1].signals["welcome_light_ms"] == 12000
