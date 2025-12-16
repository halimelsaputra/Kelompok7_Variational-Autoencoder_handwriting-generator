# api_server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from io import BytesIO
from generator_api import generate_handwriting
from PIL import Image
import uvicorn

app = FastAPI()

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/generate")
def generate_image(latent_x: float, latent_y: float, digit_label: int):
    """Generate a handwriting sample from latent values and digit label."""
    print(f"[request] latent_x={latent_x}, latent_y={latent_y}, digit_label={digit_label}")

    if digit_label < 0 or digit_label > 9:
        raise HTTPException(status_code=400, detail="digit_label must be between 0 and 9")

    # 1. Generate image 28x28
    try:
        img = generate_handwriting(latent_x, latent_y, digit_label)
    except Exception as e:
        print(f"[error] generate_handwriting failed: {e}")
        raise HTTPException(status_code=500, detail="Model failed to generate image")

    if not isinstance(img, np.ndarray):
        raise HTTPException(status_code=500, detail="Model did not return an array")

    print(f"[generate] image shape: {img.shape}")

    # 2. Convert float -> uint8 (0-255)
    img_uint8 = (img * 255).astype(np.uint8)
    print(f"[convert] uint8 min={img_uint8.min()}, max={img_uint8.max()}")

    # 3. Convert to PNG in-memory
    pil_img = Image.fromarray(img_uint8)
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)
    print(f"[response] PNG size={buffer.getbuffer().nbytes} bytes")

    # 4. Send back as PNG stream
    return StreamingResponse(buffer, media_type="image/png")


@app.get("/health")
def health_check():
    """Simple health endpoint for readiness checks."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
