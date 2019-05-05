# shebang will automaticaly be set to the pip venv
import logging
import patcher
import tools
from datetime import timedelta

from lswf.core.init import ram_dir, disk_dir
import lswf.core.scan
import lswf.core.clean_scan
import lswf.core.show
import lswf.core.ram


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


def init_parser_clean(parser_clean):
    parser_clean.add_argument(
        "--hours",
        help='clean scanned data since X hours',
        type=int,
        default=1
        )
    parser_clean.set_defaults(func=app_clean)


def app_clean(args):
    lswf.core.clean_scan.del_older_than(timedelta(hours=args.hours))


def init_parser_load(parser_load):
    parser_load.set_defaults(func=app_load)


def app_load(_):
    patcher.load(ram_dir, disk_dir)


def init_parser_save(parser_save):
    parser_save.set_defaults(func=app_save)


def app_save(_):
    patcher.save(ram_dir, disk_dir)


def init_parser_show(parser_show):
    parser_show.add_argument(
        "--frequency",
        help='frequency to begin, default to 4',
        type=int,
        default=0,
        )
    parser_show.add_argument(
        "--limit",
        help='length limit to show, default to 10',
        type=int,
        default=10,
        )
    parser_show.set_defaults(func=app_show)


def app_show(args):
    lswf.core.show.print_frequently_modify_and_in_ram(
        args.frequency, args.limit)


def init_parser_ram(parser_ram):
    parser_ram.add_argument(
        "--out",
        help='put the path out of RAM',
        action='store_const',
        const=True, default=False
        )
    parser_ram.add_argument('path', metavar='PATH', nargs=1,
                            help='path to put in ram (file/directory)')
    parser_ram.set_defaults(func=app_ram)


def app_ram(args):
    abs_path = tools.path.to_absolute_path(args.path[0])
    if args.out:
        lswf.core.ram.out_path_from_ram(abs_path)
    else:
        lswf.core.ram.add_path_to_ram(abs_path)


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
    init_parser_clean(subparsers.add_parser('clean', help="clean old scan"))
    init_parser_load(subparsers.add_parser('load', help=doc_load))
    init_parser_save(subparsers.add_parser('save', help=doc_save))
    init_parser_show(subparsers.add_parser('show', help=doc_show))
    init_parser_ram(subparsers.add_parser('ram', help=doc_ram))

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
