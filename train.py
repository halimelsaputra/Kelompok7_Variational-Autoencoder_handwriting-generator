import tensorflow as tf
from tensorflow.keras import layers, Model
import numpy as np
import os

# =====================================================
#  CONFIG
# =====================================================

image_shape = (28, 28, 1)
num_classes = 10
latent_dim = 2  # Dimensi latent space

# =====================================================
#  BUILD ENCODER (IMAGE + LABEL)
# =====================================================

def build_encoder(latent_dim):
    img_inputs = layers.Input(shape=image_shape, name="image_input")
    label_inputs = layers.Input(shape=(num_classes,), name="label_input")

    # Reshape label agar bisa digabung dengan gambar
    label_expanded = layers.Reshape((1, 1, num_classes))(label_inputs)
    
    # [PERBAIKAN 1] Menggunakan Lambda layer untuk tf.tile agar kompatibel dengan Keras 3+
    label_tiled = layers.Lambda(lambda x: tf.tile(x, [1, 28, 28, 1]))(label_expanded)

    # Gabungkan gambar dan label
    x = layers.Concatenate()([img_inputs, label_tiled])

    x = layers.Conv2D(32, 3, activation='relu', strides=2, padding='same')(x)
    x = layers.Conv2D(64, 3, activation='relu', strides=2, padding='same')(x)
    x = layers.Flatten()(x)

    z_mean = layers.Dense(latent_dim, name="z_mean")(x)
    z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)

    # Sampling trick
    def sampling(inputs):
        z_mean, z_log_var = inputs
        eps = tf.random.normal(shape=(tf.shape(z_mean)[0], latent_dim))
        return z_mean + tf.exp(0.5 * z_log_var) * eps

    z = layers.Lambda(sampling, name="z")([z_mean, z_log_var])

    return Model(inputs=[img_inputs, label_inputs], outputs=[z_mean, z_log_var, z], name="encoder")


# =====================================================
#  BUILD DECODER (LATENT + LABEL)
# =====================================================

def build_decoder(latent_dim):
    latent_inputs = layers.Input(shape=(latent_dim,), name="z_sampling")
    label_inputs = layers.Input(shape=(num_classes,), name="label_input")

    # Gabungkan latent + label
    x = layers.Concatenate()([latent_inputs, label_inputs])

    x = layers.Dense(7 * 7 * 64, activation='relu')(x)
    x = layers.Reshape((7, 7, 64))(x)

    x = layers.Conv2DTranspose(64, 3, activation='relu', strides=2, padding='same')(x)
    x = layers.Conv2DTranspose(32, 3, activation='relu', strides=2, padding='same')(x)
    outputs = layers.Conv2DTranspose(1, 3, activation='sigmoid', padding='same')(x)

    return Model(inputs=[latent_inputs, label_inputs], outputs=outputs, name="decoder")


# =====================================================
#  CONDITIONAL VAE MAIN CLASS
# =====================================================

class CVAE(Model):
    def __init__(self, encoder, decoder, **kwargs):
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        # Trackers untuk memantau loss
        self.total_loss_tracker = tf.keras.metrics.Mean(name="total_loss")
        self.recon_loss_tracker = tf.keras.metrics.Mean(name="reconstruction_loss")
        self.kl_loss_tracker = tf.keras.metrics.Mean(name="kl_loss")

    @property
    def metrics(self):
        return [
            self.total_loss_tracker,
            self.recon_loss_tracker,
            self.kl_loss_tracker,
        ]

    # [PERBAIKAN 2] Menambahkan method call() agar model lengkap
    def call(self, inputs):
        # inputs harus berupa list: [images, labels]
        if isinstance(inputs, (list, tuple)):
            images, labels = inputs[0], inputs[1]
        else:
            raise ValueError("Input harus berupa list/tuple [images, labels]")
            
        z_mean, z_log_var, z = self.encoder([images, labels])
        reconstruction = self.decoder([z, labels])
        return reconstruction

    # Training Step (Belajar)
    def train_step(self, data):
        # Unpack data (x, y)
        if isinstance(data, tuple):
            images, labels = data[0], data[1]
        else:
            images, labels = data

        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder([images, labels])
            reconstruction = self.decoder([z, labels])

            # Reconstruction Loss (Binary Crossentropy)
            reconstruction_loss = tf.reduce_mean(
                tf.reduce_sum(
                    tf.keras.losses.binary_crossentropy(images, reconstruction),
                    axis=(1, 2)
                )
            )

            # KL Divergence Loss
            kl_loss = -0.5 * tf.reduce_mean(
                tf.reduce_sum(
                    1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var),
                    axis=1
                )
            )

            total_loss = reconstruction_loss + kl_loss

        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))

        self.total_loss_tracker.update_state(total_loss)
        self.recon_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)

        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.recon_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
        }

    # [PERBAIKAN 3] Menambahkan test_step() untuk Validasi
    def test_step(self, data):
        if isinstance(data, tuple):
            images, labels = data[0], data[1]
        else:
            images, labels = data

        z_mean, z_log_var, z = self.encoder([images, labels])
        reconstruction = self.decoder([z, labels])

        reconstruction_loss = tf.reduce_mean(
            tf.reduce_sum(
                tf.keras.losses.binary_crossentropy(images, reconstruction),
                axis=(1, 2)
            )
        )

        kl_loss = -0.5 * tf.reduce_mean(
            tf.reduce_sum(
                1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var),
                axis=1
            )
        )

        total_loss = reconstruction_loss + kl_loss

        self.total_loss_tracker.update_state(total_loss)
        self.recon_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)

        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.recon_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
        }


# =====================================================
#  TRAINING SCRIPT
# =====================================================

if __name__ == "__main__":
    # Pastikan menggunakan CPU/GPU yang sesuai
    # os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # Uncomment jika ingin memaksa pakai CPU

    print("[INFO] Loading MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # Normalisasi data (0-1)
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0

    # Tambah dimensi channel (28, 28) -> (28, 28, 1)
    x_train = x_train[..., tf.newaxis]
    x_test = x_test[..., tf.newaxis]

    # Convert label ke One-Hot Encoding
    y_train = tf.keras.utils.to_categorical(y_train, num_classes)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes)

    # Bangun Model
    encoder = build_encoder(latent_dim)
    decoder = build_decoder(latent_dim)
    cvae = CVAE(encoder, decoder)

    # Compile
    cvae.compile(optimizer=tf.keras.optimizers.Adam())

    print("[INFO] Start training CVAE...")
    
    # [PERBAIKAN 4] Memisahkan x dan y agar masuk ke train_step sebagai tuple
    cvae.fit(
        x_train, y_train,
        epochs=30,
        batch_size=128,
        validation_data=(x_test, y_test)
    )

    print("[INFO] Saving models...")
    # Simpan model Encoder dan Decoder secara terpisah (lebih aman untuk VAE)
    encoder.save("conditional_encoder.h5")
    decoder.save("conditional_decoder.h5")

    print("[INFO] Training completed!")
    print("[INFO] Model saved as conditional_encoder.h5 & conditional_decoder.h5")