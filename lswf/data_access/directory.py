from database import InterfaceCRUD


class SQL(InterfaceCRUD):
    @property
    def table(self):
        return 'directory'

    @property
    def key_name(self):
        return 'directory_id'

    def get_params_and_values(self, obj):
        return (['path', 'last_update', 'listdir'],
                [obj.path, obj.last_update, obj.listdir])

    def read(self, obj):
        r = self._read(obj.key, 'path', obj.path)
        if r:
            obj.key, obj.last_update, _, obj.listdir = r
