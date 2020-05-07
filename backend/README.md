## How to start the backend

1. Create conda environment and install packages

    conda create -p .conda-env --file conda.yaml
    conda activate .conda-env/

2. Do a database update (which will initially create the database)

    flask db upgrade

3. Prepopulate the database, if you want

    python3 populate_database.py

4. Now start jupyterhub

    jupyterhub

5. You can access the service at http://127.0.0.1:8000/services/learningpage/api/v1/user
   or http://127.0.0.1:8000/services/learningpage/api/v1/content/text

   Before that, you need to login: http://127.0.0.1:8000/