# -*- coding:utf-8 -*-
import re

marks_sub = r'\!( |\n)?|\?( |\n)?|\.( |\n)?|？|。'
marks_rem = r'“|”|，|：'
en_sen = r'.*?[\!( )?\?( )?\.( )?]$'

cn_tran = re.sub(marks_rem, ' ', string4) # remove undesired marks

en_mo = set(re.findall(marks_sub, string4)) # get all would-be-replaceds without duplicates

print(cn_tran)
print('\n\n')
print(en_mo)
print('\n')

en_tran = cn_tran

for p in en_mo:
    tran = en_tran.split(p) # get a list
    en_tran = (p+'\n').join(tran) # get a string
    result = en_tran

raw_result = result.replace('。', '')

print(raw_result)

# -*- coding:utf-8 -*-


import re

marks_sub = r'\!( |\n)?|\?( |\n)?|\.( |\n)?|？|。'
marks_rem = r'“|”|，|：'
en_sen = r'.*?[\!( )?\?( )?\.( )?]$'

import os
base_path = 'C:\\Users\\zl37\\Desktop\\Pscript\\'
filename = 'tryout.txt'
path_to_file = os.path.join(base_path, filename)

with open(path_to_file, 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)
