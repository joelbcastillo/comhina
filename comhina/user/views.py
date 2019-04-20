# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, g, render_template
from flask_login import login_required

blueprint = Blueprint(
    "user", __name__, url_prefix="/<locale>/users", static_folder="../static"
)


@blueprint.url_defaults
def add_locale(endpoint, values):
    values.setdefault("locale", g.locale)


@blueprint.url_value_preprocessor
def remove_locale(endpoint, values):
    g.locale = values.pop("locale")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")
