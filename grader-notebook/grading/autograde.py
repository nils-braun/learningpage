import os
from glob import glob
import shutil
from contextlib import contextmanager

import requests

from nbgrader.apps import NbGraderApp
from nbgrader.coursedir import CourseDirectory

from utils import autograde, get_config


def get_ungraded_submissions():
    api_token = os.environ.get("GRADER_API_TOKEN")
    rv = requests.get("http://jupyterhub:8000/services/learningpage/api/v1/ungraded",
                      headers={"Authorization": f"token {api_token}"})
    rv.raise_for_status()
    ungraded_submissions = rv.json()

    return ungraded_submissions


def download_notebook(notebook_slug, dowload_location):
    api_token = os.environ.get("GRADER_API_TOKEN")
    rv = requests.get(f"http://jupyterhub:8000/services/learningpage/api/v1/notebook/{notebook_slug}",
                      headers={"Authorization": f"token {api_token}"})

    with open(dowload_location, "wb") as f:
        f.write(rv.content)


@contextmanager
def created_folder(nbgrader_folder):
    os.makedirs(nbgrader_folder)

    try:
        yield
    except:
        shutil.rmtree(nbgrader_folder)
        raise

def main():
    ungraded_submissions = get_ungraded_submissions()

    c = get_config()
    coursedir = CourseDirectory(config=c)

    for submission in ungraded_submissions:
        submission_slug = submission["slug"]
        assignment_slug = submission["assignment_slug"]

        # We choose the submission slug as the user -> TODO test if this is fine
        nbgrader_folder = coursedir.format_path(coursedir.submitted_directory, submission_slug, assignment_slug)

        if os.path.exists(nbgrader_folder):
            return

        with created_folder(nbgrader_folder):
            for submitted_file in submission["notebooks"]:
                download_notebook(submitted_file["slug"], os.path.join(nbgrader_folder, submitted_file["name"]))

            autograde(assignment_slug, submission_slug)


if __name__ == "__main__":
    main()