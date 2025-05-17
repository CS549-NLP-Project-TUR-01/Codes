import json
import os

def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)
