FROM python:3.11-slim

WORKDIR /app

COPY ./chat_engine /app
COPY ./shared /app/shared

ENV PYTHONPATH=/app

COPY ./chat_engine/requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]