import json


def features(name):
    with open('func.json') as f:
        data = json.load(f)
        name = name.lower()
    print(data)
    try:
        return data[name]
    except KeyError:
        return ''

print(features('линейная'))
