from CRUD_vanilla import InterfaceCRUD


class File(InterfaceCRUD):
    @property
    def table(self):
        return 'file'

    @property
    def key_name(self):
        return 'file_id'

    def get_params_and_values(self, obj):
        return (['path', 'last_update'],
                [obj.path, obj.last_update])

    @staticmethod
    def get_unique(obj):
        return (['path'], [obj.path])

    @staticmethod
    def set_obj(obj, selected):
        obj.key, obj.last_update, obj.path = selected
