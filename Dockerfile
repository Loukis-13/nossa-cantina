FROM python:3.11-alpine
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
