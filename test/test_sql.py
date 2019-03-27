import pytest
from datetime import datetime

from lswf.data.database.sql import db, sql, File


def test_file():
    sql('delete from file')
    assert sql('select * from file') == []

    d = datetime.now()
    f = File('/to/the', d)
    db.create(f)
    assert sql('select path from file') == [('/to/the',)]

    assert f.key == 1

    f.path = 'yo'
    print(f)
    db.update(f)
    assert sql('select path from file') == [('yo',)]
    key = f.key
    f.key = None
    with pytest.raises(ValueError):
        db.delete(f)

    f.key = key
    db.delete(f)
    assert f.key is None
    assert sql('select * from file') == []

    db.update_or_create(f)
    db.update_or_create(f)
    f.path = 'pa'
    db.update_or_create(f)
    assert f.path == 'pa'
    f.key = None
    db.update_or_create(f)
    assert len(sql('select * from file')) == 1
