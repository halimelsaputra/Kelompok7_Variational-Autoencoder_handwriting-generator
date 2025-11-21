# api_server.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import numpy as np
from io import BytesIO
from generator_api import generate_handwriting
from PIL import Image

app = FastAPI()

@app.get("/generate")
def generate_image(latent_x: float, latent_y: float):
    # 1. Generate image 28x28
    img = generate_handwriting(latent_x, latent_y)

    # 2. Convert float -> uint8 (0-255)
    img_uint8 = (img * 255).astype(np.uint8)

    # 3. Convert ke PNG dalam memory
    pil_img = Image.fromarray(img_uint8)
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)

    # 4. Kirim balik sebagai file PNG
    return StreamingResponse(buffer, media_type="image/png")
