
import os
import sys
import json
from jsonschema import validate, ValidationError

from tools.path import to_absolute_path
from CRUD_vanilla.connection import sql_sqlite

from .tables import tables

test_disk_dir = '/tmp/test_lswf/on_disk'
test_ram_dir = '/tmp/test_lswf/on_ram'

path_config_dir = to_absolute_path("~/.config/lswf")
path_config_json = os.path.join(path_config_dir, 'config.json')
db_name = "lswf.db"


def create_config_if_needed():
    base_conf = {
        "ram_directory": "/tmp/lower_ssd_write_frequency (inProgress)",
        "data_store_on_disk": "~/.config/lswf/data",
        "scan_path-to-avoid": ['/sys', '/proc', '/tmp', '/run', '/dev', '/timeshift'],
    }
    if not os.path.isdir(path_config_dir):
        os.makedirs(path_config_dir)
        with open(path_config_json, 'w') as file:
            json.dump(base_conf, file, sort_keys=True, indent=4)


def get_config():
    create_config_if_needed()
    with open(path_config_json, 'r') as file:
        try:
            conf = json.load(file)
        except json.decoder.JSONDecodeError as e:
            print("the json config at {} is not JSON valide, probably a mistake in editing it"
                  .format(path_config_json))
            print(e)
            raise SystemExit

    schema = {
        "type": "object",
        "properties": {
            "ram_directory": {"type": "string"},
            "data_store_on_disk": {"type": "string"},
            "scan_path-to-avoid": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["ram_directory", "data_store_on_disk", "scan_path-to-avoid"]
    }
    try:
        validate(instance=conf, schema=schema)
    except ValidationError as e:
        print("in the config file: {}".format(path_config_json))
        if len(e.path) > 0:
            print("\tin field: {}".format(e.path[0]))
        print("\tthe value {}".format(e.message))
        raise SystemExit
    return conf


conf = get_config()
# hanldle_conf:
disk_dir = to_absolute_path(conf['data_store_on_disk'])
ram_dir = to_absolute_path(conf['ram_directory'])
if hasattr(sys, '_called_from_test'):
    disk_dir = test_disk_dir
    ram_dir = test_ram_dir


def sql(req, *params):
    return sql_sqlite(os.path.join(disk_dir, db_name), req, *params)


def create_tables():
    for table in tables:
        sql(table)
    sql('insert into too_big_directory(path) values (?)', '/')


def try_create_table():
    is_table_exist = sql(
        "SELECT name FROM sqlite_master" +
        " WHERE type='table' AND name='directory';")
    if is_table_exist == []:
        create_tables()


def init_if_needed():
    if not os.path.isdir(disk_dir):
        try_create_table()
    if not os.path.exists(ram_dir):
        os.makedirs(ram_dir)


if __name__ == "__main__":
    init_if_needed()
