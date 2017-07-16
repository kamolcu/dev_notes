# -*- coding: utf-8 -*-
import sys
import os
import glob
import argparse
import subprocess

def run(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    (ret, err) = p.communicate()

parser = argparse.ArgumentParser(
    description='Rename all files under a directory with specified expression.')
parser.add_argument('target_dir',
    help='Target directory full path e.g. /Users/[username]/. Noted that this script will NOT work recursively.'
)
parser.add_argument('file_type',
    help='File type to filter e.g. txt'
)
parser.add_argument('exp',
    nargs=1,
    help='Expression for search and replace delimit with # chars in format search#replace e.g. Int#Ext'
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
    output_dir = args.target_dir + '/rename_output/'
    if not os.path.exists(output_dir):
        run('mkdir -p ' + output_dir)
    for input_file_name in glob.glob('*.' + args.file_type):
        print('Processing file: ' + input_file_name)
        for key in exp_map.keys():
            target_file_name = input_file_name.replace(key, exp_map[key])
            break
        target_full_path = output_dir + target_file_name
        if os.path.exists(target_full_path):
            print('Found target file, so remove the target file first before the file rename')
            run('rm -f ' + target_full_path)
        run('cp ' + input_file_name + ' ' + target_full_path)

    print('End replacer script ...')
