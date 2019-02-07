FROM python:3.7

ADD ./application/requirements.txt /deploy/requirements.txt

WORKDIR /deploy

RUN pip install --upgrade pip && pip install -r requirements.txt
