import json
import os
from urllib.parse import urljoin

from flask import Blueprint, jsonify, abort, send_file, url_for, current_app, redirect, request
from werkzeug import exceptions

from utils import authenticated
import grader_utils
from .models import Content


# Create a blueprint
blueprint = Blueprint('api_v1', __name__)

# User route: show the user information
@blueprint.route('/user')
@authenticated
def show_user(user):
    return_dict = {
        "isAdmin": user["admin"],
        "created": user["created"],
        "lastActivity": user["last_activity"],
        "name": user["name"],
    }
    return jsonify(user)


@blueprint.route("/content/<slug>")
@authenticated
def show_content(user, slug):
    content = Content.query.filter_by(slug=slug).first_or_404()
    has_assignment = bool(content.assignment_slug)

    if has_assignment:
        max_score = grader_utils.get_max_score(user["name"], content.assignment_slug)
    else:
        max_score = None

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
        "maxScore": max_score,
        "hasAssignment": has_assignment,
        "facts": [{
          "key": fact.key,
          "value": fact.value,
          "extra": fact.extra,
        } for fact in content.facts]
    }

    return jsonify(return_dict)


@blueprint.route("/content/<slug>/submissions", methods=["GET"])
@authenticated
def show_submissions(user, slug):
    content = Content.query.filter_by(slug=slug).first_or_404()
    assignment_slug = content.assignment_slug

    submissions = grader_utils.get_submissions(user["name"], assignment_slug)

    if not submissions:
        abort(404)

    def get_feedback_url(notebook_id):
        if notebook_id:
            return url_for(".get_feedback", slug=notebook_id)
        else:
            return None

    return jsonify([
        {
            "date": submission["timestamp"],
            "maxScore": grader_utils.get_max_score_for(submission),
            "notebooks": [{
                "name": notebook["name"],
                "maxScore": grader_utils.get_max_score_for(notebook),
                "feedbackUrl": get_feedback_url(notebook["id"]),
            } for notebook in submission["notebooks"]]
        } for submission in submissions]
    )


@blueprint.route("/content/<slug>/submissions", methods=["POST"])
@authenticated
def add_submissions(user, slug):
    content = Content.query.filter_by(slug=slug).first_or_404()
    assignment_slug = content.assignment_slug

    student_slug = user["name"]

    base_folder = current_app.config.get("USER_BASE_FOLDER")

    notebook_folder = os.path.join(base_folder, student_slug, assignment_slug)

    grader_utils.submit(notebook_folder, assignment_slug, student_slug)

    return jsonify({"status": "ok"})


@blueprint.route("/content/<slug>/start")
@authenticated
def start_content(user, slug):
    content = Content.query.filter_by(slug=slug).first_or_404()
    assignment_slug = content.assignment_slug

    student_slug = user["name"]

    base_folder = current_app.config.get("USER_BASE_FOLDER")

    notebook_folder = os.path.join(base_folder, student_slug, assignment_slug)

    if os.path.exists(notebook_folder):
        return redirect(os.path.join(request.host_url, "user-redirect/tree", assignment_slug))
    elif content.git_url:
        return redirect(content.git_url)
    else:
        abort(404)


@blueprint.route("/feedback/<slug>")
@authenticated
def get_feedback(user, slug):
    submitted_notebook = grader_utils.get_submitted_notebook(slug)

    if not submitted_notebook:
        abort(404)

    student_slug = user["name"]

    if not submitted_notebook["student"] == student_slug:
        abort(403)

    assignment_slug = submitted_notebook["assignment_slug"]
    notebook_name = submitted_notebook["name"]

    feedback_path = grader_utils.get_feedback_path(student_slug, assignment_slug, notebook_name)

    if not feedback_path:
        abort(404)

    return send_file(feedback_path)

