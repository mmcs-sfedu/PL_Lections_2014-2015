#!/usr/bin/python
# coding: utf8

import sys
import argparse

sys.path.append(sys.path[0] + '/scripts')
from project_rebuild import make_der_files, make_index

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--refresh", action="store_true", help="refresh dictionary")
args = parser.parse_args()

make_der_files(args.refresh)
make_index()