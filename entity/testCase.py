"""
This class definition is for a TestCase class.
"""

class TestCase:
    """
    This class definition is for a TestCase class. Here's a summary of what each class method does:

    - __init__(self): Initializes the class with default values for test-related attributes.
    - test_values: Gets and sets the value of the test_values property.
    - tested_lines: Gets and sets the list of tested lines.
    - tested_branches_count: Gets and sets the number of tested branches.
    - tested_lines_count: Returns the number of tested lines.
    - test_coverages_rate: Gets and sets the test coverages rate.

    Initializes the class with default values for test-related attributes.

        Parameters:
            None

        Returns:
            None

        @category: Entity Classes
    """

    def __init__(self) -> None:
        """
        Initializes the class with default values for test-related attributes.

        Parameters:
            None

        Returns:
            None

        @category: Entity Classes
        """
        self.__test_values: str = ""
        self._tested_lines: list[str] = []
        self.__tested_branches_count: int = 0
        self._test_coverages_rate: float = 0

    @property
    def test_values(self) -> str:
        """
        Get the value of the test_values property.

        Returns:
            str: The value of the test_values property.
        """
        return self.__test_values

    @test_values.setter
    def test_values(self, _value: str) -> None:
        """
        Set the value of test_values.

        Args:
            _value (str): The new value for test_values.

        Returns:
            None
        """
        self.__test_values = _value

    @property
    def tested_lines(self) -> list[str]:
        """
        Get the list of tested lines.

        Returns:
            list[str]: The list of tested lines.
        """
        return self.__tested_lines

    @tested_lines.setter
    def tested_lines(self, _lines: list[str]) -> None:
        """
        Set the value of the 'tested_lines' attribute.

        Parameters:
            _lines (list[str]): A list of strings representing the lines of code that have been tested.

        Returns:
            None
        """
        self.__tested_lines = _lines

    @property
    def tested_branches_count(self) -> int:
        """
        Returns the number of tested branches.

        Returns:
            int: The number of tested branches.
        """
        return self.__tested_branches_count

    @tested_branches_count.setter
    def tested_branches_count(self, _count: int) -> None:
        """
        Setter method for the tested_branches_count attribute.

        Parameters:
            _count (int): The new value to set for the tested_branches_count attribute.

        Returns:
            None: This method does not return anything.
        """
        self.__tested_branches_count = _count

    @property
    def tested_lines_count(self) -> int:
        """
        Returns the number of tested lines.

        Parameters:
            None

        Returns:
            int: The count of tested lines.
        """
        return len(self.__tested_lines)

    @property
    def test_coverages_rate(self) -> float:
        """
        Get the test coverages rate.
        
        Returns:
            float: The test coverages rate.
        """
        return self.__test_coverages_rate

    @test_coverages_rate.setter
    def test_coverages_rate(self, _rate: float) -> None:
        """
        Setter method for the test_coverages_rate property.

        Args:
            _rate (float): The new value for the test_coverages_rate.

        Returns:
            None
        """
        self.__test_coverages_rate = _rate
