import streamlit as st
import requests
import time
from PIL import Image
import io



st.set_page_config("OCR_Microservice_test", layout="wide")
st.title("OCR_Microservice_test")


def process_image(image_file):
    files={"file":("image.jpg", image_file,"image/jpeg")}
    response = requests.post("http://localhost:8000/ocr/", files=files)
    return response.json()['task_id']

def get_result(task_id):
    response = requests.get(f"http://localhost:8000/ocr/{task_id}")
    return response.json()


uploaded_file= st.file_uploader("Choose a image or a file to upload", type=["jpg","jpeg","png"])


if uploaded_file is not none:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded image")
    
    if st.button("Extract Text"):
        with st.spinner("Processing..."):
            uploaded_file.seek(0)
            task_id=process_image(uploaded_file.read())
            
            while True:
                result= get_result(task_id)
                if result["status"] == "completed":
                    st.success("Text extracted successfully")
                    st.text_area("Extracted Text:", value=result['result'])
                    break
                elif result['status'] == "failed":
                    st.error(f"Error: {result['error']}")
                    break
                time.sleep(1)