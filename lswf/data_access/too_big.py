from CRUD_vanilla import InterfaceCRUD


class TooBig(InterfaceCRUD):
    @property
    def table(self):
        return 'too_big_directory'

    @property
    def key_name(self):
        return 'id'

    def get_params_and_values(self, obj):
        return (['path'],
                [obj.path])

    @staticmethod
    def get_unique(obj):
        return (['path'], [obj.path])

    @staticmethod
    def set_obj(obj, selected):
        obj.key, obj.path = selected
