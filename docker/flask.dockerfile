from python:3.7.2-stretch

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt