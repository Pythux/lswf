import pprint


class UpdateFrequence:
    def __init__(self, obj):
        obj_name = obj.__class__.__name__
        if obj_name == 'File':
            obj_name = 'FileUpdateFrequence'
        elif obj_name == 'Directory':
            obj_name = 'DirectoryUpdateFrequence'
        else:
            raise SystemError('class name: ' + obj_name + ' not handled')
        self.__class__.__name__ = obj_name
        self.id_fk = obj.key
        self.update_time = obj.last_update

    def __repr__(self):
        return pprint.pformat({
            'type': self.__class__.__name__,
            'key': self.key,
            'id_fk': self.id_fk,
            'update_time': self.update_time,
        })
