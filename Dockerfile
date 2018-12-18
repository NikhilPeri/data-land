FROM python:2.7-slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app

# RUN apt-get upgrade; apt-get update
RUN pip install --upgrade pip; pip install -r requirements.txt

COPY . /app
RUN mkdir logs
CMD []
