FROM jupyterhub/jupyterhub

RUN useradd -d /home/grader -m grader \
    && echo "grader:grader" | chpasswd \
    && useradd -d /home/student -m student \
    && echo "student:student" | chpasswd \
    && pip install notebook

ADD jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py