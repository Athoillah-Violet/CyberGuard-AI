"""
engine.py — AI Engine Module
Modul chatbot AI Cyber Security dengan placeholder response.
Struktur siap dikembangkan ke OpenAI API.
"""

import re
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Sequence


# ---------------------------------------------------------------------------
# Knowledge Base — Respons berbasis keyword (placeholder AI)
# ---------------------------------------------------------------------------

_KNOWLEDGE_BASE: Dict[str, str] = {
    "phishing": (
        "**Penjelasan singkat**\n"
        "**Phishing** adalah serangan *social engineering* di mana pelaku menyamar "
        "sebagai pihak terpercaya (bank, e-commerce, kantor, teman) untuk membuat korban "
        "memberikan data sensitif seperti password, OTP, PIN, atau detail kartu.\n\n"
        "**Cara kerja**\n"
        "- Mengirim email/SMS/WhatsApp/DM berisi link/attachment atau instruksi\n"
        "- Mengarahkan ke website/login palsu atau meminta OTP secara langsung\n"
        "- Memakai rasa panik (akun diblokir) atau iming-iming (hadiah/bonus)\n\n"
        "**Ciri-ciri**\n"
        "- Mendesak/ancaman/iming-iming hadiah\n"
        "- Link atau domain mirip tapi bukan yang resmi\n"
        "- Meminta password/OTP/kode verifikasi\n"
        "- Ada kesalahan ejaan, format tidak konsisten, atau lampiran mencurigakan\n\n"
        "**Risiko**\n"
        "- Akun diambil alih, transaksi ilegal, pencurian identitas, kebocoran data\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Jangan klik link/lampiran, dan jangan berikan OTP\n"
        "2. Verifikasi via kanal resmi (hubungi CS resmi / buka aplikasi resmi)\n"
        "3. Jika terlanjur klik/login: ganti password, logout dari semua perangkat, aktifkan 2FA\n"
        "4. Laporkan ke platform/email provider dan simpan bukti (screenshot, header email)\n\n"
        "**Tips keamanan tambahan**\n"
        "- Ketik URL manual atau gunakan bookmark\n"
        "- Gunakan password unik + password manager\n"
        "- Waspadai permintaan “kode verifikasi” dari siapa pun\n\n"
        "**Langkah yang Disarankan**\n"
        "- Periksa link dengan **URL Scanner** sebelum dibuka\n"
        "- Aktifkan 2FA/MFA di akun penting"
    ),
    "malware": (
        "**Penjelasan singkat**\n"
        "**Malware** (*malicious software*) adalah program berbahaya yang dibuat untuk merusak sistem, "
        "mencuri data, atau mengendalikan perangkat tanpa izin.\n\n"
        "**Cara kerja**\n"
        "- Masuk lewat unduhan/aplikasi bajakan, attachment email, link berbahaya, atau USB\n"
        "- Menjalankan aksi seperti mencuri credential, memata-matai, menghapus/mengubah file\n\n"
        "**Ciri-ciri**\n"
        "- Perangkat tiba-tiba lambat, crash, panas berlebih\n"
        "- Pop-up iklan berlebihan, browser redirect\n"
        "- Aplikasi/extension tidak dikenal muncul\n"
        "- Aktivitas jaringan mencurigakan atau storage cepat penuh\n\n"
        "**Risiko**\n"
        "- Kebocoran data, pengambilalihan akun, kerusakan sistem, penyebaran ke perangkat lain\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Putuskan koneksi internet jika dicurigai parah\n"
        "2. Jalankan scan antivirus/anti-malware dan hapus/quarantine temuan\n"
        "3. Uninstall aplikasi mencurigakan, cek extension browser\n"
        "4. Ganti password penting jika ada indikasi credential tersimpan dicuri\n\n"
        "**Tips keamanan tambahan**\n"
        "- Update OS dan aplikasi rutin\n"
        "- Hindari file bajakan/unknown source\n"
        "- Scan USB/external drive sebelum dibuka"
    ),
    "ransomware": (
        "**Penjelasan singkat**\n"
        "**Ransomware** adalah malware yang mengenkripsi file korban lalu meminta tebusan "
        "(seringnya cryptocurrency) agar akses dikembalikan.\n\n"
        "**Cara kerja**\n"
        "- Masuk lewat phishing, software bajakan, exploit yang belum dipatch, atau RDP lemah\n"
        "- Mengenkripsi file, kadang juga mencuri data (double extortion)\n\n"
        "**Ciri-ciri**\n"
        "- File berubah ekstensi/tidak bisa dibuka\n"
        "- Ada ransom note/layar pesan tebusan\n"
        "- Aktivitas disk tinggi mendadak\n\n"
        "**Risiko**\n"
        "- Kehilangan akses data, downtime bisnis, kebocoran data, pemerasan lanjutan\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Putuskan dari jaringan segera (Wi-Fi/LAN) untuk cegah penyebaran\n"
        "2. Jangan bayar tebusan (tidak menjamin recovery dan memicu serangan ulang)\n"
        "3. Dokumentasikan bukti, laporkan ke otoritas terkait (mis. BSSN) dan/atau tim IT\n"
        "4. Restore dari backup offline yang bersih, lalu patch dan reset credential\n\n"
        "**Tips keamanan tambahan**\n"
        "- Backup 3-2-1 (3 salinan, 2 media, 1 offsite)\n"
        "- Patch OS/aplikasi rutin\n"
        "- Batasi privilege user dan amankan akses remote (RDP/VPN/2FA)"
    ),
    "password": (
        "**Penjelasan singkat**\n"
        "**Password Security** adalah praktik melindungi akun dengan kata sandi yang kuat dan unik.\n\n"
        "**Risiko password lemah**\n"
        "- Mudah ditebak (*brute force*, *credential stuffing*)\n"
        "- Akun diambil alih, kebocoran data, pencurian identitas\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Gunakan password unik per akun (hindari reuse)\n"
        "2. Minimal 12–16 karakter; gunakan frasa (contoh: 4–5 kata acak)\n"
        "3. Aktifkan 2FA/MFA, terutama email dan finansial\n"
        "4. Jika password bocor/akun dibobol: ganti password, logout semua sesi, cek recovery email/nomor\n\n"
        "**Tips keamanan tambahan**\n"
        "- Gunakan password manager (Bitwarden, 1Password, dll)\n"
        "- Simpan *backup codes* 2FA dengan aman\n"
        "- Jangan bagikan password/OTP ke siapa pun\n\n"
        "**Langkah yang Disarankan**\n"
        "- Cek kekuatan password dengan **Password Checker**"
    ),
    "social engineering": (
        "**Penjelasan singkat**\n"
        "**Social Engineering** adalah teknik manipulasi yang menarget psikologi manusia "
        "(takut, panik, percaya, serakah) untuk memperoleh akses/informasi.\n\n"
        "**Cara kerja**\n"
        "- Pelaku membuat skenario (mengaku CS bank/IT kantor/kurir/teman)\n"
        "- Mengarahkan korban melakukan aksi: klik link, instal aplikasi, kirim OTP, transfer, dsb.\n\n"
        "**Ciri-ciri**\n"
        "- Mengatasnamakan otoritas, meminta rahasia (OTP/PIN/password)\n"
        "- Mendesak agar “segera” atau “jangan bilang siapa-siapa”\n"
        "- Meminta pindah ke channel lain atau instal aplikasi tertentu\n\n"
        "**Risiko**\n"
        "- Pengambilalihan akun, penipuan finansial, kebocoran data pribadi/korporat\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Jangan berikan OTP/PIN/password, meski mengaku dari pihak resmi\n"
        "2. Verifikasi identitas via saluran terpisah (nomor resmi/website resmi)\n"
        "3. Laporkan ke platform/instansi terkait dan beri tahu orang sekitar agar tidak ikut tertipu\n\n"
        "**Tips keamanan tambahan**\n"
        "- Terapkan prinsip *zero trust*: selalu verifikasi\n"
        "- Pisahkan email/nomor khusus untuk akun penting"
    ),
    "2fa": (
        "**Penjelasan singkat**\n"
        "**2FA/MFA** (*Two/Multi-Factor Authentication*) menambahkan lapisan verifikasi selain password, "
        "sehingga akun tetap lebih aman meski password bocor.\n\n"
        "**Cara kerja**\n"
        "- Setelah memasukkan password, sistem meminta faktor kedua: OTP/approval app/hardware key\n\n"
        "**Risiko jika tidak pakai 2FA**\n"
        "- Password yang bocor bisa langsung dipakai untuk ambil alih akun\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Aktifkan 2FA pada email utama (paling prioritas), lalu akun finansial dan sosial media\n"
        "2. Prioritaskan authenticator app atau passkey/hardware key\n"
        "3. Simpan *backup codes* di tempat aman (offline/manager)\n\n"
        "**Tips keamanan tambahan**\n"
        "- Waspadai permintaan OTP: pihak resmi tidak akan meminta OTP Anda\n"
        "- Jika dapat kode OTP tanpa login: segera ganti password dan cek aktivitas login"
    ),
    "scam": (
        "**Penjelasan singkat**\n"
        "**Scam/Penipuan online** adalah upaya menipu korban agar menyerahkan uang, data, atau akses akun.\n\n"
        "**Cara kerja**\n"
        "- Menggunakan iming-iming hadiah, investasi, pekerjaan, atau ancaman\n"
        "- Mengarahkan ke transfer cepat, link palsu, atau instal aplikasi\n\n"
        "**Ciri-ciri**\n"
        "- Janji keuntungan tidak masuk akal, “hadiah gratis”, atau “promo terakhir”\n"
        "- Tekanan waktu dan permintaan rahasia (OTP) atau transfer\n"
        "- Akun/nomor baru, testimoni meragukan, tautan pendek mencurigakan\n\n"
        "**Risiko**\n"
        "- Kehilangan uang, akun diambil alih, data pribadi tersebar\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Jangan transfer/klik link, berhenti komunikasi\n"
        "2. Verifikasi lewat kanal resmi, cek reputasi pihak terkait\n"
        "3. Simpan bukti dan laporkan ke platform/penyedia pembayaran\n\n"
        "**Tips keamanan tambahan**\n"
        "- Cek URL sebelum klik\n"
        "- Jangan mudah percaya screenshot “bukti transfer”\n\n"
        "**Langkah yang Disarankan**\n"
        "- Periksa link dengan **URL Scanner**"
    ),
    "vpn": (
        "**Penjelasan singkat**\n"
        "**VPN (Virtual Private Network)** membuat “terowongan” terenkripsi antara perangkat Anda dan server VPN, "
        "sehingga trafik lebih sulit disadap (terutama di Wi‑Fi publik).\n\n"
        "**Cara kerja**\n"
        "- Mengenkripsi koneksi, lalu meneruskan trafik melalui server VPN\n"
        "- Membantu privasi, namun tidak otomatis membuat Anda kebal terhadap phishing/malware\n\n"
        "**Risiko tanpa VPN di Wi‑Fi publik**\n"
        "- Penyadapan trafik, *session hijacking* (terutama jika situs tidak HTTPS), manipulasi hotspot palsu\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Gunakan VPN saat Wi‑Fi publik, terutama saat login akun penting\n"
        "2. Pastikan HTTPS aktif, hindari akses mobile banking jika hotspot tidak terpercaya\n"
        "3. Matikan auto-connect Wi‑Fi dan file sharing saat di tempat umum\n\n"
        "**Tips keamanan tambahan**\n"
        "- Pilih VPN berbayar yang reputasinya baik (no-log, audit, kill-switch)\n"
        "- Hindari VPN gratis yang menjual data atau menyisipkan iklan"
    ),
    "firewall": (
        "**Penjelasan singkat**\n"
        "**Firewall** adalah sistem yang memfilter lalu lintas jaringan masuk/keluar berdasarkan aturan, "
        "untuk mengurangi akses tidak sah.\n\n"
        "**Cara kerja**\n"
        "- Mengizinkan/menolak koneksi berdasarkan port, IP, protokol, atau aplikasi\n"
        "- Pada endpoint, bisa memblokir aplikasi yang mencoba koneksi mencurigakan\n\n"
        "**Risiko jika firewall dimatikan**\n"
        "- Permukaan serangan lebih besar, layanan terbuka bisa dipindai dan dieksploitasi\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Pastikan firewall OS aktif (mis. Windows Defender Firewall)\n"
        "2. Tutup port/layanan yang tidak perlu, batasi akses remote\n"
        "3. Untuk kantor: gunakan firewall jaringan + segmentasi + logging\n\n"
        "**Tips keamanan tambahan**\n"
        "- Jangan membuka port ke internet tanpa kebutuhan jelas\n"
        "- Kombinasikan dengan update rutin dan antivirus"
    ),
    "encryption": (
        "**Penjelasan singkat**\n"
        "**Enkripsi** mengubah data menjadi bentuk yang tidak bisa dibaca tanpa kunci, "
        "agar kerahasiaan tetap terjaga.\n\n"
        "**Cara kerja**\n"
        "- *In transit*: data saat dikirim (HTTPS/TLS, VPN)\n"
        "- *At rest*: data saat tersimpan (full disk encryption, database encryption)\n\n"
        "**Risiko jika tidak terenkripsi**\n"
        "- Data mudah disadap (di jaringan) atau dibaca saat perangkat hilang/diambil alih\n\n"
        "**Langkah yang harus dilakukan**\n"
        "1. Pastikan situs memakai HTTPS sebelum login/masukkan data sensitif\n"
        "2. Aktifkan enkripsi perangkat (mis. BitLocker/FileVault) untuk laptop kerja\n"
        "3. Gunakan aplikasi yang mendukung enkripsi end-to-end untuk komunikasi sensitif\n\n"
        "**Tips keamanan tambahan**\n"
        "- Enkripsi tidak menggantikan kebutuhan password kuat dan 2FA\n"
        "- Backup tetap diperlukan meski data terenkripsi"
    ),
}


_KEYWORD_MAP: Dict[str, List[str]] = {
    "phishing": [
        "phishing",
        "phish",
        "email palsu",
        "email penipuan",
        "penipuan email",
        "sms palsu",
        "pesan palsu",
        "link palsu",
        "tautan palsu",
        "website palsu",
        "situs palsu",
        "web palsu",
        "website aneh",
        "situs aneh",
        "tautan mencurigakan",
        "halaman login palsu",
        "form palsu",
        "pencurian akun",
        "akun dicuri",
        "akun dibajak",
        "akun kena hack",
        "akun diretas",
        "akun dibobol",
        "otp",
        "kode verifikasi",
    ],
    "malware": [
        "malware",
        "virus",
        "virus komputer",
        "virus laptop",
        "trojan",
        "spyware",
        "adware",
        "worm",
        "keylogger",
        "botnet",
        "aplikasi berbahaya",
    ],
    "ransomware": [
        "ransomware",
        "ransom",
        "tebusan",
        "enkripsi file",
        "file terenkripsi",
        "file terkunci",
        "ransom note",
    ],
    "password": [
        "password",
        "kata sandi",
        "sandi",
        "sandi akun",
        "passphrase",
        "credential",
        "login",
        "akun dibobol",
        "akun diretas",
        "akun kena hack",
        "password bocor",
        "password lemah",
        "kebocoran password",
    ],
    "social engineering": [
        "social engineering",
        "sosial engineering",
        "rekayasa sosial",
        "manipulasi",
        "menipu",
        "mengaku cs",
        "mengaku customer service",
        "mengaku admin",
        "mengaku petugas",
        "mengaku kurir",
    ],
    "2fa": [
        "2fa",
        "mfa",
        "two factor",
        "two-factor",
        "multi factor",
        "otp",
        "kode otp",
        "kode verifikasi",
        "autentikasi dua faktor",
        "autentikasi multi faktor",
        "authenticator",
        "google authenticator",
        "authy",
        "passkey",
    ],
    "scam": [
        "scam",
        "penipuan",
        "tipu",
        "modus",
        "hadiah gratis",
        "giveaway",
        "undian",
        "investasi bodong",
        "pinjol",
        "lowongan palsu",
        "transfer",
        "rekening",
        "whatsapp",
        "wa",
        "dm",
    ],
    "vpn": [
        "vpn",
        "virtual private",
        "wifi publik",
        "wi fi publik",
        "hotspot",
        "public wifi",
        "jaringan publik",
    ],
    "firewall": [
        "firewall",
        "fire wall",
        "port",
        "blokir koneksi",
        "filter jaringan",
    ],
    "encryption": [
        "enkripsi",
        "encryption",
        "encrypt",
        "https",
        "tls",
        "ssl",
        "end to end",
        "e2ee",
        "disk encryption",
    ],
}

_PHRASE_SYNONYMS: Dict[str, str] = {
    "kata sandi": "password",
    "sandi akun": "password",
    "passwrod": "password",
    "pasword": "password",
    "paswod": "password",
    "password bocor": "password bocor",
    "kode verifikasi": "otp",
    "kode otp": "otp",
    "one time password": "otp",
    "autentikasi dua faktor": "2fa",
    "autentikasi multi faktor": "2fa",
    "rekayasa sosial": "social engineering",
    "wifi publik": "wifi publik",
    "wi fi publik": "wifi publik",
    "web palsu": "website palsu",
}

_TOKEN_SYNONYMS: Dict[str, str] = {
    "phising": "phishing",
    "pishing": "phishing",
    "phishin": "phishing",
    "malwer": "malware",
    "mallware": "malware",
    "malwaer": "malware",
    "ransomeware": "ransomware",
    "ransmware": "ransomware",
    "ransomwer": "ransomware",
    "passwrod": "password",
    "pasword": "password",
    "paswod": "password",
    "katasandi": "password",
    "verif": "verifikasi",
    "otpp": "otp",
    "wifii": "wifi",
    "whatsap": "whatsapp",
    "watshapp": "whatsapp",
    "akun": "akun",
    "hack": "hack",
    "hacked": "hack",
    "diretas": "hack",
    "dibobol": "hack",
}

_REPEAT_CHAR_RE = re.compile(r"(.)\1{2,}")
_NON_ALNUM_RE = re.compile(r"[^0-9a-z\s]+")
_WHITESPACE_RE = re.compile(r"\s+")


def _normalize_message(message: str) -> str:
    text = message.strip().lower()
    text = _REPEAT_CHAR_RE.sub(r"\1", text)
    text = _NON_ALNUM_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()

    for phrase, replacement in _PHRASE_SYNONYMS.items():
        text = re.sub(rf"\b{re.escape(phrase)}\b", replacement, text)

    tokens = []
    for token in text.split():
        tokens.append(_TOKEN_SYNONYMS.get(token, token))

    return " ".join(tokens)


def _tokenize(message: str) -> List[str]:
    return [t for t in message.split() if t]


def _seq_ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _fuzzy_token_in_tokens(token: str, tokens: Sequence[str], min_ratio: float = 0.88) -> bool:
    if len(token) < 4:
        return False
    for t in tokens:
        if t == token:
            return True
        if abs(len(t) - len(token)) > 2:
            continue
        if _seq_ratio(t, token) >= min_ratio:
            return True
    return False


def _is_otp_scam_context(message: str) -> bool:
    indicators = ("minta", "meminta", "kirim", "share", "bagikan", "kode", "otp", "verifikasi", "login")
    return any(x in message for x in indicators) and ("otp" in message or "verifikasi" in message)


def _is_suspicious_link_context(message: str) -> bool:
    indicators = (
        "link",
        "tautan",
        "url",
        "website",
        "web",
        "hadiah",
        "giveaway",
        "gratis",
        "bonus",
        "promo",
    )
    return any(x in message for x in indicators) and ("link" in message or "tautan" in message or "url" in message)


def _is_password_leak_context(message: str) -> bool:
    indicators = ("bocor", "leak", "kebocoran", "dibobol", "diretas", "kena hack", "akun diambil alih")
    return "password" in message and any(x in message for x in indicators)


def _is_public_wifi_context(message: str) -> bool:
    return "wifi publik" in message or "public wifi" in message or "hotspot" in message


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

    normalized = _normalize_message(user_message)
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
    tokens = _tokenize(message)

    for topic, keywords in _KEYWORD_MAP.items():
        matches = 0
        for kw in keywords:
            if kw in message:
                matches += 1
                continue
            if " " not in kw and _fuzzy_token_in_tokens(kw, tokens):
                matches += 1
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
        if _is_otp_scam_context(message):
            return (
                "**Penjelasan singkat**\n"
                "Permintaan **OTP/kode verifikasi** hampir selalu terkait upaya pengambilalihan akun. "
                "OTP adalah “kunci sekali pakai” untuk login atau reset akun.\n\n"
                "**Risiko**\n"
                "- Akun diambil alih, transaksi ilegal, perubahan email/nomor pemulihan\n\n"
                "**Langkah yang harus dilakukan**\n"
                "1. Jangan berikan OTP/kode verifikasi ke siapa pun\n"
                "2. Jika Anda sudah terlanjur membagikan: segera ganti password, logout semua sesi, aktifkan 2FA, dan cek aktivitas login\n"
                "3. Hubungi CS resmi via aplikasi/website resmi untuk mengamankan akun\n\n"
                "**Tips keamanan tambahan**\n"
                "- Pihak resmi tidak meminta OTP Anda\n"
                "- Aktifkan notifikasi login dan simpan *backup codes*\n\n"
                "**Langkah yang Disarankan**\n"
                "- Aktifkan 2FA/MFA dan gunakan authenticator app"
            )

        if _is_suspicious_link_context(message):
            return (
                "**Penjelasan singkat**\n"
                "Link “hadiah gratis/promo/bonus” sering dipakai untuk **phishing** atau pemasangan malware.\n\n"
                "**Risiko**\n"
                "- Website palsu mencuri password/OTP, atau file berisi malware\n\n"
                "**Langkah yang harus dilakukan**\n"
                "1. Jangan klik link sebelum diperiksa\n"
                "2. Cek domain dengan teliti (typo, subdomain aneh), dan pastikan HTTPS\n"
                "3. Verifikasi promo lewat aplikasi/akun resmi brand tersebut\n\n"
                "**Tips keamanan tambahan**\n"
                "- Hindari mengisi form yang meminta data sensitif\n"
                "- Waspadai tautan pendek dan akun pengirim baru\n\n"
                "**Langkah yang Disarankan**\n"
                "- Periksa link menggunakan **URL Scanner**"
            )

        if _is_password_leak_context(message):
            return (
                "**Penjelasan singkat**\n"
                "Jika **password bocor** atau akun pernah dibobol, anggap credential tersebut tidak aman lagi.\n\n"
                "**Risiko**\n"
                "- *Credential stuffing* ke akun lain, pembajakan email utama, pencurian identitas\n\n"
                "**Langkah yang harus dilakukan**\n"
                "1. Ganti password sekarang (utamakan email utama), dan jangan pakai ulang password lama\n"
                "2. Logout dari semua perangkat/sesi aktif\n"
                "3. Aktifkan 2FA/MFA dan perbarui email/nomor pemulihan\n"
                "4. Cek aturan forwarding email dan aplikasi pihak ketiga yang terhubung\n\n"
                "**Tips keamanan tambahan**\n"
                "- Gunakan password manager untuk password unik\n"
                "- Aktifkan notifikasi login dan review perangkat yang terhubung\n\n"
                "**Langkah yang Disarankan**\n"
                "- Cek password dengan **Password Checker** dan aktifkan 2FA"
            )

        if _is_public_wifi_context(message):
            return (
                "**Penjelasan singkat**\n"
                "Wi‑Fi publik berisiko karena Anda tidak tahu siapa pengelolanya dan siapa yang memantau trafik.\n\n"
                "**Risiko**\n"
                "- Penyadapan, hotspot palsu, pencurian sesi login (terutama jika situs tidak HTTPS)\n\n"
                "**Langkah yang harus dilakukan**\n"
                "1. Gunakan VPN saat terhubung Wi‑Fi publik\n"
                "2. Hindari login ke akun finansial jika ragu\n"
                "3. Matikan auto-connect dan file sharing\n\n"
                "**Tips keamanan tambahan**\n"
                "- Pastikan HTTPS aktif\n"
                "- Gunakan tethering jika memungkinkan\n\n"
                "**Langkah yang Disarankan**\n"
                "- Gunakan VPN dan periksa URL sebelum login"
            )

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
            "Jika ada pertanyaan lain, saya siap membantu."
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
