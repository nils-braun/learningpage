from app import db

IdentifierType = db.String(32)

ContentInstructorAssociations = db.Table("content_instructor_association", db.metadata,
    db.Column('content_slug', IdentifierType, db.ForeignKey('contents.slug')),
    db.Column('instructor_slug', IdentifierType, db.ForeignKey('instructors.slug'))
)


ContentSkillAssociations = db.Table("content_skill_association", db.metadata,
    db.Column('content_slug', IdentifierType, db.ForeignKey('contents.slug')),
    db.Column('skill_slug', IdentifierType, db.ForeignKey('skills.slug'))
)


class Content(db.Model):
    __tablename__ = 'contents'

    slug = db.Column(IdentifierType, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    subtitle = db.Column(db.String(255), default="", nullable=False)
    description = db.Column(db.String, default="", nullable=False)
    learnings = db.Column(db.String, default="", nullable=False)
    logo_url = db.Column(db.String, nullable=True)
    content_group_slug = db.Column(
        IdentifierType, db.ForeignKey('content_groups.slug'), nullable=False)
    sort_number = db.Column(db.Integer, default=0, nullable=False)
    level = db.Column(db.String(50), default="", nullable=False)
    assignment_slug = db.Column(db.String, nullable=True)

    content_group = db.relationship("ContentGroup", back_populates="contents")
    instructors = db.relationship(
        "Instructor", secondary="content_instructor_association")
    facts = db.relationship("Fact", back_populates="content")
    skills = db.relationship(
        "Skill", secondary=ContentSkillAssociations)

    @property
    def course_slug(self):
        return self.content_group.course_slug

    @property
    def course(self):
        return self.content_group.course

    def __repr__(self):
        return f"<Content(name='{self.name}', content_group='{self.content_group.name}', course='{self.course.name}')>"


class ContentGroup(db.Model):
    __tablename__ = 'content_groups'

    slug = db.Column(IdentifierType, primary_key=True)
    name = db.Column(db.String, nullable=False)
    course_slug = db.Column(IdentifierType, db.ForeignKey('courses.slug'), nullable=False)
    sort_number = db.Column(db.Integer, default=0, nullable=False)

    course = db.relationship("Course", back_populates="content_groups")
    contents = db.relationship(
        "Content", back_populates="content_group", order_by=Content.sort_number)

    def __repr__(self):
        return f"<ContentGroup(name='{self.name}', course='{self.course.name}')>"


class Course(db.Model):
    __tablename__ = 'courses'

    slug = db.Column(IdentifierType, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # "*" for all or list of users separated by ","
    access_string = db.Column(db.String, default="*", nullable=False)
    sort_number = db.Column(db.Integer, default=0, nullable=False)

    content_groups = db.relationship(
        "ContentGroup", back_populates="course", order_by=ContentGroup.sort_number)

    @property
    def contents(self):
        contents = {}
        for content_group in self.content_groups:
            contents[content_group.name] = content_group.courses

        return contents

    def __repr__(self):
        return f"<Course(name='{self.name}')>"


class Instructor(db.Model):
    __tablename__ = "instructors"

    slug = db.Column(IdentifierType, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, default="", nullable=False)
    image_url = db.Column(db.String, nullable=True)

    content = db.relationship("Content", back_populates="instructors", secondary="content_instructor_association")

    def __repr__(self):
        return f"<Instructor(name='{self.name}')>"


class Fact(db.Model):
    __tablename__ = "facts"

    slug = db.Column(IdentifierType, primary_key=True)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    extra = db.Column(db.JSON, default={}, nullable=False)
    content_slug = db.Column(IdentifierType, db.ForeignKey('contents.slug'), nullable=False)

    content = db.relationship("Content", back_populates="facts")

    def __repr__(self):
        return f"<Fact(key='{self.key}', value='{self.value}')>"


class Skill(db.Model):
    __tablename__ = "skills"

    slug = db.Column(IdentifierType, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    content = db.relationship("Content", back_populates="skills", secondary="content_skill_association")

    def __repr__(self):
        return f"<Skill(name='{self.name}')>"
