import json
from CRUD_vanilla import InterfaceCRUD


class Directory(InterfaceCRUD):
    @property
    def table(self):
        return 'directory'

    @property
    def key_name(self):
        return 'directory_id'

    def get_params_and_values(self, obj):
        return (['path', 'last_update', 'listdir'],
                [obj.path, obj.last_update, json.dumps(obj.listdir)])

    @staticmethod
    def get_unique(obj):
        return (['path'], [obj.path])

    @staticmethod
    def set_obj(obj, selected):
        obj.key, obj.last_update, obj.path, obj.listdir = selected
        obj.listdir = json.loads(obj.listdir)
