# generator_api.py
import tensorflow as tf
import numpy as np

# Global cache
model_cache = None

# Konfigurasi model
LATENT_DIM = 2
NUM_CLASSES = 10


# Bangun ulang arsitektur decoder agar tidak perlu deserialisasi penuh (hindari masalah kompatibilitas Keras)
def _build_decoder(latent_dim=LATENT_DIM, num_classes=NUM_CLASSES):
    latent_inputs = tf.keras.layers.Input(shape=(latent_dim,), name="z_sampling")
    label_inputs = tf.keras.layers.Input(shape=(num_classes,), name="label_input")

    x = tf.keras.layers.Concatenate()([latent_inputs, label_inputs])
    x = tf.keras.layers.Dense(7 * 7 * 64, activation="relu")(x)
    x = tf.keras.layers.Reshape((7, 7, 64))(x)
    x = tf.keras.layers.Conv2DTranspose(64, 3, activation="relu", strides=2, padding="same")(x)
    x = tf.keras.layers.Conv2DTranspose(32, 3, activation="relu", strides=2, padding="same")(x)
    outputs = tf.keras.layers.Conv2DTranspose(1, 3, activation="sigmoid", padding="same")(x)

    return tf.keras.Model(inputs=[latent_inputs, label_inputs], outputs=outputs, name="decoder")


def load_decoder():
    global model_cache
    if model_cache is None:
        try:
            decoder = _build_decoder()
            # Muat bobot dari file H5 (lebih toleran terhadap versi Keras berbeda)
            decoder.load_weights("conditional_decoder.h5")
            model_cache = decoder
            print("[load] Model CVAE Decoder berhasil dimuat via load_weights!")
        except Exception as e:
            print(f"[error] Error loading model weights: {e}")
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
    label_input = np.zeros((1, NUM_CLASSES))
    label_input[0, digit_label] = 1.0

    # 3. Prediksi (Kirim 2 input sekaligus: [Latent, Label])
    generated = decoder.predict([z_sample, label_input], verbose=0)

    return generated[0].squeeze()
