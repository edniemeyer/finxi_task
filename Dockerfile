FROM python:3.6

ENV PYTHONBUFFERED 1

RUN mkdir /droidshop_app

WORKDIR /droidshop_app

ADD . /droidshop_app/

RUN pip install -r requirements.txt