# -*- coding: utf-8 -*-
'''
This script is created solely for one task:
to replace '@' mark with two '\n's in a *.txt
which holds the subtitles of a youtube video.
'''

from os import environ
from os.path import join
import argparse


def args_processor():
    ROOT = join(environ['USERPROFILE'], 'YS')
    parser = argparse.ArgumentParser(description='Reformat the subtitles with new linebreaks')

    # 1st arg: subtitles dir
    parser.add_argument('-c', '--catagory',
                        help='The sub dir under ROOT, where subtitles.txt is stored')

    # 2nd arg: subtitles.txt
    parser.add_argument('-s', '--subtitles',
                        help='The name of subtitles file, without extention')

    args = parser.parse_args()

    target_dir = join(ROOT, args.catagory)
    subtitles_file = join(target_dir, args.subtitles) + '.txt'

    return target_dir, subtitles_file


def new_linebreaks():
    target_dir, file_path = args_processor()

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()
        # remove the whitespaces and newline at the end of each line
        content = [line.rstrip(' \n') for line in content if line != '\n']
        content = ' '.join(content)
        content = content.replace('@', '\n\n')

    with open(join(target_dir, 'output.txt'), 'w', encoding='utf-8') as opt:
            opt.write(content)


if __name__ == '__main__':
    new_linebreaks()
