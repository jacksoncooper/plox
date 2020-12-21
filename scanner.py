from token import Token, TokenType

from typing import List

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

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))

        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c = self.advance()
        if   c == '(': self.add_token(TokenType.LEFT_PAREN)
        elif c == ')': self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{': self.add_token(TokenType.LEFT_BRACE)
        elif c == '}': self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',': self.add_token(TokenType.COMMA)
        elif c == '.': self.add_token(TokenType.DOT)
        elif c == '-': self.add_token(TokenType.MINUS)
        elif c == '+': self.add_token(TokenType.PLUS)
        elif c == ';': self.add_token(TokenType.SEMICOLON)
        elif c == '*': self.add_token(TokenType.STAR)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type: TokenType, literal: Literal = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))
