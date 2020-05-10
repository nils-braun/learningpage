FROM jupyterhub/jupyterhub

RUN useradd grader \
    && echo "grader:grader" | chpasswd \
    && useradd student \
    && echo "student:student" | chpasswd

ADD jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py