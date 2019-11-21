#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from sys import argv
script, filename = argv

cwd = os.getcwd()
origin = 'para'   # the transcripts folder
subt   = 'line'   # the subtitles folder
filename = 'testsub.txt'

cn_marks = r'，|：|“|”|·|、|——'

# open the original files in para dir
# separate the paras (en-cn) to lines (cn - en)
# put the new content in a file with the same name
# but into a different dir line

with open(os.path.join(cwd, origin, filename), 'r+', encoding='utf-8', errors = 'ignore') as f:
    content = f.read()
    cn_swap = re.sub(cn_marks, ' ', content)
    cn_sent = re.findall('[\u4e00-\u9fff0-9A-Za-z( )\[\]]+[。？!]', cn_swap)
    # “\u4e00-\u9fff0-9A-Za-z( )” can get strings with quotes like “你好”

    # replace cn punctuations with en ones
    swap = content.replace('." ', '."\n')
    p_swap = swap.replace('. ', '.\n')
    q_swap = p_swap.replace('? ', '?\n')
    e_swap = q_swap.replace('! ', '?\n')
    en_sent = re.findall(r'[A-Z""].*[\!\."\?]', e_swap)

    cn_en = list(zip(cn_sent, en_sent))

with open(os.path.join(cwd, subt, filename), 'w', encoding='utf-8', errors = 'ignore') as fnew:
    for cn, en in cn_en:
        fnew.write(cn+'\n'+en+'\n')

print('cn_sent contains: ', len(cn_sent), 'sentences.')
print('en_sent contains: ', len(en_sent), 'sentences.')

# this is the final working code
# need to handle the 'U.S.' issue
# need to get rid of [Name: words.] first
