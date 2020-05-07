from app import db, create_app
from api.v1.models import Content, Skill, ContentGroup, Course

app = create_app()
app.app_context().push()

skill = Skill(slug="test", name="Test")
course = Course(slug="dex", name="DEX")
content_group = ContentGroup(slug="prep", name="Preparations", course=course)
content = Content(slug="test", title="Test", skills=[skill], content_group=content_group)

db.session.add(skill)
db.session.add(content)
db.session.commit()