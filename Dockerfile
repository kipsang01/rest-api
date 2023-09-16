FROM python:3.10-slim-buster
LABEL authors="kipsang"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBIAN_FRONTEND noninteractive


RUN pip install --no-cache-dir --upgrade pip
RUN pip install gunicorn==20.1.0

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Moving application files
WORKDIR /app
COPY . /app

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]