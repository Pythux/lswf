# shebang will automaticaly be set to the pip venv
import logging

import patcher

from lswf.core.init import ram_dir, disk_dir
import lswf.core.scan
import lswf.core.list_frequence


def init_parser_scan(parser_scan):
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


def app_scan(args):
    mode = {
        'fast': [5, 0],
        'medium': [3, 2],
        'slow': [2, 8],
    }
    timeout, sleep_ratio = mode[args.speed]
    avoid_paths = []
    lswf.core.scan.main(args.path, timeout, sleep_ratio, avoid_paths)


def init_parser_load(parser_load):
    parser_load.set_defaults(func=app_load)


def app_load(_):
    patcher.load(ram_dir, disk_dir)


def init_parser_save(parser_save):
    parser_save.set_defaults(func=app_save)


def app_save(_):
    patcher.save(ram_dir, disk_dir)


def init_parser_frequency(parser_frequency):
    parser_frequency.add_argument(
        "--frequency",
        help='frequency to begin, default to 4',
        type=int,
        default=0,
        )
    parser_frequency.add_argument(
        "--limit",
        help='length limit to show, default to 10',
        type=int,
        default=10,
        )
    parser_frequency.set_defaults(func=app_list_frequently_modify)


def app_list_frequently_modify(args):
    lswf.core.list_frequence.print_frequently_modify_and_in_ram(
        args.frequency, args.limit)


def init_parser_ram(parser_ram):
    parser_ram.add_argument(
        "--out",
        help='the path must be in ram with this programme,'
        ' this action take it out of it',
        nargs='?',
        const=True, default=False
        )
    parser_ram.set_defaults(func=app_ram)


def app_ram(_):
    pass


def main():
    logging.basicConfig(level=logging.DEBUG)
    doc = """
        manage scan, caching in ram with symlink,
        autosave on hard disk, loading in ram at boot"""
    doc_scan = """search for frequente modification:
        Scan thought all directory, don't go above mount point nor symlink
        research frequently create, update, delete in the filesystem
    """
    doc_save = """save data in RAM with patcher (making diff)"""
    doc_load = """load data from store to RAM with patcher"""
    doc_show = "show frequently modified and already in RAM"
    doc_ram = "put file/directory in/out of RAM"
    import argparse
    parser = argparse.ArgumentParser(
        description=doc, formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers()

    init_parser_scan(subparsers.add_parser('scan', help=doc_scan))
    init_parser_load(subparsers.add_parser('load', help=doc_load))
    init_parser_save(subparsers.add_parser('save', help=doc_save))
    init_parser_frequency(subparsers.add_parser('show', help=doc_show))
    init_parser_ram(subparsers.add_parser('ram', help=doc_ram))

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
