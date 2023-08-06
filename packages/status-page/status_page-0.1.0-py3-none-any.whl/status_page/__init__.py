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

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
"""
The Flask App
"""

db = SQLAlchemy()
"""
The SQLAlchemy database connection
"""

login_manager = LoginManager(app)
"""
The Flask-Login Login Manager
"""

# Config
app.config["TRAP_HTTP_EXCEPTIONS"] = True
login_manager.session_protection = "strong"


if "FLASK_TESTING" in os.environ:  # pragma: no cover
    app.testing = os.environ["FLASK_TESTING"] == "1"
