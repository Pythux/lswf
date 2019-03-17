#!/home/pythux/dev/venv/bin/python

import os
import sys
import time

from lib_scan_file_change import (
    init_working_dir_if_needed,
    working_dir, err_print, sql,
    scan, TimeoutExpired, check_file_dirs)


running_time = 0


def big_scan(path, run_time, run_percent, timeout, avoid_paths, change_since):
    global running_time
    if path in avoid_paths:
        return

    def sleep():
        global running_time
        sleep_time = max(0, run_time / run_percent * (1 - run_percent))
        print('sleep: {}'.format(sleep_time))
        time.sleep(sleep_time)
        running_time = 0

    time_left = run_time - running_time
    if time_left < timeout:
        print('no enouth time, time_left: {}'.format('%.3f' % time_left))
        sleep()
    is_path_big = sql('select 1 from too_big_directory where path=?', path) \
        != []
    print('path: {} in “is too big” DB ? {}'.format(path, is_path_big))
    if is_path_big:
        if not os.path.isdir(path):
            sql('delete from too_big_directory where path=?', path)
            big_scan(path, run_time, run_percent, timeout,
                     avoid_paths, change_since)
        else:
            for file_or_dir in os.listdir(path):
                big_scan(os.path.join(path, file_or_dir),
                         run_time, run_percent, timeout,
                         avoid_paths, change_since)
    else:
        if not os.path.isdir(path):
            check_file_dirs([path])
        else:
            start = time.time()
            try:
                scan(path, timeout, change_since)
            except TimeoutExpired:
                print('the path: “{}” is too big, '.format(path) +
                      'insert it in “is too big” DB and re-run')
                sql('insert into too_big_directory(path) values (?)', path)
                return big_scan(path, run_time, run_percent, timeout,
                                avoid_paths, change_since)
            finally:
                stop = time.time()
                delta = stop - start
                print('delta: {}, running_time: {}, new running_time: {}'
                      .format('%.3f' % delta, '%.3f' % running_time,
                              '%.3f' % (running_time + delta)))
                running_time += delta


# src = '/usr/bin/python'
# dst = '/tmp/python'

# # This creates a symbolic link on python in tmp directory
# os.symlink(src, dst)

if __name__ == "__main__":
    doc = """
        Scan thought all directory, don't go above mount point nor symlink
        research frequently create, update, delete in the filesystem (frequente modification)
    """
    import argparse
    parser = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_argument("--init_and_quit",
    #                     help="init /tmp/<working_dir> folder, then quit",
    #                     action='store_true')
    # if args.init_and_quit:
    #     init_working_dir()

    # parser.add_argument(
    #     "--run_percent",
    #     help='10%% means: scan files 10%%, "sleep 90%%" of time',
    #     default='10%%'
    #     )
    # parser.add_argument(
    #     "--run_time",
    #     help='max time in secondes for a single scan, ' +
    #          'minimum is 1 seconde',
    #     default=5, type=int,
    #     )
    # parser.add_argument(
    #     "--timeout",
    #     help='timeout on a scan in seconde',
    #     default=3, type=int,
    #     )
    parser.add_argument(
        "--scan_speed",
        help='fast, medium, slow',
        default='fast',
        )
    args = parser.parse_args()
    # try:
    #     args.run_percent = int(args.run_percent.rstrip('%%')) / 100
    # except ValueError:
    #     err_print('args run_percent must be a percent: XX%%')

    # if args.run_time < 1:
    #     err_print('option run_time must be at least 1 seconde')
    #     sys.exit(1)
    # if args.timeout < 1:
    #     err_print('option timeout must be at least 1 seconde')
    #     sys.exit(1)
    # if args.timeout > args.run_time:
    #     err_print('option timeout > run_time, can\'t work, must be <=')
    #     sys.exit(1)

    if args.scan_speed not in ['fast', 'medium', 'slow']:
        err_print('option timeout > run_time, can\'t work, must be <=')
        sys.exit(1)
    mode = {
        'fast': [100, 5, 400],
        'medium': [60, 3, 5],
        'slow': [40, 2, 4],
    }
    run_percent, timeout, run_time = mode[args.scan_speed]
    change_since = 1  # in minutes

    init_working_dir_if_needed()
    os.chdir(working_dir)
    avoid_paths = ['/sys', '/proc', '/tmp', '/timeshift']

    scan_number = 0

    while True:
        running_time = 0
        start = time.time()
        big_scan('/', run_time=run_time,
                 run_percent=run_percent, timeout=timeout,
                 avoid_paths=avoid_paths, change_since=change_since)
        stop = time.time()
        delta = stop - start
        print('full scan in {}s'.format('%.1f' % delta))
        scan_number += 1
        sleep = min(50, scan_number * 2)
        print('wait before next full scan: {}s'.format('%.0f' % sleep))
        time.sleep(sleep)
