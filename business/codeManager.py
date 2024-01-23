"""
The CodeManager class extends the CodeAnalyzer class
"""
from business.codeAnalyzer import CodeAnalyzer


class CodeManaager(CodeAnalyzer):
    """
    The CodeManager class extends the CodeAnalyzer class and has the following methods:

    - __init__() - Initializes the instance variables __current_line, __coverage_rate, and __branched_count.
    - current_line - Gets the value of the __current_line attribute.
    - coverage_rate - Gets the coverage rate of the object.
    - branched_count - Gets the value of the __branched_count property.
    - get_code_lines(_code_str: str) -> list[str] - Extracts and returns a list of code lines from the given code string.
    - __loop_line(code: str) -> bool - Checks if a line of code is a loop statement.
    - __if_elif_else_line(code: str) -> bool - Checks if a line of code is an if, elif, or else statement.
    - __increase_number_of_branches(_line: str, _loop: bool, _code_lines: list[str], _index: int, _branches: int) -> int - Increases the number of branches based on certain conditions.
    - __return_line(code: str) -> bool - Checks if a code line starts with the keyword "return".
    - get_branched_count(_code_str: str) -> int - Calculates the number of branches in the given code.
    - add_content_to_code(_code_str: str) -> str - Generates a modified version of the code string by adding content comments.

        Parameters:
            None

        Returns:
            None

        @category: Business, Manager
        @import: CodeAnalyzer
        @see: CodeAnalyzer
        """

    def __init__(self) -> None:
        """
        Initializes an instance of the class.

        This function sets the initial values for the instance variables:
        - self.__current_line: representing the current line
        - self.__coverage_rate: representing the coverage rate
        - self.__branched_count: representing the branched count

        Parameters:
        None

        Returns:
        None
        """
        super().__init__()
        self.__current_line = "current line"
        self.__coverage_rate = "coverage rate"
        self.__branched_count = "branched count"

    @property
    def current_line(self) -> str:
        """
        This function is a property that returns the value of the current_line attribute.

        Returns:
            str: The value of the current_line attribute.
        """
        return self.__current_line

    @property
    def coverage_rate(self) -> str:
        """Returns the coverage rate of the object.

        Returns:
            str: A string representing the coverage rate.
        """
        return self.__coverage_rate

    @property
    def branched_count(self) -> str:
        """
        Getter method for the branched_count property.

        Returns:
            str: The value of the branched_count property.
        """
        return self.__branched_count

    def get_code_lines(self, _code_str: str) -> list[str]:
        """
        Extracts and returns a list of code lines from the given code string.

        Args:
            _code_str (str): The code string from which to extract the code lines.

        Returns:
            list[str]: A list of code lines extracted from the code string.
        """
        lines: str = self.fixed_source_code(_code_str)
        code_lines: list[str] = lines.splitlines()
        return code_lines

    # GET BRANCHED COUNT
    def __loop_line(self, code: str) -> bool:
        """
        Checks if a line of code is a loop statement.

        Parameters:
            code (str): The line of code to check.

        Returns:
            bool: True if the line of code is a loop statement, False otherwise.
        """
        line_without_space: str = code.strip()
        return line_without_space.endswith(":") and any(line_without_space.startswith(loop) for loop in ["for", "while"])

    def __if_elif_else_line(self, code: str) -> bool:
        """
        Checks if a given line of code is an if, elif, or else statement.

        Parameters:
            code (str): The line of code to be checked.

        Returns:
            bool: True if the line is an if, elif, or else statement, False otherwise.
        """
        line_without_space: str = code.strip()
        return line_without_space.endswith(":") and (line_without_space.startswith("if") or line_without_space.startswith("elif") or line_without_space.startswith("else"))

    def __increase_number_of_branches(self, _line: str, _loop: bool, _code_lines: list[str], _index: int, _branches: int) -> int:
        """
        Increase the number of branches in the code based on certain conditions.

        Args:
            _line (str): The current line of code being processed.
            _loop (bool): A flag indicating whether the code is inside a loop.
            _code_lines (list[str]): The list of code lines being analyzed.
            _index (int): The index of the current line in the code_lines list.
            _branches (int): The current number of branches.

        Returns:
            int: The updated number of branches after processing the current line of code.
        """
        if (self.__if_elif_else_line(_line) and not _loop) or (_loop and not _code_lines[_index-1].strip().startswith("return") and _line.strip().startswith("return")):
            _branches += 1
        return _branches

    def __return_line(self, code: str) -> bool:
        """
        Check if the given code line starts with the keyword "return".

        Parameters:
            code (str): The code line to be checked.

        Returns:
            bool: True if the code line starts with "return", False otherwise.
        """
        line_without_space: str = code.strip()
        return line_without_space.startswith("return")

    def get_branched_count(self, _code_str: str) -> int:
        """
        Calculate the number of branches in the given code.

        Parameters:
            _code_str (str): The code string to analyze.

        Returns:
            int: The number of branches in the code.

        """
        code_lines: list[str] = _code_str.splitlines()
        branches: int = 0
        loop_spaces: list[int] = []

        for index, line in enumerate(code_lines):
            if self.__loop_line(line):
                loop_space: int = self.left_space_count(line)
                if loop_space not in loop_spaces:
                    loop_spaces.append(loop_space)
            else:
                line_space: int = self.left_space_count(line)
                if loop_spaces and (line_space <= loop_spaces[-1] or self.__return_line(line)):
                    loop_spaces.pop()

            branches = self.__increase_number_of_branches(
                line, bool(loop_spaces), code_lines, index, branches)

        return branches

    def add_content_to_code(self, _code_str: str) -> str:
        """
        Generates a modified version of the given code string by adding content comments.

        Args:
            _code_str (str): The original code string.

        Returns:
            str: The modified code string with content comments.
        """
        code_with_content: str = ""
        codes: list[str] = self.get_code_lines(_code_str)
        left_space_count: int = 0

        for line in codes:
            if self.is_skip_statement_line(line):
                left_space_count = self.left_space_count(line)
                code_with_content += (
                    f"\n{' '*left_space_count}{self.last_code_line}='{line}'"
                )

                code_with_content += f"\n{line}"
            else:
                left_space_count = self.left_space_count(line)
                if line.startswith(f"{' '* left_space_count}def ") and line.endswith(
                    ":"
                ):
                    code_with_content += (
                        f"\n{' '*left_space_count}{self.last_code_line}='{line}'"
                    )

                    code_with_content += f"\n{' '*left_space_count}{line}"
                    code_with_content += (
                        f"\n{' '*left_space_count}{' '*4}global {self.last_code_line}"
                    )
                elif line.startswith(f"{' '*left_space_count}#"):
                    code_with_content += f"\n{line}"
                elif self.is_branched_line(line):
                    code_with_content += f"\n{line}"
                    code_with_content += f"\n{' '*left_space_count}{' '*4}{self.last_code_line}='{line}'"

                else:
                    code_with_content += (
                        f"\n{' '*left_space_count}{self.last_code_line}='{line}'"
                    )

                    code_with_content += f"\n{line}"

        return code_with_content
