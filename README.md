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

    docker-compose exec grader_notebook python3 autograde.py

Then, call the feedback batch script:

    docker-compose exec grader_notebook python3 feedback.py

If you have manual grading in your assignments, it will not create a feedback already.
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

## Backend

GET /api/v1/content/$ID

Show information for a given content from the database.
Can be accessed without authentication.

```
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
```


GET /api/v1/content/$ID/submission

Show the last submission for an authenticated user for this
specific content.
A submission can consist of multiple notebooks, each of them can have a distinct score.
If grading is still pending, the `graded` variable will be set to false.
If no submission was done, a 404 is returned.

In all cases, only the single latest submission is returned.
If an old submission was already graded and a new submission was submitted, only the new ungraded submission will be returned.

```
{
    date: date,
    maxScore: float,
    score: float,
    graded: boolean
    notebooks: [{
        feedbackUrl: string,
        name: string, # name of the notebook
        score: float,
        maxScore: float,
    }]
}
```


POST /api/v1/content/$ID/submission

Send a post to this endpoint to submit a new submission
for the given content.
The submission content is automatically fetched from `$USER_BASE_FOLDER/student_slug/assignment_slug`.

No grading will happen on submission.
See above on how to autograde and create feedback.


GET /api/v1/content/$ID/start

Redirect to the notebook (if already downloaded) or the specific git-link of this content.


GET /api/v1/user

Get information on an authenticated user.
```
{
    isAdmin: bool,
    created: date,
    lastActivity: date,
    name: string,
}
```


GET /api/v1/feedback/$ID

Download the feedback of a given ID if present.
Will return a pdf with the feedback.
This endpoint is used in the `feedbackUrl` of the submissions.