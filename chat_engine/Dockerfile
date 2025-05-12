FROM python:3.11-slim

WORKDIR /app

COPY ./chat_engine /app
COPY ./shared /app/shared

ENV PYTHONPATH=/app

COPY ./chat_engine/requirements.txt /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-server-dev-all \
    libpq-dev

RUN pip install wheel
RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]