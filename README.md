
# OCR Microservice

This is an OCR (Optical Character Recognition) microservice using **PyTesseract, Redis, Celery, and Streamlit**. It processes images to extract text asynchronously using Celery and provides a frontend using Streamlit.

## Features

- Asynchronous OCR processing using **Celery** and **Redis**
- Image text extraction using **PyTesseract**
- Streamlit-based web UI for easy image upload and text extraction
- Docker support for easy deployment

## Technologies Used

- **Python**
- **PyTesseract** (Tesseract OCR Engine)
- **Redis** (Message broker for Celery tasks)
- **Celery** (Task queue for asynchronous processing)
- **Streamlit** (Web frontend)

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Redis
- Tesseract OCR ([Installation Guide](https://github.com/tesseract-ocr/tesseract))

### Clone the Repository

```sh
git clone https://github.com/adikal25/OCR_Microservice.git
cd OCR_Microservice
```

### Set Up Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

### Start Redis Server

Ensure Redis is running before starting the Celery worker:

```sh
redis-server
```

### Start Celery Worker

```sh
celery -A app.celery_worker worker --loglevel=info
```

### Run the Streamlit App

```sh
streamlit run app/frontend/streamlit.py
```

## API Usage

### Submit an Image for OCR Processing

Send an image to the backend for processing:

```sh
POST /process
Content-Type: multipart/form-data
```

Example using `cURL`:

```sh
curl -X POST -F "file=@image.png" http://localhost:5000/process
```

### Check OCR Task Status

```sh
GET /status/<task_id>
```

Example:

```sh
curl http://localhost:5000/status/12345
```

### Get Extracted Text

```sh
GET /result/<task_id>
```

## Docker Support

To run the entire microservice using Docker:

```sh
docker-compose up --build
```

## License

This project is licensed under the MIT License.

---

**Contributors:** [Your Name]


