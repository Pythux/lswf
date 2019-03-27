from lswf.service.init import sql
import lswf.data.database.interface


class SQL(lswf.data.database.interface.SQL):
    @property
    def table(self):
        return 'file'

    @property
    def key_name(self):
        return 'file_id'

    def create(self, obj):
        obj.key = self._create(
            ['path', 'last_update'], [obj.path, obj.last_update])

    def read(self, obj):
        r = self._read(obj.key, 'path', obj.path)
        if r:
            obj.key, obj.last_update, _ = r

    def update(self, obj):
        self._update(
            obj.key, ['path', 'last_update'], [obj.path, obj.last_update])

    def delete(self, obj):
        if not obj.key:
            raise ValueError("can't delete without the obj key")
        sql('delete from {} where file_id=?'
            .format(self.table), obj.key)
        obj.key = None
