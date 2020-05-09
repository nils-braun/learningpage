#!/usr/bin/env bash
set -e

# 0. Make sure we can access the pip-installed binaries
export PATH="/home/flask/.local/bin/:$PATH"

# 1. Make sure the database is ready
flask db upgrade

# 2. Now start the application
exec uwsgi --ini app.ini