from unittest import TestCase, main

from plox.scanner import Scanner

from plox.token import (
    Token,
    TokenType as Type
)

example_one = '''\
// Please do not mutate the biscotti.

var biscotti = "hazelnut";
var remaining = 3;

while (remaining >= 1) {
    print "*munch*";
    remaining = remaining / 2;
}\
'''

class TestScannerState(TestCase):
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

class TestScanning(TestCase):
    def test_example_one(self) -> None:
        scanner = Scanner(example_one)

        tokens = scanner.scan_tokens()

        expected = [
            Token(Type.VAR, 'var', None, 3),
            Token(Type.IDENTIFIER, 'biscotti', None, 3),
            Token(Type.EQUAL, '=', None, 3),
            Token(Type.STRING, '"hazelnut"', 'hazelnut', 3),
            Token(Type.SEMICOLON, ';', None, 3),
            Token(Type.VAR, 'var', None, 4),
            Token(Type.IDENTIFIER, 'remaining', None, 4),
            Token(Type.EQUAL, '=', None, 4),
            Token(Type.NUMBER, '3', 3, 4),
            Token(Type.SEMICOLON, ';', None, 4),
            Token(Type.WHILE, 'while', None, 6),
            Token(Type.LEFT_PAREN, '(', None, 6),
            Token(Type.IDENTIFIER, 'remaining', None, 6),
            Token(Type.GREATER_EQUAL, '>=', None, 6),
            Token(Type.NUMBER, '1', 1, 6),
            Token(Type.RIGHT_PAREN, ')', None, 6),
            Token(Type.LEFT_BRACE, '{', None, 6),
            Token(Type.PRINT, 'print', None, 7),
            Token(Type.STRING, '"*munch*"', '*munch*', 7),
            Token(Type.SEMICOLON, ';', None, 7),
            Token(Type.IDENTIFIER, 'remaining', None, 8),
            Token(Type.EQUAL, '=', None, 8),
            Token(Type.IDENTIFIER, 'remaining', None, 8),
            Token(Type.SLASH, '/', None, 8),
            Token(Type.NUMBER, '2', 2, 8),
            Token(Type.SEMICOLON, ';', None, 8),
            Token(Type.RIGHT_BRACE, '}', None, 9),
            Token(Type.EOF, '', None, 9)
        ]

        self.assertEqual(tokens, expected)

if __name__ == '__main__':
    main()
