import sys

class Lox:
    def __init__(self) -> None:
        # sys.argv[0] is the script name, which we drop.
        args = sys.argv[1:]

        if len(args) > 1:
            print("Usage: plox [script]")
            sys.exit(64)

        elif len(args) == 1:
            self.run_file(args[0])

        else:
            self.run_prompt()

    def run_file(self, path: str) -> None:
        with open(path) as file:
            self.run(file.read())

    def run_prompt(self) -> None:
        while True:
            try:
                line = input('> ')
            except EOFError:
                print('Received EOF, exiting.')
                break
            else:
                self.run(line)

    def run(self, source: str) -> None:
        pass

if __name__ == "__main__":
    Lox()
