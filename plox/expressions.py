from abc import ABC, abstractmethod
from typing import Any

import plox.token as token

class Visitor(ABC):
    @abstractmethod
    def visit_binary(self, expr: 'Binary') -> Any:
        pass

    @abstractmethod
    def visit_grouping(self, expr: 'Grouping') -> Any:
        pass

    @abstractmethod
    def visit_literal(self, expr: 'Literal') -> Any:
        pass

    @abstractmethod
    def visit_unary(self, expr: 'Unary') -> Any:
        pass

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> Any:
        pass

class Binary(Expr):
    def __init__(self, left: Expr, operator: token.Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
         return visitor.visit_binary(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Binary): return False

        return all([
            self.left == other.left,
            self.operator == other.operator,
            self.right == other.right
        ])

class Grouping(Expr):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def accept(self, visitor: Visitor) -> Any:
         return visitor.visit_grouping(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grouping): return False

        return all([
            self.expr == other.expr
        ])

class Literal(Expr):
    def __init__(self, value: token.Literal) -> None:
        self.value = value

    def accept(self, visitor: Visitor) -> Any:
         return visitor.visit_literal(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Literal): return False

        return all([
            self.value == other.value
        ])

class Unary(Expr):
    def __init__(self, operator: token.Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
         return visitor.visit_unary(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Unary): return False

        return all([
            self.operator == other.operator,
            self.right == other.right
        ])
