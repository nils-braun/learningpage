FROM jupyterhub/jupyterhub

RUN useradd grader \
    && echo "grader:grader" | chpasswd \
    && useradd student \
    && echo "student:student" | chpasswd
