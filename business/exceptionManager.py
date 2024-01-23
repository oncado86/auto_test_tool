from PyQt5.QtWidgets import (
    QTextEdit as text_edit,
    QListWidget as list_widget,
)

from PyQt5.QtGui import (
    QTextCursor as text_cursor,
)

from core.showMessageBox import ShowMessageBox
from business.codeAnalyzer import CodeAnalyzer


class ExceptionManager:
    def __init__(self) -> None:
        """
        Initializes a new instance of the class.

        Parameters:
            None

        Returns:
            None

        @category: Business, Manager
        @import: CodeAnalyzer, ShowMessageBox
        @see: CodeAnalyzer, ShowMessageBox
        """
        self._smb = ShowMessageBox()
        self._last_code_line = CodeAnalyzer().last_code_line

    # ----->> SYNTAX ERROR
    def handle_syntax_error(
        self,
        _exception: SyntaxError,
        _function_code_lines: list[str],
        _txt_source_code: text_edit,
        _lw_fixed_code: list_widget,
    ) -> None:
        """
        Handle syntax errors that occur during code execution.

        Parameters:
            _exception (SyntaxError): The syntax error that occurred.
            _function_code_lines (list[str]): The list of code lines of the function.
            _txt_source_code (text_edit): The text edit widget containing the source code.
            _lw_fixed_code (list_widget): The list widget displaying the fixed code lines.

        Returns:
            None. This function does not return any value.
        """
        wrong_code: str = str(_exception.text).replace("\n", "")

        if self._last_code_line in wrong_code:
            wrong_code = wrong_code.split("'")[1].replace("'", "")

        self.syntax_error(_exception, _function_code_lines)
        error_line_number: int = _function_code_lines.index(wrong_code)
        _lw_fixed_code.setCurrentRow(error_line_number)

        self.set_cursor_position_to_text_edit(
            _txt_source_code, wrong_code, _exception.msg
        )

    def syntax_error(self, _error: SyntaxError, _code_lines: list[str]) -> None:
        """
        Handles a syntax error and displays an error message.

        Parameters:
        - _error: The syntax error that occurred.
        - _code_lines: A list of code lines.

        Returns:
        - None
        """
        wrong_code: str = str(_error.text).replace("\n", "")
        if "_lcl_" in wrong_code:
            wrong_code = wrong_code.split("'")[1].replace("'", "")
        error_line_number: int = _code_lines.index(wrong_code) + 1

        if " (" in _error.msg:
            error_msg = _error.msg[: _error.msg.index(" (")]
        elif " [" in _error.msg:
            error_msg = _error.msg[: _error.msg.index(" [")]
        elif " {" in _error.msg:
            error_msg = _error.msg[: _error.msg.index(" {")]
        else:
            error_msg = _error.msg

        error_message: str = f"\nLine Number\t:\t{error_line_number}\t\nExplanation\t:\t{error_msg}\t\nCode Line\t:\t{wrong_code}\t"

        self._smb.show_message("Syntax Error", error_message)

    # ----->> NAME ERROR
    def handle_name_error(
        self,
        _exception: NameError,
        _function_code_lines: list[str],
        _txt_source_code: text_edit,
        _lw_fixed_code: list_widget,
    ) -> None:
        """
        Handles a NameError exception in the code.

        Parameters:
            _exception (NameError): The NameError exception that was raised.
            _function_code_lines (list[str]): The lines of code in the function.
            _txt_source_code (text_edit): The text editor widget that displays the source code.
            _lw_fixed_code (list_widget): The list widget that displays the fixed code.

        Returns:
            None
        """

        error_line_number: int = next(
            index + 1 for index, line in enumerate(_function_code_lines) if _exception.name in line)
        self.name_error(_exception, _function_code_lines)
        _lw_fixed_code.setCurrentRow(error_line_number - 1)
        wrong_code: str = _function_code_lines[error_line_number - 1]
        self.set_cursor_position_to_text_edit(
            _txt_source_code, wrong_code, _exception.args[0])

    def name_error(self, _error: NameError, _code_lines: list[str]) -> None:
        """
        Handles a NameError exception by retrieving the name of the variable causing the error, determining the line number where the error occurred, and displaying an error message.

        Parameters:
            _error (NameError): The NameError exception that was raised.
            _code_lines (list[str]): A list of code lines where the error occurred.

        Returns:
            None: This function does not return anything.
        """
        wrong_code: str = str(_error.name).replace("\n", "")
        error_line_number: int = next(
            (index + 1 for index, line in enumerate(_code_lines) if wrong_code in line), 0)
        error_message = f"\nLine Number\t:\t{error_line_number}\t\nExplanation\t:\t{_error}\t\nCode Line\t:\t{_code_lines[error_line_number-1]}\t"
        self._smb.show_message("Name Error", error_message)

    # ----->> INDEX ERROR
    def handle_index_error(
        self,
        _exception: IndexError,
        _function_code_lines: list[str],
        _txt_source_code: text_edit,
        _lw_fixed_code: list_widget,
    ) -> None:
        self.index_error(_exception, _function_code_lines)
        _txt_source_code.setEnabled(True)

    def index_error(self, _error: IndexError, _code_lines: list[str]) -> None:
        # TODO: hangi liste olduğunu yakalayıp kod satırını tespit et
        self._smb.show_message("Index Error", str(_error))

    # ----->> VALUE ERROR
    def handle_value_error(
        self,
        _exception: ValueError,
        _function_code_lines: list[str],
        _txt_source_code: text_edit,
        _lw_fixed_code: list_widget,
    ) -> None:
        self.value_error(_exception, _function_code_lines)

    def value_error(self, _error: ValueError, _code_lines: list[str]) -> None:
        # TODO: kod satırını tespit et
        self._smb.show_message("Value Error", str(_error))

    # ----->> TYPE ERROR
    def handle_type_error(
        self,
        _exception: TypeError,
        _function_code_lines: list[str],
        _txt_source_code: text_edit,
        _lw_fixed_code: list_widget,
    ) -> None:
        self.type_error(_exception, _function_code_lines)

    def type_error(self, _error: TypeError, _code_lines: list[str]) -> None:
        # TODO: kod satırını tespit et
        if "'list' object is not callable" == str(_error):
            self._smb.show_message("Type Error", str(_error))

    # ----->> KEY ERROR
    def handle_key_error(
        self,
        _exception: KeyError,
        _function_code_lines: list[str],
        _txt_source_code: text_edit,
        _lw_fixed_code: list_widget,
    ) -> None:
        self.key_error(_exception, _function_code_lines)

    def key_error(self, _error: KeyError, _code_lines: list[str]) -> None:
        # TODO: kod satırını tespit et
        self._smb.show_message("Key Error", str(_error))

    # ----->> ATTRIBUTE ERROR
    def handle_attribute_error(
        self,
        _exception: AttributeError,
        _function_code_lines: list[str],
        _txt_source_code: text_edit,
        _lw_fixed_code: list_widget,
    ) -> None:
        self.attribute_error(_exception, _function_code_lines)

    def attribute_error(self, _error: AttributeError, _code_lines: list[str]) -> None:
        # TODO: kod satırını tespit et
        error_message = str(_error.args[0])
        attribute_name: str = _error.name
        object_content: object = _error.obj
        message: str = f"{error_message}\t\nAttribure Name: {attribute_name}\t\nObject Contet: {object_content}"
        self._smb.show_message("Attribute Error", message)

    # ----->> ZERO DIVISION ERROR
    def handle_zero_division_error(
        self,
        _exception: ZeroDivisionError,
        _function_code_lines: list[str],
        _txt_source_code: text_edit,
        _lw_fixed_code: list_widget,
    ) -> None:
        self.zero_division_error(_exception, _function_code_lines)

    def zero_division_error(
        self, _error: ZeroDivisionError, _code_lines: list[str]
    ) -> None:
        # TODO: kod satırını tespit et
        self._smb.show_message("Zer0 Error", str(_error))

    # ----->> ARITHMETIC ERROR
    def handle_arithmetic_error(
        self,
        _exception: ArithmeticError,
        _function_code_lines: list[str],
        _txt_source_code: text_edit,
        _lw_fixed_code: list_widget,
    ) -> None:
        self.arithmetic_error(_exception, _function_code_lines)

    def arithmetic_error(self, _error: ArithmeticError, _code_lines: list[str]) -> None:
        # TODO: kod satırını tespit et
        self._smb.show_message("Attribute Error", str(_error))

    # ----->> SET CURSOR POSITION
    def _get_cursor_position_to_text_edit(
        self, _wrong_code_str: str, _source_code_str: str, _error_message_str: str
    ) -> int:
        """
        Get the cursor position in the source code where the error occurred.

        Args:
            _wrong_code_str (str): The incorrect code string.
            _source_code_str (str): The source code string.
            _error_message_str (str): The error message string.

        Returns:
            int: The cursor position in the source code.

        """
        wrong_code_fix: str = "".join(_wrong_code_str.split(" "))

        source_code_lines: list[str] = _source_code_str.splitlines()
        source_code_fix_lines: list[str] = [line.replace(
            " ", "") if line else line for line in source_code_lines]

        if wrong_code_fix not in source_code_fix_lines and wrong_code_fix.startswith("def"):
            source_code_fix_lines.insert(0, wrong_code_fix)

        if _wrong_code_str not in source_code_lines and _wrong_code_str.startswith("def"):
            source_code_lines.insert(0, _wrong_code_str)

        wrong_code_index: int = source_code_fix_lines.index(wrong_code_fix)
        search_wrong_code: str = source_code_lines[wrong_code_index]

        position: int = self._calculate_cursor_position(
            _source_code_str, search_wrong_code, _error_message_str
        )

        return position

    def _calculate_cursor_position(
        self, _source_code_str: str, _search_code_str: str, _error_msg_str: str
    ) -> int:
        """
        Calculates the cursor position based on the given source code, search code, and error message.

        Args:
            _source_code_str (str): The source code string.
            _search_code_str (str): The search code string.
            _error_msg_str (str): The error message string.

        Returns:
            int: The calculated cursor position.

        """
        position: int = 0
        name_error_name: str = ""
        if "name '" in _error_msg_str:
            name_error_name = _error_msg_str.split("'")[1].split("'")[0]

        error_conditions: list[str] = [
            "invalid syntax",
            "expected ':'",
            "'(' was never closed",
            "'[' was never closed",
            "'{' was never closed",
            "unterminated string literal",
        ]
        if _error_msg_str in error_conditions:
            position = _source_code_str.index(
                _search_code_str) + len(_search_code_str)
        elif _error_msg_str == "invalid syntax. Maybe you meant '==' or ':=' instead of '='?":
            position = _source_code_str.index(_search_code_str) + len(
                _search_code_str[: _search_code_str.index("=")]
            )
        elif f"name '{name_error_name}' is not defined" == _error_msg_str:
            position = _source_code_str.index(name_error_name)
        else:
            position = _source_code_str.index(_search_code_str)
        return position

    def set_cursor_position_to_text_edit(
        self, _text_edit: text_edit, _wrong_code_str: str, _error_message_str: str
    ) -> None:
        """
        Set the cursor position to the specified text edit.

        Args:
            _text_edit (text_edit): The text edit to set the cursor position to.
            _wrong_code_str (str): The wrong code string.
            _error_message_str (str): The error message string.

        Returns:
            None
        """
        txt_sc = _text_edit
        txt_sc.setFocus()

        source_code: str = txt_sc.toPlainText()

        position: int = self._get_cursor_position_to_text_edit(
            _wrong_code_str, source_code, _error_message_str
        )
        cursor = text_cursor(_text_edit.document())
        cursor.setPosition(position)
        _text_edit.setTextCursor(cursor)
