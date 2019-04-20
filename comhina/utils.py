# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import current_app, flash, g, request

from comhina.extensions import babel


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config["LANGUAGES"])
