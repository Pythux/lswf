
import os
import sys
import json
from shutil import copytree

from tools.path import to_absolute_path
from database.connection import sql_sqlite


test_disk_dir = '/tmp/test_lswf/on_disk'
test_ram_dir = '/tmp/test_lswf/on_ram'


# ! loading config
with open('config.json') as conf:
    conf = json.loads(conf.read())
    db_name = conf['db_name']
    disk_dir = to_absolute_path(conf['data_store_on_disk'])
    ram_dir = to_absolute_path(conf['ram_directory'])
    if hasattr(sys, '_called_from_test'):
        disk_dir = test_disk_dir
        ram_dir = test_ram_dir

    disk_data = os.path.join(disk_dir, 'data')
    ram_data = os.path.join(ram_dir, 'data')


def sql(req, *params):
    return sql_sqlite(os.path.join(ram_dir, db_name), req, *params)


def create_db():
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
        sql_sqlite(os.path.join(disk_dir, db_name), table)
    sql_sqlite(os.path.join(disk_dir, db_name),
               'insert into too_big_directory(path) values (?)', '/')


def create_app_dir():
    os.makedirs(disk_data)
    create_db()


def init_if_needed():
    if os.path.isfile(os.path.join(disk_dir, db_name)):
        pass
    else:
        create_app_dir()
    if os.path.isfile(os.path.join(ram_dir, db_name)):
        pass
    else:
        try:
            copytree(disk_dir, ram_dir)
        except FileExistsError:
            if os.listdir(ram_dir) == []:
                os.rmdir(ram_dir)
                copytree(disk_dir, ram_dir)
            else:
                SystemError(
                    '{} is not empty, but {}'.format(ram_dir, db_name) +
                    ' is not inside this directory'
                )


if __name__ == "__main__":
    init_if_needed()
