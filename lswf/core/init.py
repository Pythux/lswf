
import os
import sys

from tools.path import to_absolute_path
from CRUD_vanilla.connection import sql_sqlite
import patcher


test_disk_dir = '/tmp/test_lswf/on_disk'
test_ram_dir = '/tmp/test_lswf/on_ram'


conf = {
    "ram_directory": "/tmp/lower_ssd_write_frequency",
    "db_name": "sqlite.db",
    "data_store_on_disk": "~/.config/lower_ssd_write_frequency"
}


# hanldle_conf:
db_name = conf['db_name']
disk_dir = to_absolute_path(conf['data_store_on_disk'])
ram_dir = to_absolute_path(conf['ram_directory'])
if hasattr(sys, '_called_from_test'):
    disk_dir = test_disk_dir
    ram_dir = test_ram_dir

ram_data = os.path.join(ram_dir, 'data')


def sql(req, *params):
    return sql_sqlite(os.path.join(ram_dir, db_name), req, *params)


def create_tables():
    create_tables = ['''
        CREATE TABLE directory
            (directory_id INTEGER PRIMARY KEY NOT NULL,
            last_update timestamp NOT NULL, path TEXT UNIQUE NOT NULL,
            listdir TEXT NOT NULL)
        ''', '''
        CREATE TABLE file
            (file_id INTEGER PRIMARY KEY NOT NULL,
            last_update timestamp NOT NULL, path TEXT UNIQUE NOT NULL)
        ''', '''
        create table directory_update_frequence
            (directory_id INTEGER NOT NULL,
            update_time timestamp NOT NULL,
            CONSTRAINT UC_key UNIQUE (directory_id, update_time)
            CONSTRAINT fk_directory
                FOREIGN KEY (directory_id)
                REFERENCES directory(directory_id)
                ON DELETE CASCADE
            )
        ''', '''
        create table file_update_frequence
            (file_id INTEGER NOT NULL,
            update_time timestamp NOT NULL,
            CONSTRAINT UC_key UNIQUE (file_id, update_time)
            CONSTRAINT fk_file
                FOREIGN KEY (file_id)
                REFERENCES file(file_id)
                ON DELETE CASCADE
            )
        ''', '''
        create table too_big_directory
            (id INTEGER PRIMARY KEY NOT NULL,
            path TEXT UNIQUE NOT NULL)
        ''', '''
        create table symlink
            (symlink_id INTEGER PRIMARY KEY NOT NULL,
            is_dir boolean NOT NULL,
            path TEXT UNIQUE NOT NULL,
            symlink_to TEXT)
        ''']

    for table in create_tables:
        sql(table)
    sql('insert into too_big_directory(path) values (?)', '/')


def try_create_table():
    is_table_exist = sql(
        "SELECT name FROM sqlite_master" +
        " WHERE type='table' AND name='directory';")
    if is_table_exist == []:
        create_tables()


def try_create_data():
    if not os.path.exists(ram_data):
        os.makedirs(ram_data)


def init_if_needed():
    if not os.path.isdir(ram_dir):
        patcher.load(ram_dir, disk_dir)
        try_create_table()
        try_create_data()


if __name__ == "__main__":
    init_if_needed()
