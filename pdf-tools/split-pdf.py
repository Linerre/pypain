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
parser.add_argument('schema', 
                    nargs='?',
                    default=join(abspath('.'), 'schema-example.txt'),
                    help='a txt file which describes how the pdf will be splitted; with extension')

# 4th arg: offset 
parser.add_argument('offset', 
                    nargs='?',
                    default=0,
                    help='Offset between the first printed page number and the page\
                          number shown in the PDF viewer.')

# 5th arg: spliited part name: chapter, part, section
parser.add_argument('-p', '--part', 
                    metavar='chapter|section|part', 
                    nargs='?',
                    const='chapter',
                    default='chapter',
                    choices=['chapter', 'section', 'part'],
                    help='Set part name; defaults to chapter.')

args = parser.parse_args()

# all splitted chapters will be stored in a target dir named like
# barcode_title under the CDL_TARG_PARENT_DIR
separator = '_'
orgi_file = join(CDL_ORIG_DIR, args.filename)
targ_file = args.barcode + separator + args.filename
offset = int(args.offset)


# create target children dir for the title
if not exists(join(CDL_TARG_PARENT_DIR, targ_file[:-4])):
    mkdir(join(CDL_TARG_PARENT_DIR, targ_file[:-4]))

# to use CDL_TARG_CHILDREN_DIR as a string as well
CDL_TARG_CHILDREN_DIR = join(CDL_TARG_PARENT_DIR, targ_file[:-4])

# get the page ranges for each part, e.g:
# pages begin at 0 according to
# https://pythonhosted.org/PyPDF2/PdfFileReader.html#PyPDF2.PdfFileReader.getPage
# ONLY needs two elements: part notation and start page
# However, for the last part, the end page of the file is required
# [
#   [t,1]	---TOC(t)
#   [1,10]	---chapter1(1)
#   [2,21]	---chapter2(2)
#   ...
#   [10,80]	---chapter10(10)
#   [i,100, 105] ---index(i)
# ]

# using 1,2,3,4 ... to represent chapters simply because
# it is convenient to name a chapter_X file later
# such page ranges are stored in a txt file
with open(args.schema, 'r', encoding='utf-8') as part:
    toc = [sec.rstrip('\n').split(',')
                for sec in part.readlines()
                if sec != '\n']

# Raise Except early if the end page of the last part is missing!
try:
    if len(toc[-1]) != 3:
        print('End page of the last part is missing!')
        raise IndexError
except IndexError:
    raise SystemExit('List index will be out of range due to missing the last page number.')


# pre-process elements in outlines:
# 1st, use offset to get start, end page
def get_start_end(outlines, offset):
    for i in range(len(outlines)):
        # for the first part, its start page should always be 1
        if i == 0:
            outlines[i].append(int(outlines[i+1][1]) - 1 + offset)

        # then calibre start page, end page for all, except the last part
        if i > 0 and i < len(outlines) - 1:
            # each element has two children elemnts
            # the start page is the second element in the list, hence index 1
            # for the ith part, its end page should be calibred as such:
            # the (i+1)th part's start page - 1, and then plus offset
            # its start page should be added offset
            outlines[i][1] = int(outlines[i][1]) + offset
            outlines[i].append(int(outlines[i+1][1]) - 1 + offset) 

        # start page of the last part needs to be added offset
        if i == len(outlines) - 1:
            outlines[i][1] = int(outlines[i][1]) + offset

get_start_end(toc, offset)

# 2nd, use case to replace keys with their values
# e.g. : t-->toc; 1-->chapter_1; i-->index
# also turn all page_nums into integers (they are strs from input file)
def prepare_schema(sec_list):
    # Use dict as switch syntax
    keys = {
        'A': 'Appendix-1',
        'B': 'Appendix-2',
        'C': 'Appendix-3',
        'D': 'Appendix-4',
        'E': 'Appendix-5',
        'a': 'appendix',
        'b': 'bibliography',
        'e': 'epilogue',
        'g': 'glossary',
        'i': 'index',
        'n': 'notes',
        'o': 'introduction',
        'p': 'preface',
        'r': 'references',
        't': 'TOC',
           }
    if sec_list[0].isdigit():
        sec_list[0] = args.part + separator + sec_list[0]
    else:
        sec_list[0] = keys[sec_list[0]]
    sec_list[1] = int(sec_list[1])
    sec_list[2] = int(sec_list[2])

# create PDF reader obj
reader = pdf.PdfFileReader(orgi_file)

# start splitting PDF based on the args.schema
for sec in toc:
    prepare_schema(sec)
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
    # NOTE: until_page should not be deducted because Python's range
    # does not include the end!
    # until_page is the last page of the current chp/sec in reality
    # A starting page must be given
    # otherwise writer will always start at the first real page!
    for page in range(start_page - 1, until_page):
        writer.addPage(reader.getPage(page))

    # update start_page to be used for the next loop
    # start_page = until_page
    # once got the partial PDF, save it to destination
    with open(join(CDL_TARG_CHILDREN_DIR, part_name), 'wb') as chp:
        writer.write(chp)

    # TODO: consider rjust or ljust the output
    print(f'{args.part} {sec} done.')


print('THE PDF HAS BEEN SPLITTED')
