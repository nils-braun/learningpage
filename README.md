# Learn-Page

Bringing a frontpage to jupyterhub.

## Quickstart

Start all components:

    docker-compose up -d

Log into http://127.0.0.1:8000/services/grader-notebook/formgrader with "grader:grader" and create (and generate) an assignment
called "pandas-io".
Download the notebooks in the preview.

Create a test database entry for "pandas-io"

    docker-compose exec backend python3 populate_database.py

Log into the jupyterhub instance at http://127.0.0.1:8000 with the "student:student"
(you might need to logout again).
After login, you should be able to access the API, e.g. under

    http://127.0.0.1:8000/services/learningpage/api/v1/content/pandas-io

or

    http://127.0.0.1:8000/services/learningpage/api/v1/user

However, you will not have any submission already:

    http://127.0.0.1:8000/services/learningpage/api/v1/content/pandas-io/submissions

Now go back to the notebook server under http://127.0.0.1:8000, create a folder "pandas-io" and
upload the notebook(s) you downloaded earlier.
Feel free to actually do some exercises.

Then call a POST on

    http://127.0.0.1:8000/services/learningpage/api/v1/content/pandas-io/submissions

with the correct cookie.
Now you will see submissions showing up, but without grade so far.

Do the batch autograding

    docker-compose exec backend python3 autograde.py

Then, call the feedback batch script:

    docker-compose exec backend python3 feedback.py

If you have manual grading in your assignments, it will output the ids you need to manually grade.
Go to

    http://127.0.0.1:8000/services/grader-notebook/formgrader/submissions/<id>

for each of them and do the grading.

After that, call the feedback script again.

Now, the shown submissions on

    http://127.0.0.1:8000/services/learningpage/api/v1/content/pandas-io/submissions

are updated accordingly.

## Components

* jupyterhub: "normal" jupyterhub instance with two users and the services defined (with tokes etc.)
* postgres: SQL database to store the grades as well as the content definitions
* grader-notebook: special jupyterhub service accessible under http://127.0.0.1:8000/services/grader-notebook/ which is a notebook
  with the `nbgrader` extensions installed. Has access to the grader database and can only be used by the grader user.
* backend: flask service for the API. Can be accessed via http://127.0.0.1:8000/services/learningpage, but needs a
  correct jupyterhub login cookie. Exchanges the user hoe folders with the jupyterhub component,
  to be able tu submit and access the notebooks of the users.

## Open ToDos Backend:
* handle multiple versions of assignments correctly during submit
  Currently we assume that the notebook related to a assignment needs to be compared with exactly this
  assignment. The way this is done, is that the assignment is looked up in the content database
  based on the POST command the user calls.
  However if there was an update, the notebook could in principle still be related to another assignment.
  This needs to be handled.

## Backend

GET /api/v1/content/<ID>
{
    slug: string
    title: string,        # max len 50
    description: string,  # markdown raw format
    subtitle: string,     # max len 255
    learnings: string[],
    skills: [
        slug: string,
        name: string,
    ],
    logoUrl: string,
    instructors: [{
            imageUrl: string,
            firstName: string,
            lastName: string,
            description: string  # markdown raw format
    }]
    level: ‘beginner’ | ‘intermediate’ | ‘expert’,
    contentGroup: string,
    contentGroupSlug: string,
    course: string,
    courseSlug: string,
    hasAssignment: bool, # “submittable” or not
    facts: [{
        key: string,
        value: string,
        extra: string,   # JSON string
    }]
}


GET /api/v1/content/<ID>/submissions
{
    date: date,
    maxScore: float,
    notebooks: [{
        feedbackUrl: string,
        name: string, # name of the notebook
        maxScore: float,
    }]
}


POST /api/v1/content/<ID>/submissions

GET /api/v1/content/<ID>/start
	only forward, HTTP 302 (temporary redirect, der Client sollte sich das nicht merken!)

GET /api/v1/user
{
    isAdmin: bool,
    created: date,
    lastActivity: date,
    name: string,
}


GET /api/v1/feedback/<ID>
	file download
