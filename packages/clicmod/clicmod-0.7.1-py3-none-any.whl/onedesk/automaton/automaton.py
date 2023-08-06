import logging

from util.models import AutomatonVersion, ExportedAutomaton

logger = logging.getLogger('main')


def get_automaton_list_for_client(session, instance, client):
    logger.info('>>Getting automata for client: {}'.format(client['name']))
    automata_list = session.get(instance + "/api/automata/client/" + str(client['id']))
    logger.debug('Get automata list for client %s Response: %s', client['name'], automata_list.status_code)
    return automata_list.json()


def get_automaton_list_for_category(session, instance, category):
    logger.info('>>Getting automata for category: {}'.format(category.name))
    automata_list = session.get(instance + "/api/automata/category/" + str(category.id))
    logger.debug('Get automata list for category %s Response: %s'.format(category.name, automata_list.status_code))
    return automata_list.json()


def get_automaton(session, instance, automaton_id):
    automaton_response = session.get('{}/api/{}'.format(instance, automaton_id))
    logger.debug('Get automaton %s Response: %s', automaton_id, automaton_response.status_code)
    return automaton_response.json()


def update_automaton(session, instance, automaton):
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br'}
    params = {'newVersion': True}
    update_response = session.put('{}/api/automata/'.format(instance), data=automaton.json(), headers=headers,
                                  params=params)
    logger.debug('Update automaton response: {}'.format(update_response.status_code))
    return update_response.json()


def save_automaton(session, instance, automation):
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br'}
    rpc_action = {'action': 'automataController', 'method': 'saveAutomaton', 'type': 'rpc', 'tid': 0,
                  'data': automation.json()}
    save_response = session.post('{}/IPautomata/router'.format(instance), headers=headers, json=rpc_action)
    logger.debug('Save automaton response: %s', save_response.status_code)
    return save_response.json()


def delete_automata(session, instance, automata):
    logging.debug("!!Deleting automata {}".format(automata['name']))
    delete_response = session.delete(instance + "/api/automata/" + str(automata['id']))
    logging.debug('Delete automata %s Response: %s', automata['name'], delete_response.status_code)


def automaton_exists(session, instance, client, name):
    automata_list = get_automaton_list_for_client(session, instance, client)
    for automaton in automata_list:
        if name == automaton['name']:
            return automaton

    return None


def export_automata(session, instance, automaton):
    logging.debug('>Exporting automata {} | {}'.format(automaton['id'], automaton['name']))
    automaton_response = session.get('{}/api/automaton-import-export/export/{}'.format(instance, automaton['id']))
    logging.debug('Export automata response: {}'.format(automaton_response.status_code))
    return automaton_response.json()


def import_automaton(session, instance, category, automaton_name, automata_dto):
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br'}
    import_command = dict(clientId=category['clientId'], categoryId=category['id'],
                          exportedAutomatonDto=automata_dto, automatonName=automaton_name,
                          relinkExisting=True, importCategoryStructure=False,
                          tags=[], linkedImportCommands=[], automatonConnectionGroups=[])
    import_response = session.post('{}/api/automaton-import-export/import'.format(instance), headers=headers,
                                   json=import_command)
    logging.debug('Import automaton response: {}'.format(import_response.status_code))
    logging.debug(import_response.text)
    # return import_response.json()
