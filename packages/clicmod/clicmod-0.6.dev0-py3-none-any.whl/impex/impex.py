import os
import ssl
import time

import requests
import urllib3
from pyfiglet import Figlet

from onedesk.auth.auth import get_token
from onedesk.automaton.automaton import export_automata, import_automaton, get_automaton_list_for_client, \
    delete_automata, automaton_exists
from onedesk.category.category import get_category_list_for_client, get_category, \
    get_category_tree, delete_category, create_path
from onedesk.client.client import get_client
from util.arguments import parser
from util.models import Category, Automaton, ExportedAutomaton
from util.util import get_directory_tree, write_json_file


def do_export(args):
    f = Figlet(font='slant')
    print(f.renderText('Export Start!'))
    start_time = time.time()

    # create export path on local file system
    try:
        os.makedirs(args.directory, exist_ok=True)
        print('Exporting to local directory: {}'.format(args.directory))
    except Exception:
        print("Failed to create export directory: " + args.directory)
        raise SystemExit

    # create session object
    s = requests.Session()
    s.verify = args.ignorecert

    # get token for session
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}

    client = get_client(s, args.instance, args.client)
    category_tree = get_category_tree(s, args.instance, client, args.category)

    for node in category_tree:
        if type(node.val) is Category and node.key == 'root':
            continue

        if type(node.val) is Category and len(node.children) == 0:
            continue

        data = None
        if type(node.val) is Category:
            data = get_category(s, args.instance, node)
            try:
                os.makedirs(args.directory + node.path, exist_ok=True)
            except Exception:
                print("Failed to create export directory: " + args.directory + node.path)
                raise SystemExit
        elif type(node.val) is Automaton:
            data = export_automata(s, args.instance, node.val.json())

        write_json_file(args.directory + node.path + '.json', data)

    print(f.renderText('FINISH!'))
    print(f.renderText('{0:.3g} seconds'.format((time.time() - start_time))))


def do_import(args):
    f = Figlet(font='slant')
    print(f.renderText('Import Start!'))
    start_time = time.time()

    if not os.path.exists(args.directory):
        print("Given directory does not exist! {}".format(args.directory))
        raise SystemExit(1)

    directory_tree = get_directory_tree(os.path.abspath(args.directory))

    # create session object
    s = requests.Session()
    s.verify = args.ignorecert

    # get token for session
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}

    # get client and their category list
    client = get_client(s, args.instance, args.client)
    target_category_list = get_category_list_for_client(s, args.instance, client)

    for node in directory_tree:
        if type(node.val) is ExportedAutomaton:
            print('<Importing automaton: [{} > {}]'.format(node.val.categoryPath, node.val.name))
            if automaton_exists(s, args.instance, client, node.val.name):
                print('Automata {} already exists, skipping...')  # TODO implement update logic
                continue

            parent = create_path(s, args.instance, client, node.val.categoryPath.split(">"))
            import_automaton(s, args.instance, parent, node)

    print(f.renderText('FINISH!'))
    print(f.renderText('{0:.3g} seconds'.format((time.time() - start_time))))


def do_wipe(args):
    f = Figlet(font='slant')
    print(f.renderText('Wipe Start!'))
    start_time = time.time()

    # create session object
    s = requests.Session()
    s.verify = args.ignorecert

    # get token for session
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}

    client = get_client(s, args.instance, args.client)
    automata_list = get_automaton_list_for_client(s, args.instance, client)
    category_list = get_category_list_for_client(s, args.instance, client)

    for automaton in automata_list:
        delete_automata(s, args.instance, automaton)

    for category in category_list:
        delete_category(s, args.instance, category)

    print(f.renderText('FINISH!'))
    print(f.renderText('{0:.3g} seconds'.format((time.time() - start_time))))


def main():
    print(ssl.OPENSSL_VERSION)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    subparsers = parser.add_subparsers()
    export_parser = subparsers.add_parser('export', help="Export automata from the given client/category")
    export_parser.set_defaults(func=do_export)
    import_parser = subparsers.add_parser('import', help="Import automata to the given client/category")
    import_parser.set_defaults(func=do_import)
    wipe_parser = subparsers.add_parser('wipe', help="Delete all automata and categories in the given client/category")
    wipe_parser.set_defaults(func=do_wipe)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
