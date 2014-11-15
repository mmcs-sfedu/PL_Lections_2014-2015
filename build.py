#!/usr/bin/env python3
# coding: utf8

import sys
import argparse

sys.path.append(sys.path[0] + '/scripts')
from project_rebuild import make_der_files, make_index, make_stream

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--refresh", action="store_true", help="refresh dictionary")
parser.add_argument("-p", "--public", action="store_true", help="public lectures")
args = parser.parse_args()


make_stream()

if args.public:
	make_der_files(args.refresh)
	make_index()