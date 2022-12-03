# syntax=docker/Dockerfile:1
# docker build --tag settle-regulation-torch-pythonflask .

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
ADD /uploads /uploads/
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "-b" , ":5000", "app:create_app()"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]