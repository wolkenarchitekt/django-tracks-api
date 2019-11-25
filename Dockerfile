FROM python:3.7.4-slim

ENV PYTHONUNBUFFERED="true"

WORKDIR /app

COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY . .

RUN pip install .
