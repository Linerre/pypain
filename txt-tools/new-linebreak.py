# -*- coding: utf-8 -*-
'''
This script is created solely for one task:
to replace '@' mark with two '\n's in a *.txt
which holds the subtitles of a youtube video.
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

    parser = argparse.ArgumentParser(description='Reformat the subtitles with new linebreaks')

    # 1st arg: subtitles dir
    parser.add_argument('-d', '--directory',
                        help='The sub dir under ROOT, where subtitles.txt is stored')

    # 2nd arg: subtitles.txt
    parser.add_argument('-s', '--subtitles',
                        help='The name of subtitles file, without extention')

    #TODO:
    # 3rd arg: delimiter = or \, just something that can be typed in directly without Shift
    args = parser.parse_args()

    target_dir = join(ROOT, args.directory)
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

    with open(join(target_dir, 'en.txt'), 'w', encoding='utf-8') as opt:
            opt.write(content)


if __name__ == '__main__':
    print("Start breaking lines ...")
    new_linebreaks()
    print("Done!")
