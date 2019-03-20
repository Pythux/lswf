#!/usr/bin/python3

import os
import sys
import json
from shutil import copytree

sys.path.append(os.path.join(os.environ['HOME'], 'dev/library/py-lib'))
from tools import to_absolute_path, sql_sqlite, err_print  # noqa: E402


# ! loading config
with open('config.json') as conf:
    conf = json.loads(conf.read())
    ram_dir = to_absolute_path(conf['ram_directory'])
    db_name = conf['db_name']
    data_store_on_disk = to_absolute_path(conf['data_store_on_disk'])


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
            (id INTEGER PRIMARY KEY NOT NULL,
            directory_id INTEGER,
            update_time timestamp NOT NULL,
            CONSTRAINT fk_directory
                FOREIGN KEY (directory_id)
                REFERENCES directory(directory_id)
                ON DELETE CASCADE
            )
        ''', '''
        create table file_update_frequence
            (id INTEGER PRIMARY KEY NOT NULL,
            file_id INTEGER,
            update_time timestamp NOT NULL,
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
        create table symlinked_path
            (id INTEGER PRIMARY KEY NOT NULL,
            is_dir boolean NOT NULL,
            path TEXT UNIQUE NOT NULL,
            symlink_to TEXT)
            ''']

    def sql(req, *params):
        sql_sqlite(req, os.path.join(data_store_on_disk, db_name), *params)

    for table in create_tables:
        sql(table)
    sql('insert into too_big_directory(path) values (?)', '/')


def create_app_dir():
    os.makedirs(os.path.join(data_store_on_disk, 'ram_save'))
    create_db()


def init_if_needed():
    if os.path.isfile(os.path.join(data_store_on_disk, db_name)):
        pass
    else:
        create_app_dir()
    if os.path.isfile(os.path.join(ram_dir, db_name)):
        pass
    else:
        try:
            copytree(data_store_on_disk, ram_dir)
        except FileExistsError:
            if os.listdir(ram_dir) == []:
                os.unlink(ram_dir)
                copytree(data_store_on_disk, ram_dir)
            else:
                err_print('{} is not empty, but {}'.format(ram_dir, db_name) +
                          ' is not inside this directory')


if __name__ == "__main__":
    init_if_needed()
