from unittest import TestCase, main

from plox.ast_printer import AstPrinter
from plox.expressions import *
from plox.token import Token, TokenType as Type

class TestPrinting(TestCase):
    def test_binary_expression(self) -> None:
        expression = Binary(
            Unary(Token(Type.MINUS, '-', None, 1), Literal(123)),
            Token(Type.STAR, '*', None, 1),
            Grouping(Literal(45.67))
        )

        printer = AstPrinter()

        self.assertEqual(
            printer.print(expression),
            '(* (- 123) (group 45.67))'
        )

if __name__ == '__main__':
    main()
