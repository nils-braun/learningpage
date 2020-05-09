import os
import sys

# Add the backend service to our proxy (it is started in the docker-compose file)
c.JupyterHub.services = [
    {
        "name": "learningpage",
        "url": "http://backend:5000",
        "api_token": "very-secret-very-safe",
    }
]

# Make sure the API can be reached from the other containers (especially backend),
# as they need it for authorization
# Also make the port more explicit
# https://jupyterhub.readthedocs.io/en/stable/getting-started/networking-basics.html
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_port = 8081