"""
This class CodeAnalyzer extends from the CodeFormatter class and provides methods for analyzing and formatting code. 
"""
from business.codeFormatter import CodeFormatter


class CodeAnalyzer(CodeFormatter):
    """This class CodeAnalyzer extends from the CodeFormatter class and provides methods for analyzing and formatting code. 
        Here is a summary of what each class method does:

        - __init__(self): Initializes the instance variables of the class.
        - branched_keys(self): Returns the list of branched keys.
        - skip_statement_keys(self): Returns the list of skip statement keys.
        - last_code_line(self): Returns the last code line.
        - left_space_count(self, _code_lines): Returns the number of leading spaces in the given code line.
        - right_space_count(self, _code_lines): Returns the number of trailing spaces in the given code line.
        - is_skip_statement_line(self, _code_lines): Checks if the given code lines contain any skip statement keys.
        - is_branched_line(self, _code_lines): Determines if the given code line is a branched line.
        - is_branches_numerical(self, _code_lines): Determines if the branches in the given code lines are numerical.

    Args:
        CodeFormatter (Class): Parrent class of this class.
    """

    def __init__(self) -> None:
        """
        Initialize the instance variables of the class.

        Parameters:
            None

        Return:
            None
        """
        self.__branched_keys: list[str] = [
            "if", "elif", "else", "for", "while"]
        self.__skip_statement_keys: list[str] = ["return", "break"]
        self.__last_code_line: str = "_lcl_"

    @property
    def branched_keys(self) -> list[str]:
        """Returns the list of branched keys.

        Returns:
            list[str]: The list of branched keys.
        """
        return self.__branched_keys

    @property
    def skip_statement_keys(self) -> list[str]:
        """Returns the list of skip statement keys.
        This property returns the list of skip statement keys in the object.

        Returns:
            list[str]: A list of strings representing the skip statement keys.
        """
        return self.__skip_statement_keys

    @property
    def last_code_line(self) -> str:
        """Returns the last code line.

        Returns:
            str: A string representing the last code line.
        """
        return self.__last_code_line

    def left_space_count(self, _code_lines: str) -> int:
        """
        Calculate the number of leading spaces or tabs in a given string of code lines.

        Parameters:
            _code_lines (str): The string of code lines to calculate the leading space count.

        Returns:
            int: The number of leading spaces or tabs in the given code lines.
        """
        return len(_code_lines) - len(_code_lines.lstrip())

    def right_space_count(self, _code_lines: str) -> int:
        """
        Calculates the number of right spaces at the end of each line in a given string of code lines.

        Args:
            _code_lines (str): The string of code lines to analyze.

        Returns:
            int: The number of right spaces at the end of each line.
        """
        return len(_code_lines) - len(_code_lines.rstrip())

    def is_skip_statement_line(self, _code_lines: str) -> bool:
        """
        Check if the given code lines contain any skip statement keys.

        Args:
            _code_lines (str): The code lines to check.

        Returns:
            bool: True if any skip statement key is found in the code lines, False otherwise.
        """
        return any(skip in _code_lines for skip in self.skip_statement_keys)

    def is_branched_line(self, _code_lines: str) -> bool:
        """
        Determines if the given code line is a branched line.

        Args:
            _code_lines (str): The code line to check.

        Returns:
            bool: True if the code line is a branched line, False otherwise.
        """
        left_space_count: int = self.left_space_count(_code_lines)
        for branch in self.__branched_keys:
            if _code_lines.startswith(
                f"{' '*left_space_count}{branch}"
            ) and _code_lines.endswith(":"):
                return True
        return False

    def is_branches_numerical(self, _code_lines: str) -> bool:
        """
        Determines if the branches in the given code lines are numerical.

        Parameters:
            _code_lines (str): The code lines to be checked.

        Returns:
            bool: True if the branches are numerical, False otherwise.
        """
        codes: list[str] = self.fixed_source_code(_code_lines).splitlines()
        mat_operators: list[str] = [
            ">", "<", ">=", "<=", "!=", "==", "range(", "%"]

        strings_op: list[str] = ["'", '"', "len("]

        for line in codes:
            if (self.is_branched_line(line)) and ("else" not in line) and (not any(op in line for op in mat_operators)) and (any(char in line for char in strings_op)):
                return False
        return True
