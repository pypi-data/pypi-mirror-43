"""LICENSE
Copyright 2019 Hermann Krumrey <hermann@krumreyh.com>

This file is part of status-page.

status-page is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

status-page is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with status-page.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import bcrypt


def generate_hash(password: str or bytes) -> bytes:
    """
    Salts and hashes a password to generate a hash for storage in a database
    :param password: The password to hash
    :return: The hash of the password
    """

    if isinstance(password, str):
        password = bytes(password, "utf-8")

    return bcrypt.hashpw(password, bcrypt.gensalt())


def verify_password(password: str or bytes, hashed: str or bytes):
    """
    Verifies that a password matches a given hash
    :param password: The password to verify
    :param hashed: The hash to verify the password against
    :return: True if the password matches, otherwise False
    """

    if isinstance(password, str):
        password = bytes(password, "utf-8")
    if isinstance(hashed, str):
        hashed = bytes(hashed, "utf-8")

    try:
        return bcrypt.checkpw(password, hashed)
    except ValueError:
        return False
