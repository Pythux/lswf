import pprint


class SymLink:
    def __init__(self, is_dir, path, symlink_to=None, key=None):
        self.key = key
        self.is_dir = is_dir
        self.path = path
        self.symlink_to = symlink_to

    def __repr__(self):
        return pprint.pformat({
            'type': self.__class__.__name__,
            'key': self.key,
            'is_dir': self.is_dir,
            'path': self.path,
            'symlink_to': self.symlink_to,
        })

    @staticmethod
    def from_select_stars(li_t):
        return list(map(lambda t: SymLink(*t[1:], t[0]), li_t))
