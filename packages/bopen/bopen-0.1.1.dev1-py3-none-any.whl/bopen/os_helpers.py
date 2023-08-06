import logging
import platform
import os
from shutil import which
from subprocess import run

MACOS = not platform.mac_ver() == ('', ('', '', ''), '')
CWD = os.getcwd()


def get_open_name():
    commands = ['xdg-open', 'open']
    for command in commands:
        if which(command) is not None:
            return command


def get_default_browser():
    try:
        if MACOS:
            logging.info('Macos: {}'.format(MACOS))
            print('Macos: {}'.format(MACOS))
            return _get_macos_default_browser()
        return _get_linux_default_browser()
    except Exception as e:
        logging.debug(e)
        logging.info('Couldn\'t get the default browser.')


def _get_linux_default_browser():
    with open('/usr/share/applications/defaults.list', 'r') as system_defaults:
        for line in system_defaults:
            if 'x-scheme-handler/http' in line:
                default_value = line.split('=')[1]
                if ';' in default_value:
                    return default_value.split(';')[0].strip('.desktop').lower()
                return default_value


def _get_macos_default_browser():
    command = """
    defaults read ~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist | awk -F '"' '/http;/{print window[(NR)-1]}{window[NR]=$2}'
    """
    return run(command, shell=True, capture_output=True, check=True).stdout.decode('utf-8').split('.')[1]
