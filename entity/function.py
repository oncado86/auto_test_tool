"""
This class definition is for a class called "Function".
"""
from typing import Any
from entity.testCase import TestCase


class Function:
    """
    This class definition is for a class called "Function". 
    It represents a function in a programming language and has several attributes and methods:

    - __init__: Initializes the object with default values for the attributes.
    - name: Gets or sets the name of the function.
    - signature: Gets or sets the signature of the function.
    - arguments: Gets or sets the arguments of the function.
    - code_lines: Gets or adds a code line to the list of code lines.
    - exec_lines: Gets or sets the execution lines of the function.
    - branch_count: Gets or sets the branch count of the function.
    - code_lines_count: Gets or sets the number of lines of code in the function.
    - test_cases: Gets or adds a test case to the list of test cases associated with the function.
    - support_cases: Gets or sets the support cases associated with the function.

    @category: Entity Classes
    @see: TestCase (Entity Class)
    @import: TestCase (Entity Class)
    """

    def __init__(self) -> None:
        """
        Initializes the object with default values for the attributes.

        @category: Entity Classes
        @see: TestCase (Entity Class)
        @import: TestCase (Entity Class)
        """
        self.__name: str = ""
        self.__signature: str = ""
        self.__arguments: str = ""
        self.__code_lines: list[str] = []
        self.__exec_lines: str = ""
        self.__branch_count: int = 0
        self.__code_lines_count: int = 0
        self.__test_cases: list[list[TestCase]] = []
        self.__support_values: list[Any] = []

    @property
    def name(self) -> str:
        """
        Return the name of the object.

        Returns:
            str: A string representing the name of the object.
        """
        return self.__name

    @name.setter
    def name(self, _name: str) -> None:
        """
        Set the value of the `name` attribute.

        Parameters:
            _name (str): The new value for the `name`.

        Returns:
            None: This function does not return anything.
        """
        self.__name = _name

    @property
    def signature(self) -> str:
        """
        Returns the signature of the object.

        Returns:
            str: The signature of the object.
        """
        return self.__signature

    @signature.setter
    def signature(self, _signature: str) -> None:
        """
        Sets the signature of the object.

        Parameters:
            _signature (str): The signature to be set.

        Returns:
            None
        """
        self.__signature = _signature

    @property
    def arguments(self) -> str:
        """
        Returns the value of the `arguments` property.
        It is a string representing the arguments of the function.

        Returns:
            str: The arguments of the function.
        """
        return self.__arguments

    @arguments.setter
    def arguments(self, _arguments: str) -> None:
        """
        Setter method for the 'arguments' attribute.

        Args:
            _arguments (str): The new value for the 'arguments' attribute.

        Returns:
            None: This method does not return anything.
        """
        self.__arguments = _arguments

    @property
    def code_lines(self) -> list[str]:
        """
        Return the code lines of the object as a list.

        Parameters:
            None

        Returns:
            list[str]: A list of code lines.
        """
        return self.__code_lines

    @code_lines.setter
    def add_code_line(self, _code_line: str) -> None:
        """
        Adds a code line to the list of code lines.

        Parameters:
            _code_line (str): The code line to be added.

        Returns:
            None
        """
        self.__code_lines.append(_code_line)

    @property
    def exec_lines(self) -> str:
        """
        Get the value of the `exec_lines` property.

        Returns:
            str: The value of the `exec_lines` property.
        """
        return self.__exec_lines

    @exec_lines.setter
    def exec_lines(self, _exec_line: str) -> None:
        """
        Setter method for the `exec_lines` attribute.

        Parameters:
            _exec_line (str): The new value for the `exec_lines` attribute.

        Returns:
            None: This method does not return anything.
        """
        self.__exec_lines = _exec_line

    @property
    def branch_count(self) -> int:
        """
        Returns the branch count of the object.

        Returns:
            int: The branch count.
        """
        return self.__branch_count

    @branch_count.setter
    def branch_count(self, _count: int) -> None:
        """
        Setter method for the branch_count attribute.

        Parameters:
            _count (int): The new value for the branch_count attribute.

        Returns:
            None
        """
        self.__branch_count = _count

    @property
    def code_lines_count(self) -> int:
        """
        Get the number of lines of code in the file.

        Returns:
            int: The number of lines of code in the file.
        """
        return self.__code_lines_count

    @code_lines_count.setter
    def code_lines_count(self, _count: int) -> None:
        """
        Set the count of code lines.

        Parameters:
            _count (int): The count of code lines.

        Returns:
            None
        """
        self.__code_lines_count = _count

    @property
    def test_cases(self) -> list[list[TestCase]]:
        """
        Returns the test cases associated with the current instance.

        Returns:
            list[list[TestCase]]: The test cases.
        """
        return self.__test_cases

    @test_cases.setter
    def add_test_case(self, _test_case: list[TestCase]) -> None:
        """
        Setter method for the add_test_case property.

        Parameters:
            _test_case (list[TestCase]): The test case to add.

        Returns:
            None: This method does not return anything.
        """
        self.__test_cases.append(_test_case)

    @property
    def support_cases(self) -> list[Any]:
        """
        Returns the support cases.

        Returns:
            list[Any]: A list of support cases.
    """
        return self.__support_values

    @support_cases.setter
    def support_cases(self, _support_values: list[Any]) -> None:
        """
        Setter method for the support_cases attribute.

        Parameters:
            _support_values (list[Any]): The new value for the support_cases attribute.

        Returns:
            None: This method does not return anything.
        """
        self.__support_values = _support_values
