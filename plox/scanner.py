import string
from typing import List

import plox.error as error

from plox.token import (
    Literal,
    Token,
    TokenType as TT,
    Tokens
)

def is_digit(char: str) -> bool:
    return char in string.digits

def is_alpha(char: str) -> bool:
    return char in string.ascii_letters + '_'

def is_alpha_numeric(char: str) -> bool:
    return is_alpha(char) or is_digit(char)

keywords = {
    'and'   : TT.AND,
    'class' : TT.CLASS,
    'else'  : TT.ELSE,
    'false' : TT.FALSE,
    'for'   : TT.FOR,
    'fun'   : TT.FUN,
    'if'    : TT.IF,
    'nil'   : TT.NIL,
    'or'    : TT.OR,
    'print' : TT.PRINT,
    'return': TT.RETURN,
    'super' : TT.SUPER,
    'this'  : TT.THIS,
    'true'  : TT.TRUE,
    'var'   : TT.VAR,
    'while' : TT.WHILE
}

class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source

        self.tokens: Tokens = []

        # The index of the first character of the lexeme being scanned.
        self.start = 0

        # The index of the character being considered.
        self.current = 0

        self.line = 1

    def scan_tokens(self) -> Tokens:
        while not self.is_at_end():
            # We are at the beginning of a new lexeme.
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TT.EOF, '', None, self.line))

        return self.tokens

    def scan_token(self) -> None:
        c = self.advance()

        # Single-character tokens.
        if   c == '(': self.add_token(TT.LEFT_PAREN)
        elif c == ')': self.add_token(TT.RIGHT_PAREN)
        elif c == '{': self.add_token(TT.LEFT_BRACE)
        elif c == '}': self.add_token(TT.RIGHT_BRACE)
        elif c == ',': self.add_token(TT.COMMA)
        elif c == '.': self.add_token(TT.DOT)
        elif c == '-': self.add_token(TT.MINUS)
        elif c == '+': self.add_token(TT.PLUS)
        elif c == ';': self.add_token(TT.SEMICOLON)
        elif c == '*': self.add_token(TT.STAR)

        # Two-character tokens.
        elif c == '!': self.add_token_if('=', TT.BANG_EQUAL, TT.BANG)
        elif c == '=': self.add_token_if('=', TT.EQUAL_EQUAL, TT.EQUAL)
        elif c == '<': self.add_token_if('=', TT.LESS_EQUAL, TT.LESS)
        elif c == '>': self.add_token_if('=', TT.GREATER_EQUAL, TT.GREATER)

        # Longer tokens.
        elif c == '/': self.slash()
        elif c == '"': self.string()

        # Whitespace.
        elif c == '\n': self.line += 1
        elif c in [' ', '\r', '\t']: pass

        # Numbers.
        elif is_digit(c): self.number()

        # Identifiers.
        elif is_alpha(c): self.identifier()

        # Character is not in Lox's grammar.
        else: error.error(self.line, f"Unexpected character '{c}'.")

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def peek(self) -> str:
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def add_token(self, type: TT, literal: Literal = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def add_token_if(self, char: str, match: TT, no_match: TT) -> None:
        self.add_token(match if self.match(char) else no_match)

    def slash(self) -> None:
        if self.match('/'):
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()
        else:
            self.add_token(TT.SLASH)

    def string(self) -> None:
        # No escape characters exist in the Lox grammar. Newline characters
        # are preserved.

        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.is_at_end():
            error.error(self.line, 'Unterminated string.')
            return

        # The closing quotation mark.
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1 : self.current - 1]

        self.add_token(TT.STRING, value)

    def number(self) -> None:
        while is_digit(self.peek()): self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and is_digit(self.peek_next()):
            # Consume the dot.
            self.advance()

            while is_digit(self.peek()): self.advance()

        value = float(self.source[self.start : self.current])

        self.add_token(TT.NUMBER, value)

    def identifier(self) -> None:
        while is_alpha_numeric(self.peek()): self.advance()
        text = self.source[self.start : self.current]
        type = keywords.get(text)
        if type is None: type = TT.IDENTIFIER
        self.add_token(type)
