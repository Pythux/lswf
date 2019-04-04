from CRUD_vanilla import InterfaceCRUD


class SQL(InterfaceCRUD):
    @property
    def key_name(self):
        raise SystemError('no key_name on update_frequence')

    def get_params_and_values(self, obj):
        return ([self.fk_name, 'update_time'],
                [obj.id_fk, obj.update_time])

    @staticmethod
    def get_unique(obj):
        raise SystemError('no get_unique funct on update_frequence')

    @staticmethod
    def set_obj(obj, selected):
        raise SystemError('no set_obj funct on update_frequence')
