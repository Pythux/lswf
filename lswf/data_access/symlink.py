from database import InterfaceCRUD


class SymLink(InterfaceCRUD):
    @property
    def table(self):
        return 'symlink'

    @property
    def key_name(self):
        return 'symlink_id'

    def get_params_and_values(self, obj):
        return (['is_dir', 'path', 'symlink_to'],
                [obj.is_dir, obj.path, obj.symlink_to])

    @staticmethod
    def get_unique(obj):
        return (['path'], [obj.path])

    @staticmethod
    def set_obj(obj, selected):
        obj.key, obj.is_dir, obj.path, obj.symlink_to = selected
