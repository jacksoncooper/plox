from plox.expressions import (
    Binary,
    Expr,
    Grouping,
    Literal,
    Unary
)

from plox.token import (
    Token,
    TokenType as TT,
    Tokens
)

class Parser:
    def __init__(self, tokens: Tokens) -> None:
        self.current = 0
        self.tokens = tokens

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while self.match(TT.BANG_EQUAL, TT.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr = self.term()

        while self.match(TT.GREATER, TT.GREATER_EQUAL, TT.LESS, TT.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr = self.factor()

        while self.match(TT.MINUS, TT.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr = self.unary()

        while self.match(TT.SLASH, TT.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self.match(TT.BANG, TT.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self) -> Expr:
        if self.match(TT.FALSE): return Literal(False)
        if self.match(TT.TRUE): return Literal(True)
        if self.match(TT.NIL): return Literal(None)

        if self.match(TT.NUMBER, TT.STRING):
            return Literal(self.previous().literal)

        if self.match(TT.LEFT_PAREN):
            expr = self.expression()
            self.consume(TT.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        # TODO: primary() is partial because we haven't exhausted our alphabet
        # of possible tokens. If we get to this point, the program contains a
        # syntax error.

        raise NotImplementedError('We still need syntax error reporting.')

    def match(self, *types: TT) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True

        return False

    def check(self, type: TT) -> bool:
        if self.is_at_end(): return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end(): self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TT.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]
