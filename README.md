# Learn-Page

Bringing a frontpage to jupyterhub.

## Quickstart

Start all components:

    docker-compose up -d

### Prepare the database

Create a test database entry for "my_course"

    docker-compose exec backend python3 populate_database.py

And an nbgrader assignment for this course (you can also do this via the web UI with the user:password grader:grader)

    docker-compose exec grader-notebook nbgrader generate_assignment my_course

The notebook files for this assignment are already preinstalled in the running container.

### Test the API

Log into the jupyterhub instance at http://127.0.0.1:8000 with "student:student".
After login, you should be able to access the API, e.g. under

    http://127.0.0.1:8000/services/learningpage/api/v1/content/my_course

or

    http://127.0.0.1:8000/services/learningpage/api/v1/user

However, you will not have any submission already:

    http://127.0.0.1:8000/services/learningpage/api/v1/content/my_course/submissions

### Do a submission

An example submission file is already preinstalled in the container, you just need to copy it:

    docker-compose exec jupyterhub cp /example/student/my_course /home/student/my_course -r

Call a POST on

    http://127.0.0.1:8000/services/learningpage/api/v1/content/pandas-io/submissions

with the correct cookie.
Now you will see submissions showing up, but without grade so far.

    http://127.0.0.1:8000/services/learningpage/api/v1/content/my_course/submissions

Do the batch autograding

    docker-compose exec grader-notebook python3 -m grading.autograde

Then, call the feedback batch script:

    docker-compose exec grader_notebook python3 -m grading.feedback

If you have manual grading in your assignments, it will not create a feedback already.
Log in with "grader:grader" (you might need to logout again) and go to

    http://127.0.0.1:8000/services/grader-notebook/formgrader/

to do the grading.

After that, call the feedback script again.

Now, the shown submissions on (for "student:student")

    http://127.0.0.1:8000/services/learningpage/api/v1/content/my_course/submissions

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