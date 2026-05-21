"""
engine.py — AI Engine Module
Mengatur logika chatbot AI CyberGuard berbasis keyword matching.
Struktur siap dikembangkan ke OpenAI API di masa depan.
"""

# Import typing untuk tipe data dictionary, list, dan optional
from typing import Dict, List, Optional


# =========================================================
# KNOWLEDGE BASE
# =========================================================
# Menyimpan seluruh respons AI berdasarkan topik cyber security

_KNOWLEDGE_BASE: Dict[str, str] = {

    # Respons AI tentang phishing
    "phishing": (
        "**Phishing** adalah serangan social engineering di mana penyerang "
        "menyamar sebagai entitas terpercaya (bank, perusahaan, teman) untuk "
        "mencuri data login atau finansial.\n\n"
        "**Ciri-ciri phishing:**\n"
        "- Email/SMS mendesak dengan ancaman atau hadiah\n"
        "- Link URL yang tidak sesuai domain resmi\n"
        "- Permintaan kredensial atau OTP\n"
        "- Ejaan dan grammar buruk\n\n"
        "**Cara melindungi diri:**\n"
        "1. Verifikasi pengirim melalui saluran resmi\n"
        "2. Jangan klik link — ketik URL langsung di browser\n"
        "3. Aktifkan 2FA di semua akun penting\n"
        "4. Laporkan email phishing ke provider email"
    ),

    # Respons AI tentang malware
    "malware": (
        "**Malware** (malicious software) adalah program berbahaya yang dirancang "
        "untuk merusak, mencuri data, atau mengendalikan perangkat tanpa izin.\n\n"
        "**Jenis malware umum:**\n"
        "- **Virus** — menyebar dengan menempel pada file\n"
        "- **Worm** — menyebar otomatis di jaringan\n"
        "- **Trojan** — menyamar sebagai software legitimate\n"
        "- **Spyware** — memantau aktivitas pengguna\n"
        "- **Adware** — menampilkan iklan berlebihan\n\n"
        "**Pencegahan:**\n"
        "- Install antivirus terpercaya dan update rutin\n"
        "- Jangan unduh dari sumber tidak dikenal\n"
        "- Scan USB/external drive sebelum dibuka"
    ),

    # Respons AI tentang ransomware
    "ransomware": (
        "**Ransomware** mengenkripsi file korban dan meminta tebusan (biasanya "
        "cryptocurrency) untuk mengembalikan akses.\n\n"
        "**Langkah jika terkena:**\n"
        "1. Putuskan dari jaringan segera\n"
        "2. Jangan bayar tebusan — tidak menjamin recovery\n"
        "3. Laporkan ke otoritas cyber (BSSN di Indonesia)\n"
        "4. Restore dari backup offline\n\n"
        "**Pencegahan:**\n"
        "- Backup 3-2-1 (3 salinan, 2 media, 1 offsite)\n"
        "- Patch sistem operasi secara rutin\n"
        "- Batasi privilege user di jaringan kantor"
    ),

    # Respons AI tentang keamanan password
    "password": (
        "**Keamanan Password** adalah fondasi perlindungan digital Anda.\n\n"
        "**Best practices:**\n"
        "- Minimal 12 karakter dengan kombinasi huruf, angka, simbol\n"
        "- Password unik untuk setiap akun\n"
        "- Gunakan password manager (Bitwarden, 1Password, dll)\n"
        "- Aktifkan 2FA/MFA di semua akun penting\n"
        "- Ganti password jika ada indikasi breach\n\n"
        "Gunakan fitur **Password Checker** di sidebar untuk menganalisis "
        "kekuatan password Anda secara real-time."
    ),

    # Respons AI tentang social engineering
    "social engineering": (
        "**Social Engineering** mengeksploitasi psikologi manusia, bukan celah teknis.\n\n"
        "**Teknik umum:**\n"
        "- **Pretexting** — berpura-pura sebagai orang berwenang\n"
        "- **Baiting** — menawarkan sesuatu menarik (USB, file)\n"
        "- **Quid pro quo** — menawarkan bantuan teknis palsu\n"
        "- **Tailgating** — mengikuti orang masuk area terbatas\n\n"
        "**Pertahanan:**\n"
        "- Verifikasi identitas melalui saluran terpisah\n"
        "- Jangan bagikan informasi sensitif via telepon/chat\n"
        "- Latih awareness security secara berkala"
    ),

    # Respons AI tentang 2FA
    "2fa": (
        "**Two-Factor Authentication (2FA)** menambah lapisan keamanan di luar password.\n\n"
        "**Metode 2FA:**\n"
        "- SMS OTP (kurang aman, rentan SIM swap)\n"
        "- Authenticator app (Google Authenticator, Authy) — disarankan\n"
        "- Hardware key (YubiKey) — paling aman\n"
        "- Biometric (sidik jari, face ID)\n\n"
        "Aktifkan 2FA di semua akun penting."
    ),

    # Respons AI tentang scam online
    "scam": (
        "**Scam & Penipuan Online** semakin canggih di era digital.\n\n"
        "**Red flags:**\n"
        "- Janji keuntungan tidak masuk akal\n"
        "- Tekanan waktu untuk transfer uang\n"
        "- Permintaan transfer ke rekening pribadi\n"
        "- Profil media sosial baru tanpa riwayat\n\n"
        "**Tips:**\n"
        "- Verifikasi lewat website resmi\n"
        "- Jangan transfer uang sembarangan"
    ),

    # Respons AI tentang VPN
    "vpn": (
        "**VPN (Virtual Private Network)** mengenkripsi koneksi internet Anda.\n\n"
        "**Kapan menggunakan VPN:**\n"
        "- Wi-Fi publik\n"
        "- Remote work\n"
        "- Menambah privasi online\n\n"
        "Gunakan VPN terpercaya dengan kebijakan no-log."
    ),

    # Respons AI tentang firewall
    "firewall": (
        "**Firewall** adalah penghalang antara jaringan internal dan eksternal.\n\n"
        "**Jenis firewall:**\n"
        "- Network Firewall\n"
        "- Host Firewall\n"
        "- Web Application Firewall (WAF)\n\n"
        "Pastikan firewall aktif di perangkat Anda."
    ),

    # Respons AI tentang enkripsi
    "encryption": (
        "**Enkripsi** mengubah data menjadi format yang tidak bisa dibaca "
        "tanpa kunci dekripsi.\n\n"
        "**Jenis enkripsi:**\n"
        "- Data at rest\n"
        "- Data in transit\n\n"
        "Selalu gunakan HTTPS saat memasukkan data sensitif."
    ),
}


# =========================================================
# KEYWORD MAP
# =========================================================
# Menghubungkan keyword user dengan topik tertentu

_KEYWORD_MAP: Dict[str, List[str]] = {

    # Keyword phishing
    "phishing": [
        "phishing",
        "phish",
        "email palsu",
        "penipuan email"
    ],

    # Keyword malware
    "malware": [
        "malware",
        "virus",
        "trojan",
        "spyware",
        "adware",
        "worm"
    ],

    # Keyword ransomware
    "ransomware": [
        "ransomware",
        "ransom",
        "tebusan",
        "enkripsi file"
    ],

    # Keyword password
    "password": [
        "password",
        "kata sandi",
        "sandi",
        "passphrase",
        "credential"
    ],

    # Keyword social engineering
    "social engineering": [
        "social engineering",
        "sosial engineering",
        "manipulasi",
        "penipuan"
    ],

    # Keyword 2FA
    "2fa": [
        "2fa",
        "two factor",
        "mfa",
        "otp",
        "autentikasi dua faktor"
    ],

    # Keyword scam
    "scam": [
        "scam",
        "penipuan",
        "tipu",
        "modus"
    ],

    # Keyword VPN
    "vpn": [
        "vpn",
        "virtual private"
    ],

    # Keyword firewall
    "firewall": [
        "firewall",
        "fire wall"
    ],

    # Keyword encryption
    "encryption": [
        "enkripsi",
        "encryption",
        "https",
        "ssl"
    ],
}


# =========================================================
# DEFAULT RESPONSE
# =========================================================
# Respons default jika keyword tidak ditemukan

_DEFAULT_RESPONSE = (
    "Terima kasih atas pertanyaan Anda.\n\n"
    "Saya dapat membantu topik seperti:\n"
    "- Phishing\n"
    "- Malware\n"
    "- Password Security\n"
    "- VPN\n"
    "- Firewall\n\n"
    "Silakan gunakan kata kunci cyber security yang lebih spesifik."
)


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

def process_message(user_message: str, chat_history: Optional[List[Dict]] = None) -> Dict:
    """
    Memproses pesan pengguna dan menghasilkan respons AI.
    """

    # Mengecek apakah input kosong
    if not user_message or not user_message.strip():
        return {
            "response": "Silakan ketik pertanyaan Anda tentang cyber security.",
            "topic": "general",
            "confidence": 0.0,
        }

    # Mengubah teks menjadi lowercase
    normalized = user_message.strip().lower()

    # Mencocokkan topik berdasarkan keyword
    topic, confidence = _match_topic(normalized)

    # Membuat respons AI
    response = _generate_response(normalized, topic)

    # Mengembalikan hasil respons
    return {
        "response": response,
        "topic": topic,
        "confidence": confidence,
    }


# =========================================================
# MATCH TOPIC
# =========================================================

def _match_topic(message: str) -> tuple:
    """
    Mendeteksi topik berdasarkan keyword user.
    """

    best_topic = "general"
    best_score = 0.0

    # Loop seluruh keyword map
    for topic, keywords in _KEYWORD_MAP.items():

        # Menghitung jumlah keyword yang cocok
        matches = sum(1 for kw in keywords if kw in message)

        # Jika ada keyword cocok
        if matches > 0:

            # Menghitung score kecocokan
            score = matches / len(keywords)

            # Menyimpan topic dengan score tertinggi
            if score > best_score:
                best_score = score
                best_topic = topic

    # Mengatur confidence score
    confidence = min(best_score * 2, 1.0) if best_score > 0 else 0.3

    return best_topic, round(confidence, 2)


# =========================================================
# GENERATE RESPONSE
# =========================================================

def _generate_response(message: str, topic: str) -> str:
    """
    Membuat respons AI berdasarkan topik.
    """

    # Jika topic ditemukan di knowledge base
    if topic in _KNOWLEDGE_BASE:
        return _KNOWLEDGE_BASE[topic]

    # Respons sapaan
    if "halo" in message or "hai" in message or "hello" in message:
        return (
            "Halo! Saya CyberGuard AI.\n\n"
            "Saya siap membantu Anda memahami keamanan digital."
        )

    # Respons ucapan terima kasih
    if "terima kasih" in message or "makasih" in message:
        return (
            "Sama-sama! Tetap jaga keamanan digital Anda 🛡️"
        )

    # Respons tips keamanan
    if "tips" in message or "saran" in message:
        return (
            "Tips keamanan digital:\n"
            "1. Gunakan password kuat\n"
            "2. Aktifkan 2FA\n"
            "3. Hindari link mencurigakan"
        )

    # Jika tidak ada topik cocok
    return _DEFAULT_RESPONSE


# =========================================================
# WELCOME MESSAGE
# =========================================================

def get_welcome_message() -> str:
    """
    Menampilkan pesan awal chatbot.
    """

    return (
        "Selamat datang di CyberGuard AI Chat 🛡️\n\n"
        "Tanyakan apa saja tentang cyber security."
    )


# =========================================================
# FORMAT CHAT FOR API
# =========================================================

def format_chat_for_api(chat_history: List[Dict]) -> List[Dict]:
    """
    Mengubah format chat agar siap digunakan untuk OpenAI API.
    """

    formatted = []

    # Loop seluruh riwayat chat
    for msg in chat_history:

        # Menentukan role user atau assistant
        role = "user" if msg.get("role") == "user" else "assistant"

        # Menambahkan format baru
        formatted.append({
            "role": role,
            "content": msg.get("content", ""),
        })

    return formatted
