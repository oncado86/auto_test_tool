"""
Opens a file with the default program based on the operating system.
"""
import os
import subprocess
import platform
from core.showMessageBox import ShowMessageBox


class OpenFileWithDefaultProgram:
    """    
    This class, OpenFileWithDefaultProgram, opens a file with the default program based on the operating system. 
    Here's what each class method does:

    - open_file_with_default_program(_file_path: str) -> None: 
    Opens the file with the default program based on the operating system. 
    It takes the _file_path as an argument and doesn't return anything. 
    It raises an exception if there's an error while opening the file.

    @see: ShowMessageBox (Utilities Class)
    @import: ShowMessageBox (Utilities Class)
    @category: Utilities

    """

    def open_file_with_default_program(self, _file_path: str) -> None:
        """
        Opens a file with the default program based on the operating system.

        Args:
            _file_path (str): The path of the file to be opened.

        Returns:
            None: This function does not return anything.

        Raises:
            Exception: If an error occurs while opening the file.
        """
        try:
            platform_name: str = platform.system()
            command: list[str] = []
            if platform_name == "Linux":
                command = ["xdg-open", _file_path]
            elif platform_name == "Darwin":
                command = ["open", _file_path]
            elif platform_name == "Windows":
                command = ["start", "", _file_path]
            else:
                ShowMessageBox().show_message(
                    "Error", "This operating system is not supported."
                )
                return

            if not os.path.isfile(_file_path):
                ShowMessageBox().show_message(
                    "Error", "Invalid file path."
                )
                return

            subprocess.run(command, shell=False, check=True)
        except Exception as e:
            ShowMessageBox().show_message(
                "Error", f"An error occurred while opening the file: \n{e}"
            )
