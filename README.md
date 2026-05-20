# 🛡️ CyberGuard AI

**AI Cyber Security Assistant** — Aplikasi web edukasi dan analisis keamanan siber profesional.

Dibangun dengan **Python + Streamlit**, siap dijalankan lokal, di-upload ke GitHub, dan di-deploy ke **Streamlit Community Cloud**.

> **Catatan lokasi:** ini adalah **repository / folder proyek tersendiri** (misalnya `CyberGuard-AI` di `htdocs`), **bukan** bagian dari proyek PHP lain. Untuk GitHub, push isi folder ini saja sebagai satu repo.

---

## 🗄️ Tanpa database (cocok untuk GitHub + Streamlit Cloud)

Aplikasi ini **tidak memerlukan database** (tidak ada MySQL, PostgreSQL, SQLite file, dll.):

- Chat history memakai **`st.session_state`** (hilang saat tab/browser ditutup atau session baru).
- Chatbot memakai **knowledge base di `engine.py`** (bukan penyimpanan server).
- Password checker & URL scanner memproses input **hanya di memori** saat itu juga.

Jadi hosting lewat **GitHub + Streamlit Community Cloud** cukup: tidak perlu mengatur DB connection string atau layanan database tambahan.

---

## 📁 Struktur Folder Project

```
CyberGuard-AI/
├── app.py              # File utama Streamlit (UI, navigasi, layout)
├── engine.py           # Logic chatbot AI & response generator
├── fms.py              # Feature Module Security (password, URL, tips)
├── style.css           # Custom CSS modern & responsive
├── requirements.txt    # Dependencies Python
└── README.md           # Dokumentasi project (file ini)
```

### Penjelasan Tiap File

| File | Fungsi |
|------|--------|
| `app.py` | Entry point aplikasi. Mengatur halaman, sidebar, dashboard, chatbot UI, dan memanggil modul lain. |
| `engine.py` | Mesin chatbot AI dengan knowledge base & keyword matching. Siap dikembangkan ke OpenAI API. |
| `fms.py` | Modul fitur keamanan: password strength checker, URL/phishing detector, cyber tips. |
| `style.css` | Styling premium (dark theme, glassmorphism, glow biru, responsive mobile). |
| `requirements.txt` | Daftar package Python yang diperlukan untuk install & deploy. |

---

## 🚀 Cara Menjalankan Project (Lokal)

### Prasyarat

- Python 3.9 atau lebih baru
- pip (package manager Python)

### Langkah Instalasi

1. **Buka terminal** di folder project (sesuaikan path Anda), contoh di Windows:

```bash
cd c:\xampp\htdocs\CyberGuard-AI
```

2. **Buat virtual environment** (opsional tapi disarankan):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Jalankan aplikasi:**

```bash
streamlit run app.py
```

5. Browser akan terbuka otomatis di `http://localhost:8501`

### Windows: jika `pip` / `streamlit` tidak dikenali (PATH)

Gunakan launcher Python bawaan Windows:

```powershell
cd c:\xampp\htdocs\CyberGuard-AI
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Di PowerShell lama, hindari menggabungkan perintah dengan `&&` — gunakan `;` atau satu perintah per baris.

---

## 📤 Cara Upload ke GitHub

### 1. Buat Repository Baru

1. Login ke [github.com](https://github.com)
2. Klik **New repository**
3. Nama: `cyberguard-ai` (atau sesuai keinginan)
4. Pilih **Public**
5. Klik **Create repository**

### 2. Upload Project via Terminal

```bash
cd c:\xampp\htdocs\CyberGuard-AI

git init
git add .
git commit -m "Initial commit: CyberGuard AI - Cyber Security Assistant"
git branch -M main
git remote add origin https://github.com/USERNAME/cyberguard-ai.git
git push -u origin main
```

Ganti `USERNAME` dengan username GitHub Anda.

### 3. File yang Harus Ada di Repo

Pastikan file berikut ter-commit:

- `app.py`
- `engine.py`
- `fms.py`
- `style.css`
- `requirements.txt`
- `README.md`

**Jangan** commit folder `venv/`, `__pycache__/`, atau file `.env`.

Tambahkan `.gitignore`:

```
venv/
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
```

---

## ☁️ Cara Deploy ke Streamlit Community Cloud

### 1. Pastikan Repo di GitHub

Project harus sudah di-push ke GitHub (langkah di atas).

### 2. Deploy

1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login dengan akun GitHub
3. Klik **New app**
4. Pilih repository `cyberguard-ai`
5. Branch: `main`
6. **Main file path:** `app.py`
7. Klik **Deploy**

### 3. Tunggu Build

Streamlit Cloud akan otomatis:

- Install `requirements.txt`
- Menjalankan `streamlit run app.py`

URL aplikasi Anda akan tersedia di:
`https://USERNAME-cyberguard-ai-app-xxxxx.streamlit.app`

### Tips Deploy Sukses

- Semua import menggunakan file lokal (`engine`, `fms`) — tanpa path absolut
- CSS dimuat via `Path(__file__).parent` — kompatibel cloud
- Hanya dependency `streamlit` di `requirements.txt`
- Tidak ada konfigurasi lokal yang wajib (`.env` opsional untuk future OpenAI)

---

## ✨ Fitur Aplikasi

| Fitur | Deskripsi |
|-------|-----------|
| **AI Chatbot** | Tanya jawab cyber security (phishing, malware, password, dll) |
| **Password Checker** | Analisis kekuatan password + rekomendasi |
| **URL Scanner** | Deteksi indikasi phishing pada URL |
| **Security Tips** | Tips keamanan digital modern |
| **Chat History** | Riwayat chat tersimpan di session |
| **Dashboard** | Welcome screen dengan quick start & metrics |

---

## 🔧 Pengembangan ke OpenAI API

Struktur `engine.py` sudah disiapkan. Untuk integrasi OpenAI:

1. Tambahkan `openai` ke `requirements.txt`
2. Simpan API key di Streamlit Secrets (`OPENAI_API_KEY`)
3. Ganti fungsi `_generate_response()` di `engine.py` dengan API call

```python
# Contoh future integration di engine.py
import openai

def _generate_response_openai(message, chat_history):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=format_chat_for_api(chat_history),
    )
    return response.choices[0].message.content
```

---

## 📱 Responsive Design

Aplikasi dioptimalkan untuk:

- Laptop / Desktop
- Tablet
- Android & iPhone

CSS custom dengan media queries di `style.css`.

---

## ⚠️ Disclaimer

CyberGuard AI adalah aplikasi **edukasi dan awareness** keamanan siber.
Bukan tools hacking. Gunakan secara etis dan legal.

---

## 👨‍💻 Author

Final Project — AI Cyber Security Assistant  
**CyberGuard AI** © 2026
