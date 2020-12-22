from typing import List

from error import error
from token import Token, TokenType as Type

from token import Literal, Tokens

class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source

        self.tokens: Tokens = []

        # 'start' is the index of the first character of the lexeme being
        # scanned. 'current' is the index of the character being considered.
        # 'line' is the line number of the character that 'current' points to.

        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> Tokens:
        while not self.is_at_end():
            # We are at the beginning of the next lexeme.
            start = self.current
            self.scan_token()

        self.tokens.append(Token(Type.EOF, '', None, self.line))

        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c = self.advance()

        # Single-character tokens.
        if   c == '(': self.add_token(Type.LEFT_PAREN)
        elif c == ')': self.add_token(Type.RIGHT_PAREN)
        elif c == '{': self.add_token(Type.LEFT_BRACE)
        elif c == '}': self.add_token(Type.RIGHT_BRACE)
        elif c == ',': self.add_token(Type.COMMA)
        elif c == '.': self.add_token(Type.DOT)
        elif c == '-': self.add_token(Type.MINUS)
        elif c == '+': self.add_token(Type.PLUS)
        elif c == ';': self.add_token(Type.SEMICOLON)
        elif c == '*': self.add_token(Type.STAR)

        # Two-character tokens.
        elif c == '!': self.add_token(Type.BANG_EQUAL if self.match('=') else Type.BANG)
        elif c == '=': self.add_token(Type.EQUAL_EQUAL if self.match('=') else Type.EQUAL)
        elif c == '<': self.add_token(Type.LESS_EQUAL if self.match('=') else Type.LESS)
        elif c == '>': self.add_token(Type.GREATER_EQUAL if self.match('=') else Type.GREATER)

        # Character is not in Lox's grammar.
        else: error(self.line, 'Unexpected character.')

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: Type, literal: Literal = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected: str) -> bool:
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True
