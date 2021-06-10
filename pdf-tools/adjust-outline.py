# -*- coding: utf-8 -*-

"""
This script will adjust a PDF file's real pages based on the offset.
For example, real pages start at 23 where the pagination just starts,
so the offset will be counted as 23 - 1 = 22.
"""

import argparse
import os.path
import sys

# parser accepts 2 command line args: offset path to the PDF
parser = argparse.ArgumentParser(
        description='Generate a scheme file using the offset cmd line arg.',
        prog='scheme-gen')

# 1st arg: offset
parser.add_argument('offset', default=0,
                    help='Pagination offset.\
                    Usually it is the digital page number minus the real one.')
parser.add_argument('-p', '--pdf', const=None, default=None,
                    help='The absolute path to the PDF file for which a scheme\
                    is going to be generated. If omitted, then an empty scheme\
                    file will be created under the current direcotory and user\
                    will be notified by a message to stdout.')

parser.parse_args()
