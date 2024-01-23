from entity.function import Function
from entity.testCase import TestCase


class TestCode:
    def __init__(self) -> None:
        self._fixed_code_lines:list[str] = []
        self._functions:list[Function] = []
        self._test_cases:list[TestCase]=[]
        self._exec_lines: str = ""
        self._branc_count: int = 0
        self._code_lines_count: int = 0