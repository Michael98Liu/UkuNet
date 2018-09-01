# utility functions
import json
def save_json(data, name):
    with open('../obj/'+ name + '.json', 'w') as fp:
        json.dump(data, fp)

def load_json(name):
    with open('../obj/'+ name + '.json', 'r') as fp:
        data = json.load(fp)
    return data
