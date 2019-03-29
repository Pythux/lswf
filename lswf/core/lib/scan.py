import os
from datetime import datetime
import re

from tools.shell import sh

from lswf.core.init import to_absolute_path
from lswf.database import db, File, Directory, UpdateFrequence


"""
find . -type f -mtime -1 -printf '%h\n' | sort | uniq
find all files modified less than 1 day ago
-mmin n
        File's data was last modified n minutes ago.
give relative path from the find (absolute if '/' given)
say : find: ‘<path>’: Permission non accordée

for root, directories, filenames in os.walk(path):
    for directory in directories:
        print(os.path.join(root, directory))
    for filename in filenames:
        print(os.path.join(root, filename))
"""


def scan(path, timeout, change_since_mn):
    """path should be absolute,
        scan everything inside the path
    """
    path = to_absolute_path(path)
    find = 'find "{search_start}" -mmin -{mn}' \
        .format(search_start=path, mn=change_since_mn)
    outs, errs = sh(find, timeout=timeout)
    check_file_dirs(outs.split('\n'), errs.split('\n'))


def check_file_dirs(file_dirs, errs=None):
    errs = errs if errs else []
    for file_dir in file_dirs:
        if os.path.isfile(file_dir) or os.path.isdir(file_dir):
            if os.path.isfile(file_dir):
                o = File(file_dir)
            else:
                o = Directory(file_dir)
                o.listdir = os.listdir(file_dir)

            o.last_update = datetime.fromtimestamp(
                os.path.getmtime(file_dir)).replace(microsecond=0)
            update_change(o)

        elif file_dir == '':
            pass
        else:
            print("path: {} is not a file or a directory, skip"
                  .format(file_dir))

    for err in errs:
        if err == '':
            pass
        elif re.match(r"find: (.)+: ", err):
            pass
        else:
            raise ValueError('unhandled ! “{}”'.format(repr(err)))


def update_change(obj):
    update_or_create = False
    new_date = obj.last_update
    if db.read(obj):
        old_date = obj.last_update
        if old_date < new_date:
            update_or_create = True
    else:
        update_or_create = True

    if update_or_create:
        db.update_or_create(obj)
        db.create(UpdateFrequence(obj))
