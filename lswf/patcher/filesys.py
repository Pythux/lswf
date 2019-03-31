import os
from os.path import join as pj
import shutil

from tools.path import get_relative_path

from lswf.patcher.init import ram_data, disk_data, dir_patch_name


def get_binary_file_content(path):
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            return f.read()
    if os.path.exists(path):
        raise SystemError('path must be a file, path: ' + path)
    return None


def create_binary_file(path, content):
    with open(path, 'wb') as f:
        f.write(content)


def copy_data_in_src(abs_path):
    path_src = os.path.join(disk_data, 'src')
    if os.path.isdir(abs_path):
        shutil.copytree(abs_path, path_src)
    else:
        shutil.copy2(abs_path, path_src)


def delete_old_and_mv_new_to_src():
    """only work on file/dir in "src_new",
       a file/dir in "src_new" means it's already exist
        at least in "src" folder

        if there is files/dirs in "src_new":
            for each, delete it's occurence in
                src, xpatch-1, 2, ...
            move the file to "src"
            delete emptied dir in src_new
    """
    src_new = os.path.join(disk_data, 'src_new')
    walk = os.walk(src_new, topdown=False)
    for dirpath, dirnames, filenames in walk:
        for file_name in filenames:
            relative_path = get_relative_path(src_new, pj(dirpath, file_name))
            delete_olds(relative_path)
            os.rename(pj(disk_data, 'src_new', relative_path),
                      pj(disk_data, 'src', relative_path))

        for emptied_dir in dirnames:
            os.rmdir(pj(dirpath, emptied_dir))


def delete_olds(relative_path):
    def try_delete(path, delete_fn):
        if os.exists(path):
            delete_fn(path)
            return True
        return False

    delete_fn = os.remove
    if os.path.isfile(pj(ram_data, relative_path)):
        delete_fn = os.unlink

    try_delete(pj(disk_data, 'src', relative_path), delete_fn)
    i = 0
    while True:
        i += 1
        patch_dir = pj(disk_data, dir_patch_name(i), relative_path)
        if not try_delete(patch_dir, delete_fn):
            break
