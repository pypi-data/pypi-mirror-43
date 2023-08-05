import json


def get_token(session, instance, username, password):
    headers = {'Content-Type': 'application/json'}
    token_payload = {"username": username, "password": password, "grant_type": "password"}
    # get auth token and create headers dict
    response = session.post(instance + "/api/auth-service/token/", headers=headers, json=token_payload)
    print("Get token: " + str(response.status_code))
    print(response.reason)

    return json.loads(response.text)['access_token']