# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An OCR (Optical Character Recognition) microservice that extracts text from images asynchronously. It has two components:

- **Backend** (`ocr/`): FastAPI REST API with Celery workers for async OCR processing via PyTesseract
- **Frontend** (`frontend/`): Streamlit web UI for uploading images and viewing extracted text

## Architecture

The flow: Streamlit UI → FastAPI → Celery task (queued in Redis) → PyTesseract → result stored in Redis → polled by client.

### API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/ocr/` | Submit image, returns `{"task_id": "..."}` |
| `GET` | `/ocr/{task_id}` | Poll status: `processing` / `completed` / `failed` |
| `GET` | `/health` | Health check |

### Configuration

`ocr/config.py` uses pydantic-settings. Override via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | `localhost` | Redis hostname |
| `REDIS_PORT` | `6379` | Redis port |
| `CELERY_BROKER_URL` | `redis://localhost:6379/0` | Celery broker |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/0` | Celery result store |

## Code Structure

```
ocr/
  main.py          # FastAPI app: /ocr/ POST, /ocr/{task_id} GET, /health GET
  celery_worker.py # Celery app + process_image task (bytes → string via PyTesseract)
  config.py        # Pydantic settings for Redis/Celery URLs
frontend/
  app.py           # Streamlit UI: uploads image, polls backend for result
requirements.txt
```

## Development Setup

### Prerequisites

- Python 3.7+
- Redis running on `localhost:6379`
- Tesseract OCR installed ([installation guide](https://github.com/tesseract-ocr/tesseract))

### Install

```sh
pip install -r requirements.txt
```

### Run locally (three separate terminals)

```sh
# 1. Celery worker
celery -A ocr.celery_worker worker --loglevel=info

# 2. FastAPI backend
uvicorn ocr.main:app --reload --port 8000

# 3. Streamlit frontend
streamlit run frontend/app.py
```

### Run tests

```sh
pytest
```

## Key Dependencies

- **FastAPI** — REST API framework
- **Celery** — Distributed task queue for async OCR processing
- **Redis** — Celery broker and result backend
- **PyTesseract** — Python wrapper for Tesseract OCR engine
- **Pillow** — Image loading and pre-processing
- **Streamlit** — Frontend web UI
- **pydantic-settings** — Environment-variable-based configuration
- **uvicorn** — ASGI server for FastAPI

## Important Notes

- `process_image` receives raw image bytes and returns extracted text as a plain string
- The frontend polls `/ocr/{task_id}` every second until the task reaches `completed` or `failed`
- The Streamlit frontend assumes the backend runs on `http://localhost:8000`
- No `.env` file is committed; all configuration is via environment variables
