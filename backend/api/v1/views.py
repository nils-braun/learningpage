import json

from flask import Blueprint, jsonify

from utils import authenticated
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
        "maxScore": content.max_score,
        "hasAssignment": bool(content.assignment_slug),
        "facts": [{
          "key": fact.key,
          "value": fact.value,
          "extra": fact.extra,
        } for fact in content.facts]
    }

    return jsonify(return_dict)
