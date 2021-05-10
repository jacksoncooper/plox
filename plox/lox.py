import builtins
import sys

# TODO: We don't import Scanner directly because it causes a circular import
# with scanner.py. For some reason using the pure import statement doesn't
# seem to cause Scanner to be immediately interpreted.

import plox.ast_printer
import plox.parser
import plox.scanner
import plox.token

had_error = False

class RuntimeError(builtins.RuntimeError):
    def __init__(self, token: plox.token.Token, message: str):
        self.token = token
        self.message = message

def lox() -> None:
    # sys.argv[0] is the script name, which we drop.
    args = sys.argv[1:]

    if len(args) > 1:
        print('Usage: plox [script]')
        sys.exit(64)

    elif len(args) == 1:
        run_file(args[0])

    else:
        run_prompt()

def run_file(path: str) -> None:
    with open(path) as file:
        run(file.read())
        if (had_error): sys.exit(65)

def run_prompt() -> None:
    while True:
        try:
            line = input('> ')
        except EOFError:
            print('Received EOF, exiting.')
            break
        else:
            run(line)

def run(source: str) -> None:
    scanner = plox.scanner.Scanner(source)
    tokens = scanner.scan_tokens()
    parser = plox.parser.Parser(tokens)
    expression = parser.parse()

    # TODO: The scanner discards unexpected tokens, and we parse the source
    # without these tokens. So why bail out over a scanner error if the parser
    # succeeds? Why group scanner and parser errors together?

    if had_error: return

    printer = plox.ast_printer.AstPrinter()

    if expression is not None:
        print(printer.print(expression))

def error(line: int, message: str) -> None:
    report(line, '', message)

def parse_error(token: plox.token.Token, message: str) -> None:
    if token.type == plox.token.TokenType.EOF:
        report(token.line, ' at end', message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)

def report(line: int, where: str, message: str) -> None:
    print(f'[line {line}] Error{where}: {message}')
    global had_error
    had_error = True

if __name__ == '__main__':
    lox()
