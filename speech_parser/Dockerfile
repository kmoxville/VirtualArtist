FROM nvidia/cuda:12.8.0-cudnn-runtime-ubuntu24.04
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    ffmpeg \
    python3-dev \
    build-essential \
    portaudio19-dev

WORKDIR /app

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY ./speech_parser /app
COPY ./shared /app/shared

ENV PYTHONPATH=/app

COPY ./speech_parser/requirements.txt /app

RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
RUN pip install --cache-dir=/tmp/pip_cache -r requirements.txt

CMD ["python", "main.py"]