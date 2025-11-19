import tensorflow as tf
from tensorflow.keras import layers, Model

# =================================================

# Variational Autoencoder (VAE)

# =================================================

class Sampling(layers.Layer):
"""Reparameterization: z = mean + exp(log_var / 2) * epsilon"""
def call(self, inputs):
z_mean, z_log_var = inputs
epsilon = tf.random.normal(shape=tf.shape(z_mean))
return z_mean + tf.exp(0.5 * z_log_var) * epsilon

def build_vae(latent_dim=2):

```
# =================================================
#  Encoder
# =================================================
encoder_inputs = layers.Input(shape=(28, 28, 1))

x = layers.Flatten()(encoder_inputs)
x = layers.Dense(256, activation="relu")(x)
x = layers.Dense(128, activation="relu")(x)

z_mean = layers.Dense(latent_dim, name="z_mean")(x)
z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)

z = Sampling()([z_mean, z_log_var])

encoder = Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")


# =================================================
#  Decoder
# =================================================
latent_inputs = layers.Input(shape=(latent_dim,))
x = layers.Dense(128, activation="relu")(latent_inputs)
x = layers.Dense(256, activation="relu")(x)
x = layers.Dense(28 * 28, activation="sigmoid")(x)
decoder_outputs = layers.Reshape((28, 28, 1))(x)

decoder = Model(latent_inputs, decoder_outputs, name="decoder")


# =================================================
#  VAE Model (Custom training step)
# =================================================
class VAE(Model):
    def __init__(self, encoder, decoder, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder

    def train_step(self, data):
        if isinstance(data, tuple):
            data = data[0]

        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder(data)
            reconstruction = self.decoder(z)

            # Reconstruction loss
            reconstruction_loss = tf.reduce_mean(
                tf.keras.losses.binary_crossentropy(data, reconstruction)
            ) * 28 * 28

            # KL Divergence loss
            kl_loss = -0.5 * tf.reduce_sum(
                1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var)
            )

            total_loss = reconstruction_loss + kl_loss

        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))

        return {
            "loss": total_loss,
            "reconstruction_loss": reconstruction_loss,
            "kl_loss": kl_loss,
        }

vae = VAE(encoder, decoder)
return vae, encoder, decoder
```
