import pprint


class TooBig:
    def __init__(self, path, last_update=None, key=None):
        self.key = key
        self.path = path

    def __repr__(self):
        return pprint.pformat({
            'type': self.__class__.__name__,
            'key': self.key,
            'path': self.path,
        })
