#!/usr/bin/env python

import argparse
import os
import sys

from construct.core import ChecksumError
from keefind.keefinder import KeeFinder
from signal import signal, SIGPIPE, SIG_DFL  # noqa
signal(SIGPIPE, SIG_DFL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        help="Increase verbosity",
                        action='count')
    parser.add_argument('words', nargs='+', help="Word to search")
    args = parser.parse_args()
    try:
        kp_database = os.environ['KP_DATABASE']
        kp_password_file = os.environ['KP_PASSWORD_FILE']
    except KeyError:
        print('Export KP_DATABASE and KP_PASSWORD_FILE first')
        sys.exit(1)
    try:
        with open(kp_password_file, 'rt') as f:
            kp_password = f.readline().strip()
        finder = KeeFinder(kp_database, kp_password, args.verbose)
    except ChecksumError:
        print('Unable to decrypt database')
        sys.exit(1)
    except FileNotFoundError:
        print('Unable to find file with db password')
        sys.exit(1)
    except PermissionError:
        print('Unable to read file with db password: permission denied')
        sys.exit(1)
    finder.find(args.words)
    finder.print_found()


if __name__ == '__main__':
    main()
