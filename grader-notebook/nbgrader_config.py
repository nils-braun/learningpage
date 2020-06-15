import os

c = get_config()

c.CourseDirectory.course_id = "course"
c.CourseDirectory.root = "/home/jovyan/content"
c.CourseDirectory.db_url = os.environ.get("GRADER_DATABASE_STRING")
