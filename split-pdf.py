# -*- encoding: utf-8 -*-

"""
Split PDF files into chapters;
each chapter as a single PDF file;
all chapters stored in a dir with the
name being the same as the original PDF.
"""

import PyPDF2 as pdf
import os
import os.path
import sys


# os and user info for file path
os_name = sys.platform
# PDF file location
if os_name.startswith('win32'):
    # Windows
    CDL_DIR = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'CDL')
elif os_name.startswith('darwin'):
    # macOS for testing only
    CDL_DIR = os.path.join(os.environ['HOME'], 'Desktop/')

# passing cmd line argvs
orig_filename = str(sys.argv[1])
orig_filedir = os.path.join(CDL_DIR + orig_filename)
part_scheme = os.path.join(CDL_DIR + str(sys.argv[2]))
barcode = str(sys.argv[3]) + '_'


# os.mkdir returns none type but create it anyway since I need it
DEST_DIR = os.mkdir(CDL_DIR + barcode + orig_filename.replace('.pdf', ''))
# to use DEST_DIR as a string, concate them using os.path.join
DEST_DIR_STR = os.path.join(CDL_DIR \
        + barcode \
        + orig_filename.replace('.pdf', '/'))

# get the page ranges for each part, e.g:
# [
#   [1,10]	---TOC
#   [11,26]	---chapter1
#   [27,48]	---chapter2
#   ...
#   [99, 105]	---chapter10
# ]
# with open(part_scheme, 'r', encoding='utf-8') as part:
#     outlines = [chp.replace('\n', '').split('-') for chp in part.readlines()]

# since pages begin at 0 according to 
# https://pythonhosted.org/PyPDF2/PdfFileReader.html#PyPDF2.PdfFileReader.getPage
# [
#   [t,1,10]	---TOC(t)
#   [1,10,20]	---chapter1(1)
#   [2,21,27]	---chapter2(2)
#   ...
#   [10,80,99]	---chapter10(10)
#   [i,100,106] ---index(i)
# ]

# using 1,2,3,4 ... to represent chapters simply because
# it is convenient to name a chapter_X file later
# such page ranges are stored in a txt file
with open(part_scheme, 'r', encoding='utf-8') as part:
     outlines = [sec.strip('\n').split(',') for sec in part.readlines()]

# pre-process some elements in outlines:
# e.g. : t-->toc; 1--> chapter_1; i-->index
def integer_page(sec_list):
    sec_list[1] = int(sec_list[1])
    sec_list[1] = int(sec_list[1])
for sec in outlines:
    # I miss the swtich/case statement in C so much:
    if sec[0] == 't':
        sec[0] = 'toc'
        integer_page(sec)
    elif sec[0].isdigit():
        sec[0] = '_chapter_' + sec[0]
        integer_page(sec)
    elif sec[0] == 'i':
        sec[0] = '_index'
        integer_page(sec)
    elif sec[0] == 'r':
        sec[0] = '_reference'
        integer_page(sec)
    elif sec[0] == 'n':
        sec[0] = '_notes'
        integer_page(sec)
    elif sec[0] == 'b':
        sec[0] = '_bibliography'
        integer_page(sec)
    elif sec[0] == 'p':
        sec[0] = '_preface'
        integer_page(sec)
    elif sec[0] == 'o':
        sec[0] = '_introdcution'
        integer_page(sec)

# create PDF reader obj
reader = pdf.PdfFileReader(orig_filedir)

# start splitting PDF based on the part_scheme
# A starting page must be given otherwise writer will start at first page!
start_page = 0
for until_page in outlines:
    # writer has good memory and will remember previouly-added pages
    # so each time writer needs overriding
    writer = pdf.PdfFileWriter()

    # get suffix for chapter file name: XXX_chapter_1, XXX_chapter_2 ...
    # chapter_0 means TOC for now
    part_name = orig_filename.replace('.pdf', '') \
            + '_chapter_' \
            + str(outlines.index(until_page)) \
            + '.pdf'

    # with a brand new (empty if you will) writer, start adding
    # pages begin at 0 so below: page = real_page_num - 1
    # e.g: page = 58, then the real page num is 59
    # similary, pp.0 to x = (real) pp.1 to (x+1)
    # until_page is the first page of the next chp/sec in reality
    for page in range(start_page, until_page - 1):
        writer.addPage(reader.getPage(page))
    
    # update start_page to be used for the next loop
    start_page = until_page - 1
    # once got the partial PDF, save it to destination
    with open(os.path.join(DEST_DIR_STR + part_name), 'wb') as chp:
        writer.write(chp)


print('JOB DONE')
