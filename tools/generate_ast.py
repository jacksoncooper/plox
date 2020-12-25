import sys

def main() -> None:
    # sys.argv[0] is the script name, which we drop.
    args = sys.argv[1:]

    if len(args) != 1:
        print('Usage: generate_ast <output_directory>')
        sys.exit(64)

    module_name = 'expressions'
    base_name = 'Expr'
    output_directory = args[0]
    output_path = f'{output_directory}/{module_name}.py'
    indent = '    '

    types = [
        'Binary   : Expr left, Token operator, Expr right',
        'Grouping : Expr expression',
        'Literal  : Lit value',
        'Unary    : Token operator, Expr right'
    ]

    with open(output_path, 'w') as file:
        # Write imports.
        file.write('from plox.token import Literal as Lit, Token\n')
        file.write('from plox.visitor import Visitor\n')
        file.write('\n')

        # Write base class definition.
        file.write(f'class {base_name}:\n')
        file.write(f'{indent} pass\n')
        file.write('\n')

        for i in range(len(types)):
            type = types[i]

            # Write class definition header.
            class_name = type.split(':')[0].strip()
            fields = type.split(':')[1].strip().split(', ')
            file.write(f'class {class_name}({base_name}):\n')

            # Write __init__() definition.
            file.write(f'{indent}def __init__(')
            file.write(f'self, ')

            for j in range(len(fields)):
                field = fields[j]
                name = field.split(' ')[1]
                annotation = field.split(' ')[0]
                file.write(f'{name}: {annotation}')
                if j < len(fields) - 1: file.write(', ')

            file.write(f') -> None:\n')

            # Write statements that bind __init__() arguments to class instance.
            for field in fields:
                name = field.split(' ')[1]
                file.write(f'{indent}{indent}self.{name} = {name}\n')

            file.write('\n')

            # Write accept() definition.
            file.write(f'{indent}def accept(')
            file.write(f'self, ')
            file.write(f'visitor: Visitor')
            file.write(f') -> None:\n')
            file.write(f'{indent}{indent}return visitor.visit{class_name}(self)\n')

            # Omit newline after last class definition is written.
            if i < len(types) - 1: file.write('\n')

if __name__ == '__main__':
    main()
