import os
import sys
import json
import time
import argparse
#from tree_sitter import Language, Parser

t0 = time.time()
#GO_LANGUAGE = Language('/Users/anabiha/past_projects/twosixtech/reachability_code/Reachability/build/my-languages.so', 'go')
# JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
#PY_LANGUAGE = Language('/Users/anabiha/past_projects/twosixtech/reachability_code/Reachability/build/my-languages.so', 'python')

from tree_sitter_languages import get_language, get_parser

language = get_language('python')
lang_parser = get_parser('python')

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Scan Python code using Tree-sitter')
parser.add_argument('file', metavar='file', type=str, help='the name of the input file')
parser.add_argument('lang', metavar='lang', type=str, help='the name of the language of your input file')
parser.add_argument('-o', '--output', metavar='output', type=str, help='the name of the output file')

args = parser.parse_args()

# Read the Python code from the file
try:
    with open(args.file, 'r') as f:
        code = f.read()
except IOError:
    print(f'Error: could not read file {args.file}')
    sys.exit(1)
    
if args.lang == 'python':
    language = language
elif args.lang == 'go':
    language = language
else:
    print('This test environment only takes python and go as input languages. Please enter a file with one of these languages to proceed with testing.')
    sys.exit(1)
# Parse the code using the Python language grammar
#parser = Parser()
lang_parser.set_language(language)
tree = lang_parser.parse(bytes(code, 'utf-8'))

# Uncomment to print all nodes and their children of a given file
# Traverse the parse tree and print the nodes
# def print_node(node, depth=0):
#     print('  ' * depth + f'{node.type}: "{code[node.start_byte:node.end_byte].strip()}"')
#     for child in node.children:
#         print_node(child, depth+1)


print(f'Scanning {args.file}...')
# print_node(tree.root_node)
# print(dir(tree.root_node))

def node_to_dict(node):
    children = [node_to_dict(child) for child in node.children]
    if children:
        return {
            'type': node.type,
            'text': code[node.start_byte:node.end_byte].replace('\n', '\\n'),
            'children': children
        }
    else:
        return {
            'type': node.type,
            'text': code[node.start_byte:node.end_byte].replace('\n', '\\n')
        }

ast = node_to_dict(tree.root_node)

# Write the JSON object to a file.
if args.output:
    output_file = args.output
else:
    # If no output file was specified, use the input file name with a .json extension.
    output_file = os.path.splitext(args.file)[0] + '.json'

with open(f'{output_file}.json', 'w') as f:
    json.dump(ast, f, indent=2)
print(f'Parsing complete in {time.time() - t0} seconds!')
