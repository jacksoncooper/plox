from abc import ABC, abstractmethod
from typing import Any

import plox.token as token

class Visitor(ABC):
    @abstractmethod
    def visitBinary(self, expr: 'Binary') -> Any:
        pass

    @abstractmethod
    def visitGrouping(self, expr: 'Grouping') -> Any:
        pass

    @abstractmethod
    def visitLiteral(self, expr: 'Literal') -> Any:
        pass

    @abstractmethod
    def visitUnary(self, expr: 'Unary') -> Any:
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
        return visitor.visitBinary(self)

class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitGrouping(self)

class Literal(Expr):
    def __init__(self, value: token.Literal) -> None:
        self.value = value

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitLiteral(self)

class Unary(Expr):
    def __init__(self, operator: token.Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> Any:
        return visitor.visitUnary(self)
