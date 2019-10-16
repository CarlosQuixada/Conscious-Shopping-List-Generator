FROM python:3.7-slim

MAINTAINER Carlos Quixadá

ADD requirements.txt /app/requirements.txt

EXPOSE 5000

WORKDIR /app

RUN python3.7 -m pip install -r requirements.txt

ADD . /app

RUN mkdir logs

CMD ["python3.7", "run.py"]
