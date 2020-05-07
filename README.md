# Learn-Page

Bringing a frontpage to jupyterhub.

## Backend

GET /api/v1/content/<ID>
{
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
    maxScore: float,  # 0 <= max_score <= 1
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
    feedbackUrl: string,
    score: float,
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
