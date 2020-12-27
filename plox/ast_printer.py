from typing import Any

from plox.expressions import (
    Binary,
    Expr,
    Grouping,
    Literal,
    Unary,
    Visitor
)

# The overridden visit methods of AstPrinter return a string. Visitors are free
# to return whatever they'd like. Because the accept method of an expression
# must support all visitors, it must return what the visitor returns if it is to
# have a return value. So it bails out of type safety and returns Any. This is
# *not* parametric polymorphism. Any is a subtype of any type. Not sure how to
# correctly implement the visitor pattern in Python with type safety. The book
# is written in Java and uses generics.

class AstPrinter(Visitor):
    def print(self, expr: Expr) -> Any:
        return expr.accept(self)

    def visitBinary(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGrouping(self, expr: Grouping) -> str:
        return self.parenthesize('group', expr.expression)

    def visitLiteral(self, expr: Literal) -> str:
        if expr.value == None: return 'nil'
        return str(expr.value)

    def visitUnary(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        readable = f'({name}'

        # expr.accept(self) has type Any, so we may concatenate with a string
        # without any type checking.

        for expr in exprs:
            readable += f' {expr.accept(self)}'

        readable += ')'

        return readable
