from unittest.mock import patch
import os
from subprocess import check_call

from nbgrader.coursedir import CourseDirectory
from nbgrader.api import Gradebook

from grading.utils import get_config
from grading.autograde import main
from tests.fixtures import TestCase


@patch("grading.autograde.get_ungraded_submissions")
class AutogradeTestCase(TestCase):
    def test_no_submissions(self, ungraded_submission):
        main()

    @patch("grading.autograde.download_notebook")
    def test_single_submission(self, download_notebook, ungraded_submission):
        check_call(["nbgrader", "generate_assignment", "assignment"])

        ungraded_submission.return_value = [
            {
                "slug": "submission",
                "assignment_slug": "assignment",
                "user": "testing",
                "notebooks": [{"slug": "notebook", "name": "name.ipynb"}],
            }
        ]

        def download_mock(notebook_slug, download_location):
            with open(download_location, "w") as f:
                f.write(self.assignment_student)

        download_notebook.side_effect = download_mock

        main()

        c = get_config()

        coursedir = CourseDirectory(config=c)

        assert os.path.exists(
            os.path.join(
                coursedir.format_path(
                    coursedir.autograded_directory, "submission", "assignment"
                ),
                "name.ipynb",
            )
        )

        with Gradebook(coursedir.db_url, coursedir.course_id) as gb:
            submission = gb.find_submission("assignment", "submission")
            assert not submission.needs_manual_grade

            self.assertEqual(len(submission.notebooks), 1)
            notebook = submission.notebooks[0]

            self.assertEqual(notebook.max_score, 100)
            self.assertEqual(notebook.score, 100)

        # Calling it twice should not change the grades
        with patch("grading.autograde.autograde") as autograde_patch:
            main()
            autograde_patch.assert_not_called()
