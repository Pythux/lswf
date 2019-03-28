import pytest
from datetime import datetime
import sqlite3

from lswf.core.init import sql
from lswf.database import db, File, Directory, UpdateFrequence

from lswf.core.lib import scan


date = datetime(2019, 3, 28)


def update_change(o, select_freq):
    db.create(o)
    scan.update_change(o)
    assert select_freq() == []
    db.delete(o)
    scan.update_change(o)
    assert select_freq() == [(1, date)]
    scan.update_change(o)
    assert select_freq() == [(1, date)]
    with pytest.raises(sqlite3.IntegrityError) as e_info:
        db.create(UpdateFrequence(o))

    assert 'UNIQUE constraint failed' in str(e_info)


def test_update_change_file():
    sql('delete from file')
    o = File('/to/the', date)

    def select_freq():
        return sql('select * from file_update_frequence')
    update_change(o, select_freq)


def test_update_change_directory():
    sql('delete from directory')
    o = Directory('/to/the', date, [])

    def select_freq():
        return sql('select * from directory_update_frequence')
    update_change(o, select_freq)
