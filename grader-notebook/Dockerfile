FROM jupyter/base-notebook

# Install nbgrader as additional dependency
# All needed extensions are automatically enabled
RUN conda install --quiet --yes \
    'nbgrader=0.6.1' && \
    conda clean --all -f -y && \
    npm cache clean --force && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER