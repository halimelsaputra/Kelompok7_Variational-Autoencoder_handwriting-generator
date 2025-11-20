# generator_api.py
import tensorflow as tf
import numpy as np
from PIL import Image

# Load model sekali aja
decoder = tf.keras.models.load_model("decoder.h5")

def generate_handwriting(latent_x, latent_y):
    """
    Input dari Frontend:
    - latent_x: float (-3.0 sampai 3.0)
    - latent_y: float (-3.0 sampai 3.0)
    
    Output:
    - numpy array gambar 28x28
    """
    z_sample = np.array([[latent_x, latent_y]])
    generated = decoder.predict(z_sample, verbose=0)
    return generated[0].squeeze()  # Return gambar 28x28


# Test fungsi
if __name__ == "__main__":
    img = generate_handwriting(0.5, -0.3)
    print(f"✅ Generate berhasil! Shape: {img.shape}")

    # Convert float image (0-1) → uint8 (0-255)
    img_uint8 = (img * 255).astype(np.uint8)

    # Simpan sebagai PNG
    image = Image.fromarray(img_uint8)
    image.save("test_generated.png")

    print("📁 File tersimpan: test_generated.png")
