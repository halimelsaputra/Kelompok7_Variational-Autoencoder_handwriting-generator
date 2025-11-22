import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Handwriting Generator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - MAXIMUM OPTIMIZATION
st.markdown("""
<style>
    /* ==================== RESET & HIDE STREAMLIT ==================== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Remove default padding/margin */
    .main > div {
        padding-top: 0rem;
    }
    
    /* ==================== GLOBAL STYLES ==================== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(to bottom right, #F8FAFC 0%, #F8FAFC 80%, #EFF6FF 100%) !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        color: #0F172A;
    }
    
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* ==================== MAIN CONTAINER ==================== */
    .block-container {
        max-width: 1400px !important;
        padding: 0 !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* ==================== HEADER ==================== */
    .custom-header {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(226, 232, 240, 0.8);
        padding: 2rem 0;
        margin-bottom: 3rem;
        margin-left: -2rem;
        margin-right: -2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    .header-content {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .header-icon {
        width: 3.5rem;
        height: 3.5rem;
        background: linear-gradient(135deg, #0EA5E9 0%, #06B6D4 100%);
        border-radius: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.25);
    }
    
    .header-text h1 {
        background: linear-gradient(135deg, #0EA5E9 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.875rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    .header-text p {
        color: #64748B;
        font-size: 1.125rem;
        font-weight: 600;
        margin: 0.5rem 0 0 0;
    }
    
    /* ==================== BUTTON ==================== */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%);
        color: white;
        border: none;
        padding: 0.875rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        letter-spacing: 0.025em;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4);
        background: linear-gradient(135deg, #0284C7 0%, #1D4ED8 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ==================== CARDS ==================== */
    .custom-card {
        background: #FFFFFF;
        border: 1px solid rgba(226, 232, 240, 0.6);
        border-radius: 1rem;
        padding: 2rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 10px 25px rgba(0, 0, 0, 0.05);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .custom-card:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 15px 35px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        gap: 0.625rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.875rem;
        border-bottom: 1px solid rgba(226, 232, 240, 0.5);
    }
    
    /* Hide Streamlit h2 in card headers */
    .card-header h2 {
        display: none !important;
    }
    
    .card-icon {
        font-size: 1.25rem;
        line-height: 1;
    }
    
    .card-title {
        font-size: 1.375rem;
        font-weight: 600;
        color: #0F172A;
        margin: 0;
        line-height: 1.2;
    }
    
    /* ==================== FORM ELEMENTS ==================== */
    .stSelectbox label {
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        margin-bottom: 0.75rem !important;
        letter-spacing: 0.01em !important;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%) !important;
        border: 2px solid #CBD5E1 !important;
        border-radius: 0.875rem !important;
        height: 3.5rem !important;
        font-size: 1.125rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06), 0 4px 12px rgba(0, 0, 0, 0.04) !important;
        padding-left: 1.25rem !important;
        cursor: pointer !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #0EA5E9 !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%) !important;
        box-shadow: 0 4px 8px rgba(14, 165, 233, 0.15), 0 0 0 3px rgba(14, 165, 233, 0.08) !important;
        transform: translateY(-1px) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #0EA5E9 !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%) !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2), 0 0 0 4px rgba(14, 165, 233, 0.12) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Dropdown arrow */
    .stSelectbox svg {
        color: #0EA5E9 !important;
        width: 1.25rem !important;
        height: 1.25rem !important;
    }
    
    /* Selected option text */
    .stSelectbox [data-baseweb="select"] > div {
        color: #0F172A !important;
        font-weight: 600 !important;
    }
    
    /* ==================== SLIDERS ==================== */
    /* Style dari tes.py - lebih clean dan simple */
    
    /* 1. Ubah Warna & Bentuk Jalur (Track) */
    div[data-baseweb="slider"] > div > div {
        background: #E2E8F0 !important; /* Warna abu soft */
        height: 8px !important; /* Lebih tebal */
        border-radius: 10px !important;
        cursor: pointer;
    }

    /* 2. Ubah Warna Jalur yang Terisi (Filled Track) */
    div[data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, #3B82F6, #2563EB) !important; /* Gradasi Biru */
    }

    /* 3. Ubah Kepala Geseran (Thumb) */
    div[role="slider"] {
        background-color: #FFFFFF !important; /* Tengah putih */
        border: 4px solid #2563EB !important; /* Pinggir biru tebal */
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4) !important; /* Efek Glow/Bayangan */
        height: 24px !important; /* Lebih besar */
        width: 24px !important;
    }
    
    /* 4. Hapus angka bawaan Streamlit yang jelek di bawah slider */
    .stSlider [data-testid="stMarkdownContainer"] p {
        font-weight: 600;
        font-size: 14px;
    }
    
    .stSlider {
        padding: 1rem 0 !important;
    }
    
    .stSlider label {
        font-size: 0.9375rem !important;
        font-weight: 600 !important;
        color: #0F172A !important;
        margin-bottom: 0.75rem !important;
    }
    
    .slider-container {
        margin-bottom: 2rem;
    }
    
    .slider-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    /* Badge Angka Slider (Kotak Biru Kecil) - style dari tes.py */
    .slider-value {
        background: #EFF6FF;
        color: #2563EB;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid #BFDBFE;
    }
    
    .slider-labels {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 0.5rem;
        font-size: 0.75rem;
        color: #64748B;
    }
    
    .slider-center {
        color: #0EA5E9;
        font-weight: 600;
        font-size: 0.8125rem;
    }
    
    /* ==================== INFO BOX ==================== */
    .info-box {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.05) 0%, rgba(6, 182, 212, 0.08) 100%);
        border: 1px solid rgba(14, 165, 233, 0.2);
        border-left: 4px solid #0EA5E9;
        border-radius: 0.75rem;
        padding: 1rem 1.25rem;
        margin-top: 2rem;
    }
    
    .info-box p {
        font-size: 0.875rem;
        color: #475569;
        line-height: 1.6;
        margin: 0;
    }
    
    .info-box strong {
        color: #0F172A;
        font-weight: 600;
    }
    
    /* ==================== PREVIEW AREA ==================== */
    .preview-container {
        aspect-ratio: 1;
        background: linear-gradient(135deg, rgba(241, 245, 249, 0.6) 0%, rgba(226, 232, 240, 0.4) 100%);
        border: 2px dashed #CBD5E1;
        border-radius: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        position: relative;
        transition: all 0.3s ease;
        width: 100%;
        margin-bottom: 1.5rem;
    }
    
    .preview-container:hover {
        border-color: #0EA5E9;
        background: linear-gradient(135deg, rgba(239, 246, 255, 0.8) 0%, rgba(219, 234, 254, 0.6) 100%);
    }
    
    .preview-placeholder {
        text-align: center;
        padding: 2rem;
    }
    
    .preview-icon {
        width: 7rem;
        height: 7rem;
        margin: 0 auto 1.5rem;
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(6, 182, 212, 0.15) 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    .preview-text {
        color: #64748B;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* ==================== STATS GRID ==================== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-top: 0;
        width: 100%;
    }
    
    .stat-box {
        text-align: center;
        padding: 1.25rem 1rem;
        background: linear-gradient(135deg, rgba(241, 245, 249, 0.5) 0%, rgba(226, 232, 240, 0.3) 100%);
        border: 1px solid rgba(226, 232, 240, 0.6);
        border-radius: 0.75rem;
        transition: all 0.2s ease;
    }
    
    .stat-box:hover {
        background: linear-gradient(135deg, rgba(239, 246, 255, 0.8) 0%, rgba(219, 234, 254, 0.6) 100%);
        border-color: #0EA5E9;
        transform: translateY(-2px);
    }
    
    .stat-value {
        font-size: 1.875rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #64748B;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
    
    /* ==================== LAYOUT ==================== */
    [data-testid="column"] {
        padding: 0 1rem !important;
    }
    
    [data-testid="stHorizontalBlock"] {
        gap: 2rem !important;
    }
    
    [data-testid="stVerticalBlock"] > [data-testid="element-container"] {
        margin-bottom: 0 !important;
    }
    
    /* Fix container spacing inside cards */
    .st-emotion-cache-1n6tfoc {
        gap: 0 !important;
    }
    
    /* Remove default gap from vertical blocks in columns */
    [data-testid="column"] .st-emotion-cache-wfksaw {
        gap: 0 !important;
    }
    
    /* Specific spacing for elements inside cards */
    .custom-card .st-emotion-cache-1vo6xi6 {
        margin-bottom: 0 !important;
    }
    
    /* Remove default gap from vertical blocks in columns */
    [data-testid="column"] .st-emotion-cache-wfksaw {
        gap: 0 !important;
    }
    
    /* Specific spacing for elements inside cards */
    .custom-card .st-emotion-cache-1vo6xi6 {
        margin-bottom: 0 !important;
    }
    
    /* Hide all default Streamlit markdown headings that aren't custom */
    [data-testid="stMarkdownContainer"] h1:not(.header-title),
    [data-testid="stMarkdownContainer"] h2:not(.card-title) {
        display: none !important;
    }
    
    /* Remove extra margin from markdown containers */
    .custom-card + [data-testid="stMarkdownContainer"] {
        margin-top: 0 !important;
    }
    
    .st-emotion-cache-467cry {
        margin-bottom: 0 !important;
    }
    
    /* ==================== RESPONSIVE ==================== */
    @media (max-width: 1024px) {
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        [data-testid="stHorizontalBlock"] {
            gap: 1rem !important;
        }
        
        .custom-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="custom-header">
    <div class="header-content">
        <div class="header-text" style="margin-left: 0;">
            <h1>Generator Angka VAE</h1>
            <p>Handwriting Generator</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content - two columns
col1, col2 = st.columns([1, 1], gap="large")

# Left Column - Controls
with col1:
    st.markdown("""
    <div class="custom-card">
        <div class="card-header">
            <span class="card-title">Control</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Digit selection
    selected_digit = st.selectbox(
        "Pilih Angka (0-9)",
        options=list(range(10)),
        format_func=lambda x: f"Angka {x}",
        key="digit_select"
    )
    
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    # Latent Variable Z1
    st.markdown(f'''
    <div class="slider-container">
        <div class="slider-header">
            <span style="font-size: 0.9375rem; font-weight: 600; color: #0F172A;">Variabel Laten Z₁</span>
            <span class="slider-value">{st.session_state.get("z1", 0.0):.2f}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    z1 = st.slider(
        "Z1",
        min_value=-3.0,
        max_value=3.0,
        value=0.0,
        step=0.1,
        key="z1",
        label_visibility="collapsed"
    )
    
    st.markdown("""
    <div class="slider-labels">
        <span>-3.0</span>
        <span>3.0</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)
    
    # Latent Variable Z2
    st.markdown(f'''
    <div class="slider-container">
        <div class="slider-header">
            <span style="font-size: 0.9375rem; font-weight: 600; color: #0F172A;">Variabel Laten Z₂</span>
            <span class="slider-value">{st.session_state.get("z2", 0.0):.2f}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    z2 = st.slider(
        "Z2",
        min_value=-3.0,
        max_value=3.0,
        value=0.0,
        step=0.1,
        key="z2",
        label_visibility="collapsed"
    )
    
    st.markdown("""
    <div class="slider-labels">
        <span>-3.0</span>
        <span>3.0</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    # Generate button
    generate_btn = st.button(" Generate Handwriting", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Right Column - Preview
with col2:
    # 1. Buka KARTU UTAMA
    st.markdown("""
    <div class="custom-card" style="height: 100%; display: flex; flex-direction: column;">
        <div class="card-header">
            <span class="card-title">Hasil Generate</span>
        </div>
        <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center;">
    """, unsafe_allow_html=True)
    
    # 2. LOGIKA TAMPILAN
    if generate_btn:
        # === KONDISI A: USER SUDAH KLIK TOMBOL ===
        with st.spinner("Sedang membayangkan angka..."):
            try:
                from generator_api import generate_handwriting
                
                # Generate gambar
                generated_image_array = generate_handwriting(z1, z2, selected_digit)
                
                # Proses gambar
                img_uint8 = (generated_image_array * 255).astype(np.uint8)
                img_pil = Image.fromarray(img_uint8)
                
                # Resize agar besar
                img_display = img_pil.resize((400, 400), resample=Image.NEAREST)
                
                # TAMPILKAN GAMBAR
                st.image(img_display, use_container_width=True)
                
                # --- FITUR SIMPAN GAMBAR (BARU) ---
                # Konversi gambar ke Bytes (Memori)
                buf = BytesIO()
                img_pil.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # Tombol Download
                st.download_button(
                    label="⬇️ Simpan Hasil (PNG)",
                    data=byte_im,
                    file_name=f"vae_angka_{selected_digit}_z1_{z1}_z2_{z2}.png",
                    mime="image/png",
                    use_container_width=True
                )
                # ----------------------------------

                st.success(f"Sukses! Model membayangkan angka {selected_digit}")
                
            except Exception as e:
                st.error(f"Error: {e}")

    else:
        # === KONDISI B: BELUM ADA GAMBAR ===
        st.markdown("""
        <div class="preview-container" style="min-height: 350px;">
            <div class="preview-placeholder">
                <div class="preview-icon">🎨</div>
                <p class="preview-text">Klik "Generate Handwriting"<br>untuk melihat hasil</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 3. Tutup KARTU UTAMA
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Stats display
    st.markdown(f"""
    <div style="margin-top: 20px;">
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-value">{selected_digit}</div>
                <div class="stat-label">Terpilih</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{z1:.1f}</div>
                <div class="stat-label">Nilai Z₁</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{z2:.1f}</div>
                <div class="stat-label">Nilai Z₂</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Store values in session state for future use (when you add actual VAE model)
if 'parameters' not in st.session_state:
    st.session_state.parameters = {}

st.session_state.parameters = {
    'digit': selected_digit,
    'z1': z1,
    'z2': z2
}
