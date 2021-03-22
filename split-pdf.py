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
    # original root/parent dir for PDF files
    CDL_ORIG_DIR = os.path.join(os.environ['USERPROFILE'], \
                                'Dropbox', \
                                'Han - NYU')
    # target root/parent dir for splitted files
    CDL_TARG_PARENT_DIR = os.path.join(os.environ['USERPROFILE'], \
                                'Desktop', \
                                'CDL')
elif os_name.startswith('darwin'):
    # macOS for testing only
    CDL_DIR = os.path.join(os.environ['HOME'], 'Desktop')

# passing cmd line argvs
orig_filename = str(sys.argv[1])
orig_filedir = os.path.join(CDL_ORIG_DIR, orig_filename)
part_scheme = os.path.join(CDL_TARG_PARENT_DIR, str(sys.argv[2]))
separator = '_'
barcode = str(sys.argv[3]) + separator 
# all splitted chapters will be stored in a dir named like
# barcode_title under the CDL_TARG_PARENT_DIR
targ_filedir = barcode + orig_filename.strip('.pdf')


# create target children dir for the title
# os.mkdir returns none type but create it anyway since I need it
CDL_TARG_CHILDREN_DIR = os.mkdir(os.path.join(CDL_TARG_PARENT_DIR, \
        targ_filedir))
# to use CDL_TARG_CHILDREN_DIR as a string as well
CDL_TARG_CHILDREN_DIR_STR = os.path.join(CDL_TARG_PARENT_DIR, \
        targ_filedir)

# get the page ranges for each part, e.g:
# pages begin at 0 according to 
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
# also turn all page_nums into integers (they are strs from input file)
def integer_page(sec_list):
    sec_list[1] = int(sec_list[1])
    sec_list[2] = int(sec_list[2])
for sec in outlines:
    # I miss the swtich/case statement in C so much:
    if sec[0] == 't':
        sec[0] = 'TOC'
        integer_page(sec)
    elif sec[0].isdigit():
        sec[0] = 'chapter' + separator + sec[0]
        integer_page(sec)
    elif sec[0] == 's':
        # make sure first part always directly follows toc
        sec[0] = 'part' + separator + str(outlines.index(sec))
        integer_page(sec)
    elif sec[0] == 'i':
        sec[0] = 'index'
        integer_page(sec)
    elif sec[0] == 'r':
        sec[0] = 'reference'
        integer_page(sec)
    elif sec[0] == 'n':
        sec[0] = 'notes'
        integer_page(sec)
    elif sec[0] == 'b':
        sec[0] = 'bibliography'
        integer_page(sec)
    elif sec[0] == 'p':
        sec[0] = 'preface'
        integer_page(sec)
    elif sec[0] == 'o':
        sec[0] = 'introdcution'
        integer_page(sec)

# create PDF reader obj
reader = pdf.PdfFileReader(orig_filedir)

# start splitting PDF based on the part_scheme
for sec in outlines:
    # writer has good memory and will remember previouly-added pages
    # so each time writer needs overriding
    writer = pdf.PdfFileWriter()
    sec_name = sec[0]
    start_page = sec[1]
    until_page = sec[2]

    # set chapter file name string, e.g.: barcode_title_chapter_1.pdf
    part_name = targ_filedir + separator + sec_name + '.pdf'

    # with a brand new (empty if you will) writer, start adding
    # pages begin at 0 so below: page = real_page_num - 1
    # e.g: page = 58, then the real page num is 59
    # similary, pp.0 to x = (real) pp.1 to (x+1)
    # until_page is the last page of the current chp/sec in reality
    # A starting page must be given 
    # otherwise writer will always start at first page!
    for page in range(start_page - 1, until_page - 1):
        writer.addPage(reader.getPage(page))
    
    # update start_page to be used for the next loop
    start_page = until_page
    # once got the partial PDF, save it to destination
    with open(os.path.join(CDL_TARG_CHILDREN_DIR_STR, part_name), 'wb') as chp:
        writer.write(chp)

    print(f'Section/Part/Chapter {sec} done.')


print('JOB DONE')
