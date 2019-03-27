from lswf.service.init import sql
import lswf.data.database.interface


class SQL(lswf.data.database.interface.SQL):
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
        where = 'path', obj.path
        if obj.key:
            where = ('file_id', obj.key)
        r = sql('select file_id, last_update' +
                ' from {} where {} = ?'
                .format(self.table, where[0]),
                where[1])
        if r == []:
            pass
        elif len(r) != 1:
            raise ValueError('read must return a single element')
        else:
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
