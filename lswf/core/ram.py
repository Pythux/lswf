import os
from lswf.database import db, SymLink
from lswf.lib import create_needed_symlink, delete_symlink


def add_path_to_ram(path):
    symlink = SymLink(os.path.isdir(path), path)
    if db.read(symlink):
        print('path: “{}” already in RAM'.format(path))
    else:
        db.create(symlink)
        create_needed_symlink()


def out_path_from_ram(path):
    symlink = SymLink(os.path.isdir(path), path)
    if db.read(symlink):
        delete_symlink(symlink)
    else:
        print('path: “{}” not in RAM'.format(path))
