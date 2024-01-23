"""
This class, FunctionManager, is responsible for managing functions and their operations. 
"""

import random
import string
from typing import Any
from business.codeManager import CodeManaager
from entity.function import Function


class FunctionManager:
    """
    This class, FunctionManager, is responsible for managing functions and their operations. 
    Here's what each class method does:

    - __init__(self): Initializes an instance of the class and sets up a CodeManaager object.
    - str_to_function(self, _code_str: str) -> Function: Converts a string representation of a function into a Function object. 
    It extracts information such as branch count, code lines count, and executable lines.
    - __convert_type(self, _type: str) -> type[str] | type[float] | type[int] | None: Converts an input type string to the corresponding Python type.
    - parse_function_args(self, _function: Function) -> dict[str, Any]: Parses the function arguments of a given Function object and returns a dictionary mapping the argument names to their corresponding types.
    - __create_values_to_arguments(self, _function: Function) -> dict[str, Any]: Generates a dictionary of random values for each argument of a given function.
    - change_argument_value(self, _function: Function) -> str: Generates a string representation of the arguments for a given function.
    - remove_function_calls_in_funcexeclines(self, _function: Function) -> None: Removes all function calls in the exec_lines attribute of the given _function.
    - add_function_call_in_funcexeclines(self, _function: Function, pars: str) -> None: Adds a function call to the exec_lines list of a Function object.

    @category: Business, Manager
    @import: Function, CodeManaager
    @see: Function, CodeManaager
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the class.

        Parameters:
            None

        Returns:
            None

        @category: Business, Manager
        @import: Function, CodeManaager
        @see: Function, CodeManaager
        """
        self.__cm = CodeManaager()

    def str_to_function(self, _code_str: str) -> Function:
        """
        Converts a string representation of a function into a Function object.

        Parameters:
            _code_str (str): The string representation of the function.

        Returns:
            Function: The Function object representing the converted function.
        """
        code: str = self.__cm.fixed_source_code(_code_str)
        code_lines: list[str] = self.__cm.get_code_lines(code)

        func: Function = Function()
        func.branch_count = self.__cm.get_branched_count(code)
        func.code_lines_count = len(code_lines)
        func.exec_lines = self.__cm.add_content_to_code(code)

        for line in code_lines:
            left_space_count: int = self.__cm.left_space_count(line)

            func.add_code_line = line

            if line.startswith(f"{' '*left_space_count}def "):
                func.name = line.split("def ")[1].split("(")[0]
                func.arguments = (
                    "(" +
                    line.split("def ")[1].split("(")[1].split(")")[0] + ")"
                )
                func.signature = func.name + func.arguments

        return func

    def __convert_type(self, _type: str) -> type[str] | type[float] | type[int] | None:
        """
        Convert the input type string to the corresponding Python type.

        Args:
            _type (str): The type string to be converted.

        Returns:
            Union[type[str], type[float], type[int], None]: The corresponding Python type if found, 
            or None if the type string is not recognized.
        """
        return {"str": str, "float": float, "int": int}.get(_type)

    def parse_function_args(self, _function: Function) -> dict[str, Any]:
        """
        Parses the function arguments of a given Function object and returns a dictionary mapping the argument names to their corresponding types.

        Parameters:
            _function (Function): The Function object to parse the arguments from.

        Returns:
            dict[str, Any]: A dictionary mapping the argument names to their corresponding types.
        """
        args: list[str] = _function.arguments.split("(")[1].split(")")[
            0].split(",")

        function_args: dict[str, Any] = {}
        for arg in args:
            key, *typ_parts = arg.split(":")
            typ: type[str] | type[float] | type[int] | None = self.__convert_type(
                typ_parts[0].strip()) if typ_parts else None
            function_args[key.strip()] = typ

        return function_args

    def __create_values_to_arguments(self, _function: Function) -> dict[str, Any]:
        """
        Generates a dictionary of random values for each argument of a given function.

        Args:
            _function (Function): The function for which to generate the values.

        Returns:
            dict[str, Any]: A dictionary mapping each argument name to its randomly generated value.
        """
        args: dict[str, Any] = {}

        letters: str = string.ascii_letters + string.digits + "!#$%&*+,-.:;<=>?@^_`|~ "
        arguments: dict[str, Any] = self.parse_function_args(_function)

        if len(_function.arguments) <= 2:
            return args

        edge_right: int = random.choice(
            [*range(11)] + [*range(101)] + [*range(1001)] + [*range(10001)]
        )
        edge_left: int = random.choice(
            [*range(0, -10, -1)]
            + [*range(-10, -101, -1)]
            + [*range(-100, -1001, -1)]
            + [*range(-1001, -10001, -1)]
        )

        while len(args) < len(arguments):
            for arg, arg_type in arguments.items():
                if arg in args:
                    continue

                if arg_type == int:
                    args[arg] = random.randint(edge_left, edge_right)
                elif arg_type == float:
                    args[arg] = round(random.uniform(-1, 1) * edge_right, 1)
                elif arg_type == str:
                    edge_left, edge_right = abs(edge_left), abs(edge_right)
                    if edge_left > edge_right:
                        edge_left, edge_right = edge_right, edge_left
                    args[arg] = "".join(random.choices(
                        letters, k=random.randint(edge_left, edge_right)))
                elif arg_type is None:
                    edge_left, edge_right = abs(edge_left), abs(edge_right)
                    if edge_left > edge_right:
                        edge_left, edge_right = edge_right, edge_left

                    args[arg] = random.choice(
                        [
                            random.randint(edge_left, edge_right),
                            round(random.uniform(-1, 1) * edge_right, 1),
                            f'{"".join(random.choices(letters, k=random.randint(edge_left, edge_right)))}',
                        ]
                    )

        return args

    def change_argument_value(self, _function: Function) -> str:
        """
        Generates a string representation of the arguments for a given function.

        Args:
            _function (Function): The function object for which the argument values need to be generated.

        Returns:
            str: A string representation of the arguments in the format "(arg1,arg2,arg3,...)".

        """
        arg_values: dict[str, Any] = self.__create_values_to_arguments(
            _function)
        return "(" + ",".join([f'"{val}"' if isinstance(val, str) else str(val) for val in arg_values.values()]) + ")" if arg_values else ""

    def remove_function_calls_in_funcexeclines(self, _function: Function) -> None:
        """
        Remove all function calls in the `exec_lines` attribute of the given `_function`.

        Args:
            _function (Function): The function object containing the `exec_lines` attribute.

        Returns:
            None: This function does not return anything.
        """
        remove: str = f"\n\n{_function.name}"
        _function.exec_lines = _function.exec_lines.split(remove)[0]

    def add_function_call_in_funcexeclines(
        self, _function: Function, pars: str
    ) -> None:
        """
        Add a function call to the exec_lines list of a Function object.

        Parameters:
            _function (Function): The Function object to add the function call to.
            pars (str): The parameters to be included in the function call.

        Returns:
            None
        """
        _function.exec_lines += f"\n\n{_function.name}{pars}"
