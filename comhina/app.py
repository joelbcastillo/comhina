# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import abort, Flask, g, request, render_template

from comhina import commands, public, user
from comhina.extensions import (
    babel,
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    login_manager,
    migrate,
    moment,
    webpack,
)


def create_app(config_object="comhina.settings"):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    @app.url_defaults
    def set_language_code(endpoint, values):
        if "lang_code" in values or not g.get("lang_code", None):
            return
        if app.url_map.is_endpoint_expecting(endpoint, "lang_code"):
            values["lang_code"] = g.lang_code

    @app.url_value_preprocessor
    def get_lang_code(endpoint, values):
        if values is not None:
            g.lang_code = values.pop("lang_code", None)

    @app.before_request
    def ensure_lang_support():
        lang_code = g.get("lang_code", None)
        if lang_code and lang_code not in app.config["LANGUAGES"]:
            return abort(404)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    babel.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    webpack.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(public.views.blueprint, url_prefix="/<lang_code>/")
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(user.views.blueprint, url_prefix="/<lang_code>/user")
    return None


def register_errorhandlers(app):
    """Register error handlers."""  # noqa: D202

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""  # noqa: D202

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.translate)
