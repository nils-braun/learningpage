import os
import tempfile
import logging
import sys
from shutil import rmtree
from traitlets.config.loader import Config

from nbgrader.exchange import ExchangeReleaseAssignment, ExchangeCollect, ExchangeSubmit
from nbgrader.converters import Autograde, GenerateFeedback
from nbgrader.coursedir import CourseDirectory
from nbgrader.auth import Authenticator

from nbgrader.apps import NbGrader
from nbgrader.api import Gradebook, MissingEntry
from nbgrader.apps.api import NbGraderAPI


def _get_grader_app():
    # Create the nbgrader config "on the fly" out of the env variables
    c = Config()
    c.CourseDirectory.course_id = "course"
    c.CourseDirectory.root = "/var/lib/content"
    c.CourseDirectory.db_url = os.environ.get('GRADER_DATABASE_STRING')

    grader_app = NbGrader(config=c)
    grader_app.initialize()
    grader_app.notebook_dir = "."

    return grader_app


def _get_grader_api():
    grader_app = _get_grader_app()
    api = NbGraderAPI(config=grader_app.config)

    return api


def _get_gradebook():
    grader_app = _get_grader_app()
    coursedir = grader_app.coursedir
    return Gradebook(coursedir.db_url, coursedir.course_id)


def get_assignment(assignment_slug):
    api = _get_grader_api()
    return api.get_assignment(assignment_slug)


def get_submissions(student_slug, assignment_slug):
    with _get_gradebook() as gb:
        try:
            submission = gb.find_submission(assignment_slug, student_slug)
            notebooks = [notebook.to_dict() for notebook in submission.notebooks]

            return_dict = submission.to_dict()
            return_dict["notebooks"] = notebooks

            return return_dict
        except MissingEntry:
            return {}


def get_max_score(student_slug, assignment_slug):
    submissions = get_submissions(student_slug, assignment_slug)
    return get_max_score_for(submissions)


def get_max_score_for(submission):
    if not submission:
        return

    if submission["needs_manual_grade"]:
        return

    max_score = float(submission["max_score"])
    score = float(submission["score"])

    return score / max_score


def get_submitted_notebook(notebook_id):
    with _get_gradebook() as gb:
        try:
            notebook = gb.find_submission_notebook_by_id(notebook_id)
            return_dict = notebook.to_dict()
            return_dict["assignment_slug"] = notebook.assignment.name
            return return_dict
        except MissingEntry:
            return {}


def get_feedback_path(student_slug, assignment_slug, notebook_name):
    grader_app = _get_grader_app()
    coursedir = grader_app.coursedir

    feedback_folder = coursedir.format_path(coursedir.feedback_directory, student_slug, assignment_slug)
    feedback_path = os.path.join(feedback_folder, notebook_name + ".html")

    if os.path.exists(feedback_path):
        return feedback_path


def submit(input_folder, assignment_slug, student_slug):
    def run(app):
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        app.log.addHandler(handler)

        app.start()

        app.log.removeHandler(handler)

    c = Config()
    c.CourseDirectory.course_id = "course"
    c.CourseDirectory.root = "/var/lib/content"
    c.CourseDirectory.assignment_id = assignment_slug
    c.CourseDirectory.student_id = student_slug
    c.Exchange.root = tempfile.mkdtemp()
    c.CourseDirectory.db_url = os.environ.get('GRADER_DATABASE_STRING')

    try:
        os.makedirs(c.Exchange.root, exist_ok=True)
        os.chmod(c.Exchange.root, 0o777)

        authenticator = Authenticator(config=c)
        coursedir = CourseDirectory(config=c)

        # TODO: what to do if the assignment has multiple notebooks? test that!

        # 1. Release assignment. We need to have it in the outbound folder, otherwise nbgrader can not match the assignment properly
        # TODO: What should we do if we have different versions of it? We should make sure to have the correct assignment checked out!
        app = ExchangeReleaseAssignment(coursedir=coursedir, authenticator=authenticator, config=c)
        run(app)
        # Works! Notebook copied into exchange/course/outbound

        # 2. Now store the incoming notebook in the exchange, as if the student would have submitted it
        # We need to cheat a bit to let nbgrader think, all notebooks are stored in "input"
        class MyExchangeSubmit(ExchangeSubmit):
            def init_src(self):
                self.src_path = os.path.abspath(input_folder)

        app = MyExchangeSubmit(coursedir=coursedir, authenticator=authenticator, config=c)
        run(app)
        # Works! Copies to exchange/course/inbound/nils+..../*.ipynb
        # Attention: assignment needs to be present in exchange/course/outbound/

        # 3. Now collect the submitted notebooks (will be only one)
        app = ExchangeCollect(coursedir=coursedir, authenticator=authenticator, config=c)
        app.update = True # we want to replace the already present one, if any
        app.check_owner = False # we will always commit with the flask user, so it is not a cheating attempt
        run(app)
        # Works! Uses files in exchange/course/inbound/ and puts them into the database
        # But so far not in "submitted_assignment" table

        # 4. Do the autograding
        app = Autograde(coursedir=coursedir, config=c)
        app.force = True
        app.create_student = True
        run(app)
        # Works! Does autograding, but feedback is not present so far

        # TODO: what to do if manual grading is needed?

        # 5. Generate the feedback and make it visible to the student
        app = GenerateFeedback(coursedir=coursedir, config=c)
        app.force = True
        run(app)
        # Works! Feedback present in content/feedback/..., (but not in exchange folder, where it is not needed)

    finally:
        rmtree(c.Exchange.root)