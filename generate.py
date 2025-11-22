import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 1. Load model yang BENAR
decoder = tf.keras.models.load_model("conditional_decoder.h5", compile=False)

# 2. Tentukan Angka yang mau digambar (Misal mau angka 7)
angka_target = 7 
num_samples = 10

# 3. Buat One-Hot Encoding untuk label
label_input = np.zeros((num_samples, 10))
label_input[:, angka_target] = 1.0  # Set kolom ke-7 jadi 1

# 4. Generate Latent Space Random (Variasi Gaya)
z_sample = np.random.normal(size=(num_samples, 2))

# 5. Generate Gambar (Inputnya DUA: Z dan Label)
generated_images = decoder.predict([z_sample, label_input], verbose=0)

# 6. Plotting
fig, axes = plt.subplots(2, 5, figsize=(10, 4))
fig.suptitle(f'Hasil Generate Angka {angka_target} dengan Gaya Random', fontsize=16)

for i, ax in enumerate(axes.flat):
    ax.imshow(generated_images[i].squeeze(), cmap='gray')
    ax.axis('off')

plt.tight_layout()
plt.savefig('manual_test_result.png')
print("✅ Gambar berhasil disimpan di 'manual_test_result.png'")