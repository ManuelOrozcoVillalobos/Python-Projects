import regex as re
import sys
import os
import ast

# Regular expressions patterns.
semicolon_pattern = re.compile(r"(?<!#.*)[.]*;(?!.*[\'\"])")
comment_pattern = re.compile(r'(?<!#.*)[\w;:)] {,1}#[\s\w]*')
todo_pattern = re.compile(r'# *[Tt][Oo][Dd][Oo]')


# Arguments and variables.
path = sys.argv


def line_long(line, line_number):
    if len(line) > 79:
        print(f'{f.name}: Line {line_number}: S001 Too long')


def indentation(line, line_number):
    leading_spaces = len(line) - len(line.lstrip())
    if leading_spaces % 4 != 0:
        print(f'{f.name}: Line {line_number}: S002 Indentation is not a multiple of four')


def semicolon(line, line_number):
    if semicolon_pattern.search(line):
        print(f'{f.name}: Line {line_number}: S003 Unnecessary semicolon after a statement')


def comment_todo(line, line_number):
    if comment_pattern.search(line):
        print(f'{f.name}: Line {line_number}: S004 Less than two spaces before inline comments')
    if todo_pattern.search(line):
        print(f'{f.name}: Line {line_number}: S005 TODO found')


def class_names_spaces(line, line_number):
    if re.search(r'class {2,}.*', line):
        print(f'{f.name}: Line {line_number}: S007 Too many spaces after class')

    if re.search(r'def {2,}.*', line):
        print(f'{f.name}: Line {line_number}: S007 Too many spaces after def')


def function_class_verifier(line_number):
    """Use the ast module to verify the functions and class PEP8 compliance"""
    for n in nodes:

        if type(n) == ast.ClassDef:
            class_name = n.name

            if re.search(r'^[a-z0-9][\w\d_-]*', class_name):
                print(f"{f.name}: Line {n.lineno}: S008 Class name '{class_name}' should be written in CamelCase")

        if type(n) == ast.FunctionDef:
            function_name = n.name
            arguments = n.args
            body_tree = n.body
            argument_name = arguments.args
            argument_value = arguments.defaults

            if re.search(r'[A-Z]+', function_name):
                print(f"{f.name}: Line {n.lineno}: S009 Function name '{function_name}' should be written in snake_case")

            for body_nodes in body_tree:
                if type(body_nodes) == ast.Assign:
                    targets_node = body_nodes.targets
                    for variable_name in targets_node:
                        if type(variable_name) == ast.Attribute:
                            continue
                        elif re.search(r'[A-Z]+', variable_name.id):
                            print(f"{f.name}: Line {variable_name.lineno}: S011 Variable '{variable_name.id}' should be written in snake_case")

            for name in argument_name:
                if re.search(r'[A-Z]+', name.arg):
                    print(f"{f.name}: Line {name.lineno}: S010 Argument name '{name.arg}' should be written in snake_case")

            for values in argument_value:
                if type(values) in (ast.List, ast.Dict, ast.Set):
                    print(f"{f.name}: Line {values.lineno}: S012 The default argument value is mutable")


def function_caller():
    file_length = len(file_lines)
    blank_lines_count = 0

    for x in range(file_length):
        line = file_lines[x]
        line_number = x + 1
        line_long(line, line_number)
        indentation(line, line_number)
        semicolon(line, line_number)
        comment_todo(line, line_number)

        if line != '' and blank_lines_count > 2:
            print(f'{f.name}: Line {line_number}: S006 More than two blank lines preceding a code line')
            blank_lines_count = 0
        elif line == '':
            blank_lines_count += 1
        else:
            blank_lines_count = 0

        class_names_spaces(line, line_number)
        function_class_verifier(line_number)


if os.path.isfile(path[1]) and '.py' in path[1]:
    with open(path[1], 'r') as f:
        file = f.read()
        tree = ast.parse(file)
        nodes = ast.walk(tree)
        file_lines = file.split('\n')
    function_caller()


elif os.path.isdir(path[1]):
    for i in os.listdir(path[1]):
        if '.py' in i and i != "tests.py":
            blank_line = 0
            with open(f"{path[1]}\\{i}", 'r') as f:
                file = f.read()
                tree = ast.parse(file)
                nodes = ast.walk(tree)
                file_lines = file.split('\n')
            function_caller()
        else:
            pass
