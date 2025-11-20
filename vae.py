import tensorflow as tf
from tensorflow.keras import layers, Model

# Layer untuk melakukan sampling dari distribusi Gaussian menggunakan reparameterization trick
class Sampling(layers.Layer):
    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]          # ukuran batch
        dim = tf.shape(z_mean)[1]            # dimensi latent
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))  # noise acak
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon  # rumus reparameterization trick

# Fungsi untuk membangun arsitektur Variational Autoencoder (VAE)
def build_vae(latent_dim=2):
    # ----------------------------
    # ENCODER
    # ----------------------------
    encoder_inputs = layers.Input(shape=(28, 28, 1))  # input gambar MNIST
    x = layers.Flatten()(encoder_inputs)               # meratakan gambar
    x = layers.Dense(256, activation="relu")(x)       # hidden layer 1
    x = layers.Dense(128, activation="relu")(x)       # hidden layer 2
    z_mean = layers.Dense(latent_dim, name="z_mean")(x)        # mean distribusi latent
    z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)  # log-variance distribusi latent
    z = Sampling()([z_mean, z_log_var])                # sampling variabel latent

    encoder = Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")

    # ----------------------------
    # DECODER
    # ----------------------------
    latent_inputs = layers.Input(shape=(latent_dim,))
    x = layers.Dense(128, activation="relu")(latent_inputs)      # hidden layer decoder 1
    x = layers.Dense(256, activation="relu")(x)                  # hidden layer decoder 2
    x = layers.Dense(28 * 28, activation="sigmoid")(x)          # output rekonstruksi (flatten)
    decoder_outputs = layers.Reshape((28, 28, 1))(x)              # reshape kembali ke bentuk gambar

    decoder = Model(latent_inputs, decoder_outputs, name="decoder")

    # -----------------------------------------
    # KELAS UTAMA VAE (untuk custom training loop)
    # -----------------------------------------
    class VAE(Model):
        def __init__(self, encoder, decoder, **kwargs):
            super(VAE, self).__init__(**kwargs)
            self.encoder = encoder
            self.decoder = decoder

            # tracker untuk memonitor loss selama training
            self.total_loss_tracker = tf.keras.metrics.Mean(name="total_loss")
            self.reconstruction_loss_tracker = tf.keras.metrics.Mean(name="reconstruction_loss")
            self.kl_loss_tracker = tf.keras.metrics.Mean(name="kl_loss")

        # daftar metrik yang akan ditampilkan
        @property
        def metrics(self):
            return [self.total_loss_tracker, self.reconstruction_loss_tracker, self.kl_loss_tracker]

        # custom training step
        def train_step(self, data):
            with tf.GradientTape() as tape:
                # encoding: menghasilkan z_mean, z_log_var, dan sample z
                z_mean, z_log_var, z = self.encoder(data)

                # decoding: rekonstruksi gambar
                reconstruction = self.decoder(z)

                # menghitung reconstruction loss
                reconstruction_loss = tf.reduce_mean(
                    tf.reduce_sum(
                        tf.keras.losses.binary_crossentropy(data, reconstruction), axis=(1, 2)
                    )
                )

                # menghitung KL divergence loss (regularisasi latent space)
                kl_loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
                kl_loss = tf.reduce_mean(tf.reduce_sum(kl_loss, axis=1))

                # total loss = reconstruction + KL divergence
                total_loss = reconstruction_loss + kl_loss

            # menghitung dan menerapkan gradient
            grads = tape.gradient(total_loss, self.trainable_weights)
            self.optimizer.apply_gradients(zip(grads, self.trainable_weights))

            # update nilai metrik
            self.total_loss_tracker.update_state(total_loss)
            self.reconstruction_loss_tracker.update_state(reconstruction_loss)
            self.kl_loss_tracker.update_state(kl_loss)

            # mengembalikan log metrik
            return {
                "loss": self.total_loss_tracker.result(),
                "reconstruction_loss": self.reconstruction_loss_tracker.result(),
                "kl_loss": self.kl_loss_tracker.result(),
            }

    vae = VAE(encoder, decoder)  # membangun objek VAE
    return vae, encoder, decoder
