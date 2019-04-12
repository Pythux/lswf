
import os
from shutil import copy2, copytree, move, rmtree

from lswf.core.init import ram_data, disk_dir
from lswf.database import sql, db, SymLink


disk_data = os.path.join(disk_dir, 'src', 'data')


def create_needed_symlink():
    delete_sym_in_symdir()
    li_symlink_to_do = SymLink.from_select_stars(sql(
        'select * from symlink where symlink_to is null'
    ))
    for symlink in li_symlink_to_do:
        name = os.path.split(symlink.path)[1]
        symlink.symlink_to = name + ' ' + str(symlink.key)
        move_to_disk_and_copy_to_ram(symlink)


def move_to_disk_and_copy_to_ram(symlink):
    path_on_disk = os.path.join(disk_data, symlink.symlink_to)
    path_on_ram = os.path.join(ram_data, symlink.symlink_to)

    move(symlink.path, path_on_disk)
    if symlink.is_dir:
        copytree(path_on_disk, path_on_ram)
    else:
        copy2(path_on_disk, path_on_ram)

    os.symlink(path_on_ram, symlink.path)
    db.update(symlink)


def delete_symlink(symlink):
    if symlink.symlink_to is not None:
        if os.path.islink(symlink.path):
            os.unlink(symlink.path)
            move(os.path.join(ram_data, symlink.symlink_to), symlink.path)
            to_delete = os.path.join(disk_data, symlink.symlink_to)
            if symlink.is_dir:
                rmtree(to_delete)
            else:
                os.unlink(to_delete)
        else:
            SystemError(
                'delete_symlink: path should be ' +
                'a symlink, please, check path: {}'
                .format(symlink.path)
            )
    db.delete(symlink)


def delete_sym_in_symdir():
    li_path_dir = list(map(lambda t: t[0], sql(
        'select path from symlink where is_dir = 1')))
    li_sym = SymLink.from_select_stars(sql(
        'select * from symlink'))

    for symlink in li_sym:
        splited_path = symlink.path
        while True:
            splited_path, rest = os.path.split(splited_path)
            if rest == '':
                break
            if splited_path in li_path_dir:
                delete_symlink(symlink)
                break
