FROM python:3.8-slim-buster
WORKDIR /app
COPY . .
RUN pip3 install -U pip
# COPY requirements.txt /app
# WORKDIR /app
RUN pwd
RUN ls
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD python src/flask_app.py

#docker build -t flask-app/v0.0.1 -f docker/Dockerfile .
#docker run -d --name flask-1 --link mysql flask-app/v0.0.4