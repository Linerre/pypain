# -*- coding: utf-8 -*-

"""
This script will rename chapter PDFs in a batch
within the same folder. It requires one command
line argv, which is the barcode of the book.
Input: 
    <scriptname> <barcode> <book_title>
Output: 
    <barcode>_chapter_X.pdf
    <barcode>_<book_title>  # dir name also changed
"""

import sys
import os

# root dir
parent = os.path.join(os.environ['USERPROFILE'], 'Desktop')
print(f'Changes will be made to {parent}\'s sub dir.')

# get barcode and book title from cmd line
barcode = str(sys.argv[1])
title = str(sys.argv[2])
prefix = barcode + '_'

try:
    # enter CDL dir
    os.chdir(parent)
    
    # first change book dir name
    os.rename(title, prefix + title)

    # update title 
    title = prefix + title
    print('Book tile dir renamed to: ', title)
    print()
    # enter the book dir
    os.chdir(parent + title)
    print(f'Entered {title} dir')
    print()
    # get all the chapters in an unordred list
    chapters = os.listdir()
    print('Got all chapter names: ')
    print(chapters)
    print()

    # loop through them and modify their names 
    print('Start renameing chapters ...')
    for chapter in chapters:
        os.rename(chapter, prefix + chapter)

    print('Renaming done!', 'Going back to parent dir ...')

    # cd to the parent dir
    os.chdir('..\\')
    print('JOB DONE')
except:
    print('Oops, sth wrong!')

