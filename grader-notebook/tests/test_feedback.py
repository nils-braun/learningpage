from unittest.mock import patch
import os
from subprocess import check_call

from nbgrader.coursedir import CourseDirectory
from nbgrader.api import Gradebook

from grading.utils import get_config
from grading.feedback import main
from grading.autograde import main as autograde_main
from tests.fixtures import TestCase


@patch("grading.feedback.get_ungraded_submissions")
@patch("grading.feedback.upload_feedback")
class FeedbackTestCase(TestCase):
    def test_no_submissions(self, upload_feedback, ungraded_submission):
        main()

    def test_not_autograded_submission(self, upload_feedback, ungraded_submission):
        check_call(["nbgrader", "generate_assignment", "assignment"])

        ungraded_submission.return_value = [
            {
                "slug": "submission",
                "assignment_slug": "assignment",
                "user": "testing",
                "notebooks": [{"slug": "notebook", "name": "name.ipynb"}],
            }
        ]

        main()

    @patch("grading.autograde.get_ungraded_submissions")
    @patch("grading.autograde.download_notebook")
    def test_single_submission(
        self,
        download_notebook,
        ungraded_submission_autograde,
        upload_feedback,
        ungraded_submission,
    ):
        check_call(["nbgrader", "generate_assignment", "assignment"])

        ungraded_submission.return_value = [
            {
                "slug": "submission",
                "assignment_slug": "assignment",
                "user": "testing",
                "notebooks": [{"slug": "notebook", "name": "name.ipynb"}],
            }
        ]

        ungraded_submission_autograde.return_value = ungraded_submission.return_value

        def download_mock(notebook_slug, download_location):
            with open(download_location, "w") as f:
                f.write(self.assignment_student)

        download_notebook.side_effect = download_mock

        autograde_main()

        main()

        c = get_config()

        coursedir = CourseDirectory(config=c)

        assert not os.path.exists(
            os.path.join(
                coursedir.format_path(
                    coursedir.autograded_directory, "submission", "assignment"
                ),
                "name.ipynb",
            )
        )

        feedback_file = os.path.join(
            coursedir.format_path(
                coursedir.feedback_directory, "submission", "assignment"
            ),
            "name.html",
        )
        assert not os.path.exists(feedback_file)

        upload_feedback.assert_called_once_with("notebook", feedback_file, 100.0, 100.0)

        # twice should not do anything
        upload_feedback.reset_mock()
        main()

        upload_feedback.assert_not_called()
