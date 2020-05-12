from nbgrader.coursedir import CourseDirectory

from utils.grader_utils import autograde, get_config
from glob import glob
from shutil import rmtree


def main():
    c = get_config()
    coursedir = CourseDirectory(config=c)

    submission_glob = coursedir.format_path(coursedir.submitted_directory, "*", "*")
    submissions = glob(submission_glob)

    for submission in submissions:
        path, student_slug, assignment_slug = submission.rsplit("/", 2)

        autograde(assignment_slug, student_slug)
        rmtree(submission)


if __name__ == "__main__":
    main()