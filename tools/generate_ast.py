import sys

from typing import Dict, List, Tuple

Attribute = Tuple[str, str]
Attributes = List[Attribute]
Expressions = Dict[str, Attributes]

module_name = 'expressions'
base_name = 'Expr'
indent = ' ' * 4

expressions: Expressions = {
    'Binary'  : [('left', 'Expr'), ('operator', 'token.Token'), ('right', 'Expr')],
    'Grouping': [('expr', 'Expr')],
    'Literal' : [('value', 'token.Literal')],
    'Unary'   : [('operator', 'token.Token'), ('right', 'Expr')]
}

def main() -> None:
    # sys.argv[0] is the script name, which we drop.
    args = sys.argv[1:]

    if len(args) != 1:
        print('Usage: generate_ast <output_directory>')
        sys.exit(64)

    output_directory = args[0]
    output_path = f'{output_directory}/{module_name}.py'

    lines: List[str] = []

    write_imports(lines)
    lines.append('\n')

    write_visitor_base(lines, list(expressions.keys()))
    lines.append('\n')

    write_expression_base(lines)
    lines.append('\n')

    for (name, attributes) in expressions.items():
        write_expression(lines, name, attributes)
        lines.append('\n')

    lines.pop()

    with open(output_path, 'w') as file:
        file.writelines(lines)

def write_imports(lines: List[str]) -> None:
    lines.extend([
        'from abc import ABC, abstractmethod\n',
        'from typing import Any\n',
        '\n',
        'import plox.token as token\n'
    ])

def write_visitor_base(lines: List[str], names: List[str]) -> None:
    lines.append(f'class Visitor(ABC):\n')

    for name in names:
        lines.extend([
            f'{indent}@abstractmethod\n',
            f"{indent}def visit{name}(self, {base_name.lower()}: '{name}') -> Any:\n",
            f'{indent}{indent}pass\n',
            '\n'
        ])

    # Remove last newline that separates the visitor methods. Line breaks
    # between definitions should be enforced by the top-level function.
    lines.pop()

def write_expression_base(lines: List[str]) -> None:
    lines.extend([
        'class Expr(ABC):\n',
        f'{indent}@abstractmethod\n',
        f'{indent}def accept(self, visitor: Visitor) -> Any:\n',
        f'{indent}{indent}pass\n'
    ])

def write_expression(lines: List[str], name: str, attributes: Attributes) -> None:
    # Write expression class definition.
    lines.append(f'class {name}({base_name}):\n')

    # Write __init__().
    lines.append(f'{indent}def __init__(self,')
    for (attribute, attribute_type) in attributes:
        lines.append(f' {attribute}: {attribute_type}')
        lines.append(',')

    # Pop the last comma in the argument list.
    lines.pop()

    lines.append(') -> None:\n')

    # Bind __init__() arguments to class instance.
    for (attribute, _) in attributes:
        lines.append(f'{indent}{indent}self.{attribute} = {attribute}\n')

    lines.append('\n')

    # Write accept().
    lines.extend([
        f'{indent}def accept(self, visitor: Visitor) -> Any:\n',
        f'{indent}{indent} return visitor.visit{name}(self)\n',
        '\n'
    ])

    # Write __eq__().
    lines.extend([
        f'{indent}def __eq__(self, other: object) -> bool:\n',
        f'{indent}{indent}if not isinstance(other, {name}): return False\n',
        '\n'
        f'{indent}{indent}return all([\n'
    ])

    for (attribute, _) in attributes:
        lines.append(f'{indent}{indent}{indent}self.{attribute} == other.{attribute}')
        lines.append(',\n')

    # Pop the trailing comma and newline in the argument list to all() and
    # replace the newline.
    lines.pop()
    lines.append('\n')

    lines.append(f'{indent}{indent}])\n')

if __name__ == '__main__':
    main()
