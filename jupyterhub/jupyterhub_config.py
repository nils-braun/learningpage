import os
import sys

# Make sure the API can be reached from the other containers (especially backend),
# as they need it for authorization
# Also make the port more explicit
# https://jupyterhub.readthedocs.io/en/stable/getting-started/networking-basics.html
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8081

# Define a group of users, which will have access to the grader notebook server below
c.JupyterHub.load_groups = {
    'graders': [
        'grader'
    ],
}

# Add the backend and grader-notebook service to our proxy (it is started in the docker-compose file)
c.JupyterHub.services = [
    {
        "name": "learningpage",
        "url": "http://backend:5000",
        "api_token": "very-secret-very-safe",
    },
    {
        'name': 'grader-notebook',
        'url': 'http://grader-notebook:8888',
        'api_token': 'even-more-secret-key',
        "oauth_client_id": "grader-notebook",
        "oauth_no_confirm": True,
    },
]
