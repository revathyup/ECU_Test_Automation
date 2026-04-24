from __future__ import annotations

import ast
from pathlib import Path

import pytest


@pytest.mark.req("REQ-TRACE-001")
def test_all_tests_have_requirement_markers():
    test_files = Path("tests").glob("test_*.py")
    missing: list[str] = []

    for test_file in test_files:
        tree = ast.parse(test_file.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                if not _has_req_marker(node):
                    missing.append(f"{test_file}:{node.name}")

    assert not missing, "missing requirement markers: " + ", ".join(missing)


def _has_req_marker(node: ast.FunctionDef) -> bool:
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call):
            continue
        func = decorator.func
        if isinstance(func, ast.Attribute) and func.attr == "req":
            return True
    return False
