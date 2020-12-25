import sys

from typing import List

def main() -> None:
    # sys.argv[0] is the script name, which we drop.
    args = sys.argv[1:]

    if len(args) != 1:
        print('Usage: generate_ast <output_directory>')
        sys.exit(64)

    output_directory = args[0]

    types = [
        'Binary   : Expr left, Token operator, Expr right',
        'Grouping : Expr expression',
        'Literal  : Literal value',
        'Unary    : Token operator, Expr right'
    ]

    define_ast(output_directory, 'Expr', types)

def define_ast(
    output_directory: str,
    base_name: str,
    types: List[str]
) -> None:
    pass

if __name__ == '__main__':
    main()
