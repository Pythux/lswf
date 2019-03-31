import os
import bsdiff4
from tools.path import to_absolute_path
# from lswf.database import db, SymLink


def test_bsdiff4():
    with open(to_absolute_path('~/dev/test_diff/yo'), 'rb') as src:
        s = src.read()
    with open(to_absolute_path('~/dev/test_diff/new_yo'), 'rb') as dst:
        d = dst.read()

    print(s, d)
    print(bsdiff4.diff(s, d))
    print(bsdiff4.patch(s, bsdiff4.diff(s, d)) == d)
