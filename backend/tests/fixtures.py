import os
import tempfile
import shutil

from flask_testing import TestCase

from app import create_app, db


class BaseTestCase(TestCase):
    def create_app(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        os.chdir(self.tmpdir.name)

        os.makedirs("users")
        os.makedirs("storage")

        os.environ["CONTENT_DATABASE_STRING"] = f"sqlite:///database.db"
        os.environ["JUPYTERHUB_SERVICE_PREFIX"] = ""
        os.environ["USER_BASE_FOLDER"] = "users"
        os.environ["STORAGE_BASE_FOLDER"] = "storage"
        os.environ["GRADER_API_TOKEN"] = "grader"

        app = create_app()

        app.config["TESTING"] = True

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        shutil.rmtree(self.tmpdir.name)
