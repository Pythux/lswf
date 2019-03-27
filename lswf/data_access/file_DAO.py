import lswf.database.interface


class SQL(lswf.database.interface.SQL):
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
