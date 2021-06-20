# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

# OS dependencies

# Application dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Source code
COPY . .


ENV FLASK_APP=ml_model_app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONDONTWRITEBYTECODE=1
EXPOSE 5000

CMD ["flask", "run"]