FROM python:3.11-slim

WORKDIR /app

COPY ./core /app
COPY ./shared /app/shared

ENV PYTHONPATH=/app

COPY ./core/requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]