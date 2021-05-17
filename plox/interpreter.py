from typing import Any

import plox.error

from plox.expressions import (
    Binary,
    Expr,
    Grouping,
    Literal,
    Unary,
    Visitor
)

import plox.token as token
from plox.token import Token, TokenType as TT

def stringify(object: Any) -> str:
    if object is None: return 'nil'

    if isinstance(object, float):
        text = str(object)
        if text.endswith('.0'):
            text = text[:-2]
        return text

    if isinstance(object, bool):
        if object is True:
            return "true"
        return "false"

    return str(object)

def is_truthy(value: token.Literal) -> bool:
    # Lox follows Ruby’s simple rule: false and nil are falsey, and everything
    # else is truthy.
    if value is None: return False
    if value is False: return False
    return True

def is_equal(value: token.Literal, another_value: token.Literal) -> bool:
    # From https://docs.python.org/3/library/stdtypes.html.
    # - Objects of different types, except different numeric types, never compare equal.
    # - Floating point numbers are usually implemented using double in C.
    return value == another_value

def check_number_operand(operator: Token, operand: Any) -> None:
    if isinstance(operand, float): return
    raise plox.error.RuntimeError(operator, 'Operand must be a number.')

def check_number_operands(operator: Token, left: Any, right: Any) -> None:
    if isinstance(left, float) and isinstance(right, float): return
    raise plox.error.RuntimeError(operator, 'Operands must be numbers.')

class Interpreter(Visitor):
    # The evaluate function returns a token.Literal when we visit a unary
    # expression, and then we start smushing them together in an unsafe manner.
    # token.Literal is a sum type, but I don't have any value-level pattern
    # matching abilities, so we proceed with unsafe smushing and isinstance().

    def interpret(self, expression: Expr) -> None:
        try:
            value = self.evaluate(expression)
            print(stringify(value))
        except plox.error.RuntimeError as error:
            plox.error.runtime_error(error)

    def visit_binary(self, expr: Binary) -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        token_type = expr.operator.type

        if token_type == TT.BANG_EQUAL:
            return not is_equal(left, right)

        if token_type == TT.EQUAL_EQUAL:
            return is_equal(left, right)

        if token_type == TT.GREATER:
            check_number_operands(expr.operator, left, right)
            return left > right

        if token_type == TT.GREATER_EQUAL:
            check_number_operands(expr.operator, left, right)
            return left >= right

        if token_type == TT.LESS:
            check_number_operands(expr.operator, left, right)
            return left < right

        if token_type == TT.LESS_EQUAL:
            check_number_operands(expr.operator, left, right)
            return left <= right

        if token_type == TT.MINUS:
            check_number_operands(expr.operator, left, right)
            return left - right

        if token_type == TT.PLUS:
            are_numbers = isinstance(left, float) and isinstance(right, float)
            are_strings = isinstance(left, str) and isinstance(right, str)

            if are_numbers or are_strings:
                return left + right

            raise plox.error.RuntimeError(
                expr.operator,
                'Operands must be two numbers or two strings.'
            )

        if token_type == TT.SLASH:
            check_number_operands(expr.operator, left, right)

            if right == 0:
                raise plox.error.RuntimeError(
                    expr.operator,
                    'Division by zero.'
                )

            return left / right

        if token_type == TT.STAR:
            check_number_operands(expr.operator, left, right)
            return left * right

    def visit_grouping(self, expr: Grouping) -> Any:
        return self.evaluate(expr.expr)

    def visit_literal(self, expr: Literal) -> token.Literal:
        return expr.value

    def visit_unary(self, expr: Unary) -> Any:
        right = self.evaluate(expr.right)

        token_type = expr.operator.type

        if token_type == TT.MINUS:
            check_number_operand(expr.operator, right)
            return -right

        if token_type == TT.BANG:
            return not is_truthy(right)

    def evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)
