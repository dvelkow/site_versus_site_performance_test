import json
from typing import Dict

def load_config(config_file: str) -> Dict:
    with open(config_file, 'r') as f:
        return json.load(f)
