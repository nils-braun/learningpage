from unittest import TestCase
from unittest.mock import patch
import tempfile
import os
import shutil
from subprocess import check_call

from nbgrader.coursedir import CourseDirectory
from nbgrader.api import Gradebook

from utils import get_config
from autograde import main


@patch("autograde.get_ungraded_submissions")
class AutogradeTestCase(TestCase):
    def setUp(self):
        self.assignment_source = open("grading/tests/source.ipynb").read()
        self.assignment_student = open("grading/tests/student.ipynb").read()
        self.assignment_autograded = open("grading/tests/autograded.ipynb").read()

        self.working_folder = tempfile.mkdtemp()
        self.old_pwd = os.getcwd()
        os.chdir(self.working_folder)

        with open("nbgrader_config.py", "w") as f:
            f.write(
                f"""
c = get_config()

c.CourseDirectory.course_id = "course"
c.CourseDirectory.root = "{self.working_folder}"
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

    def test_no_submissions(self, ungraded_submission):
        main()

    @patch("autograde.download_notebook")
    def test_single_submission(self, download_notebook, ungraded_submission):
        check_call(["nbgrader", "generate_assignment", "assignment"])

        ungraded_submission.return_value = [
            {
                "slug": "submission",
                "assignment_slug": "assignment",
                "notebooks": [{"slug": "notebook", "name": "name.ipynb"}],
            }
        ]

        def download_mock(notebook_slug, dowload_location):
            with open(dowload_location, "w") as f:
                f.write(self.assignment_student)

        download_notebook.side_effect = download_mock

        main()

        self.assertEqual(
            open("autograded/submission/assignment/name.ipynb").read(),
            self.assignment_autograded,
        )

        c = get_config()

        coursedir = CourseDirectory(config=c)

        with Gradebook(coursedir.db_url, coursedir.course_id) as gb:
            submission = gb.find_submission("assignment", "submission")
            assert not submission.needs_manual_grade

            self.assertEqual(len(submission.notebooks), 1)
            notebook = submission.notebooks[0]

            self.assertEqual(notebook.max_score, 100)
            self.assertEqual(notebook.score, 100)
