from dataclasses import dataclass

from . import Error
from .parser import Expr

class RuntimeError(Error):
    pass

class Runtime:
    def evaluate(self, ast: Expr) -> int:
        pass
