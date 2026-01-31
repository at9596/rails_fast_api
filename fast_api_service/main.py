from fastapi import FastAPI, Response, UploadFile, File
from PIL import Image, ImageFilter
import pandas as pd
import io
import numpy as np
app = FastAPI()

@app.post("/process_image")
async def process_image(file: UploadFile = File(...)):
    # Read image into memory
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))

    # Perform a heavy operation (like a Gaussian Blur)
    process_imaged = img.filter(ImageFilter.GaussianBlur(radius=15))

    # Convert back to bytes to send to Rails
    img_byte_arr = io.BytesIO()
    # process_imaged.save(img_byte_arr, format='WEBP')
    process_imaged.save(img_byte_arr, format="PNG")

    # Return the raw image bytes instead of JSON
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")


@app.get("/compute")
def get_status():
    return {
        "status": "FastAPI is Online",
        "capabilities": ["Image Blurring", "Gaussian Filter"],
        "version": "1.0.0"
    }

@app.post("/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    
    # Filter for numeric columns
    numeric_df = df.select_dtypes(include=[np.number])
    
    if numeric_df.empty:
        return {"error": "No numeric columns found in this CSV."}

    column_name = numeric_df.columns[0]
    data = numeric_df[column_name].values

    return {
        "column_analyzed": column_name,
        "row_count": len(df),
        "mean": float(np.mean(data)),
        "std_dev": float(np.std(data)),
        "max": float(np.max(data)),
        "min": float(np.min(data))
    }
