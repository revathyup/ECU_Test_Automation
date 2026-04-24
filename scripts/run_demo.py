from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nordic_ecu_lab import BodyControlEcu, HilController


def main() -> None:
    hil = HilController(BodyControlEcu())

    print("Boot check:", hil.send("read_version").payload)
    print("Default signals:", hil.send("read_signals").payload)

    hil.send("session_control", session="extended")
    print("Config write:", hil.send("write_config", welcome_light_ms=9000).payload)

    hil.inject_fault("undervoltage")
    print("DTC after undervoltage:", hil.send("read_dtc").payload)

    hil.recover_fault("undervoltage")
    print("DTC after recovery:", hil.send("read_dtc").payload)


if __name__ == "__main__":
    main()
