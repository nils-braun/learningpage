import os

import requests

from nbgrader.coursedir import CourseDirectory

from grading.utils import (
    autograde,
    get_config,
    get_ungraded_submissions,
    created_folder,
    download_notebook,
)


def main():
    ungraded_submissions = get_ungraded_submissions()

    c = get_config()
    coursedir = CourseDirectory(config=c)

    for submission in ungraded_submissions:
        submission_slug = submission["slug"]
        assignment_slug = submission["assignment_slug"]
        student_name = submission["user"]

        # We choose the submission slug as the user
        nbgrader_folder = coursedir.format_path(
            coursedir.submitted_directory, submission_slug, assignment_slug
        )

        autograder_folder = coursedir.format_path(
            coursedir.autograded_directory, submission_slug, assignment_slug
        )

        if os.path.exists(autograder_folder) and os.listdir(autograder_folder):
            # There is already an autograde -> continue
            continue

        with created_folder(nbgrader_folder):
            for submitted_file in submission["notebooks"]:
                download_notebook(
                    submitted_file["slug"],
                    os.path.join(nbgrader_folder, submitted_file["name"]),
                )

            autograde(assignment_slug, submission_slug, student_name)


if __name__ == "__main__":  # pragma no cover
    main()
