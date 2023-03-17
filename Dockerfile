# syntax=docker/dockerfile:1

FROM python:3.10-slim-bullseye
WORKDIR /app
RUN apt update; apt upgrade -y
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "run.py" ]
