FROM python:3.13-slim-bookworm AS base

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=on

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsm6 libxext6 tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml uv.lock README.md /app/

RUN uv sync --frozen

COPY . /app

CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
