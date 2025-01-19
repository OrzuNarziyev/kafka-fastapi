FROM python:3.12 as base
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN apt-get update
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /code/
