import pytest
from datetime import datetime
import sqlite3

from lswf.core.init import sql
from lswf.database import db, File, Directory, UpdateFrequence

# test import
from lswf.core.lib.scan import update_change, check_file_dirs

# function scan to use
from lswf.core.lib import scan


date = datetime(2019, 3, 28)


def check_update_change(o, select_freq):
    db.create(o)
    update_change(o)
    assert select_freq() == []
    db.delete(o)
    update_change(o)
    assert select_freq() == [(1, date)]
    update_change(o)
    assert select_freq() == [(1, date)]
    with pytest.raises(sqlite3.IntegrityError) as e_info:
        db.create(UpdateFrequence(o))

    assert 'UNIQUE constraint failed' in str(e_info)


def test_update_change_file():
    sql('delete from file')
    o = File('/to/the', date)

    def select_freq():
        return sql('select * from file_update_frequence')
    check_update_change(o, select_freq)


def test_update_change_directory():
    sql('delete from directory')
    o = Directory('/to/the', date, [])

    def select_freq():
        return sql('select * from directory_update_frequence')
    check_update_change(o, select_freq)


def test_scan():
    scan_result = ([
        '/abs_path/dev/testsym',
        '/abs_path/dev/testsym/yo',
        '/abs_path/dev/testsym/dir',
        '/abs_path/dev/testsym/dir/in_dir_2',
        '/abs_path/dev/testsym/dir/in_dir',
        '/abs_path/dev/testsym/dir/new_dir'],
        ['find: ‘/root’: Denied!', ''])

    check_file_dirs(*scan_result)
