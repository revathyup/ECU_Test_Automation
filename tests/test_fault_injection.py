from __future__ import annotations

import pytest

from nordic_ecu_lab import HilTimeoutError


@pytest.mark.req("REQ-DTC-001")
def test_undervoltage_sets_and_clears_dtc(hil):
    hil.inject_fault("undervoltage")
    faulted = hil.send("read_dtc")

    hil.recover_fault("undervoltage")
    recovered = hil.send("read_dtc")

    assert "B1325_UNDERVOLTAGE" in faulted.payload["dtcs"]
    assert "B1325_UNDERVOLTAGE" not in recovered.payload["dtcs"]


@pytest.mark.req("REQ-DTC-002")
def test_overtemperature_fault_is_reported(hil):
    hil.inject_fault("overtemperature")
    response = hil.send("read_dtc")

    assert response.positive
    assert response.payload["dtcs"] == ["B1001_OVERTEMPERATURE"]


@pytest.mark.req("REQ-DTC-003")
def test_soft_reset_preserves_active_faults(hil):
    hil.inject_fault("undervoltage")
    reset = hil.send("soft_reset")
    dtcs = hil.send("read_dtc")

    assert reset.positive
    assert "B1325_UNDERVOLTAGE" in dtcs.payload["dtcs"]


@pytest.mark.req("REQ-COM-001")
def test_timeout_is_reported_as_harness_failure(hil):
    hil.inject_fault("communication_timeout")

    with pytest.raises(HilTimeoutError):
        hil.send("read_version")

    safe_response = hil.safe_send("read_version")
    assert not safe_response.positive
    assert safe_response.payload["message"] == "harness timeout"
