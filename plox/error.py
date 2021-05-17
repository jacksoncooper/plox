import builtins
import sys

import plox.token

had_error = False
had_runtime_error = False

class RuntimeError(builtins.RuntimeError):
    def __init__(self, token: plox.token.Token, message: str):
        self.token = token
        self.message = message

def error(line: int, message: str) -> None:
    report(line, '', message)

def runtime_error(error: RuntimeError) -> None:
    print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
    had_runtime_error = True

def parse_error(token: plox.token.Token, message: str) -> None:
    if token.type == plox.token.TokenType.EOF:
        report(token.line, ' at end', message)
    else:
        report(token.line, f" at '{token.lexeme}'", message)

def report(line: int, where: str, message: str) -> None:
    print(f'[line {line}] Error{where}: {message}')
    global had_error
    had_error = True
