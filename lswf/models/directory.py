import pprint


class Directory:
    def __init__(self, path, last_update, listdir, key=None):
        self.path = path
        self.last_update = last_update
        self.key = key
        self.listdir = listdir

    def __repr__(self):
        return pprint.pformat({
            'type': self.__class__.__name__,
            'key': self.key,
            'path': self.path,
            'last_update': self.last_update,
            'listdir': self.listdir
        })
