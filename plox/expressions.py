from plox.token import Literal as Lit, Token
from plox.visitor import Visitor

class Expr:
     pass

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitBinary(self)

class Grouping(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitGrouping(self)

class Literal(Expr):
    def __init__(self, value: Lit) -> None:
        self.value = value

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitLiteral(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor) -> None:
        return visitor.visitUnary(self)
