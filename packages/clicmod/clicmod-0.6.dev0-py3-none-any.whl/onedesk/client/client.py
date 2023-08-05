def get_client(session, instance, client_name):
    params = {'size': 10000}  # TODO this could be better
    client_list = session.get(instance + "/api/clients", params=params)
    print("Get client " + client_name + ": " + str(client_list.status_code))
    print(client_list.reason)
    # print(client_list.json())

    for client in client_list.json()['content']:
        if client['code'] == client_name:
            return client

    print("No client with the provided name found, exiting...")
    raise SystemExit


def create_client(name):  # TODO implement this
    raise NotImplementedError
