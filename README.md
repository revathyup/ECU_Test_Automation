# ECU Test Automation Lab

This repository is a small learning lab for embedded ECU-style test automation.

The focus is on test design, validation strategy, and automation practice rather than hardware-specific implementation. The project uses a software-based ECU model so the tests can run locally or in CI, while keeping the structure close to a setup that could later be connected to real hardware.

---

## Objectives

The project explores:

* Systematic test design for embedded systems
* Validation of ECU-like behavior using software-based simulation
* Separation of system under test and test harness
* Fault injection and robustness testing
* Traceability between requirements and test cases
* Automated test execution and reporting

---

## Key Features

* Pytest-based automation framework for structured and repeatable testing
* Simulated ECU model with diagnostic-style interactions
* Protocol abstraction layer for request and response handling
* HIL/SIL-style controller interface for test orchestration
* Fault injection capabilities, including:

  * voltage anomalies
  * temperature faults
  * communication failures
  * watchdog-related issues

* Requirements-to-test traceability mapping
* CI integration using GitHub Actions with JUnit-style reporting

---

## Testing Approach

The project follows a simplified embedded validation workflow:

1. Define expected system behavior through requirements
2. Model ECU functionality in software
3. Design test cases aligned with requirements
4. Execute tests under normal and fault conditions
5. Validate outputs and system responses
6. Generate reproducible test results

The goal is to keep the setup lightweight while still showing how automated validation can be organized around embedded behavior.

---

## Quick Start

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements-dev.txt
pytest
```

On Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
pytest
```

### Run Demo

```bash
python scripts/run_demo.py
```

---

## Project Structure

```text
src/nordic_ecu_lab/
  ecu.py          Simulated ECU behavior
  hil.py          Test controller abstraction (HIL/SIL style)
  protocol.py     Diagnostic command/response models
  reporting.py    Test evidence and reporting helpers

tests/
  test_diagnostics.py
  test_fault_injection.py
  test_requirements_traceability.py

docs/
  TEST_STRATEGY.md
  REQUIREMENTS.md

.github/workflows/
  ci.yml
```

---

## Simulated ECU Capabilities

The ECU model supports:

* Session control
* Reading software information
* Diagnostic trouble code handling
* Configuration updates
* ECU reset behavior
* Monitoring of system signals such as voltage, temperature, and inputs

---

## Fault Injection

The framework allows controlled fault scenarios such as:

* Undervoltage conditions
* Overtemperature conditions
* Input signal faults
* Communication timeouts
* Watchdog-related failures

These scenarios are used to study robustness and error handling.

---

## Scope and Limitations

* This project uses a software-based ECU model and does not interface with real hardware
* Communication protocols are simplified abstractions, not full standard implementations
* The focus is on testing methodology, not production-level ECU development

---

## Future Extensions

* Integration with real hardware through CAN, UART, or embedded targets
* Expansion of protocol coverage
* Advanced reporting and coverage metrics
* Hardware-in-the-loop execution through external runners

---

## Summary

This project is a foundation for studying automated ECU validation concepts such as traceability, fault injection, and repeatable test execution.
