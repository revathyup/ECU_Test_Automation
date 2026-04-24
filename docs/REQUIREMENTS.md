# Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| REQ-DIAG-001 | ECU shall enter extended diagnostic session only with a valid session request. | `test_extended_session_unlocks_config_write` |
| REQ-DIAG-002 | ECU shall reject configuration writes in default session. | `test_config_write_is_rejected_in_default_session` |
| REQ-DTC-001 | ECU shall set undervoltage DTC when supply voltage is below 9.0 V. | `test_undervoltage_sets_and_clears_dtc` |
| REQ-DTC-002 | ECU shall set overtemperature DTC when internal temperature exceeds 95 C. | `test_overtemperature_fault_is_reported` |
| REQ-DTC-003 | ECU shall preserve active DTCs across a soft reset. | `test_soft_reset_preserves_active_faults` |
| REQ-COM-001 | Test harness shall fail fast when the ECU does not respond before timeout. | `test_timeout_is_reported_as_harness_failure` |
| REQ-SIG-001 | ECU shall publish CAN-like signal updates when inputs change. | `test_signal_change_generates_bus_event` |
| REQ-TRACE-001 | Every automated test shall declare at least one requirement ID. | `test_all_tests_have_requirement_markers` |
