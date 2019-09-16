#!/usr/bin/env python3

import os
import time
from datetime import datetime

from tools.shell import TimeoutExpired
from tools.pip_my_term import WeelEWonka

from tools.path.scan import scan_file_dir

from lswf.core.init import init_if_needed
from lswf.database import db, TooBig, File, Directory, UpdateFrequence


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
        obj.last_update = new_date
        db.update_or_create(obj)
        db.create(UpdateFrequence(obj))


def fn_file(path):
    o = File(path)
    fn_both(o)


def fn_dir(path):
    o = Directory(path)
    o.listdir = os.listdir(path)
    fn_both(o)


def fn_both(o):
    o.last_update = datetime.fromtimestamp(
        os.path.getmtime(o.path)).replace(microsecond=0)
    update_change(o)


def scan(path, timeout, change_since_mn):
    scan_file_dir(path, timeout, change_since_mn, fn_file, fn_dir)


def full_scan(path, const_var):
    weel_e_wonka, timeout, sleep_ratio, avoid_paths, change_since = const_var

    if path in avoid_paths:
        return

    weel_e_wonka.msg(path)

    too_big = TooBig(path)
    if db.read(too_big):
        in_too_big(too_big, const_var)
        start = time.time()
    else:
        start = time.time()
        try_scan(path, const_var)

    stop = time.time()
    time.sleep(max(0, (stop - start) * sleep_ratio))


def in_too_big(too_big, const_var):
    if os.path.isfile(too_big.path):
        db.delete(too_big)
        full_scan(too_big.path, const_var)
    else:
        for file_or_dir in os.listdir(too_big.path):
            full_scan(os.path.join(too_big.path, file_or_dir), const_var)


def try_scan(path, const_var):
    _, timeout, *_, change_since = const_var
    if os.path.isfile(path):
        fn_file(path)
    else:
        try:
            scan(path, timeout, change_since)
        except TimeoutExpired:
            print('the path: “{}” is too big, split it'.format(path))
            db.create(TooBig(path))
            return full_scan(path, const_var)


def main(path, timeout, sleep_ratio, avoid_paths):
    init_if_needed()
    change_since = 1  # in minutes
    scan_number = 0
    weel_e_wonka = WeelEWonka()

    while True:
        start = time.time()
        full_scan(path, (weel_e_wonka, timeout, sleep_ratio,
                         avoid_paths, change_since))
        stop = time.time()
        delta = stop - start
        weel_e_wonka.msg_clear()
        print('full scan in {}s'.format('%.1f' % delta))
        scan_number += 1
        sleep = min(50, scan_number * 2)
        print('wait before next full scan: {}s'.format('%.0f' % sleep))
        time.sleep(sleep)
