"""
engine.py — AI Engine Module
Modul chatbot AI Cyber Security dengan placeholder response.
Struktur siap dikembangkan ke OpenAI API.
"""

from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Knowledge Base — Respons berbasis keyword (placeholder AI)
# ---------------------------------------------------------------------------

_KNOWLEDGE_BASE: Dict[str, str] = {
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
    "2fa": (
        "**Two-Factor Authentication (2FA)** menambah lapisan keamanan di luar password.\n\n"
        "**Metode 2FA:**\n"
        "- SMS OTP (kurang aman, rentan SIM swap)\n"
        "- Authenticator app (Google Authenticator, Authy) — **disarankan**\n"
        "- Hardware key (YubiKey) — paling aman\n"
        "- Biometric (sidik jari, face ID)\n\n"
        "Aktifkan 2FA di: email, banking, social media, cloud storage, "
        "dan semua akun yang menyimpan data sensitif."
    ),
    "scam": (
        "**Scam & Penipuan Online** semakin canggih di era digital.\n\n"
        "**Red flags:**\n"
        "- Janji keuntungan tidak masuk akal\n"
        "- Tekanan waktu (\"segera transfer sekarang!\")\n"
        "- Permintaan transfer ke rekening pribadi\n"
        "- Profil media sosial baru tanpa riwayat\n\n"
        "**Tips:**\n"
        "- Verifikasi lewat website/telepon resmi\n"
        "- Jangan transfer uang ke orang tidak dikenal\n"
        "- Laporkan ke platform dan kepolisian cyber"
    ),
    "vpn": (
        "**VPN (Virtual Private Network)** mengenkripsi koneksi internet Anda.\n\n"
        "**Kapan menggunakan VPN:**\n"
        "- Wi-Fi publik (kafe, bandara, hotel)\n"
        "- Akses konten dengan privasi tambahan\n"
        "- Remote work ke server perusahaan\n\n"
        "**Pilih VPN terpercaya** — hindari VPN gratis yang menjual data. "
        "Pastikan kebijakan no-log dan enkripsi AES-256."
    ),
    "firewall": (
        "**Firewall** adalah barrier antara jaringan internal dan eksternal.\n\n"
        "**Jenis:**\n"
        "- **Network firewall** — melindungi seluruh jaringan\n"
        "- **Host firewall** — melindungi perangkat individual (Windows Defender)\n"
        "- **Web Application Firewall (WAF)** — melindungi aplikasi web\n\n"
        "Pastikan firewall aktif di router, server, dan endpoint devices."
    ),
    "encryption": (
        "**Enkripsi** mengubah data menjadi format yang tidak bisa dibaca "
        "tanpa kunci dekripsi.\n\n"
        "**Jenis:**\n"
        "- **At rest** — data tersimpan (disk encryption, database)\n"
        "- **In transit** — data dikirim (HTTPS/TLS, VPN)\n\n"
        "Selalu pastikan website menggunakan **HTTPS** (gembok hijau di browser) "
        "sebelum memasukkan data sensitif."
    ),
}


_KEYWORD_MAP: Dict[str, List[str]] = {
    "phishing": ["phishing", "phish", "email palsu", "penipuan email"],
    "malware": ["malware", "virus", "trojan", "spyware", "adware", "worm"],
    "ransomware": ["ransomware", "ransom", "tebusan", "enkripsi file"],
    "password": ["password", "kata sandi", "sandi", "passphrase", "credential"],
    "social engineering": ["social engineering", "sosial engineering", "manipulasi", "penipuan"],
    "2fa": ["2fa", "two factor", "mfa", "otp", "autentikasi dua faktor", "two-factor"],
    "scam": ["scam", "penipuan", "tipu", "modus", "investasi bodong"],
    "vpn": ["vpn", "virtual private"],
    "firewall": ["firewall", "fire wall"],
    "encryption": ["enkripsi", "encryption", "encrypt", "https", "tls", "ssl"],
}


_DEFAULT_RESPONSE = (
    "Terima kasih atas pertanyaan Anda! Sebagai **CyberGuard AI**, saya siap "
    "membantu Anda memahami dunia keamanan siber.\n\n"
    "Saya dapat membantu topik seperti:\n"
    "- Phishing & Social Engineering\n"
    "- Malware & Ransomware\n"
    "- Password Security & 2FA\n"
    "- Scam Detection & VPN\n"
    "- Firewall & Encryption\n\n"
    "Silakan ajukan pertanyaan spesifik, atau gunakan fitur **Password Checker** "
    "dan **URL Scanner** di sidebar untuk analisis langsung.\n\n"
    "_Tip: Gunakan kata kunci seperti 'phishing', 'malware', atau 'password' "
    "untuk respons yang lebih spesifik._"
)


def process_message(user_message: str, chat_history: Optional[List[Dict]] = None) -> Dict:
    """
    Memproses pesan pengguna dan menghasilkan respons AI.

    Alur pemrosesan:
        1. Normalisasi input
        2. Pencocokan keyword ke knowledge base
        3. Generate respons (placeholder — siap diganti OpenAI API)

    Args:
        user_message: Pesan teks dari pengguna.
        chat_history: Riwayat chat sebelumnya (untuk konteks future OpenAI).

    Returns:
        Dict berisi: response, topic, confidence.
    """
    if not user_message or not user_message.strip():
        return {
            "response": "Silakan ketik pertanyaan Anda tentang cyber security.",
            "topic": "general",
            "confidence": 0.0,
        }

    normalized = user_message.strip().lower()
    topic, confidence = _match_topic(normalized)
    response = _generate_response(normalized, topic)

    return {
        "response": response,
        "topic": topic,
        "confidence": confidence,
    }


def _match_topic(message: str) -> tuple:
    """
    Mencocokkan pesan pengguna dengan topik knowledge base.

    Args:
        message: Pesan yang sudah dinormalisasi (lowercase).

    Returns:
        Tuple (topic_key, confidence_score).
    """
    best_topic = "general"
    best_score = 0.0

    for topic, keywords in _KEYWORD_MAP.items():
        matches = sum(1 for kw in keywords if kw in message)
        if matches > 0:
            score = matches / len(keywords)
            if score > best_score:
                best_score = score
                best_topic = topic

    confidence = min(best_score * 2, 1.0) if best_score > 0 else 0.3
    return best_topic, round(confidence, 2)


def _generate_response(message: str, topic: str) -> str:
    """
    Menghasilkan respons berdasarkan topik yang terdeteksi.

    Untuk integrasi OpenAI nanti, ganti fungsi ini dengan API call:
        openai.ChatCompletion.create(...)

    Args:
        message: Pesan pengguna (normalized).
        topic: Topik yang terdeteksi dari keyword matching.

    Returns:
        str: Respons AI untuk ditampilkan ke pengguna.
    """
    if topic in _KNOWLEDGE_BASE:
        return _KNOWLEDGE_BASE[topic]

    if "halo" in message or "hai" in message or "hello" in message:
        return (
            "Halo! Saya **CyberGuard AI** — asisten keamanan siber profesional Anda.\n\n"
            "Saya di sini untuk membantu Anda memahami ancaman digital dan "
            "cara melindungi diri. Apa yang ingin Anda ketahui hari ini?\n\n"
            "Contoh pertanyaan:\n"
            "- Apa itu phishing dan bagaimana mengenalinya?\n"
            "- Bagaimana membuat password yang kuat?\n"
            "- Apa itu ransomware?\n"
            "- Tips keamanan akun online"
        )

    if "terima kasih" in message or "makasih" in message or "thanks" in message:
        return (
            "Sama-sama! Tetap waspada dan jaga keamanan digital Anda. "
            "Jika ada pertanyaan lain, saya siap membantu. Stay safe! 🛡️"
        )

    if "tips" in message or "saran" in message or "rekomendasi" in message:
        return (
            "**Tips Keamanan Digital Harian:**\n\n"
            "1. Aktifkan 2FA di semua akun penting\n"
            "2. Update software dan OS secara rutin\n"
            "3. Gunakan password unik + password manager\n"
            "4. Waspadai link dan attachment tidak dikenal\n"
            "5. Backup data penting secara berkala\n"
            "6. Gunakan VPN di Wi-Fi publik\n"
            "7. Review permission aplikasi di smartphone\n"
            "8. Edukasi diri tentang social engineering"
        )

    return _DEFAULT_RESPONSE


def get_welcome_message() -> str:
    """
    Mengembalikan pesan sambutan default untuk chatbot.

    Returns:
        str: Pesan pembuka chatbot.
    """
    return (
        "Selamat datang di **CyberGuard AI Chat**! 🛡️\n\n"
        "Saya asisten keamanan siber Anda. Tanyakan apa saja tentang "
        "phishing, malware, password security, dan topik cyber lainnya.\n\n"
        "_Ketik pertanyaan Anda di bawah untuk memulai._"
    )


def format_chat_for_api(chat_history: List[Dict]) -> List[Dict]:
    """
    Memformat riwayat chat ke format OpenAI API (untuk pengembangan future).

    Args:
        chat_history: List dict dengan keys 'role' dan 'content'.

    Returns:
        List[Dict]: Format siap dikirim ke OpenAI ChatCompletion API.
    """
    formatted = []
    for msg in chat_history:
        role = "user" if msg.get("role") == "user" else "assistant"
        formatted.append({
            "role": role,
            "content": msg.get("content", ""),
        })
    return formatted
