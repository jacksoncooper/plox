from unittest import TestCase, main

from plox.expressions import (
    Binary,
    Literal,
    Unary
)

from plox.parser import Parser
from plox.scanner import Scanner

from plox.token import (
    Token,
    TokenType as TT
)

class TestExpressions(TestCase):
    def test_binary_association(self) -> None:
        tokens = Scanner('1 == 2 != 3').scan_tokens()
        expression = Parser(tokens).parse()

        self.assertIsNotNone(expression)

        inner = Binary(
            Literal(1),
            Token(TT.EQUAL_EQUAL, '==', None, 1),
            Literal(2)
        )

        expected = Binary(
            inner,
            Token(TT.BANG_EQUAL, '!=', None, 1),
            Literal(3)
        )

        self.assertEqual(expression, expected)

    def test_unary_association(self) -> None:
        tokens = Scanner('!-1').scan_tokens()
        expression = Parser(tokens).parse()
        
        expected = Unary(
            Token(TT.BANG, '!', None, 1),
            Unary(
                Token(TT.MINUS, '-', None, 1),
                Literal(1)
            )
        )
        
        self.assertEqual(expression, expected)

if __name__ == '__name__':
    main()
