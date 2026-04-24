from __future__ import annotations

import pytest

from nordic_ecu_lab import BodyControlEcu, HilController


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "req(id): requirement covered by a test")


@pytest.fixture
def ecu() -> BodyControlEcu:
    return BodyControlEcu()


@pytest.fixture
def hil(ecu: BodyControlEcu) -> HilController:
    return HilController(ecu=ecu)
