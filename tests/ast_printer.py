from unittest import TestCase, main

from plox.ast_printer import AstPrinter

from plox.expressions import (
    Binary,
    Grouping,
    Literal,
    Unary
)

from plox.token import (
    Token,
    TokenType as TT
)

class TestPrinting(TestCase):
    def test_binary_expression(self) -> None:
        expression = Binary(
            Unary(Token(TT.MINUS, '-', None, 1), Literal(123)),
            Token(TT.STAR, '*', None, 1),
            Grouping(Literal(45.67))
        )

        printer = AstPrinter()

        self.assertEqual(
            printer.print(expression),
            '(* (- 123) (group 45.67))'
        )

if __name__ == '__main__':
    main()
