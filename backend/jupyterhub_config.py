import os
import sys

c.JupyterHub.services = [
    {
        "name": "learningpage",
        "url": "http://127.0.0.1:10101",
        "command": ["flask", "run", "--port=10101"],
        "environment": {"FLASK_APP": "app.py", "FLASK_DEBUG": "1"},
    }
]
