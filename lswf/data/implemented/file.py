import pprint

from lswf.service.init import sql
import lswf.data.interface


class File:
    def __init__(self, path, last_update, key=None):
        self.path = path
        self.last_update = last_update
        self.key = key

    def __repr__(self):
        return pprint.pformat({
            'type': self.__class__.__name__,
            'key': self.key,
            'path': self.path,
            'last_update': self.last_update,
        })


class SQL_Service(lswf.data.interface.SQLService):
    @property
    def table(self):
        return 'file'

    def create(self, obj):
        key = sql(
            'insert into {}({}, {}) values (?, ?)'
            .format(self.table, 'path', 'last_update'),
            obj.path, obj.last_update)
        obj.key = key

    def read(self, obj):
        where = self.get_where(obj)
        r = sql('select file_id, last_update' +
                ' from {} where {} = ?'
                .format(self.table, where[0]),
                where[1])
        if r == []:
            return None
        if len(r) != 1:
            raise ValueError('read must return a single element')
        obj.key, obj.last_update = r[0]

    def update(self, obj):
        if not obj.key:
            raise ValueError("can't update without the obj key")
        sql('update {} set path= ?, last_update=? where file_id=?'
            .format(self.table),
            obj.path, obj.last_update, obj.key)

    def delete(self, obj):
        if not obj.key:
            raise ValueError("can't delete without the obj key")
        sql('delete from {} where file_id=?'
            .format(self.table), obj.key)
        obj.key = None

    @staticmethod
    def get_where(obj):
        where = 'path', obj.path
        if obj.key:
            where = ('file_id', obj.key)
        return where
