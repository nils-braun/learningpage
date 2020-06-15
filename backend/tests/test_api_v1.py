import os
import shutil
import io
from unittest.mock import patch

from flask import current_app

from tests.fixtures import BaseTestCase
from app import create_app, db
from api.v1.models import (
    Content,
    Skill,
    ContentGroup,
    Course,
    Fact,
    Instructor,
    Notebook,
)
from utils.api_utils import get_user_assignment_folder, get_storage_folder, auth


class APITestCase(BaseTestCase):
    def add_content(self):
        skills = [Skill(slug="skill", name="Skill")]

        instructors = [
            Instructor(
                slug="instructor", first_name="First", last_name="Last", description="",
            )
        ]

        course = Course(slug="course", name="Course")
        content_group = ContentGroup(slug="group", name="Group", course=course)
        content = Content(
            slug="content",
            title="Content",
            subtitle="subtitle",
            description="description",
            learnings="learnings",
            level="level",
            skills=skills,
            content_group=content_group,
            instructors=instructors,
            assignment_slug="assignment",
        )

        facts = [
            Fact(slug="fact", content=content, key="Fact", value="value"),
        ]

        db.session.add(content)

    def add_notebook(self):
        assignment_folder = get_user_assignment_folder("testing", "assignment")
        os.makedirs(assignment_folder)

        with open(os.path.join(assignment_folder, "notebook.ipynb"), "w") as f:
            f.write("test")

    def test_empty_db(self):
        rv = self.client.get("/api/v1/content/my-content")
        self.assert404(rv)

    def test_user(self):
        rv = self.client.get("/api/v1/user")

        self.assertEqual(
            rv.json,
            {
                "isAdmin": False,
                "created": "created",
                "lastActivity": "last_activity",
                "name": "testing",
            },
        )

    def test_courses(self):
        self.add_content()

        rv = self.client.get("/api/v1/course")

        self.assertEqual(
            rv.json,
            [
                {
                    "contentGroups": [
                        {
                            "contentGroup": "Group",
                            "contentGroupSlug": "group",
                            "contents": [
                                {
                                    "description": "description",
                                    "slug": "content",
                                    "title": "Content",
                                }
                            ],
                        }
                    ],
                    "courseSlug": "course",
                    "course": "Course",
                }
            ],
        )

    def test_course(self):
        self.add_content()

        rv = self.client.get("/api/v1/course/course")

        self.assertEqual(
            rv.json,
            {
                "contentGroups": [
                    {
                        "contentGroup": "Group",
                        "contentGroupSlug": "group",
                        "contents": [
                            {
                                "description": "description",
                                "slug": "content",
                                "title": "Content",
                            }
                        ],
                    }
                ],
                "courseSlug": "course",
                "course": "Course",
            },
        )

        rv = self.client.get("/api/v1/course/other_course")
        self.assert404(rv)

    def test_content_group(self):
        self.add_content()

        rv = self.client.get("/api/v1/content_group/group")

        self.assertEqual(
            rv.json,
            {
                "contentGroup": "Group",
                "contentGroupSlug": "group",
                "courseSlug": "course",
                "course": "Course",
                "contents": [
                    {
                        "description": "description",
                        "slug": "content",
                        "title": "Content",
                    }
                ],
            },
        )

        rv = self.client.get("/api/v1/content_group/other_group")
        self.assert404(rv)

    def test_content(self):
        self.add_content()

        rv = self.client.get("/api/v1/content/content")
        self.assertEqual(
            rv.json,
            {
                "contentGroup": "Group",
                "contentGroupSlug": "group",
                "course": "Course",
                "courseSlug": "course",
                "description": "description",
                "facts": [{"extra": {}, "key": "Fact", "value": "value"}],
                "hasAssignment": True,
                "instructors": [
                    {
                        "description": "",
                        "firstName": "First",
                        "imageUrl": None,
                        "lastName": "Last",
                    }
                ],
                "learnings": ["learnings"],
                "level": "level",
                "logoUrl": None,
                "skills": [{"name": "Skill", "slug": "skill"}],
                "slug": "content",
                "subtitle": "subtitle",
                "title": "Content",
            },
        )

    def test_empty_submissions(self):
        self.add_content()

        rv = self.client.get("/api/v1/content/content/submissions")
        self.assert200(rv)
        self.assertEqual(rv.json, [])

    def test_submission(self):
        # Submission should fail, as content is not available
        rv = self.client.post("/api/v1/content/content/submissions")
        self.assert404(rv)

        self.add_content()

        # Submission should fail, as source notebook is not available
        rv = self.client.post("/api/v1/content/content/submissions")
        self.assert404(rv)

        self.add_notebook()

        # Submission should be successful
        rv = self.client.post("/api/v1/content/content/submissions")
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.json, {"status": "ok"})

        # Submission should be created and in the list
        rv = self.client.get("/api/v1/content/content/submissions")
        self.assert200(rv)

        submissions = rv.json
        self.assertEqual(len(submissions), 1)

        submission = submissions[0]
        self.assertEqual(
            submission,
            {
                "slug": submission["slug"],  # not tested on purpose
                "date": submission["date"],  # not tested on purpose
                "maxScore": 0.0,
                "score": 0.0,
                "graded": False,
                "notebooks": [
                    {
                        "slug": submission["notebooks"][0][
                            "slug"
                        ],  # not tested on purpose
                        "name": "notebook.ipynb",
                        "maxScore": 0.0,
                        "score": 0.0,
                        "feedbackUrl": submission["notebooks"][0][
                            "feedbackUrl"
                        ],  # not tested on purpose
                    }
                ],
            },
        )

        # Notebook should be copied and ready for external grading
        target_folder = get_storage_folder(submission["slug"], "assignment")
        assert os.path.exists(os.path.join(target_folder, "notebook.ipynb"))
        self.assertEqual(
            open(os.path.join(target_folder, "notebook.ipynb")).read(), "test"
        )

        # Notebook should be downloadable
        notebook_slug = submission["notebooks"][0]["slug"]
        rv = self.client.get(
            f"/api/v1/notebook/{notebook_slug}",
            headers={"Authorization": "token grader"},
        )
        self.assert200(rv)
        self.assertEqual(rv.data, b"test")

        # Notebook is intentionally deleted
        shutil.rmtree(target_folder)
        rv = self.client.get(
            f"/api/v1/notebook/{notebook_slug}",
            headers={"Authorization": "token grader"},
        )
        self.assert404(rv)

    def test_start_content(self):
        self.add_content()

        rv = self.client.get("/api/v1/content/content/start")
        self.assert404(rv)

        content = Content.query.filter_by(slug="content").first()
        content.git_url = "http://example.com"
        db.session.commit()

        rv = self.client.get("/api/v1/content/content/start")
        self.assertRedirects(rv, "http://example.com")

        notebook_folder = get_user_assignment_folder("testing", "assignment")
        os.makedirs(notebook_folder)

        rv = self.client.get("/api/v1/content/content/start")
        self.assertRedirects(rv, "user-redirect/tree/assignment")

        # Content without assignment is not startable
        content = Content.query.filter_by(slug="content").first()
        content.assignment_slug = None
        db.session.commit()

        rv = self.client.get("/api/v1/content/content/start")
        self.assert404(rv)

    def test_feedback(self):
        self.add_content()
        self.add_notebook()

        # Create and get the submissions
        rv = self.client.post("/api/v1/content/content/submissions")
        self.assertEqual(rv.status_code, 201)

        rv = self.client.get("/api/v1/content/content/submissions")
        self.assert200(rv)
        notebook_slug = rv.json[0]["notebooks"][0]["slug"]

        # No feedback available so far
        rv = self.client.get(f"/api/v1/feedback/{notebook_slug}")
        self.assert404(rv)

        # Add feedback = grade; wrong request
        rv = self.client.post(
            f"/api/v1/feedback/{notebook_slug}",
            headers={"Authorization": "token grader"},
        )
        self.assert400(rv)

        # Add feedback = grade; wrong reqest
        data = {"feedback": (io.BytesIO(b"feedback"), "feedback.html")}

        rv = self.client.post(
            f"/api/v1/feedback/{notebook_slug}",
            data=data,
            content_type="multipart/form-data",
            headers={"Authorization": "token grader"},
        )
        self.assert400(rv)

        # Add feedback = grade; correct reqest
        data = {
            "score": 0.5,
            "max_score": 1,
            "feedback": (io.BytesIO(b"feedback"), "feedback.html"),
        }

        rv = self.client.post(
            f"/api/v1/feedback/{notebook_slug}",
            data=data,
            content_type="multipart/form-data",
            headers={"Authorization": "token grader"},
        )
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.json, {"status": "ok"})

        rv = self.client.get("/api/v1/content/content/submissions")
        self.assert200(rv)

        self.assertEqual(rv.json[0]["notebooks"][0]["maxScore"], 1.0)
        self.assertEqual(rv.json[0]["notebooks"][0]["score"], 0.5)
        self.assertEqual(rv.json[0]["maxScore"], 1.0)
        self.assertEqual(rv.json[0]["score"], 0.5)
        self.assertEqual(rv.json[0]["graded"], True)

        # Feedback should be fetchable
        rv = self.client.get(f"/api/v1/feedback/{notebook_slug}")
        self.assert200(rv)
        self.assertEqual(rv.data, b"feedback")

        # But not with the wrong user
        notebook = Notebook.query.filter_by(slug=notebook_slug).first()
        notebook.submission.user = "other-user"
        db.session.commit()

        rv = self.client.get(f"/api/v1/feedback/{notebook_slug}")
        self.assert403(rv)

    def test_ungraded_submission(self):
        self.add_content()
        self.add_notebook()

        # Submission should be successful
        rv = self.client.post("/api/v1/content/content/submissions")
        self.assertEqual(rv.status_code, 201)

        # Submission should be ungraded so far
        rv = self.client.get(
            "/api/v1/ungraded", headers={"Authorization": "token grader"}
        )
        self.assert200(rv)

        submissions = rv.json
        self.assertEqual(len(submissions), 1)

        submission = submissions[0]
        notebook_slug = submission["notebooks"][0]["slug"]
        self.assertEqual(
            submission,
            {
                "assignment_slug": "assignment",
                "slug": submission["slug"],  # not tested on purpose
                "user": "testing",
                "notebooks": [
                    {
                        "slug": notebook_slug,  # not tested on purpose
                        "name": "notebook.ipynb",
                    }
                ],
            },
        )

        # now do the grading
        data = {
            "score": 0.5,
            "max_score": 1,
            "feedback": (io.BytesIO(b"feedback"), "feedback.html"),
        }
        rv = self.client.post(
            f"/api/v1/feedback/{notebook_slug}",
            data=data,
            content_type="multipart/form-data",
            headers={"Authorization": "token grader"},
        )
        self.assertEqual(rv.status_code, 201)

        # Submission should not show up
        rv = self.client.get(
            "/api/v1/ungraded", headers={"Authorization": "token grader"}
        )
        self.assert200(rv)

        self.assertEqual(rv.json, [])


class AuthorizationTestCase(BaseTestCase):
    def _test_user_api(self, url, post=False):
        if post:
            cmd = self.client.post
        else:
            cmd = self.client.get

        # Needs authentication
        current_app.config["TESTING"] = False

        rv = cmd(url)
        self.assert401(rv)

        with patch("jupyterhub.services.auth.HubAuth._api_request") as mock_get:
            # Make sure the jupyterhub returns nothing (= invalid token)
            # and also does not cache the result
            mock_get.return_value = None
            auth.cache.clear()

            rv = cmd(url, headers={auth.auth_header_name: "my-token"})
            mock_get.assert_called_once_with(
                "GET",
                "http://127.0.0.1:8081/hub/api/authorizations/token/my-token",
                allow_404=True,
            )
            self.assert403(rv)

        with patch("jupyterhub.services.auth.HubAuth._api_request") as mock_get:
            # Make sure the jupyterhub returns nothing (= invalid token)
            # and also does not cache the result
            mock_get.return_value = None
            auth.cache.clear()

            self.client.set_cookie("", auth.cookie_name, "my-cookie")
            rv = cmd(url)
            mock_get.assert_called_once_with(
                "GET",
                "http://127.0.0.1:8081/hub/api/authorizations/cookie/jupyterhub-services/my-cookie",
                allow_404=True,
            )
            self.assert403(rv)

        # If everything is correct, it will not return an unauthenticated,
        # but any other status code (we do not really care which)
        current_app.config["TESTING"] = True

        rv = cmd(url)
        self.assertIn(rv.status_code, [200, 201, 404])

    def _test_grader_api(self, url, post=False):
        if post:
            cmd = self.client.post
        else:
            cmd = self.client.get

        # Needs authentication
        rv = cmd(url)
        self.assert401(rv)

        # Invalid authentication
        rv = cmd(url, headers={"Authorization": "wrong"})
        self.assert401(rv)

        # Wrong authentication
        rv = cmd(url, headers={"Authorization": "token wrong"})
        self.assert403(rv)

        # Correct authentication -> 404
        rv = cmd(url, headers={"Authorization": "token grader"})
        self.assert404(rv)

    def test_start_content_unauthenticated(self):
        self._test_user_api("/api/v1/content/slug/start")

    def test_show_submissions_unauthenticated(self):
        self._test_user_api("/api/v1/content/slug/submissions")

    def test_add_submissions_unauthenticated(self):
        self._test_user_api("/api/v1/content/slug/submissions", post=True)

    def test_get_feedback_unauthenticated(self):
        self._test_user_api("/api/v1/feedback/slug")

    def test_add_feedback_unauthenticated(self):
        self._test_grader_api("/api/v1/feedback/slug", post=True)

    def test_get_notebook_unauthenticated(self):
        self._test_grader_api("/api/v1/notebook/slug")
