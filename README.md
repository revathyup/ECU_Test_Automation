# ECU Test Automation Lab

This repository presents a structured test automation framework for validating embedded automotive software concepts in a controlled, reproducible environment.

The focus of the project is on **test design, validation strategy, and automation practices**, rather than hardware-specific implementation. The framework is intentionally hardware-independent, allowing the same testing concepts to be applied later to real ECU systems.

---

## Objectives

The project is designed to demonstrate:

* Systematic test design for embedded systems
* Validation of ECU-like behavior using software-based simulation
* Separation of system under test (SUT) and test harness
* Fault injection and robustness testing
* Traceability between requirements and test cases
* Automated test execution and reporting

---

## Key Features

* **Pytest-based automation framework** for structured and repeatable testing
* **Simulated ECU model** implementing diagnostic-style interactions
* **Protocol abstraction layer** inspired by UDS-like workflows
* **HIL/SIL-style controller interface** for test orchestration
* **Fault injection capabilities**, including:

  * voltage anomalies
  * temperature faults
  * communication failures
  * watchdog-related issues
* **Requirements-to-test traceability mapping**
* **CI integration** using GitHub Actions with JUnit-style reporting

---

## Testing Approach

The project follows a simplified but representative embedded validation workflow:

1. Define system behavior through requirements
2. Model ECU functionality in software
3. Design test cases aligned with requirements
4. Execute tests under normal and fault conditions
5. Validate outputs and system responses
6. Generate reproducible test results

The goal is to reflect how validation is performed in real embedded systems while remaining lightweight and accessible.

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
* Diagnostic trouble code (DTC) handling
* Configuration updates
* ECU reset behavior
* Monitoring of system signals (voltage, temperature, inputs)

---

## Fault Injection

The framework allows controlled fault scenarios such as:

* Undervoltage conditions
* Overtemperature conditions
* Input signal faults
* Communication timeouts
* Watchdog-related failures

These scenarios enable validation of system robustness and error handling.

---

## Scope and Limitations

* This project uses a **software-based ECU model** and does not interface with real hardware
* Communication protocols are **simplified abstractions**, not full standard implementations
* The focus is on **testing methodology**, not production-level ECU development

---

## Future Extensions

* Integration with real hardware (CAN, UART, or embedded targets)
* Expansion of protocol coverage (full UDS services)
* Advanced reporting and coverage metrics
* Hardware-in-the-loop (HIL) execution via external runners

---

## Summary

This project demonstrates how structured testing principles—such as automation, traceability, and fault-based validation—can be applied to embedded systems in a clear and reproducible way.

It is intended as a foundation for understanding and building more advanced ECU validation setups.
