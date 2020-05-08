import os

from nbgrader.apps import NbGrader
from nbgrader.api import Gradebook, MissingEntry
from nbgrader.apps.api import NbGraderAPI


def _get_grader_app():
    grader_app = NbGrader()
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


# with temp_attrs(self.coursedir, assignment_id=assignment_id, student_id=student_id):