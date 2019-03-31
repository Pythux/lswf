import os

import bsdiff4

from tools.path import get_relative_path, scan_file_dir
from lswf.patcher.init import init_if_needed, ram_data, disk_data

from lswf.patcher.time import time_in_mn_since_last_scan
from lswf.patcher.filesys import get_binary_file_content, copy_data_in_src
from lswf.patcher.patch import get_li_patch, compose_patch, add_new_patch

import logging as l
l.basicConfig(level=l.DEBUG)
inf = l.info
from tools.log import log
from IPython import embed


def fn_file(abs_path):
    log(inf, abs_path)
    ram_file = get_binary_file_content(abs_path)
    relative_path = get_relative_path(ram_data, abs_path)
    log(inf, 'relative_path ' + relative_path)
    src = get_binary_file_content(
        os.path.join(disk_data, 'src', relative_path))
    if src is None:
        log(inf, 'create src')
        copy_data_in_src(abs_path)
    else:
        log(inf, 'create patch')
        try_patch(ram_file, src, relative_path)


def try_patch(ram_file, src, relative_path):
    li_patch = get_li_patch(relative_path)
    log(inf, 'already {} patch exist'.format(len(li_patch)))
    file_stored = compose_patch(src, *li_patch)
    if ram_file != file_stored:
        patch = bsdiff4.diff(file_stored, ram_file)
        add_new_patch(relative_path, patch, len(li_patch) + 1)
    else:
        log(inf, 'no change for: ' + relative_path)


def fn_dir(path):
    log(inf, 'diff_dir not impl' + path)


def scan():
    change_since_mn = time_in_mn_since_last_scan()
    scan_file_dir(ram_data, 100, change_since_mn, fn_file, fn_dir)


if __name__ == "__main__":
    init_if_needed()
    scan()
