from unittest import TestCase, main

from plox.scanner import Scanner

from plox.token import (
    Token,
    TokenType as TT
)

multiple_lines = '''\
// Please do not mutate the biscotti.

var biscotti = "hazelnut";
var remaining = 3;

while (remaining >= 1) {
    print "*munch*";
    remaining = remaining / 2;
}\
'''

class TestState(TestCase):
    def test_initial_state(self) -> None:
        scanner = Scanner('')

        self.assertEqual(scanner.start, 0)
        self.assertEqual(scanner.current, 0)
        self.assertEqual(scanner.line, 1)

    def test_consume(self) -> None:
        source = 'biscotti'
        scanner = Scanner(source)

        for i in range(len(source)):
            consumed = scanner.advance()

            self.assertEqual(scanner.start, 0)
            self.assertEqual(scanner.current, i + 1)
            self.assertEqual(scanner.line, 1)

            self.assertEqual(consumed, source[i])

        self.assertTrue(scanner.is_at_end())

        with self.assertRaises(IndexError):
            scanner.advance()

    def test_lookahead(self) -> None:
        source = 'bis'
        scanner = Scanner(source)

        # 'current' points to 'b'.
        self.assertEqual(scanner.peek(), 'b')
        self.assertEqual(scanner.peek_next(), 'i')
        self.assertEqual(scanner.current, 0)

        # 'current' points to 'i'.
        self.assertEqual(scanner.advance(), 'b')
        self.assertEqual(scanner.current, 1)

        # 'current' point to 's'.
        self.assertTrue(scanner.match('i'))
        self.assertEqual(scanner.current, 2)
        self.assertFalse(scanner.match('i'))
        self.assertEqual(scanner.peek_next(), '\0')
        self.assertEqual(scanner.current, 2)

        # 'current' has run off the input.
        self.assertEqual(scanner.advance(), 's')
        self.assertEqual(scanner.peek(), '\0')
        self.assertEqual(scanner.current, 3)

class TestError(TestCase):
    def test_unexpected_character(self) -> None:
        scanner = Scanner('bis@cotti')
        tokens = scanner.scan_tokens()

        expected = [
            Token(TT.IDENTIFIER, 'bis', None, 1),
            Token(TT.IDENTIFIER, 'cotti', None, 1),
            Token(TT.EOF, '', None, 1)
        ]

        self.assertEqual(tokens, expected)

    def test_unterminated_string(self) -> None:
        scanner = Scanner('"biscotti')
        tokens = scanner.scan_tokens()
        expected = [Token(TT.EOF, '', None, 1)]
        self.assertEqual(tokens, expected)

class TestTokens(TestCase):
    def test_multiple_lines(self) -> None:
        scanner = Scanner(multiple_lines)
        tokens = scanner.scan_tokens()

        expected = [
            Token(TT.VAR, 'var', None, 3),
            Token(TT.IDENTIFIER, 'biscotti', None, 3),
            Token(TT.EQUAL, '=', None, 3),
            Token(TT.STRING, '"hazelnut"', 'hazelnut', 3),
            Token(TT.SEMICOLON, ';', None, 3),
            Token(TT.VAR, 'var', None, 4),
            Token(TT.IDENTIFIER, 'remaining', None, 4),
            Token(TT.EQUAL, '=', None, 4),
            Token(TT.NUMBER, '3', 3, 4),
            Token(TT.SEMICOLON, ';', None, 4),
            Token(TT.WHILE, 'while', None, 6),
            Token(TT.LEFT_PAREN, '(', None, 6),
            Token(TT.IDENTIFIER, 'remaining', None, 6),
            Token(TT.GREATER_EQUAL, '>=', None, 6),
            Token(TT.NUMBER, '1', 1, 6),
            Token(TT.RIGHT_PAREN, ')', None, 6),
            Token(TT.LEFT_BRACE, '{', None, 6),
            Token(TT.PRINT, 'print', None, 7),
            Token(TT.STRING, '"*munch*"', '*munch*', 7),
            Token(TT.SEMICOLON, ';', None, 7),
            Token(TT.IDENTIFIER, 'remaining', None, 8),
            Token(TT.EQUAL, '=', None, 8),
            Token(TT.IDENTIFIER, 'remaining', None, 8),
            Token(TT.SLASH, '/', None, 8),
            Token(TT.NUMBER, '2', 2, 8),
            Token(TT.SEMICOLON, ';', None, 8),
            Token(TT.RIGHT_BRACE, '}', None, 9),
            Token(TT.EOF, '', None, 9)
        ]

        self.assertEqual(tokens, expected)

if __name__ == '__main__':
    main()
