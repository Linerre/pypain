# -*- coding: utf-8 -*-
'''
This script will interweave English subtitles with their
corresponding Chinese translation, line by line. The output
is a txt file containing lines in the following format:
1. English line
2. Chinese Translation
3. [optional blank lines]
...
n. Another English line
n+1. Chinese translaton
...
EOF
'''

from os import environ
from os.path import join
from sys import platform
import argparse

def args_processor():
    if platform == "win32":
        ROOT = join(environ['USERPROFILE'], 'Desktop', 'YS')
    else:
        ROOT = join(environ['HOME'], 'Desktop', 'YS')

    parser = argparse.ArgumentParser(description='Make bilingual subtitles')

    # 1st arg: subtitles dir
    parser.add_argument('-d', '--directory',
                        help='The sub dir under ROOT, where subtitles.txt is stored')

    # 2nd arg: en.txt
    parser.add_argument('-s', '--source',
                        default='en',
                        help='The name of subtitles file, without extention. Default: en')

    # 3rd arg: cn.txt
    parser.add_argument('-t', '--target',
                        default='zh',
                        help='The name of target language file, without extention. Default: zh')
    args = parser.parse_args()

    working_dir = join(ROOT, args.directory)
    source_lang_file = join(working_dir, args.source) + '.txt'
    target_lang_file = join(working_dir, args.target) + '.txt'

    return working_dir, source_lang_file, target_lang_file


def interweave():
    working_dir, source_file_path, target_file_path = args_processor()

    # O(n)?
    with open(source_file_path, 'r', encoding='utf-8') as s:
        source_raw = s.readlines()
        source_content = [line.rstrip(' \r\n') for line in source_raw if line != '\n' or line !='\r\n']

    # O(n)?
    with open(target_file_path, 'r', encoding='utf-8') as t:
        target_raw = t.readlines()
        target_content = [line.rstrip(' \r\n') for line in target_raw if line != '\n' or line != '\r\n']

    src_ln_num = len(source_content)
    tge_ln_num = len(target_content)

    if (src_ln_num < tge_ln_num):
        print('Warning: The src and tge file have different numbers of lines!')
        print(f'Source and target files have {src_ln_num} and {tge_ln_num} lines separately.')
        # return src_ln_num if src_ln_num > tge_ln_num else tge_ln_num


    print("Start making bilingual scripts ...")
    # O(n)?
    bi_sub = '\n'.join([source_content[i] + '\n' + target_content[i] for i in range(len(source_content))])


    with open(join(working_dir, 'output.txt'), 'w', encoding='utf-8') as opt:
            opt.write(bi_sub)

    print("DONE!")


if __name__ == '__main__':
    interweave()
