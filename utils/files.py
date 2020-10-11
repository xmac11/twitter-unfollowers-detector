import json


def write_json_file(data):
    with open('followers.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json_file():
    try:
        with open('followers.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
