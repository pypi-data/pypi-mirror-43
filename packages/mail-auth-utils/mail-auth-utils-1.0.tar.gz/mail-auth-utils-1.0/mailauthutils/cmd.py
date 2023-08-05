# Copyright (C) 2019  Evan Klitzke <evan@eklitzke.org>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import getpass
import logging
import os

from typing import Tuple


def new_parser(description: str) -> argparse.ArgumentParser:
    """Create a new ArgumentParser with a set of default arguments."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-p',
        '--password',
        default='',
        help='Password to use for authentication')
    parser.add_argument(
        '-v',
        '--verbose',
        help='Log debugging information',
        action='store_true')
    parser.add_argument('user', nargs='?')
    return parser


def _default_user() -> str:
    """Select a default username."""
    mailenv = os.environ.get('MAIL')
    if mailenv:
        return mailenv
    return getpass.getuser()


def parse_args_and_password(parser: argparse.ArgumentParser
                            ) -> Tuple[argparse.Namespace, str, str]:
    """Parse options and return the args, username, and password.

    If a password was not supplied on the command line, the user will be
    prompted for a password using the getpass module for secure password entry.
    """
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(levelname)s: %(message)s')

    user = args.user
    if not user:
        user = _default_user()
        logging.info('Using default username %s', user)

    passwd = args.password
    if not passwd:
        passwd = getpass.getpass('Password for remote user {}: '.format(user))

    return args, user, passwd
