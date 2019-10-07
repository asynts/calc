from dataclasses import dataclass
from enum import Enum

class Reader:
    def __init__(self, input_: str):
        self._input = input_
        self._cursor = 0

    @property
    def has_more(self):
        return self._cursor < len(self._input)
