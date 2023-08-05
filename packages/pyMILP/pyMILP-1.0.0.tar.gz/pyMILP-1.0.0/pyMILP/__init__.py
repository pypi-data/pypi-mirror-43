"""
A simple library for doing mixed-integer linear programming.

Exports:
    All the variables that can be used
    >>> from pyMILP import (RealVariable, BinaryVariable, IntegerVariable,
    ... Variable)

    The function to solve a linear programming model and its status
    >>> from pyMILP import solve, Status
"""
from pyMILP.variable import (
    Variable, RealVariable, BinaryVariable,
    IntegerVariable,
)
from pyMILP.problem import solve, Status
