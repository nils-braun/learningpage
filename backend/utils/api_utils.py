import os
from functools import wraps
import hashlib

from flask import request, current_app
from jupyterhub.services.auth import HubAuth
from werkzeug import exceptions


auth = HubAuth(api_token=os.environ.get("JUPYTERHUB_API_TOKEN", ""), cache_max_age=60,)


def authenticated(f):
    """Decorator for authenticating with the Hub"""

    @wraps(f)
    def decorated(*args, **kwargs):
        cookie = request.cookies.get(auth.cookie_name)
        token = request.headers.get(auth.auth_header_name)

        if current_app.config.get("TESTING"):
            user = {
                "admin": False,
                "created": "created",
                "last_activity": "last_activity",
                "name": "testing",
            }
        elif cookie:
            user = auth.user_for_cookie(cookie)
        elif token:
            user = auth.user_for_token(token)
        else:
            raise exceptions.Unauthorized(description="No cookie or token supplied.")
        if not user:
            raise exceptions.Forbidden(description="Invalid cookie or token supplied.")

        return f(user, *args, **kwargs)

    return decorated


def is_grader(f):
    """Decorator to check if the grader API token is set"""

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise exceptions.Unauthorized(description="No token supplied.")

        try:
            _, token = auth_header.split(" ")
        except ValueError:
            raise exceptions.Unauthorized(description="Invalid token supplied.")

        if token != current_app.config.get("GRADER_API_TOKEN"):
            raise exceptions.Forbidden(description="Invalid token supplied.")

        return f(*args, **kwargs)

    return decorated


class PrefixMiddleware(object):
    # from https://stackoverflow.com/questions/18967441/add-a-prefix-to-all-flask-routes
    def __init__(self, app, prefix=""):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ["PATH_INFO"].startswith(self.prefix):
            environ["PATH_INFO"] = environ["PATH_INFO"][len(self.prefix) :]
            environ["SCRIPT_NAME"] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response("404", [("Content-Type", "text/plain")])
            return ["This url does not belong to the app.".encode()]


def get_user_assignment_folder(student_slug, assignment_slug):
    base_folder = current_app.config.get("USER_BASE_FOLDER")
    user_folder = os.path.join(base_folder, student_slug, assignment_slug)

    return os.path.abspath(user_folder)


def get_storage_folder(submission_slug, assignment_slug):
    base_folder = current_app.config.get("STORAGE_BASE_FOLDER")
    storage_folder = os.path.join(base_folder, submission_slug, assignment_slug)

    return os.path.abspath(storage_folder)


def slugify(*args):
    return hashlib.md5("_".join(map(str, args)).encode()).hexdigest()[:32]
