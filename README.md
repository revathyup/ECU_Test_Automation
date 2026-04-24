# ECU Test Automation Lab

The repo demonstrates a compact but realistic test setup:

- Python test automation with `pytest`
- ECU-style diagnostic commands inspired by UDS workflows
- CAN-like signal/event validation without paid tooling
- HIL/SIL-style device controller abstraction
- Fault injection for voltage, temperature, watchdog, and communication failures
- Requirement IDs mapped to automated tests
- GitHub Actions CI with JUnit test output

The project is hardware-free by default, so recruiters and interviewers can run it immediately. The same harness shape can later be connected to a real board through UART, CAN, or a self-hosted runner.

- Python and Pytest automation
- HIL/SIL testing
- ECU diagnostics, CAN, LIN, UDS, and automotive workflows
- CI/CD with Jenkins, GitLab, or GitHub Actions
- Test case design, traceability, reporting, and fault analysis

This project is built to show those skills in a clean, runnable form.

## Quick Start

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

Run the demo:

```bash
python scripts/run_demo.py
```

## Project Layout

```text
src/nordic_ecu_lab/
  ecu.py          Simulated body-control ECU
  hil.py          HIL/SIL controller abstraction
  protocol.py     Diagnostic command and response models
  reporting.py    Lightweight test evidence helpers
tests/
  test_diagnostics.py
  test_fault_injection.py
  test_requirements_traceability.py
docs/
  TEST_STRATEGY.md
  REQUIREMENTS.md
.github/workflows/ci.yml
```

## What The Simulated ECU Does

The ECU exposes diagnostic commands for:

- session control
- reading software version
- reading and clearing diagnostic trouble codes
- writing configuration values
- resetting the ECU
- reading live signals such as voltage, temperature, ignition state, and door state

The HIL controller can inject:

- undervoltage
- overtemperature
- stuck door input
- communication timeout
- watchdog stall

