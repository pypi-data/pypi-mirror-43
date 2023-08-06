import json
import logging
import os
from collections import deque

from util.models import Node, Category, Automaton, ExportedAutomaton

logger = logging.getLogger('main')


# Utility function to return the preorder list of the given K-Ary Tree
def preorder_traversal_dir(directory, root_node):
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
        top_node_path = directory + os.sep + top_node.path
        if type(top_node.val) is Category:
            for item in os.listdir(top_node_path):
                if not item.endswith('.json'):
                    continue

                child_data = read_json_file(top_node_path + os.sep + item)
                if 'latestAutomatonVersion' in child_data:
                    child = Automaton(child_data)
                elif 'automatonFlow' in child_data:
                    child = ExportedAutomaton(child_data)
                else:
                    child = Category(child_data)

                child_node = Node(child.id, child)
                child_node.path = top_node.path + "/" + child_node.val.name.strip() \
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
    logger.debug("Reading directory %s", directory)

    # create fake root node
    root_category = Category(
        {'name': 'automata_root', 'id': 'root', 'clientId': '', 'parentId': None, 'deleted': False})
    root_node = Node(root_category.id, root_category)
    root_node.path = directory

    for item in os.listdir(directory):
        if not item.endswith('.json'):
            continue

        child_data = read_json_file(directory + os.sep + item)
        logger.debug(child_data)
        child = Category(child_data)
        child_node = Node(child.id, child)
        child_node.path = child.name
        root_node.children.append(child_node)

    return preorder_traversal_dir(directory, root_node)


def read_json_file(file_name):
    with open(os.path.normpath(file_name)) as infile:
        logger.debug('<Reading file %s', os.path.normpath(file_name))
        data = json.load(infile)
        return data


def write_json_file(file_name, data):
    with open(file_name, 'w') as outfile:
        logger.debug('>Writing file %s', file_name)
        json.dump(data, outfile, indent=4, sort_keys=True)
