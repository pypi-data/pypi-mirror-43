def get_automaton_list_for_client(session, instance, client):
    automata_list = session.get(instance + "/api/automata/client/" + str(client['id']))
    print('Get automata list for client {} Response: {}'.format(client['name'], automata_list.status_code))
    print('Returned {} automaton(s)'.format(len(automata_list.json())))
    return automata_list.json()


def get_automaton_list_for_category(session, instance, category):
    automata_list = session.get(instance + "/api/automata/category/" + str(category.id))
    print('Get automata list for category {} Response: {}'.format(category.name, automata_list.status_code))
    print('Returned {} automaton(s)'.format(len(automata_list.json())))
    return automata_list.json()


def get_automaton(session, instance, automaton_id):
    automaton_response = session.get('{}/api/{}'.format(instance, automaton_id))
    print('Get automaton {} Response: {}'.format(automaton_id, automaton_response.status_code))
    return automaton_response.json()


def update_automaton(session, instance, automaton):
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br'}
    update_response = session.put('{}/api/automata?newVersion=true'.format(instance), data=automaton, headers=headers)
    print('Update automaton response: {}'.format(update_response.status_code))
    return update_response.json()


def delete_automata(session, instance, automata):
    print("!Deleting automata " + automata['name'])
    delete_response = session.delete(instance + "/api/automata/" + str(automata['id']))
    print('Delete automata response: {}'.format(delete_response.status_code))


def automaton_exists(session, instance, client, name):
    automata_list = get_automaton_list_for_client(session, instance, client)
    for automaton in automata_list:
        if name == automaton['name']:
            return True

    return False


def export_automata(session, instance, automaton):
    print('>Exporting automata {} | {}'.format(automaton['id'], automaton['name']))
    automaton_response = session.get('{}/api/automaton-import-export/export/{}'.format(instance, automaton['id']))
    print('Export automata response: {}'.format(automaton_response.status_code))
    return automaton_response.json()


def import_automaton(session, instance, category, automata):
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br'}

    import_command = dict(clientId=category['clientId'], categoryId=category['id'],
                          exportedAutomatonDto=automata.val.json(), automatonName=automata.val.name,
                          relinkExisting=True, importCategoryStructure=False,
                          tags=[], linkedImportCommands=[], automatonConnectionGroups=[])
    import_response = session.post('{}/api/automaton-import-export/import'.format(instance), headers=headers,
                                   json=import_command)
    print('Import automaton response: {}'.format(import_response.status_code))
    print(import_response.text)
    return import_response.json()
