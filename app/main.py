from fastapi import FastAPI, File, UploadFile, HTTPException
from celery.result import AsyncResult

app = FastAPI(title="OCR Microservice")

@app.post("/ocr/")
async def create_ocr_task(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image ")
    
    contents = await file.read()
    
    task=process_image.delay(contents)
    return {"task_id":task.id}

@app.get("/ocr/{task_id}")

async def get_ocr_result(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.ready():
        if task_result.successful():
            return {"status":"completed", "result": task_result.result}
        
        else:
            return {"status": "failed", "error": str(task_result.result)}
        
    return {"status":"processing"}