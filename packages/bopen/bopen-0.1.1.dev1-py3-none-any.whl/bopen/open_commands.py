from subprocess import run
from .os_helpers import get_open_name
from .bookmarks import get_url_from_bookmark
from .make_aliases import make_bopen_aliases_file


def _open_url(url):
    try:
        open_command = get_open_name()
        run('{} {}'.format(open_command, url).split())
    except Exception as error:
        print(str(error))


def open_bookmark(bookmark_name, **kwargs):
    try:
        _open_url(get_url_from_bookmark(bookmark_name, **kwargs), **kwargs)
    except Exception as error:
        print(str(error))


def make_aliases_file(**kwargs):
    try:
        make_bopen_aliases_file(**kwargs)
    except Exception as error:
        print(str(error))


def main():
    bookmark_name = input('Bookmark: ')
    open_bookmark(bookmark_name)


if __name__ == '__main__':
    main()
