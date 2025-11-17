import tensorflow as tf
from tensorflow.keras.datasets import mnist
from vae import VAE  # import arsitektur VAE dari vae.py

# ======================
# 1. Loading Dataset MNIST  
# ======================
(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

x_train = x_train.reshape(-1, 28, 28, 1)
x_test  = x_test.reshape(-1, 28, 28, 1)

print("Training data:", x_train.shape)
print("Testing data:", x_test.shape)

# ======================
# 2. Inisialisasi Model VAE
# ======================
vae = VAE(latent_dim=2)

# ======================
# 3. Training
# ======================
vae.compile(optimizer=tf.keras.optimizers.Adam())
vae.fit(x_train, epochs=20, batch_size=128)

# ======================
# 4. Save Hasil (ke folder /results)
# ======================
vae.save_results(x_test)
