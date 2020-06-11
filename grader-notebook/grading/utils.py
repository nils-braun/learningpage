import os
import tempfile
import logging
import sys
from shutil import rmtree, copyfile
from traitlets.config.loader import Config
from glob import glob

from nbgrader.exchange import ExchangeReleaseAssignment, ExchangeCollect, ExchangeSubmit
from nbgrader.converters import Autograde, GenerateFeedback
from nbgrader.coursedir import CourseDirectory
from nbgrader.auth import Authenticator

from nbgrader.apps import NbGrader
from nbgrader.api import Gradebook, MissingEntry
from nbgrader.apps.api import NbGraderAPI


def get_config():
    """
    Return the current nbgrader config.

    To not duplicate code, create a temporary instance
    of the nbgrader application and use its config.
    """
    grader_app = NbGrader()
    grader_app.initialize()
    grader_app.notebook_dir = "." # TODO: needed?

    return grader_app.config


def _run_app(app):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    app.log.addHandler(handler)

    app.start()

    app.log.removeHandler(handler)


def autograde(assignment_slug, student_slug):
    c = get_config()
    c.CourseDirectory.assignment_id = assignment_slug
    c.CourseDirectory.student_id = student_slug

    coursedir = CourseDirectory(config=c)

    with Gradebook(coursedir.db_url, coursedir.course_id) as gb:
        # Store the submission in the database

        # TODO: add name etc.?
        gb.update_or_create_student(student_slug)
        gb.update_or_create_submission(assignment_slug, student_slug)

        # TODO: can we find out if grading already happened?
        # can we then skip this part?

    # Use the input in <course root>/submitted for the given assignment and studen
    # and create a submission in the database as well as store the results in the database.
    # Will need to evaluate the notebook! Needs database access.
    app = Autograde(coursedir=coursedir, config=c)
    app.force = True
    app.create_student = True
    _run_app(app)

    # After that, the autograding is performed, but feedback is not present already


def generate_feedback(assignment_slug, student_slug):
    c = get_config()
    c.CourseDirectory.assignment_id = assignment_slug
    c.CourseDirectory.student_id = student_slug

    coursedir = CourseDirectory(config=c)

    # If manual grading is needed, we can not export it already!
    with Gradebook(coursedir.db_url, coursedir.course_id) as gb:
        submission = gb.find_submission(assignment_slug, student_slug)
        if submission.needs_manual_grade:
            print(f"Not creating feedback for {assignment_slug} - {student_slug} as it needs manual grading.")
            return

    # Generate the feedback and store it in the folder
    #
    # Will use the grades stored in the database to create
    # a feedback.
    app = GenerateFeedback(coursedir=coursedir, config=c)
    app.force = True
    _run_app(app)

    # Works! Feedback present in content/feedback/...,

    with Gradebook(coursedir.db_url, coursedir.course_id) as gb:
        submission = gb.find_submission(assignment_slug, student_slug)

        submission_dict = submission.to_dict()
        submission_dict["notebooks"] = [n.to_dict() for n in submission.notebooks]

        return submission_dict
