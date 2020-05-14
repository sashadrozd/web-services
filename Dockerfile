FROM python:3.7.7-stretch

COPY . /root

WORKDIR /root

RUN pip install flask gunicorn numpy sklearn scipy flask_wtf wtforms pandas


