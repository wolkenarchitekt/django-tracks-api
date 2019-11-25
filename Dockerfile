FROM python:3.7.3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ARG CHROMAPRINT_VER=1.4.3
ARG CHROMAPRINT_ARCH=linux-x86_64

RUN apt-get update \
    && apt-get install -y sqlite3 bash-completion python-rgain ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN pip3 install --upgrade pip setuptools

# fpcalc for audio finger printing
RUN wget https://github.com/acoustid/chromaprint/releases/download/v${CHROMAPRINT_VER}/chromaprint-fpcalc-${CHROMAPRINT_VER}-${CHROMAPRINT_ARCH}.tar.gz -O /tmp/chromaprint-fpcalc-${CHROMAPRINT_VER}-${CHROMAPRINT_ARCH}.tar.gz \
    && tar xzf /tmp/chromaprint-fpcalc-${CHROMAPRINT_VER}-${CHROMAPRINT_ARCH}.tar.gz -C /tmp \
    && mv /tmp/chromaprint-fpcalc-${CHROMAPRINT_VER}-${CHROMAPRINT_ARCH}/fpcalc /usr/local/bin

WORKDIR /code
COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements-dev.txt

COPY . /code
RUN python3 setup.py install

EXPOSE 8000

CMD gunicorn tracks.wsgi --bind 0.0.0.0:8000 --reload --timeout 300
