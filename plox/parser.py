from typing import Optional

import plox.error

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

class ParseError(Exception):
    pass

def error(token: Token, message: str) -> ParseError:
    plox.error.parse_error(token, message)
    return ParseError()

class Parser:
    def __init__(self, tokens: Tokens) -> None:
        self.current = 0
        self.tokens = tokens

    def parse(self) -> Optional[Expr]:
        try:
            return self.expression()
        except ParseError:
            return None

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

        raise error(self.peek(), 'Expect expression.')

    def is_at_end(self) -> bool:
        return self.peek().type == TT.EOF

    def advance(self) -> Token:
        if not self.is_at_end(): self.current += 1
        return self.previous()

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def check(self, type: TT) -> bool:
        if self.is_at_end(): return False
        return self.peek().type == type

    def match(self, *types: TT) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True

        return False

    def consume(self, type: TT, message: str) -> Token:
        if self.check(type): return self.advance()
        raise error(self.peek(), message)

    def synchronize(self) -> None:
        # We call synchronize() when the parser enters panic mode. We consumed
        # an unexpected token and exploded the call stack. Now we seek out the
        # start of a new statement, discarding the tokens that precede it, in an
        # effort to avoid cascade errors, because we consider the current
        # expression to be hosed.

        self.advance()

        while not self.is_at_end():
            if self.previous().type == TT.SEMICOLON: return

            current = self.peek().type

            statements = [
                TT.CLASS, TT.FUN, TT.VAR, TT.FOR,
                TT.IF, TT.WHILE, TT.PRINT, TT.RETURN
            ]

            if current in statements: return

            self.advance()
