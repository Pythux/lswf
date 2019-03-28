#!/usr/bin/python3

import os
import sys
import time
from shutil import copy2, copytree, move

from lib_scan_file_change import (
    working_dir, db_name, check_init_done, err_print, sql,
    TimeoutExpired, embed, data_store_on_disk)


def save_dir_path(frequency):
    li_dir_path = map(lambda tuple: tuple[0], sql(
        """
        select path, count(directory_id) as update_frequency
        from directory
        JOIN directory_update_frequence using (directory_id)

        GROUP BY path
        HAVING update_frequency >= ?
        order by update_frequency DESC
        """, frequency))

    sql('insert into symlinked_path(is_dir, path) select 1, ? ' +
        'WHERE NOT EXISTS (select 1 from symlinked_path where path=?)',
        map(lambda x: (x, x), li_dir_path))


def save_file_path(frequency):
    li_file_path = map(lambda tuple: tuple[0], sql(
        """
        select path, count(file_id) as update_frequency from file
        JOIN file_update_frequence using (file_id)

        GROUP BY path
        HAVING update_frequency >= ?
        order by update_frequency DESC
        """, frequency))

    sql('insert into symlinked_path(is_dir, path) select 0, ? ' +
        'WHERE NOT EXISTS (select 1 from symlinked_path where path=?)',
        map(lambda x: (x, x), li_file_path))


def create_needed_symlink():
    li_path_needing_symlink = sql(
        'select id, path, is_dir from symlinked_path where symlink_to is null'
    )
    for id_, path_needing, is_dir in li_path_needing_symlink:
        path, name = os.path.split(path_needing)
        # new_name = name + ' ' + str(id_)
        new_name = name
        path_on_disk = os.path.join(data_store_on_disk, new_name)
        path_on_ram = os.path.join(working_dir, new_name)
        move(path_needing, path_on_disk)
        if is_dir:
            copytree(path_on_disk, path_on_ram)
        else:
            copy2(path_on_disk, path_on_ram)

        os.symlink(path_on_ram, path_needing)
        sql('update symlinked_path set symlink_to = ? where id = ?',
            new_name, id_)


def delete_symlink(path, symlink_to):
    if symlink_to is not None:
        if os.path.islink(path):
            os.unlink(path)
            move(os.path.join(working_dir, symlink_to), path)
            os.unlink(os.path.join(data_store_on_disk, symlink_to))
        else:
            err_print('delete_symlink: path should be ' +
                      'a symlink, please, check path: {}'
                      .format(path))
            sys.exit(1)
    sql('delete from symlinked_path where path = ?', path)


def check_and_delete_symfile_in_symdir():
    li_dir = list(map(lambda tuple: tuple[0], sql(
        'select path from symlinked_path where is_dir = 1')))
    li_file = sql(
        'select path, symlink_to from symlinked_path where is_dir = 0')

    for path, symlink_to in li_file:
        splited_path = path
        while True:
            splited_path = os.path.split(splited_path)[0]
            if splited_path == '/':
                break
            if splited_path in li_dir:
                delete_symlink(path, symlink_to)
                break


def main():
    frequency = 1
    save_dir_path(frequency)
    save_file_path(frequency)
    check_and_delete_symfile_in_symdir()
    create_needed_symlink()


if __name__ == "__main__":
    doc = """
        Detect the file and folder to cache, based on frequency of Write
    """
    import argparse
    parser = argparse.ArgumentParser(
        description=doc, formatter_class=argparse.RawTextHelpFormatter)

    args = parser.parse_args()
    check_init_done()
    main()
