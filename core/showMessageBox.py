"""
The class that holds operations related to message box communications to interact with the user.
"""
from PyQt5.QtWidgets import (
    QMessageBox as message_box,
)


class ShowMessageBox:
    """
    This class definition is for a utility class called ShowMessageBox. 
    Here's what each class method does:

    - show_message(self, _title: str, _message: str) -> None: Displays a critical message box with a specified title and message.
    - show_question(self, _title: str, _message: str): Shows a question message box with the specified title and message. 
    It returns the user's response to the question, which can be either message_box.Yes or message_box.No.

    Parameters:
        self: The object instance.

    Returns:
        None

    @category: Utilities
    """

    def show_message(self, _title: str, _message: str) -> None:
        """
        Displays a critical message box with a specified title and message.

        Args:
            _title (str): The title of the message box.
            _message (str): The message to be displayed in the message box.

        Returns:
            None
        """
        mb = message_box()
        mb.setIcon(mb.Critical)  # type: ignore
        mb.setWindowTitle(_title)
        font = mb.font()
        font.setBold(True)
        font.setPointSize(13)
        mb.setFont(font)
        mb.setText(_message)
        mb.exec_()

    def show_question(self, _title: str, _message: str):
        """
        Shows a question message box with the specified title and message.

        Parameters:
            _title (str): The title of the question message box.
            _message (str): The message to be displayed in the question message box.

        Returns:
            int: The user's response to the question. It can be either;
            message_box.Yes or message_box.No.
        """
        question = message_box.question(
            None,  # type: ignore
            _title,
            _message,
            message_box.Yes | message_box.No,  # type: ignore
            message_box.No,  # type: ignore
        )

        return question
