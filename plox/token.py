from enum import Enum

from typing import List, Union

class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11

    # One or two-character tokens.
    BANG = 12
    BANG_EQUAL = 13
    EQUAL = 14
    EQUAL_EQUAL = 15
    GREATER = 16
    GREATER_EQUAL = 17
    LESS = 18
    LESS_EQUAL = 19

    # Literals.
    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22

    # Keywords.
    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FUN = 27
    FOR = 28
    IF = 29
    NIL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    VAR = 37
    WHILE = 38

    # End-of-file.
    EOF = 39

# TODO: Scattering dependent types throughout the source is not ideal.

Literal = Union[float, str, None]

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Literal, line: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token): return False

        return all([
            self.type == other.type,
            self.lexeme == other.lexeme,
            self.literal == other.literal,
            self.line == other.line
        ])

    def __repr__(self) -> str:
        return (
            f'Token({self.type}, '
            f'{self.lexeme.__repr__()}, '
            f'{self.literal.__repr__()}, '
            f'{self.line})'
        )

Tokens = List[Token]
