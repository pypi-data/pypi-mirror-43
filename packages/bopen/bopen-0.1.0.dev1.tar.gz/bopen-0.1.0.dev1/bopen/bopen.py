#!/usr/bin/env python3
import argparse
from .open_commands import open_bookmark, make_aliases_file

parser = argparse.ArgumentParser(prog='bopen', description='B[ookmark o]pen[er].')
parser.add_argument('bookmark_name', nargs='?', default=None)
parser.add_argument('--prefix', '-p', nargs='?', default=None)
parser.add_argument('--makealiases', '-m', action='store_true')

def main():
    opt = parser.parse_args()

    # Handle bookmark option
    if opt.bookmark_name:
        open_bookmark(opt.bookmark_name)

    # Handle makealiases option
    if opt.makealiases:
        # Handle prefix suboption
        if opt.prefix:
            make_aliases_file(bopen_prefix=opt.prefix)
        else:
            make_aliases_file()

if __name__ == '__main__':
    main()
