import sys

def main() -> None:
    # sys.argv[0] is the script name, which we drop.
    args = sys.argv[1:]

    if len(args) != 1:
        print('Usage: generate_ast <output_directory>')
        sys.exit(64)

    module_name = 'expressions'
    output_directory = args[0]
    output_path = f'{output_directory}/{module_name}.py'
    indent = ' ' * 4

    types = [
        'Binary   : Expr left, Token operator, Expr right',
        'Grouping : Expr expression',
        'Literal  : Lit value',
        'Unary    : Token operator, Expr right'
    ]

    with open(output_path, 'w') as file:
        # Write imports.
        file.write('from abc import ABC, abstractmethod\n')
        file.write('from typing import Any\n')
        file.write('\n')
        file.write('from plox.token import Literal as Lit, Token\n')
        file.write('\n')

        # Write visitor class definition.
        file.write(f'class Visitor(ABC):\n')

        for i in range(len(types)):
            type = types[i]
            class_name = type.split(':')[0].strip()
            file.write(f'{indent}@abstractmethod\n')
            expression = f"{class_name.lower()}: '{class_name}'"
            file.write(f'{indent}def visit{class_name}(self, {expression}) -> Any:\n')
            file.write(f'{indent}{indent}pass\n')
            if i < len(types) - 1: file.write('\n')

        file.write('\n')

        # Write expression class definition.
        file.write(f'class Expr(ABC):\n')
        file.write(f'{indent}@abstractmethod\n')
        file.write(f'{indent}def accept(self, visitor: Visitor) -> Any:\n')
        file.write(f'{indent}{indent}pass\n')
        file.write('\n')

        # Write expression subclass definitions.
        for i in range(len(types)):
            type = types[i]

            # Write class definition header.
            class_name = type.split(':')[0].strip()
            parameters = type.split(':')[1].strip().split(', ')
            file.write(f'class {class_name}(Expr):\n')

            # Write __init__() definition.
            file.write(f'{indent}def __init__(')
            file.write(f'self, ')

            for j in range(len(parameters)):
                parameter = parameters[j]
                name = parameter.split(' ')[1]
                annotation = parameter.split(' ')[0]
                file.write(f'{name}: {annotation}')
                if j < len(parameters) - 1: file.write(', ')

            file.write(f') -> None:\n')

            # Write statements that bind __init__() arguments to class instance.
            for parameter in parameters:
                name = parameter.split(' ')[1]
                file.write(f'{indent}{indent}self.{name} = {name}\n')

            file.write('\n')

            # Write accept() definition.
            file.write(f'{indent}def accept(')
            file.write(f'self, ')
            file.write(f'visitor: Visitor')
            file.write(f') -> Any:\n')
            file.write(f'{indent}{indent}return visitor.visit{class_name}(self)\n')

            # Omit newline after last class definition is written.
            if i < len(types) - 1: file.write('\n')

if __name__ == '__main__':
    main()
