import os
from shutil import rmtree

import requests
from nbgrader.coursedir import CourseDirectory

from grading.utils import (
    generate_feedback,
    get_config,
    get_ungraded_submissions,
    upload_feedback,
    created_folder,
)


def main():
    ungraded_submissions = get_ungraded_submissions()

    c = get_config()
    coursedir = CourseDirectory(config=c)

    for submission in ungraded_submissions:
        submission_slug = submission["slug"]
        assignment_slug = submission["assignment_slug"]

        # We choose the submission slug as the user
        nbgrader_folder = coursedir.format_path(
            coursedir.feedback_directory, submission_slug, assignment_slug
        )

        autograder_folder = coursedir.format_path(
            coursedir.autograded_directory, submission_slug, assignment_slug
        )

        if not os.path.exists(autograder_folder) or not os.listdir(autograder_folder):
            # No files in the autograder folder -> continue
            continue

        with created_folder(nbgrader_folder):
            graded_submission = generate_feedback(assignment_slug, submission_slug)
            if not graded_submission:
                continue

            graded_notebooks = {
                notebook["name"]: notebook
                for notebook in graded_submission["notebooks"]
            }

            for notebook in submission["notebooks"]:
                notebook_name = os.path.splitext(notebook["name"])[0]
                notebook_slug = notebook["slug"]

                graded_notebook = graded_notebooks[notebook_name]

                feedback_file = os.path.join(nbgrader_folder, notebook_name + ".html")
                score = graded_notebook["score"]
                max_score = graded_notebook["max_score"]

                upload_feedback(notebook_slug, feedback_file, score, max_score)

            rmtree(autograder_folder)


if __name__ == "__main__":
    main()
