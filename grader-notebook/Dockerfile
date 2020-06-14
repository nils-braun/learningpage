FROM jupyter/base-notebook

# Install nbgrader as additional dependency
# All needed extensions are automatically enabled
RUN conda install --quiet --yes \
    'nbgrader' \
    'psycopg2' && \
    conda clean --all -f -y && \
    npm cache clean --force && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

RUN mkdir -p //home/$NB_USER/content \
    && chmod a+rw -R //home/$NB_USER/content

ADD nbgrader_config.py .
ADD grading .

ENTRYPOINT [ "jupyterhub-singleuser" ]
CMD [ "--group=graders" ]