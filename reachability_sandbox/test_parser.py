# Import the necessary packages
import os
import sys
import tree_sitter
from pprint import pprint

from tree_sitter import Language, Parser


GO_LANGUAGE = Language('build/my-languages.so', 'go')
# JS_LANGUAGE = Language('build/my-languages.so', 'javascript')
PY_LANGUAGE = Language('build/my-languages.so', 'python')

parser = Parser()
parser.set_language(PY_LANGUAGE)
# Define a sample Python code
src = '''
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
'''
parser = Parser()
parser.set_language(PY_LANGUAGE)
tree = parser.parse(bytes(src, 'utf-8'))

# Traverse the parse tree and print the nodes
def print_node(node, depth=0):
    print('  ' * depth + f'{node.type}: "{src[node.start_byte:node.end_byte].strip()}"')
    for child in node.children:
        print_node(child, depth+1)

# print(f'Scanning {args.file}...')
# print_node(tree.root_node)