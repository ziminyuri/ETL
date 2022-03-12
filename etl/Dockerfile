FROM python:3.9.6-alpine

WORKDIR /etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /etl/

RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
        pip install -r requirements.txt

COPY . .