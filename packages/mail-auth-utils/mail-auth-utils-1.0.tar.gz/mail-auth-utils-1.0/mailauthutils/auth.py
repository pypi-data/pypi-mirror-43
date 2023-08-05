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

import base64
import logging

from typing import Union


def b64encode(auth: Union[str, bytes]) -> str:
    """Return the base64 encoded representation of a string."""
    if isinstance(auth, str):
        auth = auth.encode('utf8')
    return base64.encodebytes(auth).decode('utf8').strip()


def plain_auth(*args, prefix_null=True) -> str:
    """Generate a base64 encoded PLAIN SASL string, as described by RFC 4616.

    By default the encoded string will be prefixed with an initial NUL byte;
    use prefix_null=False to suppress this behavior.
    """
    authbytes = b'\x00'.join(arg.encode('utf8') for arg in args)
    if prefix_null:
        authbytes = b'\x00' + authbytes
    logging.debug('Raw PLAIN auth bytes %s', authbytes)
    return b64encode(authbytes)
