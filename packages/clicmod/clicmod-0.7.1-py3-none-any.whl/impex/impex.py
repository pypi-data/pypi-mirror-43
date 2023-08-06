import logging
import os
import ssl
import time

import requests
import urllib3
from pyfiglet import Figlet
from tqdm import tqdm

from onedesk.auth.auth import get_token
from onedesk.automaton.automaton import export_automata, import_automaton, get_automaton_list_for_client, \
    delete_automata, automaton_exists
from onedesk.category.category import get_category_list_for_client, \
    get_category_tree, delete_category, create_path
from onedesk.client.client import get_client
from util.arguments import parser
from util.models import Category, Automaton, ExportedAutomaton
from util.util import get_directory_tree, write_json_file

f = Figlet(font='slant')
# setup main logger
ch = logging.StreamHandler()
formatter = logging.Formatter('{asctime} {levelname} {name} {filename} {lineno} | {message}', style='{')
ch.setFormatter(formatter)
logger = logging.getLogger('main')
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)  # This toggles all the logging
logger.debug(ssl.OPENSSL_VERSION)


def do_export(args):
    print(f.renderText('Export Start !!'))
    start_time = time.time()

    directory = os.path.abspath(args.directory)
    # create export path on local file system
    try:
        os.makedirs(directory, exist_ok=True)
        logger.info('Exporting to local directory: %s', directory)
    except Exception:
        logger.error('Failed to create export directory: %s', directory)
        raise SystemExit

    # create session object
    s = requests.Session()
    s.verify = args.ignorecert

    # get token for session
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}

    client = get_client(s, args.instance, args.client)
    category_tree = get_category_tree(s, args.instance, client, args.category)

    for node in tqdm(category_tree, desc='Exporting node tree to {}'.format(directory)):
        if type(node.val) is Category and node.key == 'root':
            continue

        if type(node.val) is Category and len(node.children) == 0:
            continue

        data = node.val.json()
        # if type(node.val) is Category:
        # data = get_category(s, args.instance, node)

        if type(node.val) is Automaton:
            data = export_automata(s, args.instance, node.val.json())

        node_path = directory + os.sep + node.path

        try:
            logger.debug('Creating directory %s', node_path)
            os.makedirs(node_path, exist_ok=True)
        except Exception:
            logger.error('Failed to create export directory: %s', node_path)
            raise SystemExit

        file_name = node.val.name.strip() \
            .replace("/", "_") \
            .replace(":", "_") \
            .replace("?", "") + '.json'

        file_path = os.path.join(node_path, file_name)
        write_json_file(file_path, data)

    print(f.renderText('FINISH !! --- {0:.3g} seconds'.format((time.time() - start_time))))


def do_import(args):
    print(f.renderText('Import Start !!'))
    start_time = time.time()
    directory = os.path.abspath(args.directory)

    if not os.path.exists(directory):
        print("Given directory does not exist! {}".format(directory))
        raise SystemExit(1)

    directory_tree = get_directory_tree(directory)

    # create session object
    s = requests.Session()
    s.verify = args.ignorecert

    # get token for session
    token = get_token(s, args.instance, args.username, args.password)
    s.headers = {'authorization': 'bearer ' + token}

    # get client and their category list
    client = get_client(s, args.instance, args.client)

    for node in tqdm(directory_tree, desc='Importing node tree to instance'):
        if type(node.val) is ExportedAutomaton:
            logging.debug('<Importing automaton: [{} > {}]'.format(node.path, node.val.name))
            existing_automaton = automaton_exists(s, args.instance, client, node.val.name)
            if existing_automaton:
                delete_automata(s, args.instance, existing_automaton)  # TODO make this not suck
                # node.val.id = existing_automaton['id']
                # update_automaton(s, args.instance, node.val)
                # continue

            parent = create_path(s, args.instance, client, node.path.split("/")[0:-1])
            # automata_version = AutomatonVersion(node.val.latestAutomatonVersion)
            # automata_dto = ExportedAutomaton(node.val.json(), automata_version.json())
            # automata_dto.categoryPath = node.path.replace("/", " > ")
            # automata_dto.clientCode = client['code']
            import_automaton(s, args.instance, parent, node.val.name, node.val.json())

    print(f.renderText('FINISH !! --- {0:.3g} seconds'.format((time.time() - start_time))))


def do_wipe(args):
    print(f.renderText('Wipe Start !!'))
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

    for automaton in tqdm(automata_list, desc='Deleting automata'):
        delete_automata(s, args.instance, automaton)

    for category in tqdm(category_list, desc='Deleting categories'):
        delete_category(s, args.instance, category)

    print(f.renderText('FINISH !! --- {0:.3g} seconds'.format((time.time() - start_time))))


def main():
    # pars args
    subparsers = parser.add_subparsers()
    export_parser = subparsers.add_parser('export', help="Export automata from the given client/category")
    export_parser.set_defaults(func=do_export)
    import_parser = subparsers.add_parser('import', help="Import automata to the given client/category")
    import_parser.set_defaults(func=do_import)
    wipe_parser = subparsers.add_parser('wipe', help="Delete all automata and categories in the given client/category")
    wipe_parser.set_defaults(func=do_wipe)
    args = parser.parse_args()

    # disable because it gets annoying
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # do something!
    args.func(args)


if __name__ == '__main__':
    main()
