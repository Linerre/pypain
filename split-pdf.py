# -*- encoding: utf-8 -*-

"""
Split PDF files into chapters;
each chapter as a single PDF file;
all chapters stored in a dir with the
name being the same as the original PDF.
"""

import PyPDF2 as pdf
import os
import sys
import getpass


# os and user info for file path
os_name = sys.platform
user_name = getpass.getuser()
# PDF file location
if os_name.startswith('win32'):
    # Windows
    CDL_DIR = f'C:\\Users\\{user_name}\\Desktop\\CDL\\' 
elif os_name.startswith('darwin'):
    # macOS for testing only
    CDL_DIR = f'/Users/{user_name}/Desktop/'
elif os_name.startswith('linux'):
    CDL_DIR = f'/home/{user_name}/Document/'

# passing cmd line argvs
orig_filename = str(sys.argv[1])
orig_filedir = CDL_DIR + orig_filename
part_scheme = CDL_DIR + str(sys.argv[2])
barcode = str(sys.argv[3]) + '_'
DEST_DIR = os.mkdir(CDL_DIR + barcode + orig_filename.replace('.pdf', '/'))
DEST_DIR_STR = CDL_DIR + barcode + orig_filename.replace('.pdf', '/')

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
# only the up-to page number is needed, e.g:
# [
#   10	---TOC
#   11	---chapter1
#   27	---chapter2
#   ...
#   99	---chapter10
# ]
# such page nums stored in a txt file
with open(part_scheme, 'r', encoding='utf-8') as part:
     outlines = [int(chp.replace('\n','')) for chp in part.readlines()]


# create PDF reader obj
reader = pdf.PdfFileReader(orig_filedir)

# start splitting PDF based on the part_scheme
# A starting page must be given otherwise writer will start at first page!
start_page = 0
for until_page in outlines:
    # writer has good memory and will remember previouly-added pages
    # so each time writer needs to overriding
    writer = pdf.PdfFileWriter()

    # get suffix for chapter file name: XXX_chapter_1, XXX_chapter_2 ...
    # chapter_0 means TOC for now
    part_name = orig_filename.replace('.pdf', '') \
            + '_chapter_' \
            + str(outlines.index(until_page))

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
    with open(DEST_DIR_STR + part_name + '.pdf', 'wb') as chp:
        writer.write(chp)


print('JOB DONE')
