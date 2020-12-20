import sys

had_error = False

def lox() -> None:
    # sys.argv[0] is the script name, which we drop.
    args = sys.argv[1:]

    if len(args) > 1:
        print("Usage: plox [script]")
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
    pass

def error(line: int, message: str) -> None:
    report(line, '', message)

def report(line: int, where: str, message: str) -> None:
    print(f'[line {line}] Error{where}: {message}')
    global had_error
    had_error = True

if __name__ == "__main__":
    lox()
