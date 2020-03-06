import requests
import json
import inspect
import felicaidm as fe

def init_request(command_name):
    with open('azure_endpoint.json') as az_json:
        url = json.load(az_json)[command_name]
    headers = {"content-type":"application/json"}
    return url, headers

def shukkin(attendance, date_attend):
    crew_data = resolve_crew()
    payload = {
        "attend":attendance,
        "crew_id":crew_data["id"],
        "date_attend":date_attend
            }
    url, headers = init_request("shukkin")
    print("resistrating shukkin...")
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    print(r)
    print(r.text)

def add_crew(name, birthday, tourokubi):
    digest = fe.inputCard()
    payload = {
    "name":name,
    "birthday":birthday,
    "tourokubi":tourokubi,
    "card_hash":digest
    }
    url, headers = init_request("add_crew")
    print("adding new crew...")
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r)
    print(payload)

def resolve_crew():
    digest = fe.inputCard()
    payload = {
    "card_hash":digest
    }
    url, headers = init_request("resolve_name")
    print("resolving crew name...")
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r)
    crew_data = r.json()["ResultSets"]['Table1'][0]
    print(crew_data)
    return crew_data