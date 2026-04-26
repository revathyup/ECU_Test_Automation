# Test Strategy

## Goal

Prove that an embedded ECU test framework can validate diagnostics, signals, fault handling, and traceability before real hardware is available.

## Test Levels

| Level | Runs In This Repo | Purpose |
| --- | --- | --- |
| SIL | Yes | Fast regression tests against an ECU simulator. |
| HIL adapter | Yes, simulated | Same controller interface that can later wrap UART, CAN, relay, or debugger tools. |
| Real HIL | Documented extension | Run on a self-hosted runner connected to an ECU or development board. |

## Automation Stack

- `pytest` for test execution
- Python fixtures for ECU setup and fault injection
- JUnit XML output for CI systems
- Requirement markers for traceability

## Fault Model

The suite includes deliberate negative tests:

- undervoltage
- overtemperature
- stuck input
- diagnostic command rejected in wrong session
- communication timeout
- reset behavior with active faults

## Learning Context

The examples combine several common embedded testing topics:

- HIL/SIL regression testing
- ECU diagnostics and fault-code validation
- Python automation
- CAN-like signal observation
- CI evidence for release readiness
- requirement-based test design
