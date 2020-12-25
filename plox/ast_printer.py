from typing import Any

from plox.expressions import Expr, Visitor

class AstPrinter(Visitor):
    def print(self, expr: Expr) -> Any:
        return expr.accept(self)
