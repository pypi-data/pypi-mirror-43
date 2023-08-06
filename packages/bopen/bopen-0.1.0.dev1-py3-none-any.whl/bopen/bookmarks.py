import os
import json
import logging
from .os_helpers import MACOS, get_default_browser

BOOKMARKS_PATH = os.environ.get('BOOKMARKS_test', None)

class BookmarksNotFound(Exception):
    pass

class BookmarkNotFound(Exception):
    pass

HOME = os.getenv('HOME')
BOOKMARK_LOCATIONS = {
    'MACOS': {
        'brave': HOME + '/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks',
        'chrome': HOME + '/Library/Application Support/Google/Chrome/Default/Bookmarks'
    },
    'LINUX': {
        'chrome': HOME + '/.config/google-chrome/Default/Bookmarks',
        'chromium': HOME +'/.config/chromium/Default/Bookmarks'
    }
}

CHROMIUM_BROWSERS = ['brave', 'chrome', 'chromium']


def get_bookmarks(browser=None, **kwargs):
    browser = get_default_browser()
    logging.info('Browser: {}'.format(browser))
    print('Browser: {}'.format(browser))
    if browser in CHROMIUM_BROWSERS:
        return _get_chromium_bookmarks(browser=browser)


def _get_chromium_bookmarks(bookmarks_folder='bookmark_bar', browser=''):
    bookmarks_file_path = BOOKMARKS_PATH
    if bookmarks_file_path is None:
        if MACOS and browser:
            try:
                bookmarks_file_path = BOOKMARK_LOCATIONS['MACOS'][browser]
            except IndexError:
                logging.info('Can\'t find bookmarks file for {}. Consider setting the BOOKMARKS environment variable. (Chromium based only.)'.format(browser))
    with open(bookmarks_file_path) as bookmarks_file:
        bookmarks_data = json.load(bookmarks_file)
        bookmarks = {
            bookmark['name']: bookmark['url']
            for bookmark in bookmarks_data['roots'][bookmarks_folder]['children']
            if not bookmark['name'] == ''
        }
    return bookmarks


def get_url_from_bookmark(bookmark, **kwargs):
    bookmarks = get_bookmarks(**kwargs)
    if bookmark in bookmarks.keys():
        return bookmarks[bookmark]
    else:
        suggestion = '  ' + '\n  '.join(list(bookmarks.keys()))
        raise BookmarkNotFound('Couldn\'t find your bookmark. These are the ' +
                               'default browser bookmarks:\n{}'.format(suggestion))


if __name__ == '__main__':
    print(get_bookmarks())
