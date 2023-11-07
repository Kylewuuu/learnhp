"""
python v3.9.0
@Project: hotpot
@File   : maths
@Auther : Zhiyuan Zhang
@Data   : 2023/11/7
@Time   : 11:16
"""
from typing import *


class BaseNum:
    """ Create an int-wise number based on custom base """
    def __init__(self, value: Union[int, list[int]], base: int = 128):
        if isinstance(value, list):
            assert all(v < base for v in value)
            self.values = value
        elif isinstance(value, int):
            self.values = []
            while value >= base:
                value, remainder = divmod(value, base)
                self.values.insert(0, remainder)
            self.values.insert(0, value)
        else:
            raise ValueError('the given value should be an int or list of int')

        self.base = base

    def __int__(self):
        return sum(v*pow(self.base, i) for i, v in enumerate(reversed(self.values)))

    def __repr__(self):
        return f"{self.base}Based({self.values})"

    def __eq__(self, other):
        return int(self) == int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def join(self, other):
        self.values += other.values

    def __add__(self, other):
        return self.__class__(int(self) + int(other), self.base)

    def __mul__(self, other):
        return self.__class__(int(self) * int(other), self.base)
