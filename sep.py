#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from sys import argv
script, filename = argv

cn_marks = r'，|：|“|”|·|、|——'

with open(filename, 'r+', encoding='utf-8', errors = 'ignore') as f:
    content = f.read()
    cn_swap = re.sub(cn_marks, ' ', content)
    cn_sent = re.findall('[\u4e00-\u9fff0-9A-Za-z( )\[\]]+[。？!]', cn_swap)
    # “\u4e00-\u9fff0-9A-Za-z( )” can get strings with quotes like “你好”

    swap = content.replace('." ', '."\n')
    p_swap = swap.replace('. ', '.\n')
    q_swap = p_swap.replace('? ', '?\n')
    e_swap = q_swap.replace('! ', '?\n')
    en_sent = re.findall(r'[A-Z""].*[\!\."\?]', e_swap)

    cn_en = list(zip(cn_sent, en_sent))

    for cn, en in cn_en:
        f.write(en+'\n'+cn+'\n')

print('cn_sent contains: ', len(cn_sent), 'sentences.')
print('en_sent contains: ', len(en_sent), 'sentences.')