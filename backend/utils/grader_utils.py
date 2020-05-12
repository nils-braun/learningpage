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
    c = Config()
    c.CourseDirectory.course_id = "course"
    c.CourseDirectory.root = "/var/lib/content"
    c.CourseDirectory.db_url = os.environ.get('GRADER_DATABASE_STRING')

    return c

def _get_grader_app():
    # Create the nbgrader config "on the fly" out of the env variables
    c = get_config()

    grader_app = NbGrader(config=c)
    grader_app.initialize()
    grader_app.notebook_dir = "."

    return grader_app


def _get_grader_api():
    grader_app = _get_grader_app()
    api = NbGraderAPI(config=grader_app.config)

    return api


def _get_gradebook(c=None):
    if c is None:
        c = get_config()

    coursedir = CourseDirectory(config=c)
    return Gradebook(coursedir.db_url, coursedir.course_id)


def _run_app(app):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    app.log.addHandler(handler)

    app.start()

    app.log.removeHandler(handler)


def get_assignment(assignment_slug):
    api = _get_grader_api()
    return api.get_assignment(assignment_slug)


def _get_submission_from_db(student_slug, assignment_slug):
    c = get_config()
    with _get_gradebook(c) as gb:
        try:
            submission = gb.find_submission(assignment_slug, student_slug)

            if submission.needs_manual_grade:
                return

            return_dict = {
                "timestamp": submission.timestamp,
                "max_score": get_max_score_for(submission),
                "graded": True,
                "notebooks": [{
                    "id": notebook.id,
                    "name": notebook.name,
                    "max_score": get_max_score_for(notebook),
                } for notebook in submission.notebooks if not notebook.needs_manual_grade]
            }

            return return_dict
        except MissingEntry:
            return


def _get_submission_from_autograded_files(student_slug, assignment_slug):
    c = get_config()
    coursedir = CourseDirectory(config=c)
    api = _get_grader_api()
    assignment_dir = os.path.abspath(coursedir.format_path(coursedir.autograded_directory, student_slug, assignment_slug))
    notebooks = glob(os.path.join(assignment_dir, "*.ipynb"))

    if not os.path.exists(assignment_dir) or not notebooks:
        return

    with _get_gradebook(c) as gb:
        submission = gb.find_submission(assignment_slug, student_slug)
        timestamp = submission.timestamp

    return_dict = {
        "timestamp": timestamp,
        "max_score": None,
        "graded": False,
        "notebooks": [{
            "id": None,
            "name": notebook,
            "max_score": None,
        } for notebook in notebooks]
    }

    return return_dict


def _get_submission_from_submitted_files(student_slug, assignment_slug):
    c = get_config()
    coursedir = CourseDirectory(config=c)
    api = _get_grader_api()
    assignment_dir = os.path.abspath(coursedir.format_path(coursedir.submitted_directory, student_slug, assignment_slug))
    notebooks = glob(os.path.join(assignment_dir, "*.ipynb"))

    if not os.path.exists(assignment_dir) or not notebooks:
        return

    timestamp = api.get_submitted_timestamp(assignment_slug, student_slug)

    return_dict = {
        "timestamp": timestamp,
        "max_score": None,
        "graded": False,
        "notebooks": [{
            "id": None,
            "name": notebook,
            "max_score": None,
        } for notebook in notebooks]
    }

    return return_dict


def get_submissions(student_slug, assignment_slug):
    file_submission = _get_submission_from_submitted_files(student_slug, assignment_slug)

    if file_submission:
        return file_submission

    file_submission = _get_submission_from_autograded_files(student_slug, assignment_slug)

    if file_submission:
        return file_submission

    db_submission = _get_submission_from_db(student_slug, assignment_slug)
    return db_submission


def get_max_score(student_slug, assignment_slug):
    submission = get_submissions(student_slug, assignment_slug)
    if not submission:
        return

    return submission["max_score"]


def get_max_score_for(submission):
    if not submission:
        return

    max_score = float(submission.max_score)
    score = float(submission.score)

    if not max_score:
        return float("nan")

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
    def _run_app(app):
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        app.log.addHandler(handler)

        app.start()

        app.log.removeHandler(handler)

    c = get_config()
    c.CourseDirectory.assignment_id = assignment_slug
    c.CourseDirectory.student_id = student_slug
    c.Exchange.root = tempfile.mkdtemp()

    try:
        os.makedirs(c.Exchange.root, exist_ok=True)
        os.chmod(c.Exchange.root, 0o777)

        authenticator = Authenticator(config=c)
        coursedir = CourseDirectory(config=c)

        # Before that: assignment needs to be present in <course root>/release and in the database
        # e.g. by using generate_assignment

        # 1. Release assignment. We need to have it in the outbound folder, otherwise nbgrader can not match the assignment properly
        # Takes it from <course root>/release. Needs no database.
        # TODO: What should we do if we have different versions of it? We should make sure to have the correct assignment checked out!
        app = ExchangeReleaseAssignment(coursedir=coursedir, authenticator=authenticator, config=c)
        _run_app(app)
        # Works! Notebook copied into exchange/course/outbound

        # 2. Now store the incoming notebook in the exchange, as if the student would have submitted it
        # Takes the notebook from the input folder and stores it in the temporary exchange folder
        # Needs no database.
        # We need to cheat a bit to let nbgrader think, all notebooks are stored in "input"
        temporary_input_dir = os.path.join(c.Exchange.root, "temporary_input")
        os.makedirs(temporary_input_dir, exist_ok=True)
        for input_file in glob(os.path.join(input_folder, "*.ipynb")):
            if not os.path.isfile(input_file):
                continue

            copyfile(input_file, os.path.join(temporary_input_dir, os.path.basename(input_file)))

        class MyExchangeSubmit(ExchangeSubmit):
            def init_src(self):
                self.src_path = temporary_input_dir

        app = MyExchangeSubmit(coursedir=coursedir, authenticator=authenticator, config=c)
        _run_app(app)
        # Works! Copies to exchange/course/inbound/nils+..../*.ipynb
        # Attention: assignment needs to be present in exchange/course/outbound/

        # 3. Now collect the submitted notebooks
        # This means copy them to the <course root>/submitted folder.
        # This will replace anything which is already there!
        app = ExchangeCollect(coursedir=coursedir, authenticator=authenticator, config=c)
        app.update = True # we want to replace the already present one, if any
        app.check_owner = False # we will always commit with the flask user, so it is not a cheating attempt
        _run_app(app)
        # Works! Uses files in exchange/course/inbound/ and puts them into the database
        # But so far not in "submitted_assignment" table

        # Make sure we have an entry in the database.
        # We do this to show the user that submission was successful, but grader has not happened so far
        with _get_gradebook(c) as gb:
            gb.update_or_create_student(student_slug)
            gb.update_or_create_submission(assignment_slug, student_slug)

        # Now we have an entry in the database, but so far with maxScore = 0 (which means grading did not happen so far)
    finally:
        rmtree(c.Exchange.root)


def autograde(assignment_slug, student_slug):
    c = get_config()
    c.CourseDirectory.assignment_id = assignment_slug
    c.CourseDirectory.student_id = student_slug

    coursedir = CourseDirectory(config=c)

    # 4. Do the autograding
    # Use the input in <course root>/submitted and create a submission in the database
    # as well as store the results in the database. Will need to evaluate the notebook!
    # Needs database access.
    app = Autograde(coursedir=coursedir, config=c)
    app.force = True
    app.create_student = True
    _run_app(app)
    # Works! Does autograding, but feedback is not present so far


def generate_feedback(assignment_slug, student_slug):
    c = get_config()
    c.CourseDirectory.assignment_id = assignment_slug
    c.CourseDirectory.student_id = student_slug

    coursedir = CourseDirectory(config=c)

    # If manual grading is needed, we can not export it already!
    with _get_gradebook(c) as gb:
        submission = gb.find_submission(assignment_slug, student_slug)
        if submission.needs_manual_grade:
            return False

    # 5. Generate the feedback and make it visible to the student
    # Will use the grades stored in the database to create
    # a feedback.
    app = GenerateFeedback(coursedir=coursedir, config=c)
    app.force = True
    _run_app(app)
    # Works! Feedback present in content/feedback/..., (but not in exchange folder, where it is not needed)

    return True
