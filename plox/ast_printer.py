from typing import Any

from plox.expressions import (
    Binary,
    Expr,
    Grouping,
    Literal,
    Unary,
    Visitor
)

class AstPrinter(Visitor):
    def print(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visit_binary(self, expr: Binary) -> Any:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping) -> Any:
        return self.parenthesize('group', expr.expr)

    def visit_literal(self, expr: Literal) -> Any:
        if expr.value == None: return 'nil'
        return str(expr.value)

    def visit_unary(self, expr: Unary) -> Any:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> Any:
        readable = f'({name}'

        for expr in exprs:
            readable += f' {expr.accept(self)}'

        readable += ')'

        return readable
