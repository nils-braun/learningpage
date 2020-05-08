from nbgrader.apps import NbGrader
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


def get_assignment(assignment_id):
    api = _get_grader_api()
    return api.get_assignment(assignment_id)


def get_submissions(student_id, assignment_id):
    api = _get_grader_api()

    return api.get_student_notebook_submissions(student_id, assignment_id)