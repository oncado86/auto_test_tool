"""
The CodeFormatter class provides methods to clean and fix source code by removing comments and clearing vertical spaces.
"""
import re


class CodeFormatter:
    """
    The CodeFormatter class provides methods to clean and fix source code by removing comments and clearing vertical spaces. 
    Here is a summary of each method:

    - __clear_vertical_spaces_in_code(_code_str: str) -> list[str]: This method takes a code string as input and returns a list of code lines without vertical spaces.
    - __clean_comments(_code_str: str) -> str: This method removes comments from the given code string and returns the code string with comments removed.
    - fixed_source_code(_code_str: str) -> str: This method fixes the source code by removing comments and clearing vertical spaces. 
    It takes a source code string as input and returns the fixed source code string.
    """

    def __clear_vertical_spaces_in_code(self, _code_str: str) -> list[str]:
        """
        Clears vertical spaces in a code string.

        Args:
            _code_str (str): The code string to be processed.

        Returns:
            list[str]: A list of code lines without vertical spaces.
        """
        return [line.rstrip() for line in _code_str.splitlines() if line.strip()]

    def __clean_comments(self, _code_str: str) -> str:
        """
        Removes comments from the given code string.

        Args:
            _code_str (str): The code string from which comments will be removed.

        Returns:
            str: The code string with comments removed.
        """
        cleaned_code: str = re.sub(r"#.*", "", _code_str)
        cleaned_code = re.sub(
            r"\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\'|#.*",
            "",
            cleaned_code,
            flags=re.MULTILINE,
        )
        return "\n".join(cleaned_code.splitlines())

    def fixed_source_code(self, _code_str: str) -> str:
        """
        Fixes the source code by removing comments and clearing vertical spaces.

        Parameters:
            _code_str (str): The source code to be fixed.

        Returns:
            str: The fixed source code.
        """
        lines: str = self.__clean_comments(_code_str)
        codes: list[str] = self.__clear_vertical_spaces_in_code(lines)
        fixed_code: str = "\n".join(codes)
        return fixed_code
