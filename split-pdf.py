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



# PDF file location
# Windows
# CDL_DIR = 'C:\\Users\\user\\Desktop\\CDL\\' 

# macOS for testing only
CDL_DIR = '/Users/leon/Desktop/'

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
with open(part_scheme, 'r', encoding='utf-8') as part:
    outlines = [chp.replace('\n', '').split('-') for chp in part.readlines()]

# get PDF reader obj
reader = pdf.PdfFileReader(orig_filedir)

# start splitting PDF based on the part_scheme
for page_range in outlines:
    # writer has good memory and will remember previouly-added pages
    # so each time writer needs to overriding
    writer = pdf.PdfFileWriter()

    # get suffix for chapter file name: XXX_chapter_1, XXX_chapter_2 ...
    # chapter_0 means TOC for now
    part_name = 'chapter' + '_' + str(outlines.index(page_range))

    # with a brand new (empty if you will) writer, start adding
    for page in range(int(page_range[0]), int(page_range[1])+1):
        writer.addPage(reader.getPage(page))


    # once got the partial PDF, save it to destination
    with open(DEST_DIR_STR + part_name, 'wb') as chp:
        writer.write(chp)

