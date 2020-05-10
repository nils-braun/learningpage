FROM python:3.8.2

RUN mkdir -p /var/lib/content \
    && chmod a+rw -R /var/lib/content

RUN useradd flask -d /home/flask -m -u 1000
USER flask

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD --chown=1000 . /app
WORKDIR /app
RUN chmod a+x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]