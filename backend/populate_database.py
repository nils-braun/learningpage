from app import db, create_app
from api.v1.models import Content, Skill, ContentGroup, Course, Fact, Instructor


def main():
    app = create_app()
    app.app_context().push()

    db.create_all()
    skills = [
        Skill(slug=slug, name=name)
        for slug, name in [
            ("file-formats", "File formats"),
            ("encoding", "Encoding"),
            ("data-wrangling", "Data Wrangling"),
            ("data-preprocessing", "Data preprocessing"),
        ]
    ]

    instructors = [
        Instructor(
            slug="larry-page",
            first_name="Larry",
            last_name="Page",
            description="Larry has been working for a Fortune 500 company the most of his professional time. He has been busy with being the CEO of such a company for years. Since he stepped back from this position, he loves to educate others and let people gain insights into his expert knowledge.",
        ),
        Instructor(
            slug="sergey-brin",
            first_name="Sergey",
            last_name="Brin",
            description="Sergey has been working for a Fortune 500 company the most of his professional time. He has been busy with being the CEO of such a company for years. Since he stepped back from this position, he loves to educate others and let people gain insights into his expert knowledge.",
        ),
    ]

    course = Course(slug="course", name="Course")
    content_group = ContentGroup(slug="prep", name="Preparations", course=course)
    content = Content(
        slug="my_course",
        title="My Course",
        subtitle="An introduction to data input and output with Pandas in Python",
        description="""Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor""",
        learnings="You will learn how to read data from various sources\n"
        "Learn about how to process data and reshape it\n"
        "Learn how data can be encoded in various ways\n"
        "You will see what schema evolution means and why it is important for your data",
        level="beginner",
        skills=skills,
        content_group=content_group,
        instructors=instructors,
        assignment_slug="my_course",
    )

    facts = [
        Fact(
            slug="a",
            content=content,
            key="prerequirements",
            value="You should  have beginner level experience with Python.",
        ),
        Fact(slug="b", content=content, key="language", value="English."),
    ]

    db.session.add(content)
    for fact in facts:
        db.session.add(fact)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise


if __name__ == "__main__":
    main()
