import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from utils import PrefixMiddleware


prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX')
content_database_string = os.environ.get('CONTENT_DATABASE_STRING')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=prefix)

    from api.v1.views import blueprint
    app.register_blueprint(blueprint, url_prefix='/api/v1')

    app.config['SQLALCHEMY_DATABASE_URI'] = content_database_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from api.v1 import models
    migrate = Migrate(app, db)

    return app