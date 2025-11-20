import tensorflow as tf
from tensorflow.keras import layers, Model

# =================================================================
#  TUGAS BE 1: SI ARSITEK MODEL
#  File ini berisi definisi "Otak" robot (Encoder, Decoder, CVAE)
# =================================================================

latent_dim = 2  # "Ruang Imajinasi" (Sumbu X dan Y untuk Slider di Frontend)

# -----------------------------------------------------------------
# 1. MENENTUKAN BENTUK INPUT (Encoder)
#    Menerima: Gambar (28x28) DAN Label (0-9)
# -----------------------------------------------------------------
def build_cvae_encoder(latent_dim):
    # Input 1: Gambar Angka (Arsitektur CNN)
    img_input = layers.Input(shape=(28, 28, 1), name="image_input")
    x = layers.Conv2D(32, 3, activation="relu", strides=2, padding="same")(img_input)
    x = layers.Conv2D(64, 3, activation="relu", strides=2, padding="same")(x)
    x = layers.Flatten()(x) # Mengubah gambar jadi vektor datar

    # Input 2: Label Angka (One-hot vector ukuran 10)
    # Agar robot tahu ini angka berapa (0-9)
    label_input = layers.Input(shape=(10,), name="label_input")
    y = layers.Dense(16, activation="relu")(label_input) # Proses label sedikit

    # GABUNGKAN (Concatenate) Gambar + Label
    concat = layers.Concatenate()([x, y])

    # Proses gabungan menuju Latent Space
    x = layers.Dense(16, activation="relu")(concat)
    
    # Output Encoder: Mean, Log Var (Parameter distribusi)
    z_mean = layers.Dense(latent_dim, name="z_mean")(x)
    z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)

    # Sampling Layer (Rumus agar robot bisa berimajinasi)
    def sampling(args):
        z_mean, z_log_var = args
        epsilon = tf.random.normal(shape=tf.shape(z_mean))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

    z = layers.Lambda(sampling, name="z")([z_mean, z_log_var])

    # Bungkus jadi Model
    return Model([img_input, label_input], [z_mean, z_log_var, z], name="encoder")


# -----------------------------------------------------------------
# 2. MENENTUKAN BENTUK OUTPUT (Decoder)
#    Menerima: Latent Vector (Gaya) DAN Label (Angka)
# -----------------------------------------------------------------
def build_cvae_decoder(latent_dim):
    # Input 1: Latent Vector (Dari slider Frontend nanti)
    z_input = layers.Input(shape=(latent_dim,), name="z_input")

    # Input 2: Label Angka (Dari dropdown Frontend nanti)
    label_input = layers.Input(shape=(10,), name="label_input")

    # GABUNGKAN "Niat Gaya" (Z) + "Niat Angka" (Label)
    concat = layers.Concatenate()([z_input, label_input])

    # Kembalikan ke bentuk gambar (Kebalikan Encoder)
    x = layers.Dense(7 * 7 * 64, activation="relu")(concat)
    x = layers.Reshape((7, 7, 64))(x)

    x = layers.Conv2DTranspose(64, 3, activation="relu", strides=2, padding="same")(x)
    x = layers.Conv2DTranspose(32, 3, activation="relu", strides=2, padding="same")(x)
    
    # Output Akhir: Gambar 28x28 (Sigmoid agar nilai 0-1)
    decoder_output = layers.Conv2DTranspose(1, 3, activation="sigmoid", padding="same")(x)

    return Model([z_input, label_input], decoder_output, name="decoder")


# -----------------------------------------------------------------
# 3. MENENTUKAN RUMUS PINTAR (Loss Function)
#    Tugas BE 1: Menentukan cara robot menilai dirinya sendiri
# -----------------------------------------------------------------
class CVAE(Model):
    def __init__(self, encoder, decoder, **kwargs):
        super(CVAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        # Tracker untuk memantau performa
        self.total_loss_tracker = tf.keras.metrics.Mean(name="total_loss")
        self.recon_loss_tracker = tf.keras.metrics.Mean(name="reconstruction_loss")
        self.kl_loss_tracker = tf.keras.metrics.Mean(name="kl_loss")

    @property
    def metrics(self):
        return [self.total_loss_tracker, self.recon_loss_tracker, self.kl_loss_tracker]

    # Definisi Testing (Saat Validasi)
    def call(self, inputs):
        # inputs is a tuple: (images, labels)
        x_input, label_input = inputs
        z_mean, z_log_var, z = self.encoder([x_input, label_input])
        reconstruction = self.decoder([z, label_input])
        return reconstruction

    # Definisi Training (Saat Belajar)
    def train_step(self, data):
        # Data harus berupa tuple (gambar, label)
        if isinstance(data, tuple):
            data = data[0] # Keras kadang membungkus data
        
        # Pisahkan Gambar dan Label
        # Asumsi data masuk format: (batch_size, 28, 28, 1) dan (batch_size, 10)
        x_input = data[0] 
        label_input = data[1]

        with tf.GradientTape() as tape:
            # 1. Encoder: Gambar + Label -> Z
            z_mean, z_log_var, z = self.encoder([x_input, label_input])
            
            # 2. Decoder: Z + Label -> Gambar Rekonstruksi
            reconstruction = self.decoder([z, label_input])

            # 3. Hitung Error (LOSS FUNCTION)
            
            # a. Reconstruction Loss: Seberapa mirip gambar tiruan dgn asli?
            recon_loss = tf.reduce_mean(
                tf.reduce_sum(
                    tf.keras.losses.binary_crossentropy(x_input, reconstruction), axis=(1, 2)
                )
            )
            
            # b. KL Divergence: Hukuman jika imajinasi terlalu liar (agar rapi)
            kl_loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
            kl_loss = tf.reduce_mean(tf.reduce_sum(kl_loss, axis=1))

            total_loss = recon_loss + kl_loss

        # Update bobot otak robot
        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))

        # Lapor nilai error
        self.total_loss_tracker.update_state(total_loss)
        self.recon_loss_tracker.update_state(recon_loss)
        self.kl_loss_tracker.update_state(kl_loss)
        
        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.recon_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
        }

# =================================================================
#  VERIFIKASI ARSITEK (Hanya jalan kalau file ini di-run langsung)
# =================================================================
if __name__ == "__main__":
    print("🔵 [BE 1] Memeriksa Cetak Biru Arsitektur...")
    
    # Coba bangun Encoder & Decoder
    try:
        test_encoder = build_cvae_encoder(latent_dim)
        test_decoder = build_cvae_decoder(latent_dim)
        
        print("\n✅ ARSITEKTUR ENCODER BERHASIL DIBUAT:")
        test_encoder.summary()
        
        print("\n✅ ARSITEKTUR DECODER BERHASIL DIBUAT:")
        test_decoder.summary()
        
        print("\n🚀 KERJA BAGUS, ARSITEK! File ini siap diserahkan ke BE 2 (Trainer).")
    except Exception as e:
        print(f"\n❌ Ada kesalahan dalam arsitektur: {e}")