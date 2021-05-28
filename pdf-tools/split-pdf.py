# -*- encoding: utf-8 -*-

"""
Split PDF files into chapters;
each chapter as a single PDF file;
all chapters stored in a dir with the
name being the same as the original PDF.
"""

# standard libs
import os
import os.path
import sys
import argparse

# 3rd-party libs
import PyPDF2 as pdf

# os and user info for file path
os_name = sys.platform

# PDF files location
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
else: 
    # else it will be macOS or Linux
    CDL_ORIG_DIR = CDL_TARG_PARENT_DIR = os.path.join(os.environ['HOME'], 'Desktop')

# passing cmd line argvs
parser = argparse.ArgumentParser(description='Split a PDF file into parts based on a schema.txt file')

# 1st arg: original filename
parser.add_argument('filename', help='file name of the PDF to be splitted; double-quoted if name has spaces')
#orig_filename = str(sys.argv[1])

# 2rd arg: barcode
parser.add_argument('barcode', help='barcode of the item to be splitted')
#barcode = str(sys.argv[3]) + separator 

# 3rd arg: schema
parser.add_argument('schema', help='a txt file which describes how the pdf will be splitted')

# 4th arg: spliited part name: chapter, part, section
parser.add_argument('-p', '--part', default='chapter', choices=['chapter','secton','part'])
#args.schema = os.path.join(CDL_TARG_PARENT_DIR, str(sys.argv[2]))

args = parser.parse_args()
# let user decide which level shall be used, e.g.: chapter/section/part
#part_level = str(sys.argv[4])

# all splitted chapters will be stored in a target dir named like
# barcode_title under the CDL_TARG_PARENT_DIR
separator = '_'
orgi_file = os.path.join(CDL_ORIG_DIR, args.filename + '.pdf')
targ_file = args.barcode + separator + args.filename


# create target children dir for the title
os.mkdir(os.path.join(CDL_TARG_PARENT_DIR, targ_file))

# to use CDL_TARG_CHILDREN_DIR as a string as well
CDL_TARG_CHILDREN_DIR = os.path.join(CDL_TARG_PARENT_DIR, \
        targ_file)

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
with open(args.schema + '.txt', 'r', encoding='utf-8') as part:
     outlines = [sec.rstrip('\n').split(',')\
             for sec in part.readlines()\
             if sec != '\n']

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
    # in this particular case, sec[0] = 1,2,3, ...
    # if this is the case, then use whatever cmd arg passed: chapter/section/part ...
    elif sec[0].isdigit():
        #sec[0] = part_level + separator + sec[0]
        sec[0] = args.schema + separator + sec[0]
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
        sec[0] = 'introduction'
        integer_page(sec)
    elif sec[0] == 'g':
        sec[0] = 'glossary'
        integer_page(sec)
    else: 
        integer_page(sec)

# create PDF reader obj
reader = pdf.PdfFileReader(orgi_file)

# start splitting PDF based on the args.schema
for sec in outlines:
    # writer has good memory and will remember previouly-added pages
    # so each time writer needs overriding
    writer = pdf.PdfFileWriter()
    sec_name = sec[0]
    start_page = sec[1]
    until_page = sec[2]

    # set chapter file name string, e.g.: barcode_title_chapter_1.pdf
    part_name = targ_file + separator + sec_name + '.pdf'

    # with a brand new (empty if you will) writer, start adding
    # pages begin at 0 so below: page = real_page_num - 1
    # e.g: page = 58, then the real page num is 59
    # similary, pp.0 to x = (real) pp.1 to (x+1)
    # until_page is the last page of the current chp/sec in reality
    # A starting page must be given 
    # otherwise writer will always start at the first real page!
    for page in range(start_page - 1, until_page - 1):
        writer.addPage(reader.getPage(page))
    
    # update start_page to be used for the next loop
    # start_page = until_page
    # once got the partial PDF, save it to destination
    with open(os.path.join(CDL_TARG_CHILDREN_DIR, part_name), 'wb') as chp:
        writer.write(chp)

    print(f'{args.part} {sec} done.')


print('JOB DONE')
