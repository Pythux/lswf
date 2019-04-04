# shebang will automaticaly be set to the pip venv
import logging

import patcher

from lswf.core.init import ram_dir, disk_dir
import lswf.core.scan


def app_scan(args):
    mode = {
        'fast': [5, 0],
        'medium': [3, 2],
        'slow': [2, 8],
    }
    timeout, sleep_ratio = mode[args.speed]
    avoid_paths = []
    lswf.core.scan.main(args.path, timeout, sleep_ratio, avoid_paths)


def app_load(_):
    patcher.load(ram_dir, disk_dir)


def app_save(_):
    patcher.save(ram_dir, disk_dir)


def main():
    logging.basicConfig(level=logging.DEBUG)
    doc = """
        manage scan, caching in ram with symlink,
        autosave on hard disk, loading in ram at boot"""
    doc_scan = """
        search for frequente modification:
        Scan thought all directory, don't go above mount point nor symlink
        research frequently create, update, delete in the filesystem
    """
    doc_save = """save data in RAM with patcher (making diff)"""
    doc_load = """load data from store to RAM with patcher"""
    import argparse
    parser = argparse.ArgumentParser(
        description=doc, formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers()

    parser_scan = subparsers.add_parser('scan', help=doc_scan)

    parser_scan.add_argument(
        "--path",
        help='define the path to scan, "/" is the default value',
        default='/'
        )
    parser_scan.add_argument(
        "--speed",
        choices=['fast', 'medium', 'slow'],
        help='fast, medium, slow',
        default='medium',
        )
    parser_scan.set_defaults(func=app_scan)

    parser_load = subparsers.add_parser('load', help=doc_load)
    parser_load.set_defaults(func=app_load)

    parser_save = subparsers.add_parser('save', help=doc_save)
    parser_save.set_defaults(func=app_save)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
