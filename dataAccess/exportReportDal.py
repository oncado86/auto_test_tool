"""
The ExportReportDal class is responsible for exporting a report to a file.
"""

import os
from entity.function import Function


class ExportReportDal:
    """The ExportReportDal class is responsible for exporting a report to a file. Here's a summary of what each class method does:

    - __init__(self): Initializes the class instance by setting the _file_name attribute to an empty string.

    - export_report(self, _file_name: str, _function: Function) -> bool: 
    Exports a report to a file. 
    It takes in the name of the file to export the report to (_file_name) and a function object (_function) representing the function to generate the report for. 
    It returns True if the report was successfully exported, False otherwise.

        Parameters:
            None

        Returns:
            None

        @see: Function (Entity Class)
        @import: Function (Entity Class)
        @category: Data Access
    """

    def __init__(self) -> None:
        """
        Initializes the class instance.

        This function is the constructor of the class. It takes no parameters.

        Parameters:
            None

        Returns:
            None

        @see: Function (Entity Class)
        @import: Function (Entity Class)
        @category: Data Access
        """
        self._file_name: str = ""

    def export_report(self, _file_name: str, _function: Function) -> bool:
        """
        Exports a report to a file.

        Args:
            _file_name (str): The name of the file to export the report to.
            _function (Function): The function object representing the function to generate the report for.

        Returns:
            bool: True if the report was successfully exported, False otherwise.
        """

        if not _file_name:
            return False

        test_values: list[str] = [
            " ".join(case.test_values).translate(str.maketrans("", "", " ()"))
            for pool in _function.test_cases
            for case in pool
        ]

        report: str = ""
        mode: str = "a" if os.path.exists(_file_name) else "w"

        if mode == "a":
            report = "\n" + " , ".join(test_values) + ","
        else:
            code_lines: str = "\n".join(_function.code_lines)
            values: str = "\n" + " , ".join(test_values) + ","
            report = f"Code Lines:\n{code_lines}\n\nBranches: {_function.branch_count}\n\nValues:{values}"

        try:
            with open(_file_name, mode, encoding="utf-8") as file:
                file.write(report)
            return True
        except Exception:
            return False
