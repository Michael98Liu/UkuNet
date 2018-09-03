# utility functions
import json
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(THIS_DIR, os.pardir)

def save_json(data, name):
    with open(ROOT_DIR + '/data/'+ name + '.json', 'w') as fp:
        json.dump(data, fp)

def load_json(name):
    with open(ROOT_DIR + '/data/'+ name + '.json', 'r') as fp:
        data = json.load(fp)
    return data

def store_page(html_doc, name):
    with open(ROOT_DIR + '/data/pages/' + name + '.html', 'w+') as f:
        f.write(html_doc)
        f.close()

if __name__ == '__main__':
    df = {}
    print(ROOT_DIR)

    save_json(df, 'empty')
