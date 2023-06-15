FROM python:3.10.0-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN python -m pip install -r requirements.txt

COPY ./kwg/ ./kwg/

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]