FROM python:3.7
USER root

COPY ./lib/requiremenst.txt /requiremenst.txt

RUN apt-get update

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt