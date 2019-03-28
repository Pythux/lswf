import pytest
from datetime import datetime

from lswf.core.init import sql
from lswf.database import db, File, Directory, SymLink


def test_sym():
    sql('delete from symlink')
    o = SymLink(True, '/to/the', '/tmp/data/')
    db.create(o)
    assert sql('select * from symlink') == \
        [(1, 1, '/to/the', '/tmp/data/')]


def test_dir():
    sql('delete from directory')
    d = datetime.now()
    o = Directory('/to/the', d, ['moon', 'stars'])
    db.create(o)
    assert sql('select path from directory') == [('/to/the',)]

    assert o.key == 1

    o.path = 'yo'
    print(o)
    db.update(o)
    assert sql('select path from directory') == [('yo',)]
    key = o.key
    o.key = None
    with pytest.raises(ValueError):
        db.delete(o)

    o.key = key
    db.delete(o)
    assert o.key is None
    assert sql('select * from directory') == []

    db.update_or_create(o)
    db.update_or_create(o)
    assert o.listdir == ['moon', 'stars']
    assert sql('select listdir from directory') == [('["moon", "stars"]',)]
    o.listdir = []
    db.update_or_create(o)
    assert o.listdir == []
    assert sql('select listdir from directory') == [('[]',)]


def test_file():
    sql('delete from file')
    assert sql('select * from file') == []

    d = datetime.now()
    o = File('/to/the', d)
    db.create(o)
    assert sql('select path from file') == [('/to/the',)]

    assert o.key == 1

    o.path = 'yo'
    print(o)
    db.update(o)
    assert sql('select path from file') == [('yo',)]
    key = o.key
    o.key = None
    with pytest.raises(ValueError):
        db.delete(o)

    o.key = key
    db.delete(o)
    assert o.key is None
    assert sql('select * from file') == []

    db.update_or_create(o)
    db.update_or_create(o)
    o.path = 'pa'
    db.update_or_create(o)
    assert o.path == 'pa'
    o.key = None
    db.update_or_create(o)
    assert len(sql('select * from file')) == 1
