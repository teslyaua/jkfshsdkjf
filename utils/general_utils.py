import json
import logging
from datetime import datetime
from pathlib import Path

import jsonschema
from faker import Faker
from jsonschema.validators import validate

logger = logging.getLogger()
fake = Faker()
pattern = 'autotest_data'
today = lambda: datetime.now().strftime("%Y:%m:%d_%H:%M:%S.%f")


def prettify_dict(dictionary):
    return json.dumps(dictionary, indent=4, sort_keys=True)


def validate_json(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        logger.error(err)
        logger.error(prettify_dict(json_data))
        return False
    return True


def get_root() -> Path:
    return Path(__file__).parent.parent


def load_json(json_path):
    with open(f'{get_root()}/{json_path}') as json_file:
        return json.load(json_file)
