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

import pkg_resources
from typing import Optional
from status_page.routes import load_routes
from status_page import app, db, login_manager
from status_page.models.User import User


def initialize_app():
    """
    Initializes the App
    :return: None
    """
    @app.context_processor
    def inject_template_variables():
        """
        Injects the project's version string so that it will be available
        in templates
        :return: The dictionary to inject
        """
        version = \
            pkg_resources.get_distribution("status-page").version
        return {
            "version": version,
            "env": app.env
        }

    load_routes()


# noinspection PyUnresolvedReferences
def initialize_db(db_uri: str):
    """
    Initializes the SQLAlchemy database
    :param db_uri: The URI of the database to initialize
    :return: None
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from status_page.models.User import User

    with app.app_context():
        db.create_all()


def initialize_login_manager():
    """
    Initializes the login manager
    :return: None
    """
    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        """
        Loads a user from an ID
        :param user_id: The ID
        :return: The User
        """
        return User.query.get(int(user_id))
