from unittest import TestCase
import tempfile
import os
import shutil


class TestCase(TestCase):
    def setUp(self):
        test_dir = os.path.dirname(__file__)
        self.assignment_source = open(os.path.join(test_dir, "source.ipynb")).read()
        self.assignment_student = open(os.path.join(test_dir, "student.ipynb")).read()

        self.working_folder = tempfile.mkdtemp()
        self.old_pwd = os.getcwd()
        os.chdir(self.working_folder)

        with open("nbgrader_config.py", "w") as f:
            f.write(
                f"""
c = get_config()

c.CourseDirectory.db_url = "sqlite:///database.db"
                """
            )

        # Prepare assignments in database
        os.makedirs("source/assignment")
        with open("source/assignment/name.ipynb", "w") as f:
            f.write(self.assignment_source)

        super().setUp()

    def tearDown(self):
        os.chdir(self.old_pwd)

        shutil.rmtree(self.working_folder)

        super().tearDown()
