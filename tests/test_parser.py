from unittest import TestCase, main

from plox.expressions import (
    Binary,
    Literal
)

from plox.parser import Parser
from plox.scanner import Scanner

from plox.token import (
    Token,
    TokenType as TT
)

class TestExpressions(TestCase):
    def test_binary_association(self) -> None:
        scanner = Scanner('1 == 2 != 3')
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()

        self.assertIsNotNone(expression)

        inner = Binary(
            Literal(1),
            Token(TT.EQUAL_EQUAL, '==', None, 1),
            Literal(2)
        )

        outer = Binary(
            inner,
            Token(TT.BANG_EQUAL, '!=', None, 1),
            Literal(3)
        )

        self.assertEqual(expression, outer)

    def test_unary_association(self) -> None:
        pass

if __name__ == '__name__':
    main()
