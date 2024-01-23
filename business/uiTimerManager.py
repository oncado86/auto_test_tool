"""
This class defines a UI progress bar value manager.
The UiLabelTextManager class is responsible for managing a label's text and value.
"""


from PyQt5.QtCore import QTimer as timer
from PyQt5.QtWidgets import (
    QProgressBar as progressbar,
    QLabel as label,
)


class UiProgressBarValueManager:
    """This class defines a UI progress bar value manager. 
    Here's a summary of what each class method does:

    - __init__: Initializes a new instance of the class and assigns the progress bar object.
    - __increase_value: Increases the value of the progress bar by one and checks if it has reached the specified rate.
    - __decrease_value: Decreases the value of the progress bar by one.
    - up_value: Increases the value of the progress bar at a given rate.
    - down_value: Decreases the value of the progress bar at a specified rate.
    - update_value: Updates the value of the progress bar to the new specified value.

    @cateory: Business, Manager, UI
    """

    def __init__(self, _progress_bar: progressbar) -> None:
        """
        Initializes a new instance of the class.

        Args:
            _progress_bar (progressbar): The progress bar object.

        Returns:
            None: This function does not return anything.
        
        @cateory: Business, Manager, UI
        """
        self.__pb: progressbar = _progress_bar

    def __increase_value(self, _rate: int, _timer: timer) -> None:
        """
        Increase the value of the progress bar by one and check if it has reached the specified rate.

        Parameters:
            _rate (int): The specified rate at which the progress bar value should be checked.
            _timer (timer): The timer object that controls the interval at which the progress bar value is checked.

        Returns:
            None: This function does not return any value.
        """
        pb_value: int = self.__pb.value()
        self.__pb.setValue(pb_value + 1)
        if self.__pb.value() == _rate:
            _timer.stop()
            del _timer

    def __decrease_value(self, _rate: int, _timer: timer) -> None:
        """
        Decreases the value of a progress bar by 1.

        Args:
            _rate (int): The rate at which the value of the progress bar is being decreased.
            _timer (timer): The timer object associated with the progress bar.

        Returns:
            None: This function does not return anything.
        """
        self.__pb.setValue(self.__pb.value() - 1)
        if self.__pb.value() == _rate:
            _timer.stop()
            del _timer

    def up_value(self, _rate: int) -> None:
        """
        Increase the value at a given rate.

        Parameters:
            _rate (int): The rate at which the value should be increased.

        Returns:
            None: This function does not return anything.
        """
        _timer = timer()
        _timer.timeout.connect(lambda: self.__increase_value(_rate, _timer))
        _timer.start(10)

    def down_value(self, _rate: int) -> None:
        """
        Decreases the value at a specified rate.

        Parameters:
            _rate (int): The rate at which the value should be decreased.

        Returns:
            None
        """
        _timer = timer()
        _timer.timeout.connect(lambda: self.__decrease_value(_rate, _timer))
        _timer.start(10)

    def update_value(self, _value: float) -> None:
        """
        Updates the value of the object.

        Args:
            _value (float): The new value to be updated.

        Returns:
            None
        """
        _rate = int(_value)

        if _rate > self.__pb.value():
            self.up_value(_rate)
        elif _rate < self.__pb.value():
            self.down_value(_rate)


class UiLabelTextManager:
    """The UiLabelTextManager class is responsible for managing a label's text and value. 
    Here's a summary of each class method:

    - __init__(_label: label, _prefix: str): Initializes the class with a label and prefix.
    - __increase_value(_tested_value: int, _timer: timer): Increases the value by 1 and updates the label text.
    - __decrease_value(_tested_value: int, _timer: timer): Decreases the value by 1 and updates the label text.
    - up_value(_value: int): Increases the value by a given integer using a timer.
    - down_value(_value: int): Decreases the value by a given integer using a timer.
    - upgrade_value(_value: int, _value_count: int): Upgrades the value by setting a new value count and calling the appropriate methods based on the given value and current value comparison.
    
    @cateory: Business, Manager, UI
    """

    def __init__(self, _label: label, _prefix: str) -> None:
        """
        Initialize the class with the given label and prefix.

        Parameters:
            _label (label): The label to be assigned to the instance.
            _prefix (str): The prefix to be assigned to the instance.

        Returns:
            None
        
        @cateory: Business, Manager, UI
        """
        self.__current_value: int = 0
        self.__lbl: label = _label
        self.__text_prefix: str = _prefix
        self.__value_count: int = 0

    def __increase_value(self, _tested_value: int, _timer: timer) -> None:
        """
        Increase the value by 1 and update the label text.

        Parameters:
            _tested_value (int): The value to test against the current value.
            _timer (timer): The timer object used to stop the timer.

        Returns:
            None
        """
        self.__current_value += 1
        lbl_txt: str = (
            f"{self.__text_prefix}: {self.__current_value} / {self.__value_count}"
        )
        self.__lbl.setText(lbl_txt)
        if self.__current_value == _tested_value:
            _timer.stop()
            del _timer

    def __decrease_value(self, _tested_value: int, _timer: timer) -> None:
        """
        Decreases the current value by 1 and updates the label text to reflect the new value.

        Parameters:
            _tested_value (int): The value to compare with the current value.
            _timer (timer): The timer object associated with the value.

        Returns:
            None
        """
        self.__current_value -= 1
        lbl_txt: str = (
            f"{self.__text_prefix}: {self.__current_value} / {self.__value_count}"
        )
        self.__lbl.setText(lbl_txt)
        if self.__current_value == _tested_value:
            _timer.stop()
            del _timer

    def up_value(self, _value: int) -> None:
        """
        Increase the value by a given integer using a timer.

        Parameters:
            _value (int): The integer value to increase.

        Returns:
            None
        """
        _timer = timer()
        _timer.timeout.connect(lambda: self.__increase_value(_value, _timer))
        _timer.start(50)

    def down_value(self, _value: int) -> None:
        """
        Decreases the given value by calling the __decrease_value method at regular intervals.

        Parameters:
            _value (int): The value to be decreased.

        Returns:
            None
        """
        _timer = timer()
        _timer.timeout.connect(lambda: self.__decrease_value(_value, _timer))
        _timer.start(50)

    def upgrade_value(self, _value: int, _value_count: int) -> None:
        """
        Upgrades the value by setting the new value count and calling the appropriate methods based on the comparison between the given value and the current value.

        Parameters:
            _value (int): The new value to be upgraded.
            _value_count (int): The new value count.

        Returns:
            None
        """
        self.__value_count = _value_count
        if _value > self.__current_value:
            self.up_value(_value)
        elif _value < self.__current_value:
            self.down_value(_value)
