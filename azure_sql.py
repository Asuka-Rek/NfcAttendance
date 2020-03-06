import requests
import json

def init_request(command_name):
    with open('azure_endpoint.json') as az_json:
        url = json.load(az_json)[command_name]
    headers = {"content-type":"application/json"}
    return url, headers

def shukkin(attendance, date_attend, crew_data):
    """
    出退勤をAzure上のDBに登録するHTTPリクエストを行う。
    
    Parameters
    ----------
    attendance : str(len <= 2)
        出勤/退勤
    date_attend : str(smalldatetime : YYYY-MM-DD HH:MM)
    crew_data : dict{id:int, name:str}
    """
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

def add_crew(name, birthday, tourokubi, card_hash):
    payload = {
    "name":name,
    "birthday":birthday,
    "tourokubi":tourokubi,
    "card_hash":card_hash
    }
    url, headers = init_request("add_crew")
    print("adding new crew...")
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r)
    print(payload)

def resolve_crew(card_hash):
    payload = {
    "card_hash":card_hash
    }
    url, headers = init_request("resolve_name")
    print("resolving crew name...")
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r)
    try:
        crew_data = r.json()["ResultSets"]['Table1'][0]
    except KeyError:
        return 400, None
    else:
        return crew_data

resolve_crew("aaadadajakdiai")
