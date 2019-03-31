import os
import shutil

from lswf.patcher.init import disk_data


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
