#!/usr/bin/env python3

import os
import json

from .bookmarks import get_bookmarks

HOME = os.environ.get('HOME')
BOPEN_ALIASES_PATH = os.environ.get('BOPEN_PATH', HOME + '/.bopenaliases')

def make_alias(bookmark, bopen_prefix='b-'):
    name, url= bookmark
    return 'alias {}{}="open {}"'.format(bopen_prefix, name, url)

def make_aliases(bookmarks, **kwargs):
    aliases = [make_alias(bookmark, **kwargs) for bookmark in bookmarks.items()]
    return aliases

def make_bopen_aliases_file(**kwargs):
    bookmarks = get_bookmarks(**kwargs)
    aliases = make_aliases(bookmarks, **kwargs)
    with open(BOPEN_ALIASES_PATH, 'w') as aliases_file:
        print('Aliases saved in {}'.format(BOPEN_ALIASES_PATH))
        contents = '\n'.join(aliases)
        aliases_file.write(contents)

