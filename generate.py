import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# Load decoder
decoder = tf.keras.models.load_model("decoder.h5")

# Generate random latent points
z_sample = np.random.normal(size=(10, 2))  # 10 gambar random

# Generate images
generated_images = decoder.predict(z_sample)

# Plot hasil
fig, axes = plt.subplots(2, 5, figsize=(10, 4))
for i, ax in enumerate(axes.flat):
    ax.imshow(generated_images[i].squeeze(), cmap='gray')
    ax.axis('off')

plt.tight_layout()
plt.savefig('generated_samples.png')
print("✅ Gambar berhasil di-generate! Cek file 'generated_samples.png'")