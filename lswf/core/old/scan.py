import os
import sys
import time

from init import init_if_needed
from lib_scan_file_change import (
    err_print, sql,
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


def main(path, run_time, run_percent, timeout):
    init_if_needed()
    avoid_paths = ['/sys', '/proc', '/tmp', '/timeshift']

    change_since = 1  # in minutes
    scan_number = 0

    while True:
        running_time = 0  # noqa: F841
        start = time.time()
        big_scan(path, run_time=run_time,
                 run_percent=run_percent, timeout=timeout,
                 avoid_paths=avoid_paths, change_since=change_since)
        stop = time.time()
        delta = stop - start
        print('full scan in {}s'.format('%.1f' % delta))
        scan_number += 1
        sleep = min(50, scan_number * 2)
        print('wait before next full scan: {}s'.format('%.0f' % sleep))
        time.sleep(sleep)


if __name__ == "__main__":
    doc = """
        Scan thought all directory, don't go above mount point nor symlink
        research frequently create, update, delete in the filesystem
        (frequente modification)
    """
    import argparse
    parser = argparse.ArgumentParser(
        description=doc, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        "--root",
        help='define the root path to scan, "/" is the default value',
        default='/'
        )
    parser.add_argument(
        "--scan_speed",
        help='fast, medium, slow',
        default='fast',
        )
    args = parser.parse_args()

    if args.scan_speed not in ['fast', 'medium', 'slow']:
        err_print('option timeout > run_time, can\'t work, must be <=')
        sys.exit(1)
    mode = {
        'fast': [100, 5, 400],
        'medium': [60, 3, 5],
        'slow': [40, 2, 4],
    }
    run_percent, timeout, run_time = mode[args.scan_speed]
    main(args.root, run_time, run_percent, timeout)
