import os
import sys
import json
import argparse
from tree_sitter import Language, Parser

PY_LANGUAGE = Language('/home/jennifer/social-cyber/Reachability/build/my-languages.so', 'python')
#C_LANGUAGE = Language('/home/jennifer/social-cyber/Reachability/build/my-languages.so', 'c')
GO_LANGUAGE = Language('/home/jennifer/social-cyber/Reachability/build/my-languages.so', 'go')
# for some reason relative paths don't work???
# until we figure this out, CHANGE THIS TO YOUR ABSOLUTE PATH



def get_import_nodes(filename, language):
    parser = Parser()
    if language == 'python':
        parser.set_language(PY_LANGUAGE)
    elif language == 'go':
        parser.set_language(GO_LANGUAGE)
    # elif language == 'c':
    #     parser.set_language(C_LANGUAGE)

    else:
        print("Unknown language")
        return
    src = open(filename, 'rb').read()
    tree = parser.parse(src)

    if language == 'python':
        node_name = filename[:-3] # take off the .py
        import_nodes = [node for node in tree.root_node.children if 'import' in node.type]
    elif language == 'c':
        node_name = filename[:-1] # take off the .c or .h
        import_nodes = [node for node in tree.root_node.children if 'include' in node.type]
    elif language == 'go':
        node_name = filename[:-3] # take of the .go
        import_nodes = []
        for node in tree.root_node.children:
            if node.type == 'import_declaration':
                for import_child in node.children:
                    if import_child.type == 'import_spec':
                        import_nodes.append(import_child)
                    elif import_child.type == 'import_spec_list':
                        import_nodes += [node for node in import_child.children if node.type == 'import_spec']
        # this will not process using subdirectores as a package correctly
        # it will just give the subdirectory name, rather than the .go files in that subdirectory
        # todo: use Haley's part to grab subdirectories and expand them

    # will this get all of them?
    # do we care if it's an aliased import, a 'from __ import __' thing, etc.?

    imports_dict = dict()
    imports_dict[node_name] = []

    for node in import_nodes:
        line = src[node.start_byte:node.end_byte]
        if language == 'python':
            name_full = line.split()[1]
        if language == 'go':
            name_full = line[1:-1] # take off the quotes
        if language == 'c':
            name_full = line.split()[1] # todo: is this right?
        name_init = name_full.split(bytes('.', 'utf-8'))[0] # do we want just the first part, or the whole package.thing.thing string?
        imports_dict[node_name].append(name_full.decode('utf-8')) # do we want this to be a string or a bytes object?
        #imports_dict[node_name].append(name_init.decode('utf-8')) # do we want this to be a string or a bytes object?
        
    print(imports_dict)
    return imports_dict

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Scan Python code using Tree-sitter')
    parser.add_argument('file', metavar='file', type=str, help='the name of the input file')
    # parser.add_argument('-o', '--output', metavar='output', type=str, help='the name of the output file')

    args = parser.parse_args()
    filename = args.file
    
    import_dict = get_import_nodes(filename, 'python')
    
if __name__ == '__main__':
    main()