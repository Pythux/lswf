#!/home/pythux/dev/venv/bin/python

import os
import sys
import sqlite3
import time
from datetime import datetime, timedelta
from IPython import embed
import json
import sys
import re

sys.path.append('~/dev/library/py-lib')
from shell import sh, err_print, TimeoutExpired


working_dir = '/tmp/ssd_temp'
db_name = 'sqlite.db'

# import glob
# for filename in glob.iglob('src/**/*.c', recursive=True):
#     print(filename)

# find . -type f -mtime -1 -printf '%h\n' | sort | uniq
# find all files modified less than 1 day ago
# -mmin n
#         File's data was last modified n minutes ago.
# give relative path from the find (absolute if '/' given)
# say : find: ‘<path>’: Permission non accordée

# for root, directories, filenames in os.walk(path):
#     for directory in directories:
#         print(os.path.join(root, directory))
#     for filename in filenames:
#         print(os.path.join(root, filename))

# os.path.getmtime("/home/pythux/dev/ShityProject/check_files_change/test.py")


def init_working_dir_if_needed():
    if not os.path.isdir(working_dir):
        try:
            os.mkdir(working_dir)
        except FileExistsError:
            # another process just created it, wait a little
            time.sleep(2)

    os.chdir(working_dir)

    if not os.path.isfile(db_name):
        try:
            create_db()
        except sqlite3.OperationalError:
            print('sqlite tables already exist, no tables creation performed')


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
    for table in create_tables:
        sql(table)
    sql('insert into too_big_directory(path) values (?)', '/')


def sql(req, params=None, many=False):
    is_insert = req.split()[0].lower() == 'insert'
    params = params if params else ()
    if not isinstance(params, (list, tuple)):
        params = params,
    with sqlite3.connect(db_name, detect_types=sqlite3.PARSE_DECLTYPES) as con:
        con.execute("PRAGMA foreign_keys = ON")
        if many:
            return con.executemany(req, params).fetchall()
        else:
            c = con.execute(req, params)
            if is_insert:
                return c.lastrowid
            return c.fetchall()


def scan(path, timeout, change_since_mn):
    """path should be absolute,
        scan everything inside the path
    """
    find = 'find "{search_start}" -type f -mmin -{mn}' \
        .format(search_start=path, mn=change_since_mn)
    outs, errs = sh(find, timeout=timeout)
    check_file_dirs(outs.split('\n'), errs.split('\n'))


def check_file_dirs(file_dirs, errs=None):
    errs = errs if errs else []
    for file_dir in file_dirs:
        if file_dir == '':
            pass
        elif os.path.isdir(file_dir):
            check_dir_change(file_dir, listdir=os.listdir(file_dir))
        elif os.path.isfile(file_dir):
            check_file_change(file_dir)
        else:
            print("path: {} is not a file or a directory, skip".format(file_dir))

    for err in errs:
        if re.match(r"find: (.)+: Permission non accordée", err):
            pass
        elif err == '':
            pass
        else:
            err_print('unhandled ! “{}”'.format(repr(err)))

    # for root, directories, filenames in os.walk(path):
    #     for directory in directories:
    #         dir_path = os.path.join(root, directory)
    #         check_dir_change(dir_path, listdir=os.listdir(dir_path))
    #     for filename in filenames:
    #         check_file_change(os.path.join(root, filename))


def check_file_change(path, listdir=None):
    now_minus_40min = datetime.now() - timedelta(minutes=40)
    dtime = datetime.fromtimestamp(os.path.getmtime(path)) \
        .replace(microsecond=0)
    if dtime > now_minus_40min:
        insert_or_update_file_change(path, dtime)


def insert_or_update_file_change(path, dtime):
    line = sql('select file_id, last_update from file where path=?', path)
    insert_into_update_frequence = \
        'insert into file_update_frequence(file_id, update_time) values (?, ?)'
    if line == []:
        insert = \
            'insert into file(path, last_update)' + \
            ' values (?, ?)'
        file_id = sql(insert, (path, dtime))
        sql(insert_into_update_frequence, (file_id, dtime))
    else:
        file_id, old_dtime = line[0]
        if dtime > old_dtime:
            sql('update file set last_update=? where file_id=?',
                (dtime, file_id))
            sql(insert_into_update_frequence, (file_id, dtime))


def check_dir_change(path, listdir):
    now_minus_40min = datetime.now() - timedelta(minutes=40)
    dtime = datetime.fromtimestamp(os.path.getmtime(path)) \
        .replace(microsecond=0)
    if dtime > now_minus_40min:
        select_dir = \
            'select directory_id, last_update, listdir from directory where path=?'
        line = sql(select_dir, path)
        if line == []:
            insert_dir_change(path, dtime, listdir)
        else:
            dir_id, old_dtime, old_listdir = line[0]
            old_listdir = json.loads(old_listdir)
            listdir, old_listdir = set(listdir), set(old_listdir)
            if dtime > old_dtime and listdir != old_listdir:
                update_dir_change(dir_id, path, dtime, list(listdir))
                # created = listdir - old_listdir
                deleted = old_listdir - listdir
                for d in deleted:
                    d = os.path.join(path, d)
                    dir_or_file = 'directory' if os.path.isdir(d) else 'file'
                    sql('delete from {} where path=?'.format(dir_or_file), d)


insert_into_dir_update_frequence = \
    'insert into directory_update_frequence(directory_id, update_time)' + \
    ' values (?, ?)'


def insert_dir_change(path, dtime, listdir):
    insert = \
        'insert into directory(path, last_update, listdir)' + \
        ' values (?, ?, ?)'
    directory_id = sql(insert, (path, dtime, json.dumps(listdir)))
    sql(insert_into_dir_update_frequence, (directory_id, dtime))


def update_dir_change(dir_id, path, dtime, listdir):
    listdir = json.dumps(listdir)
    sql('update directory set last_update=?, listdir=? where directory_id=?',
        (dtime, listdir, dir_id))
    sql(insert_into_dir_update_frequence, (dir_id, dtime))
