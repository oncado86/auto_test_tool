"""
The OpenFileWithDefaultProgramManager class is a manager class that allows you to open files with their default programs.
"""
from dataAccess.openFileWithDefaultProgramDal import OpenFileWithDefaultProgram


class OpenFileWithDefaultProgramManager:
    """
    The OpenFileWithDefaultProgramManager class is a manager class that allows you to open files with their default programs.

    - __init__ method initializes the class and creates an instance of the OpenFileWithDefaultProgram class.
    - open_file_with_default_program method opens a file with the default program associated with its file type.

    @cateory: Business, Manager
    """

    def __init__(self) -> None:
        """
        Initializes the class and creates an instance of the OpenFileWithDefaultProgram class.

        Parameters:
            None

        Returns:
            None

        @cateory: Business, Manager
        """
        self._ofwdp = OpenFileWithDefaultProgram()

    def open_file_with_default_program(self, _filepath: str) -> None:
        """
        Opens a file with the default program associated with its file type.

        Args:
            _filepath (str): The path of the file to be opened.

        Returns:
            None: This function does not return anything.
        """
        if _filepath:
            self._ofwdp.open_file_with_default_program(_filepath)
