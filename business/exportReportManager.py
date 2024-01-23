"""
The ExportReportManager class is responsible for managing the export of reports.
"""
from dataAccess.exportReportDal import ExportReportDal
from entity.function import Function


class ExportReportManager:
    """The ExportReportManager class is responsible for managing the export of reports.
    Here's what each class method does:

    - __init__(): Initializes a new instance of the class and creates an instance of the ExportReportDal class.
    - export_report(_filepath: str, _function: Function) -> bool: Exports a report by taking in a file path and a Function object. 
    It checks if all the necessary attributes of the Function object are present and then calls the export_report() method of the ExportReportDal class to export the report. 
    It returns True if the report was successfully exported, and False otherwise.

    @category: Business, Manager
    @import: ExportReportDal, Function
    @see: ExportReportDal, Function
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the class.

        Parameters:
            None

        Returns:
            None

        @category: Business, Manager
        @import: ExportReportDal, Function
        @see: ExportReportDal, Function
        """
        self._er = ExportReportDal()

    def export_report(self, _filepath: str, _function: Function) -> bool:
        """
        Exports a report.

        Args:
            _filepath (str): The file path to export the report to.
            _function (Function): The function to include in the report.

        Returns:
            bool: True if the report was successfully exported, False otherwise.
        """
        if all([
            _filepath,
            _function.name,
            _function.branch_count,
            _function.code_lines,
            _function.test_cases
        ]):
            return self._er.export_report(_filepath, _function)
        return False
