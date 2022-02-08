# -*- coding: utf-8 -*-

from os import environ
from os.path import join
from pathlib import Path
from shutil import copyfile
import argparse

def args_processor():
    parser = argparse.ArgumentParser(description='A simple subtitles processor.')
    # directory containing src files
    parser.add_argument('--directory', '-d', action='store',
                        help='The directory name that is under the root dir and \
                        contains the target file (defaul: $HOME/YS)')
    # src filename
    parser.add_argument('src',
                        help='The source srt filename that contains blocks of \
                        timelines, without extention.')
    # start number
    parser.add_argument('start', default=0, type=int,
                        help='The start timeline block. A timeline block usually \
                        contains three parts: block number, timeline, caption \
                        (default: 0)')
    # end number
    parser.add_argument('end', default=0, type=int,
                        help='The end timeline block (default: 0)')
    # output filename
    parser.add_argument('--output', '-o', action='store',
                        default='src_en.txt', type=str, nargs='?',
                        help='Output filename, without extention (default: src_en)')
    args = parser.parse_args()

    # I only use this script on Windows.
    # For unix-like systems, it is 'HOME'
    ROOT_DIR = join(environ['USERPROFILE'], 'YS')

    if args.directory:
        dest_dir = join(ROOT_DIR, args.directory)
    else:
        dest_dir = ROOT_DIR

    if args.output != 'src_en.txt':
        trg_file = join(dest_dir, args.output.rstrip('.txt') + '_en.txt')
    else:
        trg_file = join(dest_dir, args.output)

    # srt --> txt, though this is unncessary
    # src_file = copyfile(join(dest_dir, args.src + '.srt'),
    #                     join(dest_dir, args.src.rstrip('.srt') + '.txt'))

    src_file = join(dest_dir, args.src + '.srt')
    startb = args.start
    endb = args.end

    return src_file, trg_file, startb, endb


def extract_timeline_blocks(srcf):
    with open(srcf, 'r', encoding='utf8') as f:
        raw = f.read()
        lines = [line for line in raw.split('\n\n') if len(line) > 1 ]
        return lines


def remove_timelines(trgf, lines, startbl, endbl):
    with open(trgf, 'w') as nf:
        for line in lines:
            txts = line.split('\n')
            if int(txts[0]) >= startbl and int(txts[0]) <= endbl:
                nf.write(txts[2] + '\n\n')


if __name__ == '__main__':
    src_file, trg_file, start_block, end_block = args_processor()
    lines = extract_timeline_blocks(src_file)
    remove_timelines(trg_file, lines, start_block, end_block)
    print('Done!')
