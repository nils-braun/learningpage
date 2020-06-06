import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from utils.api_utils import PrefixMiddleware

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # all URLs will be prefixed with the jupyterhub hub URL
    prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX')
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=prefix)

    # lazy import to prevent cyclic dependencies
    from api.v1.views import blueprint
    app.register_blueprint(blueprint, url_prefix='/api/v1')

    # copy the environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CONTENT_DATABASE_STRING')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["USER_BASE_FOLDER"] = os.environ.get('USER_BASE_FOLDER')
    app.config["STORAGE_BASE_FOLDER"] = os.environ.get('STORAGE_BASE_FOLDER')
    app.config["GRADER_API_TOKEN"] = os.environ.get('GRADER_API_TOKEN')

    db.init_app(app)

    # lazy import to prevent cyclic dependencies
    from api.v1 import models
    migrate = Migrate(app, db)

    return app
