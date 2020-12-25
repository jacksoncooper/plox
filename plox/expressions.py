from abc import ABC, abstractmethod
from typing import Any

from plox.token import Literal as Lit, Token

class Visitor(ABC):
    @abstractmethod
    def visitBinary(self, binary: 'Binary') -> Any:
        pass

    @abstractmethod
    def visitGrouping(self, grouping: 'Grouping') -> Any:
        pass

    @abstractmethod
    def visitLiteral(self, literal: 'Literal') -> Any:
        pass

    @abstractmethod
    def visitUnary(self, unary: 'Unary') -> Any:
        pass

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> Any:
        pass

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitBinary(self)

class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitGrouping(self)

class Literal(Expr):
    def __init__(self, value: Lit) -> None:
        self.value = value

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitLiteral(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitUnary(self)
