"""
This class is a test manager that provides methods for executing code, generating test cases, and calculating the number of tested branches in a given set of code lines.
"""
import random
from typing import Any
from business.functionManager import FunctionManager
from business.codeManager import CodeManaager
from entity.function import Function
from entity.testCase import TestCase
from core.showMessageBox import ShowMessageBox


class TestManager:
    """
    This class is a test manager that provides methods for executing code, generating test cases, and calculating the number of tested branches in a given set of code lines. 
    Here's what each class method does:

    - __init__: Initializes a new instance of the class and sets up the function manager, code manager, and show message box objects.
    - lcl: Retrieves the last code line from the code manager.
    - execute_code: Executes the given code and returns the value of the last executed line.
    - get_tested_bracnhed_count: Calculates the number of tested branch counts based on the given code lines and the current line number.
    - generate_test_cases: Generates test cases for a given function by randomly selecting argument values and checking the number of tested branches.

    @category: Business Classes, Manager
    @import: FunctionManager, CodeManaager, Funciton, TextCase, ShowMessageBox
    @see: FunctionManager, CodeManaager, Funciton, TextCase, ShowMessageBox
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.

        Parameters:
            None

        Returns:
            None
        
        @category: Business Classes, Manager
        @import: FunctionManager, CodeManaager, Funciton, TextCase, ShowMessageBox
        @see: FunctionManager, CodeManaager, Funciton, TextCase, ShowMessageBox
        """
        self._func_manager = FunctionManager()
        self._code_manager = CodeManaager()
        self._smb = ShowMessageBox()

    @property
    def lcl(self) -> str:
        """
        Retrieve the last code line from the code manager.

        Returns:
            str: The last code line as a string.
        """
        return self._code_manager.last_code_line

    def execute_code(self, _code_with_contents: str) -> Any:
        """
        Execute the given code and return the value of the last executed line.

        Parameters:
            _code_with_contents (str): The code to be executed.

        Returns:
            Any: The value of the last executed line.
        """
        exec_content: dict[Any, Any] = {}
        exec(_code_with_contents, exec_content)
        return exec_content.get(self._code_manager.last_code_line)

    def get_tested_bracnhed_count(self, _code_lines: list[str], _current_line: int) -> int:
        """
        Calculate the number of tested branched counts based on the given code lines and current line.

        Parameters:
            _code_lines (list[str]): The list of code lines to analyze.
            _current_line (int): The current line number.

        Returns:
            int: The number of tested branched counts.
        """

        line_count: int = 0
        last_line_spaces_count: int = 0
        branch_line_spaces_count: int = 0
        tested_branched_counts: int = 0

        left_space_loop = 1024
        branc_line: str = ""
        for line in _code_lines:
            if self._code_manager.is_branched_line(line):
                branch_line_spaces_count = self._code_manager.left_space_count(
                    line)

                branc_line = line
                left_space = self._code_manager.left_space_count(line)
                if "for " in line or "while " in line:
                    left_space_loop = self._code_manager.left_space_count(line)

                    line_count += 1
                    continue
                if left_space > left_space_loop:
                    line_count += 1
                    continue

                tested_branched_counts += 1
            line_count += 1
            if line_count == _current_line:
                last_line_spaces_count = self._code_manager.left_space_count(
                    line)
                break
        if (
            last_line_spaces_count == branch_line_spaces_count
            and last_line_spaces_count >= 8
            and not ("for " in branc_line or "while " in branc_line)
        ):
            tested_branched_counts -= 1

        return tested_branched_counts

    def generate_test_cases(self, _function: Function) -> list[TestCase]:
        """
        Generates test cases for a given function.

        Parameters:
            _function (Function): The function object for which test cases are to be generated.

        Returns:
            list[TestCase]: A list of test cases generated for the function.
        """
        test_cases: list[TestCase] = []
        branch_pools: set[int] = set()

        if len(_function.arguments) > 2:
            tried_counts: int = 0
            check_point: int = 100_000
            parameters: str = ""

            support_count: int = len(_function.support_cases)
            arg_count: int = len(_function.signature.replace(
                "(", "").replace(")", "").split(","))
            while (
                len(branch_pools) < _function.branch_count and tried_counts < check_point
            ):
                tried_counts += 1

                if support_count > 0 and _function.branch_count - tried_counts > 0:
                    arg_values: list[Any] = random.choices(
                        _function.support_cases, k=arg_count)
                    if len(arg_values) > 0:
                        parameters = (
                            "("
                            + ",".join(
                                f'"{val}"' if isinstance(
                                    val, str) else str(val)
                                for val in arg_values
                            )
                            + ")"
                        )
                else:
                    parameters = self._func_manager.change_argument_value(
                        _function)

                self._func_manager.remove_function_calls_in_funcexeclines(
                    _function)
                self._func_manager.add_function_call_in_funcexeclines(
                    _function, parameters
                )

                try:
                    result: Any = self.execute_code(_function.exec_lines)

                    current_line_count: int = (
                        _function.code_lines.index(result) + 1
                    )
                    tested_branches_count: int = self.get_tested_bracnhed_count(
                        _function.code_lines, current_line_count
                    )

                    if (
                        tested_branches_count not in branch_pools
                        and tested_branches_count > 0
                    ):
                        branch_pools.add(tested_branches_count)

                        test_case: TestCase = TestCase()
                        test_case.test_values = parameters
                        test_case.tested_lines = _function.code_lines[
                            :current_line_count
                        ]
                        test_case.tested_branches_count = tested_branches_count
                        test_case.test_coverages_rate = round(
                            (current_line_count / _function.code_lines_count) * 100, 2
                        )
                        test_cases.append(test_case)

                    if tried_counts == check_point:
                        break

                except TypeError as te:
                    if "'list' object is not callable" == str(te):
                        message = str(te)
                        title = "Type Error"

                        self._smb.show_message(title, message)

                        break

        else:
            self._func_manager.remove_function_calls_in_funcexeclines(
                _function)
            self._func_manager.add_function_call_in_funcexeclines(
                _function, _function.arguments
            )

            result = self.execute_code(_function.exec_lines)

            current_line_count: int = (
                _function.code_lines.index(result) + 1
            )
            tested_branches_count: int = self.get_tested_bracnhed_count(
                _function.code_lines, current_line_count
            )

            test_case: TestCase = TestCase()
            test_case.test_values = _function.arguments
            test_case.tested_lines = _function.code_lines[:current_line_count]
            test_case.tested_branches_count = tested_branches_count
            test_case.test_coverages_rate = round(
                (current_line_count / _function.code_lines_count) * 100, 2
            )
            test_cases.append(test_case)

        test_cases.sort(
            key=lambda case: case.test_coverages_rate, reverse=True)
        return test_cases
