from fastapi import FastAPI, Response, UploadFile, File, Body, HTTPException
import ollama
from pydantic import BaseModel
from services.config import APP_METADATA
from services.data_service import DataService
from services.image_service import ImageService
from services.ai_service import AIService
app = FastAPI()

class LlamaRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate(request: LlamaRequest):
    text_result = AIService.generate_response(request.prompt)
    
    return {"text": text_result}

@app.post("/chat")
async def chat(messages: list = Body(...)):
    # Expects format: [{"role": "user", "content": "hello"}]
    response = ollama.chat(
        model='llama3.2',
        messages=messages
    )
    return {"message": response['message']['content']}

@app.post("/process_image")
async def process_image(file: UploadFile = File(...)):
    image_data = await file.read()

    processed_bytes = ImageService.apply_gaussian_blur(image_data)

    return Response(content=processed_bytes, media_type="image/png")

@app.get("/compute")
def get_status():
    return APP_METADATA

@app.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    result = DataService.get_column_statistics(file.file)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result