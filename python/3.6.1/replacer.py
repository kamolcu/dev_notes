# -*- coding: utf-8 -*-
import sys
import os
import glob
import argparse


parser = argparse.ArgumentParser(
    description='Replace all files under a directory with specified expression.')
parser.add_argument('target_dir',
    help='Target directory full path e.g. /Users/[username]/. Noted that this script will NOT work recursively.'
)
parser.add_argument('file_type',
    help='File type to filter e.g. txt'
)
parser.add_argument('exp',
    nargs='+',
    help='Expression for search and replace delimit with # chars in format search#replace e.g. int.#ext.'
)

args = parser.parse_args()

if __name__ == '__main__':
    print('Start replacer script ...')
    if not os.path.exists(args.target_dir):
        sys.exit('Failed to locate ' + args.target_dir)
    exp_map = {}
    for item in args.exp:
        [search, replace] = item.split('#')
        exp_map[search] = replace
    print(exp_map)
    os.chdir(args.target_dir)
    for input_file_name in glob.glob('*.' + args.file_type):
        print('Processing file: ' + input_file_name)
        file_content = ''
        with open(input_file_name, 'r') as target_file:
            file_content = target_file.read()
        for key in exp_map.keys():
            file_content = file_content.replace(key, exp_map[key])
        with open(input_file_name, 'w') as target_file:
            target_file.write(file_content)

    print('End replacer script ...')
