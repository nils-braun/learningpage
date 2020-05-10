from traitlets.config.loader import Config
import tempfile
import os
import logging
import sys
from shutil import rmtree

from nbgrader.exchange import ExchangeReleaseAssignment, ExchangeCollect, ExchangeSubmit
from nbgrader.converters import Autograde, GenerateFeedback
from nbgrader.coursedir import CourseDirectory
from nbgrader.auth import Authenticator


def run(app):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    app.log.addHandler(handler)

    app.start()

    app.log.removeHandler(handler)


c = Config()
c.CourseDirectory.course_id = "course"
c.CourseDirectory.root = "/var/lib/content"
c.CourseDirectory.assignment_id = "pandas-io"
c.CourseDirectory.student_id = "grader"
c.Exchange.root = tempfile.mkdtemp()
c.CourseDirectory.db_url = os.environ.get('GRADER_DATABASE_STRING')

try:
    os.makedirs(c.Exchange.root, exist_ok=True)
    os.chmod(c.Exchange.root, 0o777)

    authenticator = Authenticator(config=c)
    coursedir = CourseDirectory(config=c)

    # TODO: what to do if the assignment has multiple notebooks? test that!

    # 1. Release assignment. We need to have it in the outbound folder, otherwise nbgrader can not match the assignment properly
    # TODO: What should we do if we have different versions of it? We should make sure to have the correct assignment checked out!
    app = ExchangeReleaseAssignment(coursedir=coursedir, authenticator=authenticator, config=c)
    run(app)
    # Works! Notebook copied into exchange/course/outbound

    # 2. Now store the incoming notebook in the exchange, as if the student would have submitted it
    # We need to cheat a bit to let nbgrader think, all notebooks are stored in "input"
    class MyExchangeSubmit(ExchangeSubmit):
        def init_src(self):
            self.src_path = os.path.abspath("input")

    app = MyExchangeSubmit(coursedir=coursedir, authenticator=authenticator, config=c)
    run(app)
    # Works! Copies to exchange/course/inbound/nils+..../*.ipynb
    # Attention: assignment needs to be present in exchange/course/outbound/

    # 3. Now collect the submitted notebooks (will be only one)
    app = ExchangeCollect(coursedir=coursedir, authenticator=authenticator, config=c)
    app.update = True # we want to replace the already present one, if any
    app.check_owner = False # we will always commit with the flask user, so it is not a cheating attempt
    run(app)
    # Works! Uses files in exchange/course/inbound/ and puts them into the database
    # But so far not in "submitted_assignment" table

    # 4. Do the autograding
    app = Autograde(coursedir=coursedir, config=c)
    app.force = True
    app.create_student = True
    run(app)
    # Works! Does autograding, but feedback is not present so far

    # TODO: what to do if manual grading is needed?

    # 5. Generate the feedback and make it visible to the student
    app = GenerateFeedback(coursedir=coursedir, config=c)
    app.force = True
    run(app)
    # Works! Feedback present in content/feedback/..., (but not in exchange folder, where it is not needed)

finally:
    rmtree(c.Exchange.root)