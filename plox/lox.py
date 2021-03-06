import sys

import plox.ast_printer
import plox.error
import plox.interpreter
import plox.parser
import plox.scanner
import plox.token

interpreter = plox.interpreter.Interpreter()

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
        if (plox.error.had_error): sys.exit(65)
        if (plox.error.had_runtime_error): sys.exit(70)

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

    if plox.error.had_error: return

    if expression is not None: interpreter.interpret(expression)

if __name__ == '__main__':
    lox()
