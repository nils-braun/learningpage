import json
import os
import shutil
from glob import glob
from urllib.parse import urljoin
from datetime import datetime, timezone

from flask import (
    Blueprint,
    jsonify,
    abort,
    send_file,
    url_for,
    current_app,
    redirect,
    request,
)
from werkzeug import exceptions

from utils.api_utils import (
    authenticated,
    get_user_assignment_folder,
    get_storage_folder,
    slugify,
    is_grader,
)
from .models import Content, Submission, Notebook, Course, ContentGroup
from app import db


# Create a blueprint
blueprint = Blueprint("api_v1", __name__)

# User route: show the user information
@blueprint.route("/user", methods=["GET"])
@authenticated
def show_user(user):
    """
    Get information on the currently authenticated user.
    """
    return_dict = {
        "isAdmin": user["admin"],
        "created": user["created"],
        "lastActivity": user["last_activity"],
        "name": user["name"],
    }
    return return_dict


@blueprint.route("/course", methods=["GET"])
def show_courses():
    """
    Get information on the all courses
    """
    return_dict = [
        {
            "courseSlug": course.slug,
            "course": course.name,
            "contentGroups": [
                {
                    "contentGroupSlug": content_group.slug,
                    "contentGroup": content_group.name,
                    "contents": [
                        {
                            "slug": content.slug,
                            "title": content.title,
                            "description": content.description,
                        }
                        for content in content_group.contents
                    ],
                }
                for content_group in course.content_groups
            ],
        }
        for course in Course.query.all()
    ]
    return jsonify(return_dict)


@blueprint.route("/course/<course_slug>", methods=["GET"])
def show_course(course_slug):
    """
    Get information on a specific courses.
    """
    course = Course.query.get_or_404(course_slug)

    return_dict = {
        "courseSlug": course.slug,
        "course": course.name,
        "contentGroups": [
            {
                "contentGroupSlug": content_group.slug,
                "contentGroup": content_group.name,
                "contents": [
                    {
                        "slug": content.slug,
                        "title": content.title,
                        "description": content.description,
                    }
                    for content in content_group.contents
                ],
            }
            for content_group in course.content_groups
        ],
    }
    return jsonify(return_dict)


@blueprint.route("/content_group/<content_group_slug>", methods=["GET"])
def show_content_group(content_group_slug):
    """
    Get information on a specific content group.
    """
    content_group = ContentGroup.query.get_or_404(content_group_slug)

    return_dict = {
        "contentGroupSlug": content_group.slug,
        "contentGroup": content_group.name,
        "courseSlug": content_group.course.slug,
        "course": content_group.course.name,
        "contents": [
            {
                "slug": content.slug,
                "title": content.title,
                "description": content.description,
            }
            for content in content_group.contents
        ],
    }
    return jsonify(return_dict)


@blueprint.route("/content/<content_slug>", methods=["GET"])
def show_content(content_slug):
    """
    Return non-user specific information on the content
    with the given content_slug.
    """
    content = Content.query.get_or_404(content_slug)
    has_assignment = bool(content.assignment_slug)

    return_dict = {
        "slug": content.slug,
        "title": content.title,
        "description": content.description,
        "subtitle": content.subtitle,
        "learnings": list(filter(None, content.learnings.split("\n"))),
        "skills": [
            {"slug": skill.slug, "name": skill.name,} for skill in content.skills
        ],
        "logoUrl": content.logo_url,
        "instructors": [
            {
                "imageUrl": instructor.image_url,
                "firstName": instructor.first_name,
                "lastName": instructor.last_name,
                "description": instructor.description,
            }
            for instructor in content.instructors
        ],
        "level": content.level,
        "contentGroup": content.content_group.name,
        "contentGroupSlug": content.content_group_slug,
        "course": content.course.name,
        "courseSlug": content.course_slug,
        "hasAssignment": has_assignment,
        "facts": [
            {"key": fact.key, "value": fact.value, "extra": fact.extra,}
            for fact in content.facts
        ],
    }

    return return_dict


@blueprint.route("/content/<content_slug>/start", methods=["GET"])
@authenticated
def start_content(user, content_slug):
    """
    Endpoint for redirecting to a specific content.

    Tries two things in this order:
    * if a folder <user_folder>/<assignment> exists user_folder base is the
      user folder for each user and assignment
      is the assignment identifier, then redirect to this folder.
      This means, the content is already present in the users
      home folder
    * if the content has a stored git_url, redirect to this URL

    If all fails, abort with a 404.
    """
    content = Content.query.get_or_404(content_slug)
    assignment_slug = content.assignment_slug

    if not assignment_slug:
        abort(404)

    student_slug = user["name"]

    notebook_folder = get_user_assignment_folder(student_slug, assignment_slug)

    if os.path.exists(notebook_folder):
        return redirect(
            os.path.join(request.host_url, "user-redirect/tree", assignment_slug)
        )
    elif content.git_url:
        return redirect(content.git_url)
    else:
        abort(404)


@blueprint.route("/content/<content_slug>/submissions", methods=["GET"])
@authenticated
def show_submissions(user, content_slug):
    """
    Show all submissions for the given content_slug and user
    """
    submissions = Submission.query.filter_by(
        content_slug=content_slug, user=user["name"]
    ).all()

    def get_feedback_url(notebook_slug, submission_slug):
        return url_for(
            ".get_feedback",
            content_slug=content_slug,
            submission_slug=submission_slug,
            notebook_slug=notebook_slug,
        )

    return_dict = [
        {
            "slug": submission.slug,
            "date": submission.date,
            "score": submission.score,
            "maxScore": submission.max_score,
            "graded": submission.graded,
            "notebooks": [
                {
                    "slug": notebook.slug,
                    "name": notebook.name,
                    "score": notebook.score,
                    "maxScore": notebook.max_score,
                    "feedbackUrl": get_feedback_url(
                        notebook_slug=notebook.slug, submission_slug=submission.slug
                    ),
                }
                for notebook in submission.notebooks
            ],
        }
        for submission in submissions
    ]

    return jsonify(return_dict)


@blueprint.route("/content/<content_slug>/submissions", methods=["POST"])
@authenticated
def add_submission(user, content_slug):
    """
    Add a new submission for the given content.

    This is done by:
    * creating a new entry in the submission database
    * copying the contents from the user folder to the storage folder
    """
    content = Content.query.get_or_404(content_slug)
    assignment_slug = content.assignment_slug

    student_slug = user["name"]

    source_folder = get_user_assignment_folder(student_slug, assignment_slug)
    submitted_notebooks = glob(os.path.join(source_folder, "*.ipynb"))

    if not submitted_notebooks:
        abort(404)

    now = datetime.now().replace(tzinfo=timezone.utc)
    submission_slug = slugify(content_slug, now.timestamp())

    target_folder = get_storage_folder(submission_slug, assignment_slug)
    os.makedirs(target_folder)

    submission = Submission(
        slug=submission_slug, content_slug=content_slug, date=now, user=student_slug
    )
    db.session.add(submission)

    for notebook in submitted_notebooks:
        notebook_name = os.path.basename(notebook)
        notebook_slug = slugify(submission_slug, notebook_name)
        db.session.add(
            Notebook(
                slug=notebook_slug, name=notebook_name, submission_slug=submission_slug
            )
        )

        shutil.copy(notebook, target_folder)

    db.session.commit()

    return {"status": "ok"}, 201


@blueprint.route("/feedback/<notebook_slug>", methods=["GET"])
@authenticated
def get_feedback(user, notebook_slug):
    """
    Return the feedback for the given notebook_slug if it is present.
    """
    notebook = Notebook.query.get_or_404(notebook_slug)
    submission_slug = notebook.submission_slug
    assignment_slug = notebook.submission.content.assignment_slug

    if not notebook.submission.user == user["name"]:
        abort(403)

    folder = get_storage_folder(submission_slug, assignment_slug)
    feedback_file = os.path.join(folder, notebook.name + ".html")

    if not os.path.exists(feedback_file):
        abort(404)

    return send_file(feedback_file)


@blueprint.route("/feedback/<notebook_slug>", methods=["POST"])
@is_grader
def add_feedback(notebook_slug):
    """
    Add feedback for a given notebook
    """
    notebook = Notebook.query.get_or_404(notebook_slug)
    submission_slug = notebook.submission_slug
    assignment_slug = notebook.submission.content.assignment_slug

    folder = get_storage_folder(submission_slug, assignment_slug)
    feedback_filename = os.path.join(folder, notebook.name + ".html")

    feedback_file = request.files.get("feedback")

    if not feedback_file:
        abort(400)

    score = request.form.get("score")

    if score is None:
        abort(400)

    max_score = request.form.get("max_score")

    if max_score is None:
        abort(400)

    feedback_file.save(feedback_filename)

    notebook.score = score
    notebook.max_score = max_score
    notebook.graded = True
    db.session.commit()

    return {"status": "ok"}, 201


@blueprint.route("/notebook/<notebook_slug>")
@is_grader
def get_notebook(notebook_slug):
    """
    Return the notebook for the given notebook_slug if it is present.
    """
    notebook = Notebook.query.get_or_404(notebook_slug)
    submission_slug = notebook.submission_slug
    assignment_slug = notebook.submission.content.assignment_slug

    folder = get_storage_folder(submission_slug, assignment_slug)
    submission_file = os.path.join(folder, notebook.name)

    if not os.path.exists(submission_file):
        abort(404)

    return send_file(submission_file)


@blueprint.route("/ungraded")
@is_grader
def get_ungraded_submissions():
    """
    Return information on the ungraded submissions.
    """
    # We need to do a python-side-filtering, as the property
    # can not be calculated in SQL
    submissions = Submission.query.all()
    submissions = filter(lambda s: not s.graded, submissions)

    return_dict = [
        {
            "slug": submission.slug,
            "assignment_slug": submission.content.assignment_slug,
            "user": submission.user,
            "notebooks": [
                {"slug": notebook.slug, "name": notebook.name,}
                for notebook in submission.notebooks
            ],
        }
        for submission in submissions
    ]

    return jsonify(return_dict)
