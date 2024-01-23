""" In order for the application to run without errors, the following libraries must be installed.
    - PyQt5
        
    pip install PyQt5
"""
import sys
from typing import Any
from time import sleep

# ENTITIES
from entity.function import Function
from entity.testCase import TestCase

# USER INTERFACE
from ui.att_ui import Ui_MainWindow as ui_main_window
from PyQt5.QtWidgets import (
    QMainWindow as main_window,
    QApplication as application,
    QFileDialog as file_dialog,
    QMessageBox as message_box,
)

# BUSINESS
from business.testManager import TestManager
from business.functionManager import FunctionManager
from business.exceptionManager import ExceptionManager
from business.uiTimerManager import UiProgressBarValueManager
from business.uiTimerManager import UiLabelTextManager
from business.exportReportManager import ExportReportManager
from business.openFileWithDefaultProgramManager import OpenFileWithDefaultProgramManager


# CORE
from core.showMessageBox import ShowMessageBox


# APPLICATION
class AttApp(ui_main_window, main_window):
    """
        Initializes the class instance.

        This function sets up the class instance by calling the parent class's
        `__init__()` method. It then proceeds to initialize the UI and managers
        by calling the `init_ui()` and `init_managers()` methods respectively.

        Parameters:
            None

        Returns:
            None
        """

    def __init__(self) -> None:
        """
        Initializes the class instance.

        This function sets up the class instance by calling the parent class's
        `__init__()` method. It then proceeds to initialize the UI and managers
        by calling the `init_ui()` and `init_managers()` methods respectively.

        Parameters:
            None

        Returns:
            None
        """
        super().__init__()

        self.init_ui()
        self.init_managers()

        self._support_cases: list[Any] = []

    # ----->> INIT UI
    def init_ui(self) -> None:
        """
        Initialize the user interface.

        This function sets up the UI by performing the following steps:
        1. Create an instance of the `ui_main_window` class.
        2. Call the `setupUi` method of the `ui_main_window` instance, passing `self` as an argument.
        3. Set up the button functions.
        4. Set up the combobox functions.
        5. Set up the list functions.
        6. Set up the text edit functions.
        7. Set up the spin box functions.
        8. Set the fixed height of the progress bar.
        9. Set the visibility of the statistics group box to False.
        10. Set the visibility of the test completed group box to False.
        11. Show a status bar message with the text "Wellcome to Auto Test Tool".
        12. Connect the `actionExport_Report` signal of the menu bar to the `menubar_export_report` slot.
        13. Connect the `actionSupport_Cases` signal of the menu bar to the `menubar_import_support_values` slot.
        14. Show the main window.

        Parameters:
            self: The object itself.

        Returns:
            None.
        """
        self.ui: ui_main_window = ui_main_window()
        self.ui.setupUi(self)  # type: ignore

        # * BUTTON FUNCTIONS
        self.button_funcs()

        # * COMBOBOX FUNCTIONS
        self.combo_box_funcs()

        # * LIST FUNCTIONS
        self.list_funcs()

        # * TEXT EDIT FUNCTIONS
        self.text_edit_funcs()

        # * SPIN BOX FUNCTIONS
        self.spin_box_funcs()

        # * PROGRESS BAR
        self.ui.pb_test_rate.setFixedHeight(30)

        # * GROUP BOX
        self.ui.gbox_statistics.setVisible(False)
        self.ui.gbox_test_completed.setVisible(False)

        # * STATUS BAR
        self.show_statusbar_message("Wellcome to Auto Test Tool")

        # * MEMU BAR
        self.ui.actionExport_Report.triggered.connect(
            self.menubar_export_report)
        self.ui.actionSupport_Cases.triggered.connect(
            self.menubar_import_support_values
        )

        self.show()

    # ----->> INIT MANAGERS
    def init_managers(self) -> None:
        """
        Initializes the managers for the class.

        This function initializes the following managers:
        - TestManager
        - FunctionManager
        - ExceptionManager
        - UiProgressBarValueManager
        - UiLabelTextManager

        Parameters:
            None

        Returns:
            None
        """
        self._test_manager = TestManager()
        self._function_manager = FunctionManager()
        self._exception_manager = ExceptionManager()
        self._progress_bar_value_manager = UiProgressBarValueManager(
            self.ui.progressBar_coverage_rate
        )

        self._label_tested_line_value_manager = UiLabelTextManager(
            self.ui.lbl_tested_line_count, "Tested Line Count"
        )

        self._label_branced_line_value_manager = UiLabelTextManager(
            self.ui.lbl_branched_count, "Branched Count"
        )

    ##################################################################
    # * --------------------------------------------------------------
    # * * * * * * * * * * * *   UI FUNCTIONS   * * * * * * * * * * * *
    # * --------------------------------------------------------------

    ##################################################################
    # * --------------------------------------------------------------
    # * MENU BAR - ACTIONS FUNCTIONS
    # * --------------------------------------------------------------
    def show_statusbar_message(self, _message: str, _mseconds: int = 3000) -> None:
        """
        Shows a status bar message for a specified duration.

        Args:
            _message (str): The message to be displayed on the status bar.
            _mseconds (int, optional): The duration in milliseconds for which the message should be displayed. 
            Defaults to 3000.

        Returns:
            None: This function does not return anything.
        """
        self.ui.statusbar.showMessage(_message, _mseconds)

    ##################################################################
    # * --------------------------------------------------------------
    # * MENU BAR - ACTIONS FUNCTIONS
    # * --------------------------------------------------------------
    # ----->> Export Reports
    def menubar_export_report(self) -> None:
        """
        Export the report to a file.

        This function prompts the user to select a file location and saves the report
        in a text file. If the report is successfully exported, a success message is
        displayed in the status bar. The user is then given the option to open the
        saved file. If the user chooses to open the file, it is opened with the default
        program. If the export fails, an error message is displayed in the status bar.

        Parameters:
            self (object): The instance of the class calling the function.

        Returns:
            None: This function does not return any value.
        """
        try:
            file_name, _ = file_dialog.getSaveFileName(
                self,
                "Save Report",
                f"{self._function.name}_export_reports.txt",
                "Text Files (*.txt)",
            )
            if file_name and ExportReportManager().export_report(
                file_name, self._function
            ):
                self.show_statusbar_message("Export Report Success")

                reply = ShowMessageBox().show_question(
                    "Open File", "Would you like to open the file you saved?"
                )
                if reply == message_box.Yes:  # type: ignore
                    OpenFileWithDefaultProgramManager().open_file_with_default_program(
                        file_name
                    )
                    self.show_statusbar_message("File is opened successfully")

            else:
                self.show_statusbar_message(
                    "Export Report Failure! Please try later.")
        except AttributeError:
            ShowMessageBox().show_message(
                "Export Report Failure",
                "Please run the test process at least 1 time first.",
            )

    # ----->> Import Support Values
    def menubar_import_support_values(self) -> None:
        """
        Sets the current index of the stacked widget to 1, which displays the import support values page in the menubar UI.

        Parameters:
            self (Menubar): The Menubar instance.

        Returns:
            None
        """
        self.ui.stackedWidget.setCurrentIndex(1)

    ##################################################################
    # * --------------------------------------------------------------
    # * BUTTON FUNCTIONS
    # * --------------------------------------------------------------
    def button_funcs(self) -> None:
        """
        Initializes the button functions.

        This function sets up the functionality of various buttons in the user interface.
        It disables the "Import Code" button, connects the "Import Code" button to the 
        "run_test" method, and connects the "Support Case Done" button to the method 
        that changes the current index of the stacked widget to 0. Additionally, it 
        connects the "Support Case Clear Cases" button to the "clear_support_cases" 
        method, and connects the "Support Case Add" button to the "add_support_cases" 
        method.

        Parameters:
            self (ClassName): The instance of the class.

        Returns:
            None
        """
        self.ui.btn_import_code.setEnabled(False)
        self.ui.btn_import_code.clicked.connect(self.run_test)
        self.ui.btn_support_case_done.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(0)
        )
        self.ui.btn_support_case_clear_cases.clicked.connect(
            self.clear_support_cases)
        self.ui.btn_support_case_clear_cases.clicked.connect(
            self.clear_support_cases)

        self.ui.btn_support_case_add.clicked.connect(self.add_support_cases)

    # ----->> CLEAR SUPPORT CASES
    def clear_support_cases(self) -> None:
        """
        Clear support cases from the UI and the internal support cases list.

        Parameters:
            None

        Returns:
            None
        """
        self.ui.lw_support_case_values.clear()
        self._support_cases.clear()

    # ----->> ADD SUPPORT CASES
    def add_support_cases(self) -> None:
        """
        Adds a support case to the list of support cases.

        Parameters:
            None

        Returns:
            None
        """
        try:
            value = self.ui.txt_support_case_support_case.text()
            if not self.ui.checkbox_support_case_str.isChecked():
                if value.startswith("."):
                    value = "0" + value
                elif value.endswith("."):
                    value = value + "0"
                value = float(value) if "." in value else int(value)

            self._support_cases.append(value)
            self.ui.lw_support_case_values.clear()
            self.ui.lw_support_case_values.addItems(
                str(val) for val in self._support_cases
            )
            self.ui.txt_support_case_support_case.clear()
            self.ui.txt_support_case_support_case.setFocus()
        except Exception:
            ShowMessageBox().show_message(
                "Type Error",
                "Please be mindful of the value you enter and the Checkbox named 'String'.",
            )
            self.ui.txt_support_case_support_case.setFocus()
            self.ui.txt_support_case_support_case.selectAll()

    # ----->> CHECK 'IS FUNCTION'
    def _check_is_function_lines(self, _lines: str) -> bool:
        """
        Checks if the given lines of code contain any function definition.

        Parameters:
            _lines (str): The lines of code to check.

        Returns:
            bool: True if the lines contain a function definition, False otherwise.
        """
        return any(line.strip().startswith("def ") and line.strip().endswith(":") for line in _lines.split("\n"))

    # ----->> TEST CASES
    def generate_test_cases(self) -> None:
        """
        Generate test cases for the given function.

        This function generates test cases based on the specified test pool count
        and the current function. It updates the UI to display the progress of the
        test generation. The test cases generated are added to the function's list
        of test cases.

        Parameters:
            None.

        Returns:
            None.
        """
        # --->> Test Case Gererated
        test_pool_count: int = self.ui.sp_test_cases_pool_count.value()

        current_count = 0
        self.ui.gbox_test_completed.setVisible(True)
        self.ui.gbox_test_completed.setFocus()
        self.ui.pb_test_rate.setFormat(
            "0% of the test is complete, please wait")
        self.ui.pb_test_rate.setValue(0)
        self.ui.lbl_branched_count.setText("Branched Count:")
        self.ui.lbl_tested_line_count.setText("Tested Line Count:")
        self.change_object_enabled(False)

        self.show_statusbar_message("Test Started")

        application.processEvents()
        try_count = 0
        while current_count < test_pool_count:
            test_cases_list: list[TestCase] = self._test_manager.generate_test_cases(
                self._function
            )
            try_count += 1
            if self._function.branch_count == 0:
                tested_rate = 100

                self.ui.pb_test_rate.setFormat(
                    f"{tested_rate:>6}% of the test is complete, please wait")
                break

            if len(test_cases_list) == self._function.branch_count:
                self._function.add_test_case = [
                    case_pool for case_pool in test_cases_list
                ]
                current_count += 1

                step: float = 100 / test_pool_count
                tested_rate: float = round(step * current_count, 2)
                if round(step * current_count, 2) > 100:
                    tested_rate = 100.00
                point_count: int = current_count % 4
                point = "." * point_count

                self.ui.pb_test_rate.setFormat(
                    f"{tested_rate:>6}% of the test is complete, please wait {point}"
                )
                self.ui.pb_test_rate.setValue(round(tested_rate))
                application.processEvents()
            if try_count == 10:
                result = ShowMessageBox().show_question(
                    "Warning",
                    "A large number of attempts were made, but the result could not be reached. Would you like to continue?",
                )
                if result == 16_384:
                    try_count = 0
                else:
                    break
        sleep(1)
        self.ui.gbox_test_completed.setVisible(False)
        self.ui.gbox_statistics.setVisible(True)

    def create_function(self, _source_code: str) -> None:
        """
        Creates a function based on the given source code.

        Parameters:
            _source_code (str): The source code of the function.

        Returns:
            None
        """
        self._function: Function = Function()
        if self._check_is_function_lines(_source_code):
            self._function = self._function_manager.str_to_function(
                _source_code
            )
        else:
            func_lines: list[str] = ["def This_Is_The_Way():"] + [" " * 4 +
                                                                  line for line in _source_code.splitlines()]
            self._function = self._function_manager.str_to_function(
                "\n".join(func_lines))

        self._function.support_cases = self._support_cases

    def fixed_source_code(self) -> None:
        """
        Clears the 'list_fixed_code' widget and populates it with the fixed code lines.

        Parameters:
            None

        Returns:
            None
        """
        # ----->> FIXED CODE (LIST WIDGET)
        self.ui.list_fixed_code.clear()
        self.ui.list_fixed_code.addItems(
            [
                f"({index:^10})\t{line}"
                for index, line in enumerate(self._function.code_lines, start=1)
            ]
        )

    def combo_box_add_test_case_name(self) -> None:
        """
        Add the name of the test case to the combo box widget.

        This function clears the current items in the combo box and adds the name of the test case.
        The combo box is then enabled if there are test cases available.

        Parameters:
            None

        Returns:
            None
        """
        # ----->> TEST CASE NAME (COMBO BOX WIDGET)
        self.ui.cbx_test_case_name.clear()
        self.ui.cbx_test_case_name.addItem(self._function.name)
        self.ui.cbx_test_case_name.setEnabled(
            len(self._function.test_cases) > 0)

    def change_object_enabled(self, _state: bool) -> None:
        """
        Enables or disables a group of widgets.

        Args:
            _state (bool): The state to set for the widgets. If True, the widgets will be enabled. If False, the widgets will be disabled.

        Returns:
            None: This function does not return anything.
        """
        widgets = [
            self.ui.btn_import_code,
            self.ui.list_fixed_code,
            self.ui.list_test_cases,
            self.ui.list_tested_code_line,
            self.ui.txt_source_code,
            self.ui.cbx_test_case_name,
            self.ui.menubar
        ]
        for widget in widgets:
            widget.setEnabled(_state)

    # ----->> RUN TEST
    def _run_test_progress(self, _source_code: str) -> None:
        """
        Run the test progress by performing the following steps:

        1. Create a function using the provided source code.
        2. Display the fixed source code in a list widget.
        3. Generate test cases for the function.
        4. Add the test case name to the combo box widget.
        5. Show a message in the status bar indicating that the test is completed.

        Parameters:
        - _source_code (str): The source code to create the function from.

        Returns:
        - None
        """
        # ----->> SOURCE CODE (TEXT EDIT WIDGET)
        self.create_function(_source_code)

        # ----->> FIXED CODE (LIST WIDGET)
        self.fixed_source_code()
        # --->> Test Case Gererated
        self.generate_test_cases()
        # ----->> TEST CASE NAME (COMBO BOX WIDGET)
        self.combo_box_add_test_case_name()
        # ----->> STATUS BAR (STATUS BAR WIDGET)
        self.show_statusbar_message("Test Completed")

        self.change_object_enabled(True)
        self.ui.cbx_test_case_name.setFocus()

    def _handle_test_exeption(self, _exception: Exception) -> None:
        """
        Handles the given exception that occurred during the test execution.

        Args:
            _exception (Exception): The exception that occurred.

        Returns:
            None
        """
        self.ui.gbox_statistics.setVisible(False)
        self.ui.gbox_test_completed.setVisible(False)

        error_handlers = {
            SyntaxError: self._exception_manager.handle_syntax_error,
            NameError: self._exception_manager.handle_name_error,
            IndexError: self._exception_manager.handle_index_error,
            KeyError: self._exception_manager.handle_key_error,
            ValueError: self._exception_manager.handle_value_error,
            TypeError: self._exception_manager.handle_type_error,
            AttributeError: self._exception_manager.handle_attribute_error,
            ArithmeticError: self._exception_manager.handle_arithmetic_error,
        }

        handler = error_handlers.get(type(_exception))  # type: ignore
        if handler:
            handler(_exception, self._function.code_lines,  # type: ignore
                    self.ui.txt_source_code, self.ui.list_fixed_code)  # type: ignore
            self.ui.btn_import_code.setEnabled(True)
            self.ui.txt_source_code.setEnabled(True)
            self.ui.txt_source_code.setFocus()

    def run_test(self) -> None:
        """
        Run the test.

        This function is responsible for running the test. It clears the screen, retrieves the source code from the UI, and then calls the "_run_test_progress" function if the source code is not empty. It catches various exceptions and calls the "_handle_test_exception" function to handle them.

        Parameters:
            self (TestClass): The instance of the TestClass.

        Returns:
            None: This function does not return anything.
        """
        try:
            self.clear_screan()
            source_code: str = self.ui.txt_source_code.toPlainText()

            if source_code:
                self._run_test_progress(source_code)

        except (
            SyntaxError,
            NameError,
            IndexError,
            KeyError,
            ValueError,
            TypeError,
            AttributeError,
            ArithmeticError,
        ) as e:
            self._handle_test_exeption(e)

    ##################################################################
    # * --------------------------------------------------------------
    # * COMBOBOX FUNCTIONS
    # * --------------------------------------------------------------

    def combo_box_funcs(self) -> None:
        """Disables the test case name combo box and connects the currentTextChanged signal to the cbx_test_case_name_changed slot.
        """
        self.ui.cbx_test_case_name.setEnabled(False)
        self.ui.cbx_test_case_name.currentTextChanged.connect(
            self.cbx_test_case_name_changed
        )

    # ----->> TEST CASE NAME
    def cbx_test_case_name_changed(self) -> None:
        """
        Callback function triggered when the test case name is changed.

        This function updates the list of test cases displayed in the UI based on the selected test case name.

        Parameters:
            self (ClassName): The instance of the class.

        Returns:
            None
        """
        try:
            lw_test_cases = self.ui.list_test_cases
            lw_test_cases.clear()
            txt_cbx_test_case_name: str = self.ui.cbx_test_case_name.currentText()

            if txt_cbx_test_case_name:
                test_cases: list[Any] = []
                for pool in self._function.test_cases:
                    tcases: list[str] = [
                        case.test_values.replace(",", " , ") for case in pool
                    ]
                    test_cases.append(tcases)

                test_pools_count: int = self.ui.sp_test_cases_pool_count.value()
                for pool_index in range(test_pools_count):
                    test_cases_count: int = self._function.branch_count
                    for case_index in range(test_cases_count):
                        test_cases[pool_index][case_index] = test_cases[pool_index][
                            case_index:
                        ]

                for pool in test_cases:
                    for tcase in pool:
                        value: str = " , ".join(tcase)
                        lw_test_cases.addItem(value)

        except Exception:
            pass

    ##################################################################
    # * --------------------------------------------------------------
    # * LIST FUNCTIONS
    # * --------------------------------------------------------------
    def list_funcs(self) -> None:
        """
        List all available functions.

        This method connects the `currentItemChanged` signal of the `list_test_cases` object
        to the `list_test_cases_changed_selected_case` method.

        Parameters:
            None

        Returns:
            None
        """
        self.ui.list_test_cases.currentItemChanged.connect(
            self.list_test_cases_changed_selected_case
        )

    # ----->> TEST CASE LIST
    def list_test_cases_changed_selected_case(self) -> None:
        """
        Retrieves the selected test case from the list of test cases and updates the UI with the details of the selected case.

        Parameters:
            None

        Returns:
            None
        """
        try:
            list_current_row: int = self.ui.list_test_cases.currentRow()
            current_case_name: str = self.ui.cbx_test_case_name.currentText()
            if current_case_name and list_current_row >= 0:
                function_branch_count: int = self._function.branch_count
                current_test_case: TestCase = self._function.test_cases[
                    list_current_row // function_branch_count
                ][list_current_row % function_branch_count]

                # ----->> PROGRESS BAR
                self._progress_bar_value_manager.update_value(
                    current_test_case.test_coverages_rate
                )

                # ----->> TESTED CODE LINES (LIST WIDGET)
                self.ui.list_tested_code_line.clear()

                self.ui.list_tested_code_line.addItems(
                    [
                        f"({index:^10})\t{line}"
                        for index, line in enumerate(
                            current_test_case.tested_lines, start=1
                        )
                    ]
                )

                # ----->> TESTED CODE LINE AND BRANCDED (LABEL WIDGET)
                self._label_branced_line_value_manager.upgrade_value(
                    current_test_case.tested_branches_count, self._function.branch_count
                )
                self._label_tested_line_value_manager.upgrade_value(
                    current_test_case.tested_lines_count,
                    self._function.code_lines_count,
                )

                current_tc: str = self.ui.list_test_cases.currentItem().text()  # type: ignore

                # ----->> CURRENT TEST CASE
                if current_tc == "()":
                    current_tc = ""
                    self.ui.list_test_cases.clear()
                    self.ui.list_test_cases.addItem(current_tc)

        except Exception:
            pass

    ##################################################################
    # * --------------------------------------------------------------
    # * TEXT EDIT FUNCTIONS
    # * --------------------------------------------------------------
    def text_edit_funcs(self) -> None:
        """
        Connects the textChanged signal of the txt_source_code QLineEdit widget to the txt_source_code_text_changed slot.

        Parameters:
            self (self): The instance of the class.

        Returns:
            None
        """
        self.ui.txt_source_code.textChanged.connect(
            self.txt_source_code_text_changed)

    # ----->> SOURCE CODE
    def txt_source_code_text_changed(self) -> None:
        """
        A callback function that is triggered when the text in the source code text editor is changed.
        It clears the screen.
        """
        self.clear_screan()

    ##################################################################
    # * --------------------------------------------------------------
    # * SPIN BOX FUNCTIONS
    # * --------------------------------------------------------------
    def spin_box_funcs(self) -> None:
        """
        Connects the `valueChanged` signal of the `sp_test_cases_pool_count` spin box to the `sp_test_cases_pool_count_changed` slot.
        """
        self.ui.sp_test_cases_pool_count.valueChanged.connect(
            self.sp_test_cases_pool_count_changed
        )

    # ----->> TEST CASES POOL COUNT
    def sp_test_cases_pool_count_changed(self) -> None:
        """
        Update the suffix of the sp_test_cases_pool_count widget based on its value.

        This function retrieves the value of the sp_test_cases_pool_count widget and determines the appropriate suffix based on the value. If the value is 1, the suffix is set to "  pool"; otherwise, the suffix is set to "  pools". Finally, the clear_screan method is called to clear the screen.

        Parameters:
            self (TYPE): The object instance.

        Return:
            None
        """
        sp_counter = self.ui.sp_test_cases_pool_count
        count: int = sp_counter.value()
        suffix: str = "  pool" if count == 1 else "  pools"
        sp_counter.setSuffix(suffix)
        self.clear_screan()

    ##################################################################
    # * --------------------------------------------------------------
    # * CLEAR SCREAN
    # * --------------------------------------------------------------
    def clear_screan(self) -> None:
        """
        Clears the screen and resets the state of the UI.

        This function is responsible for clearing the screen and resetting the state of the UI
        elements. It is called when the user wants to start a new session or reset the current
        session. The function performs the following actions:

        - If the source code text is not empty, it shows a "Tool Ready" message in the status
          bar and enables the "Import Code" button.
        - If the source code text is empty, it disables the "Import Code" button and the
          "Test Case Name" combo box.
        - Clears the following UI elements:
          - Fixed Code List
          - Test Cases List
          - Tested Code Line List
          - Test Case Name Combo Box
          - Branched Count Label
          - Tested Line Count Label
          - Selected Test Case
          - Test Case Name Combo Box Index
          - Coverage Rate Progress Bar
        - Hides the "Statistics" and "Test Completed" group boxes.
        - Deletes the current function object.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        try:
            if len(self.ui.txt_source_code.toPlainText()) > 0:
                self.show_statusbar_message("Tool Ready")
                self.ui.btn_import_code.setEnabled(True)
            else:
                self.ui.btn_import_code.setEnabled(False)
                self.ui.cbx_test_case_name.setEnabled(False)

            # ----->> SET DEFAULTS
            self.ui.list_fixed_code.clear()
            self.ui.list_test_cases.clear()
            self.ui.list_tested_code_line.clear()
            self.ui.cbx_test_case_name.clear()
            self.ui.lbl_branched_count.setText("Branched Count:")
            self.ui.lbl_tested_line_count.setText("Tested Line Count:")
            self.ui.list_test_cases.setCurrentRow(-1)

            self.ui.cbx_test_case_name.setCurrentIndex(-1)
            self.ui.progressBar_coverage_rate.setValue(0)

            self.ui.gbox_statistics.setVisible(False)
            self.ui.gbox_test_completed.setVisible(False)

            del self._function

        except Exception:
            pass


# RUN APP
if __name__ == "__main__":
    app = application(sys.argv)
    win = AttApp()
    win.show()
    sys.exit(app.exec_())
