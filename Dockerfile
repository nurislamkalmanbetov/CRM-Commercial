FROM python:3.8.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /iwex

COPY req.txt /iwex/

RUN pip install -r req.txt

COPY . .
