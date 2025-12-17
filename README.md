# Generasi Tulisan Tangan Menggunakan Variational Autoencoder (VAE)

**<h3>Kelompok 7 - Mata Kuliah Kecerdasan Artifisial<h3/>**

**Anggota Kelompok**

| Nama | NIM |
|------|-----|
| Tinsari Rauhana | 2308107010038 |
| Faris Zain As-Shadiq | 2308107010039 |
| Halim Elsa Putra | 2308107010062 |
| Yuyun Nailufar | 2308107010066 |

---

## Tentang Proyek

Proyek ini merupakan implementasi **Conditional Variational Autoencoder (CVAE)** untuk menghasilkan gambar tulisan tangan angka (0-9) dari dataset MNIST. Sistem ini memungkinkan pengguna untuk mengontrol angka yang dihasilkan serta variasi gaya tulisan melalui manipulasi latent space secara real-time menggunakan antarmuka web interaktif.

### Fitur Utama

1. **Conditional Generation**: Pengguna dapat memilih angka spesifik (0-9) yang ingin dihasilkan
2. **Style Control**: Manipulasi gaya tulisan melalui latent space 2D menggunakan slider
3. **Web Interface**: Antarmuka berbasis web yang mudah digunakan
4. **Real-time Generation**: Generate gambar secara langsung berdasarkan input pengguna
5. **Download Feature**: Menyimpan hasil generasi gambar


## Teknologi yang Digunakan

### Backend
- **Python 3.8+**: Bahasa pemrograman utama
- **TensorFlow 2.x**: Framework deep learning
- **Keras**: High-level API untuk building neural networks
- **FastAPI**: Modern web framework untuk REST API
- **Uvicorn**: ASGI server untuk FastAPI
- **NumPy**: Library untuk komputasi numerik
- **Pillow (PIL)**: Library untuk pemrosesan gambar
- **Matplotlib**: Library untuk visualisasi data

### Frontend
- **React 18+**: Library JavaScript untuk membangun user interface
- **Vite**: Build tool dan development server
- **Node.js & npm**: Runtime dan package manager

### Tools
- **Visual Studio Code**: Editor kode
- **Git & GitHub**: Version control dan kolaborasi

---

## Struktur Proyek

```
Kelompok7_Variational-Autoencoder_handwriting-generator/
│
├── main.py                          # Entry point backend server
├── train.py                         # Script untuk training model CVAE
├── api_server.py                    # FastAPI server implementation
├── generator_api.py                 # Model loader dan generator function
├── generate.py                      # Script testing manual
├── vae.py                           # PyTorch implementation (referensi)
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore configuration
├── README.md                        # Dokumentasi proyek
├── conditional_decoder.h5           # Pre-trained decoder model
├── conditional_encoder.h5           # Pre-trained encoder model
|
├── results/                         # Folder output hasil (git ignored)
│   └── reconstructions.png
│   └── manual_test_result.png
│
└── web/                             # Frontend React application
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── src/
    │   ├── App.jsx
    │   ├── main.jsx
    │   ├── components/
    │   └── styles/
    └── public/
```

---

## Instalasi

### Prerequisites

Pastikan sistem Anda sudah terinstall:
- Python 3.8 atau lebih tinggi
- Node.js 16+ dan npm
- pip (Python package manager)
- Git (untuk clone repository)

### Langkah 1: Clone Repository

```bash
git clone https://github.com/halimelsaputra/Kelompok7_Variational-Autoencoder_handwriting-generator
cd Kelompok7_Variational-Autoencoder_handwriting-generator
```

### Langkah 2: Setup Backend

#### Membuat Virtual Environment (Disarankan)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install Dependencies Python

```bash
pip install -r requirements.txt
```

File `requirements.txt` berisi:
```
fastapi
uvicorn[standard]
numpy
pillow
tensorflow
matplotlib
```

### Langkah 3: Setup Frontend

Masuk ke folder web dan install dependencies:

```bash
cd web
npm install
```

---

## Cara Menjalankan Aplikasi

### Langkah 1: Menjalankan Backend Server

Pastikan Anda berada di root folder proyek (`Kelompok7_Variational-Autoencoder_handwriting-generator/`).

**Aktifkan Virtual Environment (jika menggunakan):**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

**Jalankan Backend Server:**

```bash
python api_server.py
```

### Langkah 2: Menjalankan Frontend Development Server

Buka terminal baru (biarkan backend tetap berjalan), kemudian:

```bash
cd Kelompok7_Variational-Autoencoder_handwriting-generator/web
npm run dev
```

### Langkah 3: Akses Aplikasi

Buka browser dan akses: `http://localhost:5173`

---

## Penggunaan Aplikasi

### Interface Pengguna

Aplikasi memiliki dua panel utama:

#### Panel Kiri - VAE Controls

1. **Dropdown Digit Selection**
   - Klik dropdown untuk memilih angka (0-9) yang ingin dihasilkan
   - Contoh: Pilih "Digit 3" untuk menghasilkan angka 3

2. **Slider Latent Dimension Z1**
   - Mengatur karakteristik gaya tulisan dimensi pertama
   - Range: -3.0 hingga 3.0
   - Default: 0.0

3. **Slider Latent Dimension Z2**
   - Mengatur karakteristik gaya tulisan dimensi kedua
   - Range: -3.0 hingga 3.0
   - Default: 0.0

4. **Tombol Generate**
   - Klik untuk menghasilkan gambar baru berdasarkan parameter yang dipilih

#### Panel Kanan - Generated Handwriting

- Menampilkan hasil gambar tulisan tangan 28x28 piksel (diperbesar untuk visibility)
- Informasi detail: Digit yang dipilih, nilai Z1 dan Z2
- Source URL dari API backend
- Tombol Download untuk menyimpan gambar

### Cara Menggunakan

1. **Pilih Angka**: Gunakan dropdown untuk memilih digit 0-9
2. **Atur Gaya Tulisan**: Geser slider Z1 dan Z2 untuk mengubah variasi gaya
3. **Generate**: Klik tombol "Generate" untuk membuat gambar
4. **Download**: Klik tombol "Download" untuk menyimpan hasil

### Tips Penggunaan

- Nilai Z1 dan Z2 di sekitar 0 menghasilkan gaya tulisan yang lebih standar
- Nilai ekstrem (-3 atau 3) menghasilkan variasi gaya yang lebih unik
- Eksplorasi berbagai kombinasi nilai untuk menemukan variasi menarik
- Setiap kombinasi digit dan latent values menghasilkan gaya tulisan yang berbeda

### Contoh Penggunaan

**Eksplorasi Gaya Tulisan Angka 7:**
- Digit: 7, Z1: 0.00, Z2: 0.00 → Gaya standar
- Digit: 7, Z1: -2.00, Z2: 1.50 → Gaya miring ke kiri
- Digit: 7, Z1: 2.50, Z2: -1.00 → Gaya lebih tegak
- Digit: 7, Z1: -0.50, Z2: 0.10 → Gaya sedikit melengkung

---

## Arsitektur Model

### Conditional Variational Autoencoder (CVAE)

Model CVAE terdiri dari tiga komponen utama:

#### 1. Encoder

Encoder menerima dua jenis input:
- Gambar angka tulisan tangan (28x28x1)
- Label kategori (one-hot encoded, 10 classes)

**Arsitektur:**
```
Input Image (28x28x1) + Label (10) 
    ↓
Concatenate (Label expanded to 28x28x10)
    ↓
Conv2D(32, kernel=3, strides=2, activation='relu')
    ↓
Conv2D(64, kernel=3, strides=2, activation='relu')
    ↓
Flatten()
    ↓
Dense(latent_dim) → z_mean
Dense(latent_dim) → z_log_var
    ↓
Sampling Layer (Reparameterization Trick)
    ↓
Output: z (latent vector 2D)
```

#### 2. Latent Space (Ruang Laten)

- Dimensi: 2D (untuk visualisasi dan kontrol yang mudah)
- Representasi: z_mean dan z_log_var
- Reparameterization Trick: `z = μ + σ × ε` dimana `ε ~ N(0,1)`

**Kegunaan Latent Space 2D:**
- Mudah divisualisasikan dalam grafik X-Y
- Kontrol intuitif melalui slider interface
- Eksplorasi style variations yang smooth

#### 3. Decoder

Decoder menerima dua input:
- Latent vector (2D)
- Label kategori (one-hot encoded, 10 classes)

**Arsitektur:**
```
Input: z (2D) + Label (10)
    ↓
Concatenate
    ↓
Dense(7×7×64, activation='relu')
    ↓
Reshape(7, 7, 64)
    ↓
Conv2DTranspose(64, kernel=3, strides=2, activation='relu')
    ↓
Conv2DTranspose(32, kernel=3, strides=2, activation='relu')
    ↓
Conv2DTranspose(1, kernel=3, activation='sigmoid')
    ↓
Output: Reconstructed Image (28x28x1)
```

### Loss Function

Model menggunakan kombinasi dua loss:

**1. Reconstruction Loss (Binary Cross-Entropy)**
```
L_recon = -Σ [x·log(x̂) + (1-x)·log(1-x̂)]
```
Mengukur kemiripan fisik antara gambar asli dengan gambar hasil rekonstruksi.

**2. KL Divergence Loss**
```
L_KL = -0.5 × Σ [1 + log(σ²) - μ² - σ²]
```
Menjaga keteraturan distribusi data di ruang laten agar mengikuti distribusi normal standar.

**Total Loss:**
```
L_total = L_recon + L_KL
```

---

## Metodologi Penelitian

### Data Penelitian

**Dataset MNIST:**
- Total: 70.000 gambar
- Training: 60.000 gambar
- Testing: 10.000 gambar
- Format: Grayscale 28x28 piksel
- Classes: 10 (angka 0-9)
- Source: Yann LeCun et al., http://yann.lecun.com/exdb/mnist/

### Tahapan Preprocessing Data

**1. Normalisasi Nilai Piksel**
```python
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0
```
Nilai piksel diubah dari range [0, 255] menjadi [0, 1] untuk efisiensi komputasi.

**2. Reshape Dimensi**
```python
x_train = x_train[..., tf.newaxis]  # (28, 28) → (28, 28, 1)
x_test = x_test[..., tf.newaxis]
```
Menambahkan dimensi channel untuk kompatibilitas dengan layer konvolusi.

**3. One-Hot Encoding Label**
```python
y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)
```
Mengubah label integer (0-9) menjadi vektor biner. Contoh: angka 5 → [0,0,0,0,0,1,0,0,0,0]



## API Documentation

### Base URL

```
http://localhost:7860
```

---

## Training Model

### Proses Training

Jika ingin melatih model dari awal atau melakukan re-training:

#### 1. Jalankan Training Script

```bash
python train.py
```

#### 2. Monitoring Training Process

Output yang akan ditampilkan:
```
[INFO] Loading MNIST dataset...
[INFO] Start training CVAE...
Epoch 1/30
469/469 [==============================] - 15s 32ms/step 
  loss: 156.2341 - reconstruction_loss: 145.1234 - kl_loss: 11.1107 
  val_loss: 142.3456 - val_reconstruction_loss: 133.2345 - val_kl_loss: 9.2111

Epoch 2/30
469/469 [==============================] - 14s 30ms/step
  loss: 138.5432 - reconstruction_loss: 128.9876 - kl_loss: 9.5556
  val_loss: 135.6789 - val_reconstruction_loss: 126.5432 - val_kl_loss: 9.1357

...

Epoch 30/30
469/469 [==============================] - 14s 30ms/step
  loss: 98.7654 - reconstruction_loss: 89.6543 - kl_loss: 9.1111
  val_loss: 96.5432 - val_reconstruction_loss: 87.5432 - val_kl_loss: 9.0000

[INFO] Saving models...
[INFO] Training completed!
[INFO] Model saved as conditional_encoder.h5 & conditional_decoder.h5
```

#### 3. Output Training

Setelah training selesai, akan menghasilkan:
- `conditional_encoder.h5`: Model encoder
- `conditional_decoder.h5`: Model decoder (digunakan untuk generation)

### Testing Manual

Untuk test hasil training secara manual:

```bash
python generate.py
```

Script ini akan:
1. Load decoder model
2. Generate 10 variasi gaya dari satu digit tertentu
3. Save hasil ke `manual_test_result.png`

**Konfigurasi di `generate.py`:**
```python
angka_target = 7      # Ganti dengan angka yang ingin ditest
num_samples = 10      # Jumlah variasi yang dihasilkan
```

---

## Hasil dan Analisis

### Hasil Implementasi

**1. Fitur Pemilihan Angka**
- Model berhasil menghasilkan angka sesuai label yang dipilih
- Tingkat akurasi kondisional: Tinggi
- Semua digit (0-9) dapat dihasilkan dengan baik

**2. Fitur Kontrol Gaya**
- Slider latent space berfungsi dengan baik
- Perubahan nilai Z1 dan Z2 menghasilkan variasi gaya yang smooth
- Tidak terjadi discontinuity atau "lompatan" yang tiba-tiba

**3. Performa Model**
- Reconstruction loss: Rendah (gambar mirip dengan data training)
- KL loss: Stabil (distribusi latent space teratur)
- Generation time: < 1 detik per image

### Analisis Latent Space

**Karakteristik Latent Space 2D:**
- Nilai sekitar (0, 0): Menghasilkan gaya tulisan "rata-rata"
- Nilai ekstrem (±3): Menghasilkan variasi gaya yang lebih unik
- Transisi smooth: Perubahan gradual saat slider digeser
- Setiap region latent space merepresentasikan style yang berbeda

### Kelebihan Sistem

1. **User-Friendly**: Interface sederhana dan intuitif
2. **Real-Time**: Generate gambar dengan cepat
3. **Controllable**: Kontrol penuh terhadap output (digit dan style)
4. **Reproducible**: Kombinasi parameter yang sama menghasilkan output yang sama
5. **Educational**: Memvisualisasikan konsep latent space dengan jelas

### Keterbatasan

1. **Dataset**: Hanya terbatas pada angka 0-9 (tidak termasuk huruf)
2. **Resolution**: Output terbatas pada 28x28 piksel
3. **Latent Dimension**: 2D memberikan kontrol terbatas dibanding dimensi yang lebih tinggi
4. **Style Control**: Makna Z1 dan Z2 tidak eksplisit (perlu eksplorasi manual)

---

## Referensi

### Framework dan Library

- TensorFlow: https://www.tensorflow.org/
- Keras: https://keras.io/
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Vite: https://vitejs.dev/

### Dataset

- MNIST Database: http://yann.lecun.com/exdb/mnist/
- The National Institute of Standards and Technology (NIST)
