import json
import os

def read_json(file_name):
    file_path = os.path.abspath(__file__+f'/../../static/{file_name}.json')
    with open(file_path,'r', encoding='utf-8') as file:
        return json.load(file)