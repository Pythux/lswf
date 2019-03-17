#!/home/pythux/dev/venv/bin/python

import os
import sys
import time

from lib_scan_file_change import (
    working_dir, db_name, err_print, sql,
    TimeoutExpired)




if __name__ == "__main__":
    doc = """
        Detect the file and folder to cache, based on frequency of Write
    """
    import argparse
    parser = argparse.ArgumentParser(
        description=doc, formatter_class=argparse.RawTextHelpFormatter)

    args = parser.parse_args()

    if not os.path.isfile(os.path.join(working_dir, db_name)):
        err_print(working_dir + ' must be initialized, run init.py first')
        sys.exit(1)


    # check_dir()

# check dir first, then if file in dir

