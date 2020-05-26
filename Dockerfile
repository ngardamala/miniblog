FROM python:3-alpine

RUN adduser -D miniblog

WORKDIR /home/miniblog

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY config.py manage.py boot.sh ./

RUN chown -R miniblog:miniblog ./
RUN chmod a+x boot.sh

USER miniblog

EXPOSE 8000

ENTRYPOINT ["./boot.sh"]
