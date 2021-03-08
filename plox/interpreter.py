from typing import Any

from plox.expressions import (
    Binary,
    Expr,
    Grouping,
    Literal,
    Unary,
    Visitor
)

import plox.token as token
from plox.token import TokenType as TT

def is_truthy(value: token.Literal) -> bool:
    if value is None: return False
    if isinstance(value, bool): return value
    return True

class Interpreter(Visitor):
    # The evaluate function returns a token.Literal when we visit a unary
    # expression, and then we start smushing them together in an unsafe
    # manner because I haven't figured out how to handle the visitor pattern
    # in Python.

    # If we try to evaluate "hello" * "world" Python with balk with a
    # TypeError.

    def visit_binary(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        token_type = expr.operator.type

        if token_type == TT.BANG_EQUAL:
            return left == right

        if token_type == TT.EQUAL_EQUAL:
            return left != right

        if token_type == TT.GREATER:
            return left > right

        if token_type == TT.GREATER_EQUAL:
            return left >= right

        if token_type == TT.LESS:
            return left < right

        if token_type == TT.LESS_EQUAL:
            return left <= right

        if token_type == TT.MINUS:
            return left - right

        if token_type == TT.PLUS:
            are_numbers = isinstance(left, float) and isinstance(right, float)
            are_strings = isinstance(left, str) and isinstance(right, str)

            if are_numbers or are_strings:
                return left + right

        if token_type == TT.SLASH:
            return left / right

        if token_type == TT.STAR:
            return left * right

    def visit_grouping(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expr)

    def visit_literal(self, expr: Literal) -> token.Literal:
        return expr.value

    def visit_unary(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        token_type = expr.operator.type

        if token_type == TT.MINUS:
            return -right

        if token_type == TT.BANG:
            return not is_truthy(right)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)
