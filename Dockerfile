# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

# OS dependencies
RUN apt-get update -y
RUN apt-get -y install libsndfile1-dev

# Application dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Source code
COPY . .

CMD ["python3", "model/preprocessing.py"]