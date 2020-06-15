import os
import logging
import sys
import shutil
from contextlib import contextmanager

import requests

from nbgrader.converters import Autograde, GenerateFeedback
from nbgrader.coursedir import CourseDirectory

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
    grader_app.initialize(argv=[])
    grader_app.notebook_dir = "."  # TODO: needed?

    return grader_app.config


def _run_app(app):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    app.log.addHandler(handler)

    app.start()

    app.log.removeHandler(handler)


def autograde(assignment_slug, student_slug, user):
    c = get_config()
    c.CourseDirectory.assignment_id = assignment_slug
    c.CourseDirectory.student_id = student_slug

    coursedir = CourseDirectory(config=c)

    with Gradebook(coursedir.db_url, coursedir.course_id) as gb:
        # Store the submission in the database
        gb.update_or_create_student(student_slug, last_name=user)

        try:
            # If there is already an entry, do not continue
            gb.find_submission(assignment_slug, student_slug)
            return
        except MissingEntry:
            pass

        gb.update_or_create_submission(assignment_slug, student_slug)

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
        try:
            submission = gb.find_submission(assignment_slug, student_slug)
        except MissingEntry:
            # no submission in the database? Ok, autograding has not happened so far
            return

        if submission.needs_manual_grade:
            print(
                f"Not creating feedback for {assignment_slug} - {student_slug} as it needs manual grading."
            )
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


def get_ungraded_submissions():
    api_token = os.environ.get("GRADER_API_TOKEN")
    rv = requests.get(
        "http://jupyterhub:8000/services/learningpage/api/v1/ungraded",
        headers={"Authorization": f"token {api_token}"},
    )
    rv.raise_for_status()
    ungraded_submissions = rv.json()

    return ungraded_submissions


def download_notebook(notebook_slug, dowload_location):
    api_token = os.environ.get("GRADER_API_TOKEN")
    rv = requests.get(
        f"http://jupyterhub:8000/services/learningpage/api/v1/notebook/{notebook_slug}",
        headers={"Authorization": f"token {api_token}"},
    )

    with open(dowload_location, "wb") as f:
        f.write(rv.content)


def upload_feedback(notebook_slug, feedback_file, score, max_score):
    api_token = os.environ.get("GRADER_API_TOKEN")
    rv = requests.post(
        f"http://jupyterhub:8000/services/learningpage/api/v1/feedback/{notebook_slug}",
        headers={"Authorization": f"token {api_token}"},
        data={"score": score, "max_score": max_score},
        files={"feedback": open(feedback_file, "r").read()},
    )
    rv.raise_for_status()


@contextmanager
def created_folder(nbgrader_folder):
    os.makedirs(nbgrader_folder, exist_ok=True)

    try:
        yield
    finally:
        shutil.rmtree(nbgrader_folder)
