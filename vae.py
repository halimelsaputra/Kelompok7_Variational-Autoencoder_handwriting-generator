import tensorflow as tf
from tensorflow.keras import layers, Model

# =================================================

# Variational Autoencoder (VAE) Implementation

# =================================================

class Sampling(layers.Layer):
"""
Custom layer for reparameterization trick.
Fungsi ini mengambil mean (z_mean) dan log_variance (z_log_var)
lalu melakukan sampling:
z = mean + std * epsilon
supaya proses sampling tetap dapat dilakukan backpropagation.
"""
def call(self, inputs):
z_mean, z_log_var = inputs

```
    # Sampling noise dari distribusi normal
    epsilon = tf.random.normal(shape=tf.shape(z_mean))
    
    # Reparameterization trick
    return z_mean + tf.exp(0.5 * z_log_var) * epsilon
```

def build_vae(latent_dim=2):
"""
Fungsi utama untuk membangun arsitektur VAE:
- Encoder
- Decoder
- Custom training loop
"""

```
# =================================================
#  ENCODER
# =================================================
# Input gambar 28x28 grayscale (1 channel)
encoder_inputs = layers.Input(shape=(28, 28, 1))

# Flatten → mengubah data 2D menjadi 1D vektor
x = layers.Flatten()(encoder_inputs)

# Fully connected layers untuk mengekstraksi fitur
x = layers.Dense(256, activation="relu")(x)
x = layers.Dense(128, activation="relu")(x)

# Encoder menghasilkan dua output:
# z_mean → mean dari distribusi latent
# z_log_var → log variance dari distribusi latent
z_mean = layers.Dense(latent_dim, name="z_mean")(x)
z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)

# Sampling z dari z_mean dan z_log_var
z = Sampling()([z_mean, z_log_var])

# Membuat model encoder
encoder = Model(
    encoder_inputs,
    [z_mean, z_log_var, z],
    name="encoder"
)


# =================================================
#  DECODER
# =================================================
# Input berupa vector z dari latent space
latent_inputs = layers.Input(shape=(latent_dim,))

# Fully connected layers untuk mengembalikan fitur menjadi gambar
x = layers.Dense(128, activation="relu")(latent_inputs)
x = layers.Dense(256, activation="relu")(x)

# Output layer menyusun kembali menjadi ukuran 28×28
# Sigmoid digunakan karena pixel bernilai 0–1
x = layers.Dense(28 * 28, activation="sigmoid")(x)

# Reshape ke format gambar
decoder_outputs = layers.Reshape((28, 28, 1))(x)

# Membuat model decoder
decoder = Model(
    latent_inputs,
    decoder_outputs,
    name="decoder"
)


# =================================================
#  MODEL VAE DENGAN CUSTOM TRAINING 
# =================================================
class VAE(Model):
    """
    Custom Model class agar dapat mengatur loss function sendiri:
    - Reconstruction Loss
    - KL Divergence Loss
    """
    def __init__(self, encoder, decoder, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder

    def train_step(self, data):
        """
        Custom training step:
        1. Encode data → dapatkan mean & log_var
        2. Sample latent vector z
        3. Decode kembali menjadi gambar
        4. Hitung total loss = Reconstruction + KL Loss
        """
        if isinstance(data, tuple):
            data = data[0]

        # Record gradient
        with tf.GradientTape() as tape:
            # Forward pass
            z_mean, z_log_var, z = self.encoder(data)
            reconstruction = self.decoder(z)

            # ---------------------------------------------------------
            # Reconstruction Loss
            # ---------------------------------------------------------
            # Mengukur seberapa mirip output dengan input
            reconstruction_loss = tf.reduce_mean(
                tf.keras.losses.binary_crossentropy(data, reconstruction)
            ) * 28 * 28  # skala agar loss lebih stabil

            # ---------------------------------------------------------
            # KL Divergence Loss
            # ---------------------------------------------------------
            # Memaksa distribusi latent mendekati Gaussian standar
            kl_loss = -0.5 * tf.reduce_sum(
                1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var)
            )

            # Total Loss VAE
            total_loss = reconstruction_loss + kl_loss

        # Hitung dan terapkan gradien
        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))

        # Nilai yang ditampilkan saat training
        return {
            "loss": total_loss,
            "reconstruction_loss": reconstruction_loss,
            "kl_loss": kl_loss,
        }

# Instance model VAE lengkap
vae = VAE(encoder, decoder)

# Mengembalikan ketiga komponen penting
return vae, encoder, decoder
```
