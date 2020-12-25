from plox import token

class Expr:
     pass

class Binary(Expr):
    def __init__(
        self,
        left: Expr,
        operator: token.Token,
        right: Expr
    ) -> None:
        self.left = left
        self.operator = operator
        self.right = right

class Grouping(Expr):
    def __init__(
        self,
        expression: Expr
    ) -> None:
        self.expression = expression

class Literal(Expr):
    def __init__(
        self,
        value: token.Literal
    ) -> None:
        self.value = value

class Unary(Expr):
    def __init__(
        self,
        operator: token.Token,
        right: Expr
    ) -> None:
        self.operator = operator
        self.right = right
