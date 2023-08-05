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

from .cmd import new_parser, parse_args_and_password
from .auth import plain_auth, b64encode


def main():
    parser = new_parser('Generate an SMTP AUTH PLAIN (or LOGIN) string')
    parser.add_argument(
        '--auth-login',
        action='store_true',
        help='Output an AUTH LOGIN command (instead of AUTH PLAIN)')

    args, user, passwd = parse_args_and_password(parser)
    if args.auth_login:
        print('AUTH LOGIN')
        print(b64encode(user))
        print(b64encode(passwd))
    else:
        print('AUTH PLAIN {}'.format(plain_auth(user, passwd)))
