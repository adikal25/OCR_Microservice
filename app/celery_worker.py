import pytesseract
import os
from celery import Celery
from PIL import Image
from io import BytesIO
from .config import settings


celery_app= Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery_app.task(name="process_image")

def process_image(image_bytes: bytes) -> str:
    try:
        image=Image.open(BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error processing the image : {str(e)}"
    