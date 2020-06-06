from tests.fixtures import BaseTestCase

from app import db
from api.v1.models import Content, Skill, ContentGroup, Course, Fact, Instructor


class APITestCase(BaseTestCase):
    def test_empty_db(self):
        rv = self.client.get("/api/v1/content/my-content")
        self.assert404(rv)


    def test_content(self):
        skills = [Skill(slug="skill", name="Skill")]

        instructors = [
            Instructor(
                slug="instructor",
                first_name="First",
                last_name="Last",
                description="",
            )
        ]

        course = Course(slug="course", name="Course")
        content_group = ContentGroup(slug="group", name="Group", course=course)
        content = Content(slug="content", title="Content", subtitle="subtitle",
                        description="description", learnings="learnings",
                        level="level", skills=skills, content_group=content_group,
                        instructors=instructors, assignment_slug="assignment")

        facts = [
            Fact(slug="fact", content=content, key="Fact", value="value"),
        ]

        db.session.add(content)

        rv = self.client.get("/api/v1/content/content")
        self.assertEqual(rv.json, {
            "contentGroup": "Group",
            "contentGroupSlug": "group",
            "course": "Course",
            "courseSlug": "course",
            "description": "description",
            "facts": [{"extra": {}, "key": "Fact", "value": "value"}],
            "hasAssignment": True,
            "instructors": [{"description": "", "firstName": "First", "imageUrl": None, "lastName": "Last"}],
            "learnings": ["learnings"],
            "level": "level",
            "logoUrl": None,
            "skills": [{"name": "Skill", "slug": "skill"}],
            "slug": "content",
            "subtitle": "subtitle",
            "title": "Content",
        })