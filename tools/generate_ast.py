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
        'Binary   : Expr left, token.Token operator, Expr right',
        'Grouping : Expr expression',
        'Literal  : token.Literal value',
        'Unary    : token.Token operator, Expr right'
    ]

    with open(output_path, 'w') as file:
        file.write('from plox import token\n')
        file.write('\n')

        file.write(f'class {base_name}:\n')
        file.write(f'{indent} pass\n')
        file.write('\n')

        for i in range(len(types)):
            type = types[i]

            class_name = type.split(':')[0].strip()
            fields = type.split(':')[1].strip().split(', ')

            file.write(f'class {class_name}({base_name}):\n')

            file.write(f'{indent}def __init__(\n')
            file.write(f'{indent}{indent}self,\n')

            for j in range(len(fields)):
                field = fields[j]

                name = field.split(' ')[1]
                annotation = field.split(' ')[0]

                file.write(f'{indent}{indent}{name}: {annotation}')

                if j < len(fields) - 1: file.write(',')

                file.write('\n')

            file.write(f'{indent}) -> None:\n')

            for field in fields:
                name = field.split(' ')[1]

                file.write(f'{indent}{indent}self.{name} = {name}\n')

            if i < len(types) - 1: file.write('\n')

if __name__ == '__main__':
    main()
