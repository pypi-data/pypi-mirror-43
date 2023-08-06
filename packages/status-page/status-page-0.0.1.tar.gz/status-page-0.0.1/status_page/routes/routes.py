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

from status_page import app, db
from status_page.models.User import User
from status_page.utils.crypto import verify_password, generate_hash
from flask import render_template, redirect, request
from flask_login import login_required, current_user, login_user


@app.route("/")
def index():
    """
    The index/home page
    :return: The generated HTML
    """
    if current_user.is_authenticated:
        return redirect("display")
    elif len(User.query.all()) == 0:
        return redirect("init")
    else:
        return redirect("login")


@app.route("/init", methods=["GET", "POST"])
def init():
    """
    The initialization page
    :return: The generated HTML
    """
    if len(User.query.all()) != 0:
        return redirect("login")
    elif request.method == "GET":
        return render_template("init.html")
    else:
        data = request.form
        username = data["username"]
        email = data["email"]
        pw = data["password"]
        pw_repeat = data["password-repeat"]

        if pw != pw_repeat:
            return render_template("init.html")
        else:
            pw_hash = generate_hash(pw)
            user = User(
                id=1,
                username=username,
                email=email,
                password_hash=pw_hash
            )
            db.session.add(user)
            db.session.commit()
            return redirect("login")


@app.route("/login", methods=["GET"])
def login_page():
    """
    The login page
    :return: The generated HTML
    """
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    """
    Logs in the user
    :return: The generated HTML
    """
    data = request.form
    username = data["username"]
    password = data["password"]
    remember = data.get("remember_me") in ["on", True]

    user = User.query.filter_by(username=username).first()

    verified = False
    if user is not None:
        verified = verify_password(password, user.password_hash)

    if verified:
        login_user(user, remember=remember)
        return redirect("display")
    else:
        return redirect("login")


@app.route("/display")
@login_required
def display():
    """
    The main page of the application
    :return: The generated HTML
    """
    return render_template("display.html")
