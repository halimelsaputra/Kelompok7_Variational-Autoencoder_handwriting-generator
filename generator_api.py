# generator_api.py
import tensorflow as tf
import numpy as np

# Global cache
model_cache = None

def load_decoder():
    global model_cache
    if model_cache is None:
        try:
            # PERHATIKAN: Nama filenya berubah jadi conditional_decoder.h5
            model_cache = tf.keras.models.load_model("conditional_decoder.h5", compile=False)
            print("✅ Model CVAE Decoder berhasil dimuat!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return None
    return model_cache

def generate_handwriting(latent_x, latent_y, digit_label):
    """
    Input:
    - latent_x, latent_y: Float (Posisi Slider)
    - digit_label: Integer (Angka 0-9 dari Dropdown)
    """
    decoder = load_decoder()
    
    if decoder is None:
        return np.zeros((28, 28))

    # 1. Siapkan Latent Vector (Input 1)
    z_sample = np.array([[latent_x, latent_y]])

    # 2. Siapkan One-Hot Encoding untuk Label (Input 2)
    # Model meminta array sepanjang 10 angka (misal angka 3 = [0,0,0,1,0,0,0,0,0,0])
    label_input = np.zeros((1, 10))
    label_input[0, digit_label] = 1.0

    # 3. Prediksi (Kirim 2 input sekaligus: [Latent, Label])
    generated = decoder.predict([z_sample, label_input], verbose=0)
    
    return generated[0].squeeze()