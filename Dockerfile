FROM python:2.7-slim

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD python -m dataland.scheduler
