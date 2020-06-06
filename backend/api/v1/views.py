import json
import os
import shutil
from glob import glob
from urllib.parse import urljoin
from datetime import datetime, timezone
import hashlib

from flask import Blueprint, jsonify, abort, send_file, url_for, current_app, redirect, request
from werkzeug import exceptions

from utils.api_utils import authenticated, get_user_assignment_folder, get_submission_folder, get_feedback_file, slugify
from .models import Content, Submission, Notebook
from app import db


# Create a blueprint
blueprint = Blueprint('api_v1', __name__)

# User route: show the user information
@blueprint.route('/user')
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
    return jsonify(user)


@blueprint.route("/content/<content_slug>")
def show_content(content_slug):
    """
    Return non-user specific information on the content
    with the given content_slug.
    """
    content = Content.query.filter_by(slug=content_slug).first_or_404()
    has_assignment = bool(content.assignment_slug)

    return_dict = {
        "slug": content.slug,
        "title": content.title,
        "description": content.description,
        "subtitle": content.subtitle,
        "learnings": list(filter(None, content.learnings.split("\n"))),
        "skills": [{
            "slug": skill.slug,
            "name": skill.name,
        } for skill in content.skills],
        "logoUrl": content.logo_url,
        "instructors": [{
            "imageUrl": instructor.image_url,
            "firstName": instructor.first_name,
            "lastName": instructor.last_name,
            "description": instructor.description,
        } for instructor in content.instructors],
        "level": content.level,
        "contentGroup": content.content_group.name,
        "contentGroupSlug": content.content_group_slug,
        "course": content.course.name,
        "courseSlug": content.course_slug,
        "hasAssignment": has_assignment,
        "facts": [{
          "key": fact.key,
          "value": fact.value,
          "extra": fact.extra,
        } for fact in content.facts]
    }

    return jsonify(return_dict)


@blueprint.route("/content/<content_slug>/start")
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
    content = Content.query.filter_by(slug=content_slug).first_or_404()
    assignment_slug = content.assignment_slug

    if not assignment_slug:
        abort(404)

    student_slug = user["name"]

    notebook_folder = get_user_assignment_folder(student_slug, assignment_slug)

    if os.path.exists(notebook_folder):
        return redirect(os.path.join(request.host_url, "user-redirect/tree", assignment_slug))
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
    submissions = Submission.query.filter_by(content_slug=content_slug, user=user["name"]).all()

    def get_feedback_url(notebook_slug, submission_slug):
        if notebook_slug:
            return url_for(".get_feedback", content_slug=content_slug, submission_slug=submission_slug, notebook_slug=notebook_slug)
        else:
            return None

    return_dict = [{
        "date": submission.date,
        "maxScore": submission.max_score,
        "graded": submission.graded,
        "notebooks": [{
            "name": notebook.name,
            "maxScore": notebook.max_score,
            "feedbackUrl": get_feedback_url(notebook_slug=notebook.slug, submission_slug=submission.slug),
        } for notebook in submission.notebooks]
    } for submission in submissions]

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
    content = Content.query.filter_by(slug=content_slug).first_or_404()
    assignment_slug = content.assignment_slug

    student_slug = user["name"]

    source_folder = get_user_assignment_folder(student_slug, assignment_slug)

    if not os.path.exists(source_folder):
        abort(404)

    submitted_notebooks = glob(os.path.join(source_folder, "*.ipynb"))

    if not submitted_notebooks:
        abort(404)

    now = datetime.now().replace(tzinfo=timezone.utc)
    submission_slug = slugify(content_slug, now.timestamp())

    submission = Submission(slug=submission_slug, content_slug=content_slug, date=now, user=student_slug)
    db.session.add(submission)

    for notebook in submitted_notebooks:
        notebook_name = os.path.basename(notebook)
        notebook_slug = slugify(submission_slug, notebook_name)
        db.session.add(Notebook(slug=notebook_slug, name=notebook_name, submission_slug=submission_slug))

    db.session.commit()

    target_folder = get_submission_folder(student_slug, submission_slug)
    os.makedirs(target_folder)

    for submission_file in submitted_notebooks:
        shutil.copy(submission_file, target_folder)

    return jsonify({"status": "ok"})


@blueprint.route("/content/<content_slug>/submissions/<submission_slug>/feedback/<notebook_slug>")
@authenticated
def get_feedback(user, content_slug, submission_slug, notebook_slug):
    """
    Return the feedback for the given content_slug and notebook_slug
    if it is present.
    """
    feedback_file = get_feedback_file(content_slug, submission_slug, notebook_slug)

    if not os.path.exists(feedback_file):
        abort(404)

    return send_file(feedback_file)

