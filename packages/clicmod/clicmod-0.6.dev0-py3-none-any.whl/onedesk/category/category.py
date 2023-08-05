from collections import deque

from onedesk.automaton.automaton import get_automaton_list_for_category
from util.models import Node, Category, Automaton


def get_category_list_for_client(session, instance, client):
    print('>>Getting categories for client: {}'.format(client['name']))
    category_list = session.get('{}/api/categories/client/{}'.format(instance, client['id']))
    print('Get categories for client'.format(client['name'], category_list.status_code))
    print('Returned {} categories'.format(len(category_list.json())))
    return category_list.json()


def get_category_list_for_category(session, instance, category):
    print('>>Getting categories for parent category: {}'.format(category['name']))
    category_list = session.get('{}/api/categories/parent/{}'.format(instance, category['id']))
    print('Get categories for client'.format(category['name'], category_list.status_code))
    print('Returned {} categories'.format(len(category_list.json())))
    return category_list.json()


def create_category(session, instance, client, name, parent):
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br'}
    if parent is not None:
        parent_id = parent['id']
    else:
        parent_id = None

    category_payload = {"name": name, "clientId": client['id'], 'parentId': parent_id}
    category_response = session.put('{}/api/categories'.format(instance), headers=headers, json=category_payload)
    print('Create category response: {}'.format(category_response.status_code))
    return category_response.json()


def delete_category(session, instance, category):
    print("!!Deleting category " + category['name'])
    delete_response = session.delete(instance + "/api/categories/" + str(category['id']))
    print('Delete category response: {}'.format(delete_response.status_code))


def create_path(session, instance, client, path):
    parent = None
    for name in path:
        if parent is None:
            category_list = []
            for item in get_category_list_for_client(session, instance, client):
                if item['parentId'] is None:
                    category_list.append(item)
        else:
            category_list = get_category_list_for_category(session, instance, parent)

        exists = False
        for category in category_list:
            if category['name'].strip() == name.strip():
                exists = True
                parent = category
                break

        if exists:
            continue
        else:
            parent = create_category(session, instance, client, name, parent)

    return parent


def get_category(session, instance, node):
    print('>>Getting category ' + node.val.name + " | " + str(node.key))
    data = session.get(instance + "/api/categories/" + str(node.key))
    print('Get category response: {}'.format(data.status_code))
    return data.json()


def get_category_tree(session, instance, client, root_category_name=None):
    category_list = get_category_list_for_client(session, instance, client)
    # create fake root node
    root_category = Category(
        {'name': client['name'] + 'automata_root', 'id': 'root', 'clientId': '', 'parentId': None, 'deleted': False})
    root_node = Node(root_category.id, root_category)
    root_node.path = ""

    for category in category_list:
        if category['name'].lower().startswith('ticket_'):
            continue

        if category['parentId'] is None:
            print(category)
            child = Category(category)
            child_node = Node(child.id, child)
            child_node.path = root_node.path + "/" + child.name
            root_node.children.append(child_node)

    category_tree = preorder_traversal_cat(session, instance, root_node)

    if root_category_name is not None:
        for x in category_tree:
            if x.val.name == root_category_name:
                return preorder_traversal_cat(session, instance, x)
        return []
    else:
        return category_tree


# Utility function to return the preorder list of the given K-Ary Tree
def preorder_traversal_cat(session, instance, root_node):
    stack = deque([])
    preorder = []
    preorder_nodes = []
    # 'preorder_nodes'-> contains all the visited nodes
    # add all children to the stack

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
            # get list of categories under top node
            category_list = get_category_list_for_category(session, instance, top_node.val.json())
            for category in category_list:
                if category['name'].lower().startswith('ticket_'):
                    continue

                print(category)
                child = Category(category)
                child_node = Node(child.id, child)
                child_node.path = top_node.path + "/" + child.name.strip() \
                    .replace(" ", "_") \
                    .replace("/", "_") \
                    .replace(":", "_") \
                    .replace("?", "")
                top_node.children.append(child_node)

            # get list of automata under top node
            automata_list = get_automaton_list_for_category(session, instance, top_node.val)
            for automaton in automata_list:
                print(automaton)
                child = Automaton(automaton)
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
