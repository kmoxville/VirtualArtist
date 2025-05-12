FROM nvidia/cuda:12.8.0-cudnn-runtime-ubuntu24.04
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    git

WORKDIR /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY ./speech_renderer /app
COPY ./shared /app/shared

ENV PYTHONPATH=/app

COPY ./speech_renderer/requirements.txt /app

RUN pip install torch==2.5.1+cu121 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121

RUN pip install --cache-dir=/tmp/pip_cache -r requirements.txt

CMD ["python", "main.py"]