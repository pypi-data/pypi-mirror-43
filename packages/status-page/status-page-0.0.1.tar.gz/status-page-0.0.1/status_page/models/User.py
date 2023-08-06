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

from status_page import db
from status_page.utils.crypto import verify_password


class User(db.Model):
    """
    Model that describes the 'users' SQL table
    A User stores a user's information, including their email address, username
    and password hash
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the Model
        :param args: The constructor arguments
        :param kwargs: The constructor keyword arguments
        """
        super().__init__(*args, **kwargs)

    __tablename__ = "users"
    """
    The name of the table
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID is the primary key of the table and increments automatically
    """

    username = db.Column(db.String(12), nullable=False, unique=True)
    """
    The user's username
    """

    email = db.Column(db.String(150), nullable=False, unique=True)
    """
    The user's email address
    """

    password_hash = db.Column(db.String(255), nullable=False)
    """
    The user's hashed password, salted and hashed.
    """

    @property
    def is_authenticated(self) -> bool:
        """
        Property required by flask-login
        :return: True if the user is confirmed, False otherwise
        """
        return True

    @property
    def is_anonymous(self) -> bool:
        """
        Property required by flask-login
        :return: True if the user is not confirmed, False otherwise
        """
        return not self.is_authenticated  # pragma: no cover

    @property
    def is_active(self) -> bool:
        """
        Property required by flask-login
        :return: True
        """
        return True

    def get_id(self) -> str:
        """
        Method required by flask-login
        :return: The user's ID as a unicode string
        """
        return str(self.id)

    def verify_password(self, password: str) -> bool:
        """
        Verifies a password against the password hash
        :param password: The password to check
        :return: True if the password matches, False otherwise
        """
        return verify_password(password, self.password_hash)
