FROM python:3.11-slim

WORKDIR /app

COPY ./core /app
COPY ./shared /app/shared

ENV PYTHONPATH=/app

COPY ./core/requirements.txt /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-server-dev-all \
    libpq-dev \
    ffmpeg

RUN pip install wheel
RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]