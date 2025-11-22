# CVAE implementation using PyTorch

import torch
import torch.nn as nn
import torch.nn.functional as F

class CVAE(nn.Module):
    """
    Conditional Variational Autoencoder (CVAE)

    - Digunakan untuk dataset seperti MNIST yang punya label kelas (0–9)
    - Input encoder       : gambar + one-hot label
    - Input decoder       : latent vector + one-hot label
    - Output decoder      : rekonstruksi gambar
    """

    def __init__(self, img_dim=784, n_classes=10, latent_dim=20):
        super(CVAE, self).__init__()

        # ------------------------------------
        # CHOICE OF DIMENSIONS
        # img_dim   : 28×28 MNIST → 784
        # n_classes : jumlah label
        # latent_dim: dimensi representasi latent
        # ------------------------------------

        self.img_dim = img_dim
        self.latent_dim = latent_dim
        self.n_classes = n_classes

        # Input encoder = gambar + label (one-hot)
        encoder_input_dim = img_dim + n_classes

        # =============== ENCODER ===============
        self.fc1 = nn.Linear(encoder_input_dim, 512)
        self.fc2 = nn.Linear(512, 256)

        # Layer untuk mean & log-variance
        self.fc_mu     = nn.Linear(256, latent_dim)
        self.fc_logvar = nn.Linear(256, latent_dim)

        # =============== DECODER ===============
        decoder_input_dim = latent_dim + n_classes

        self.fc3 = nn.Linear(decoder_input_dim, 256)
        self.fc4 = nn.Linear(256, 512)
        self.fc5 = nn.Linear(512, img_dim)


    def encode(self, x, labels):
        """
        Encoder:
        - Gabungkan gambar dengan one-hot label
        - Output: mean & log-variance dari distribusi Gaussian
        """
        x = torch.cat([x, labels], dim=1)      # concat kedua input
        h = F.relu(self.fc1(x))
        h = F.relu(self.fc2(h))

        mu     = self.fc_mu(h)
        logvar = self.fc_logvar(h)

        return mu, logvar


    def reparameterize(self, mu, logvar):
        """
        Reparameterization trick:
        z = mu + std * epsilon

        Agar proses sampling dari N(mu, sigma) tetap dapat dihitung gradiennya.
        """
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std


    def decode(self, z, labels):
        """
        Decoder:
        Input = latent vector + one-hot label
        Output = hasil rekonstruksi gambar
        """
        z = torch.cat([z, labels], dim=1)
        h = F.relu(self.fc3(z))
        h = F.relu(self.fc4(h))

        # sigmoid → output bernilai 0–1 seperti pixel
        return torch.sigmoid(self.fc5(h))


    def forward(self, x, labels):
        """
        Full CVAE forward pass:
        1. Encode (didapat mu, logvar)
        2. Sampling latent z
        3. Decode z kembali menjadi gambar
        """
        mu, logvar = self.encode(x, labels)
        z = self.reparameterize(mu, logvar)
        recon = self.decode(z, labels)
        return recon, mu, logvar


def loss_function(recon_x, x, mu, logvar):
    """
    CVAE Loss = Reconstruction loss + KL Divergence

    - Reconstruction: seberapa mirip output dengan input
    - KL divergence: regularisasi agar latent space rapi
    """
    # BCE menghitung per-pixel binary cross entropy
    BCE = F.binary_cross_entropy(
        recon_x, x, reduction='sum'
    )

    # Rumus KL divergence untuk distribusi Gaussian
    KLD = -0.5 * torch.sum(
        1 + logvar - mu.pow(2) - logvar.exp()
    )

    return BCE + KLD
