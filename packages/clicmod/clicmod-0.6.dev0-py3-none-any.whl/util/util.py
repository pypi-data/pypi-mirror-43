import json
import os
from collections import deque

from util.models import Node, Category, Automaton, ExportedAutomaton


# Utility function to return the preorder list of the given K-Ary Tree
def preorder_traversal_dir(root_node):
    stack = deque([])
    preorder = []
    preorder_nodes = []
    # 'preorder'-> contains all the visited nodes
    preorder.append(root_node.key)
    preorder_nodes.append(root_node)
    for child in root_node.children:
        stack.append(child)

    while len(stack) > 0:
        # 'flag' checks whether all the child nodes have been visited
        flag = 0
        # take top node from the stack
        top_node = stack[len(stack) - 1]

        if type(top_node.val) is Category:
            dir_list = os.listdir(os.path.abspath(top_node.path))

            for item in dir_list:
                if not item.endswith('.json'):
                    continue

                child_data = read_json_file(os.path.join(os.path.abspath(top_node.path), os.path.relpath(item)))
                if 'automatonFlow' in child_data:
                    child = ExportedAutomaton(child_data)
                else:
                    child = Category(child_data)

                child_node = Node(child.id, child)
                child_node.path = top_node.path + "/" + child.name.strip() \
                    .replace(" ", "_") \
                    .replace("/", "_") \
                    .replace(":", "_") \
                    .replace("?", "")
                top_node.children.append(child_node)

        preorder.append(top_node.key)
        preorder_nodes.append(top_node)

        if len(top_node.children) == 0:
            # CASE 1- If top of the stack is a leaf node then remove it from the stack
            x = stack.pop()  # TODO do something with x?
        else:
            # CASE 2- If top of the stack is parent with children
            par = top_node

            for i in range(0, len(par.children)):
                if par.children[i].key not in preorder:
                    flag = 1
                    # As soon as an unvisited child is found (left to right) push it to stack and store it in preorder
                    # start again from CASE-1 to explore this newly visited child
                    stack.append(par.children[i])

        # If all child nodes from left to right of a parent have been visited then remove the parent from the stack
        if flag == 0:
            stack.pop()

    return preorder_nodes


def find_category_parent(category, tree):
    for node in tree:
        if node.id == category.parent_id:
            return node

    return None


def find_automaton_parent(automaton, tree):
    for node in tree:
        if node.key == automaton.val.categoryId:
            return node

    return None


def get_directory_tree(directory):
    print("Reading directory " + directory)

    # create fake root node
    root_category = Category(
        {'name': 'automata_root', 'id': 'root', 'clientId': '', 'parentId': None, 'deleted': False})
    root_node = Node(root_category.id, root_category)
    root_node.path = directory

    for item in os.listdir(directory):
        if not item.endswith('.json'):
            continue

        child_data = read_json_file(os.path.join(os.path.abspath(directory), os.path.relpath(item)))
        if 'automaton_version' in child_data:
            child = Automaton(child_data)
        else:
            child = Category(child_data)

        child_node = Node(child.id, child)
        child_node.path = root_node.path + "/" + child.name.strip() \
            .replace(" ", "_") \
            .replace("/", "_") \
            .replace(":", "_") \
            .replace("?", "")
        root_node.children.append(child_node)

    return preorder_traversal_dir(root_node)


def read_json_file(file_name):
    with open(os.path.normpath(file_name)) as infile:
        print('<Reading file {}'.format(os.path.normpath(file_name)))
        data = json.load(infile)
        return data


def write_json_file(file_name, data):
    with open(os.path.normpath(file_name), 'w') as outfile:
        print('>Writing file {}'.format(os.path.normpath(file_name)))
        json.dump(data, outfile, indent=4, sort_keys=True)


def write_node(node, data, directory=""):
    paths = node.path.split("/")
    paths.remove(node.val.name.strip()
                 .replace(" ", "_")
                 .replace("/", "_")
                 .replace(":", "_")
                 .replace("?", ""))
    path = "/".join(paths)
    file_name = directory + path + "/" + node.val.name.strip() \
        .replace(" ", "_") \
        .replace("/", "_") \
        .replace(":", "_") \
        .replace("?", "") + '.json'

    if type(node.val) is Category and node.val.parent_id is None:
        path = ""

    try:
        os.makedirs(directory + path, exist_ok=True)
    except Exception:
        print("Failed to create export directory: " + path)
        raise SystemExit

    with open(file_name, 'w') as outfile:
        print('>Writing file ' + file_name)
        json.dump(data, outfile, indent=4, sort_keys=True)
