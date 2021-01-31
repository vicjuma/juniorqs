from flask import Blueprint, render_template

error = Blueprint('error', __name__, template_folder='../templates/errors')


@error.app_errorhandler(404)
def not_found(error):
    return render_template("errors/404.html"), 404


@error.app_errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html"), 403


@error.app_errorhandler(500)
def internal_server(error):
    return render_template("errors/500.html"), 500

