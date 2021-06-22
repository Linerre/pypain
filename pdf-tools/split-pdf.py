# -*- encoding: utf-8 -*-

"""
Split PDF files into chapters;
Each chapter as a single PDF file;
All chapters stored in a dir named after
The original PDF's filename.
"""

# standard libs
from os import environ, name, mkdir
from os.path import abspath, exists, join
import argparse

# 3rd-party libs
import PyPDF2 as pdf

# os and user info for file path

# PDF files location
if name == 'nt':
    # Windows
    # original root/parent dir for PDF files
    CDL_ORIG_DIR = join(environ['USERPROFILE'],
                                'Desktop',
                                'New Arrival')
    # target root/parent dir for splitted files
    CDL_TARG_PARENT_DIR = join(environ['USERPROFILE'],
                                       'Desktop',
                                       'CDL')
elif name == 'posix':
    # else it will be macOS or Linux
    CDL_ORIG_DIR = CDL_TARG_PARENT_DIR = join(environ['HOME'], 'Desktop')

# passing cmd line argvs
parser = argparse.ArgumentParser(description='Split a PDF file into parts based on a schema.txt file')

# 1st arg: original filename
parser.add_argument('filename', help='file name with the PDF extension; double-quoted if name has spaces')

# 2rd arg: barcode
parser.add_argument('barcode', help='barcode of the item to be splitted')

# 3rd arg: schema, defaults to the schema-example.txt under the same dir as this script
parser.add_argument('schema', nargs='?',
                    default=join(abspath('.'), 'schema-example.txt'),
                    help='a txt file which describes how the pdf will be splitted')

# 4th arg: spliited part name: chapter, part, section
parser.add_argument('-p', '--part', default='chapter',
                    choices=['chapter', 'section', 'part'])

args = parser.parse_args()

# all splitted chapters will be stored in a target dir named like
# barcode_title under the CDL_TARG_PARENT_DIR
separator = '_'
orgi_file = join(CDL_ORIG_DIR, args.filename)
targ_file = args.barcode + separator + args.filename


# create target children dir for the title
if not exists(join(CDL_TARG_PARENT_DIR, targ_file[:-4])):
    mkdir(join(CDL_TARG_PARENT_DIR, targ_file[:-4]))

# to use CDL_TARG_CHILDREN_DIR as a string as well
CDL_TARG_CHILDREN_DIR = join(CDL_TARG_PARENT_DIR, targ_file[:-4])

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
with open(args.schema, 'r', encoding='utf-8') as part:
    outlines = [sec.rstrip('\n').split(',')
                for sec in part.readlines()
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
    # if this is the case, then use whatever cmd arg passed: chapter/section/part
    elif sec[0].isdigit():
        sec[0] = args.part + separator + sec[0]
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
    sec_name = sec[0]
    start_page = sec[1]
    until_page = sec[2]

    # set chapter file name string, e.g.: barcode_title_chapter_1.pdf
    part_name = targ_file[:-4] + separator + sec_name + '.pdf'

    # writer has good memory and will remember previouly-added pages
    # so each time writer needs overriding
    writer = pdf.PdfFileWriter()


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
    with open(join(CDL_TARG_CHILDREN_DIR, part_name), 'wb') as chp:
        writer.write(chp)

    # TODO: consider rjust or ljust the output
    print(f'{args.part} {sec} done.')


print('THE PDF HAS BEEN SPLITTED')
