FROM python:3.7.4-slim

ENV PYTHONUNBUFFERED="true"

WORKDIR /app

COPY requirements.txt .
COPY requirements-dev.txt .

# Suppress pip upgrade warning
COPY pip.conf /root/.config/pip/pip.conf

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY . .

RUN pip install .
