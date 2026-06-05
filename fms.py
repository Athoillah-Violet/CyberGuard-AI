"""
fms.py — Feature Module Security
Modul analisis keamanan: password checker, URL/phishing detector, dan cyber tips.
"""

import re
import random
from typing import Dict, List
from urllib.parse import urlsplit


# ---------------------------------------------------------------------------
# Cyber Security Tips
# ---------------------------------------------------------------------------

CYBER_TIPS: List[str] = [
    "Aktifkan Two-Factor Authentication (2FA) di semua akun penting Anda.",
    "Jangan pernah mengklik link mencurigakan dari email atau pesan tidak dikenal.",
    "Gunakan password unik untuk setiap akun — jangan gunakan password yang sama.",
    "Perbarui software dan sistem operasi secara rutin untuk menutup celah keamanan.",
    "Backup data penting secara berkala ke lokasi terpisah (cloud atau external drive).",
    "Waspadai social engineering — penyerang sering memanipulasi emosi, bukan teknologi.",
    "Gunakan password manager untuk menyimpan dan membuat password yang kuat.",
    "Periksa URL sebelum memasukkan kredensial — pastikan domain resmi dan HTTPS aktif.",
    "Jangan membagikan OTP atau kode verifikasi kepada siapa pun, termasuk yang mengaku support.",
    "Nonaktifkan fitur auto-fill password di perangkat publik atau bersama.",
    "Gunakan VPN saat terhubung ke Wi-Fi publik untuk enkripsi lalu lintas data.",
    "Review permission aplikasi di smartphone — cabut akses yang tidak diperlukan.",
    "Aktifkan notifikasi login untuk mendeteksi akses tidak sah ke akun Anda.",
    "Hindari mengunduh file dari sumber tidak terpercaya — risiko malware tinggi.",
    "Edukasi diri dan tim tentang phishing — awareness adalah pertahanan pertama.",
]


def get_random_tip() -> str:
    """
    Mengambil satu tips keamanan siber secara acak dari database tips.

    Returns:
        str: Satu kalimat tips keamanan cyber.
    """
    return random.choice(CYBER_TIPS)


def get_all_tips() -> List[str]:
    """
    Mengembalikan seluruh daftar tips keamanan siber.

    Returns:
        List[str]: List berisi semua tips yang tersedia.
    """
    return CYBER_TIPS.copy()


# ---------------------------------------------------------------------------
# Password Strength Checker
# ---------------------------------------------------------------------------

def check_password_strength(password: str) -> Dict:
    """
    Menganalisis kekuatan password berdasarkan kriteria standar keamanan.

    Kriteria yang dievaluasi:
        - Panjang minimum 8 karakter (ideal 12+)
        - Huruf besar (A-Z)
        - Huruf kecil (a-z)
        - Angka (0-9)
        - Simbol khusus

    Args:
        password: String password yang akan dianalisis.

    Returns:
        Dict berisi: score, level, checks, recommendations, crack_estimate.
    """
    if not password:
        return {
            "score": 0,
            "level": "Weak",
            "checks": {},
            "recommendations": ["Masukkan password untuk dianalisis."],
            "crack_estimate": "N/A",
        }

    checks = {
        "length_8": len(password) >= 8,
        "length_12": len(password) >= 12,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "symbol": bool(re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]", password)),
        "no_common": password.lower() not in _COMMON_PASSWORDS,
        "no_sequence": not _has_simple_sequence(password),
    }

    score = 0
    if checks["length_8"]:
        score += 15
    if checks["length_12"]:
        score += 15
    if checks["uppercase"]:
        score += 15
    if checks["lowercase"]:
        score += 15
    if checks["digit"]:
        score += 15
    if checks["symbol"]:
        score += 15
    if checks["no_common"]:
        score += 5
    if checks["no_sequence"]:
        score += 5

    score = min(score, 100)

    if score < 40:
        level = "Weak"
        crack_estimate = "Kurang dari 1 menit"
    elif score < 70:
        level = "Medium"
        crack_estimate = "Beberapa jam hingga hari"
    else:
        level = "Strong"
        crack_estimate = "Bertahun-tahun (estimasi)"

    recommendations = _build_password_recommendations(checks, password)

    return {
        "score": score,
        "level": level,
        "checks": checks,
        "recommendations": recommendations,
        "crack_estimate": crack_estimate,
        "length": len(password),
    }


def _build_password_recommendations(checks: Dict, password: str) -> List[str]:
    """
    Membangun daftar rekomendasi perbaikan berdasarkan hasil pengecekan.

    Args:
        checks: Dictionary hasil evaluasi kriteria password.
        password: Password asli untuk analisis tambahan.

    Returns:
        List[str]: Rekomendasi yang belum terpenuhi.
    """
    recs: List[str] = []

    if not checks["length_8"]:
        recs.append("Gunakan minimal 8 karakter (disarankan 12+ karakter).")
    elif not checks["length_12"]:
        recs.append("Tingkatkan panjang password menjadi minimal 12 karakter.")

    if not checks["uppercase"]:
        recs.append("Tambahkan huruf besar (A-Z).")
    if not checks["lowercase"]:
        recs.append("Tambahkan huruf kecil (a-z).")
    if not checks["digit"]:
        recs.append("Tambahkan angka (0-9).")
    if not checks["symbol"]:
        recs.append("Tambahkan simbol khusus (!@#$%^&* dll).")
    if not checks["no_common"]:
        recs.append("Hindari password umum seperti 'password123' atau 'qwerty'.")
    if not checks["no_sequence"]:
        recs.append("Hindari urutan sederhana seperti '12345' atau 'abcde'.")

    if not recs:
        recs.append("Password Anda sudah memenuhi kriteria keamanan yang baik. Pertahankan!")

    return recs


def _has_simple_sequence(password: str) -> bool:
    """
    Mendeteksi urutan karakter sederhana dalam password.

    Args:
        password: Password yang diperiksa.

    Returns:
        bool: True jika ditemukan pola urutan sederhana.
    """
    sequences = ["12345", "23456", "abcde", "qwerty", "asdfg", "password"]
    lower = password.lower()
    return any(seq in lower for seq in sequences)


_COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678", "qwerty",
    "abc123", "monkey", "letmein", "admin", "welcome",
    "iloveyou", "dragon", "master", "sunshine", "princess",
}


# ---------------------------------------------------------------------------
# URL / Phishing Detector
# ---------------------------------------------------------------------------

_SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "account", "update", "confirm",
    "banking", "paypal", "wallet", "signin", "credential", "suspend",
    "urgent", "click", "free", "winner", "prize", "claim",
]

_SUSPICIOUS_TLDS = [
    ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top", ".work",
    ".click", ".link", ".buzz", ".icu",
]

_BRAND_KEYWORDS = [
    "paypal", "google", "facebook", "instagram", "amazon",
    "microsoft", "apple", "netflix", "bank", "bca", "mandiri",
    "bni", "bri", "tokopedia", "shopee", "grab", "gojek",
]

_ADULT_KEYWORDS = [
    "porn",
    "porno",
    "bokep",
    "xxx",
    "sex",
    "adult",
    "nsfw",
    "hentai",
]

_GAMBLING_KEYWORDS = [
    "judi",
    "judol",
    "slot",
    "casino",
    "poker",
    "togel",
    "bet",
    "sportsbook",
]


def _extract_url_parts(url: str) -> Dict[str, str]:
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    path = (parts.path or "").lower()
    query = (parts.query or "").lower()
    return {"host": host, "path": path, "query": query}


def _tokenize_text(text: str) -> List[str]:
    return [t for t in re.split(r"[^0-9a-z]+", text.lower()) if t]


def _token_matches_keyword(token: str, keyword: str) -> bool:
    if token == keyword:
        return True
    if keyword == "sex":
        return False
    if keyword == "bet":
        return token.startswith("bet") and len(token) > 3 and token[3].isdigit()
    prefix_ok = {
        "porn",
        "porno",
        "bokep",
        "xxx",
        "adult",
        "nsfw",
        "hentai",
        "judi",
        "judol",
        "slot",
        "casino",
        "poker",
        "togel",
        "sportsbook",
    }
    if keyword in prefix_ok:
        return token.startswith(keyword) or token.endswith(keyword)
    return False


def _detect_content_risk(url: str) -> Dict[str, List[str]]:
    parts = _extract_url_parts(url)
    tokens = _tokenize_text(" ".join([parts["host"], parts["path"], parts["query"]]))

    adult_hits_set = set()
    gambling_hits_set = set()

    for token in tokens:
        for kw in _ADULT_KEYWORDS:
            if _token_matches_keyword(token, kw):
                adult_hits_set.add(kw)
        for kw in _GAMBLING_KEYWORDS:
            if _token_matches_keyword(token, kw):
                gambling_hits_set.add(kw)

    adult_hits = sorted(adult_hits_set)
    gambling_hits = sorted(gambling_hits_set)

    return {"adult": adult_hits, "gambling": gambling_hits}


def analyze_url(url: str) -> Dict:
    """
    Menganalisis URL untuk indikasi phishing menggunakan heuristik sederhana.

    Metode analisis:
        - Validasi format URL
        - Deteksi keyword mencurigakan
        - Deteksi TLD berisiko
        - Deteksi IP address sebagai host
        - Deteksi typosquatting brand populer
        - Panjang URL berlebihan

    Args:
        url: URL yang akan dianalisis.

    Returns:
        Dict berisi: status, risk_score, findings, summary.
    """
    if not url or not url.strip():
        return {
            "status": "Suspicious",
            "risk_score": 50,
            "findings": ["URL kosong — tidak dapat dianalisis."],
            "summary": "Masukkan URL yang valid untuk pemindaian.",
        }

    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    findings: List[str] = []
    risk_score = 0

    # Cek HTTPS
    if not url.lower().startswith("https://"):
        findings.append("URL tidak menggunakan HTTPS — koneksi tidak terenkripsi.")
        risk_score += 20

    url_lower = url.lower()
    content_risk = _detect_content_risk(url_lower)
    if content_risk["adult"] or content_risk["gambling"]:
        hits: List[str] = []
        if content_risk["adult"]:
            hits.append(f"konten dewasa ({', '.join(content_risk['adult'][:5])})")
        if content_risk["gambling"]:
            hits.append(f"perjudian/judi online ({', '.join(content_risk['gambling'][:5])})")
        findings.append(
            "Indikasi kategori berisiko terdeteksi dari domain/path: " + " dan ".join(hits) + "."
        )
        risk_score = max(risk_score, 70)

    # Keyword mencurigakan
    found_keywords = [kw for kw in _SUSPICIOUS_KEYWORDS if kw in url_lower]
    if found_keywords:
        findings.append(
            f"Keyword mencurigakan terdeteksi: {', '.join(found_keywords[:5])}."
        )
        risk_score += min(len(found_keywords) * 8, 30)

    # TLD berisiko
    for tld in _SUSPICIOUS_TLDS:
        if tld in url_lower:
            findings.append(f"TLD berisiko terdeteksi ({tld}) — sering dipakai phishing.")
            risk_score += 25
            break

    # IP address sebagai host
    if re.search(r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url_lower):
        findings.append("URL menggunakan alamat IP langsung — indikasi mencurigakan.")
        risk_score += 30

    # Typosquatting brand
    for brand in _BRAND_KEYWORDS:
        if brand in url_lower:
            domain_match = re.search(
                rf"https?://([^/]+)", url_lower
            )
            if domain_match:
                host = domain_match.group(1)
                if brand in host and not _is_legitimate_domain(host, brand):
                    findings.append(
                        f"Kemungkinan typosquatting brand '{brand}' — domain tidak resmi."
                    )
                    risk_score += 35
            break

    # URL terlalu panjang
    if len(url) > 150:
        findings.append("URL sangat panjang — teknik penyamaran umum pada phishing.")
        risk_score += 15

    # Banyak subdomain
    subdomain_count = url_lower.count(".") - 1
    if subdomain_count > 4:
        findings.append("Terlalu banyak subdomain — pola umum link phishing.")
        risk_score += 20

    # @ symbol (credential hiding)
    if "@" in url:
        findings.append("Karakter '@' dalam URL — teknik menyembunyikan domain asli.")
        risk_score += 40

    # Double slash setelah domain
    if re.search(r"https?://[^/]+//", url_lower):
        findings.append("Double slash setelah domain — indikasi manipulasi URL.")
        risk_score += 15

    risk_score = min(risk_score, 100)

    if risk_score >= 60:
        status = "Dangerous"
        summary = "URL ini berpotensi berbahaya. Jangan buka atau masukkan data pribadi."
    elif risk_score >= 30:
        status = "Suspicious"
        summary = "URL menunjukkan beberapa indikasi mencurigakan. Verifikasi sebelum mengakses."
    else:
        status = "Safe"
        summary = "URL tidak menunjukkan indikasi phishing yang jelas. Tetap waspada."

    if content_risk["adult"] or content_risk["gambling"]:
        status = "Dangerous"
        summary = (
            "URL terindikasi mengarah ke kategori berisiko (konten dewasa/perjudian). "
            "Hindari akses, terutama dari perangkat kerja/akun utama."
        )

    if not findings:
        findings.append("Tidak ditemukan indikasi phishing berdasarkan analisis heuristik.")

    return {
        "status": status,
        "risk_score": risk_score,
        "findings": findings,
        "summary": summary,
        "url_checked": url,
    }


def _is_legitimate_domain(host: str, brand: str) -> bool:
    """
    Memeriksa apakah host merupakan domain resmi dari brand tertentu.

    Args:
        host: Hostname dari URL.
        brand: Nama brand yang dicocokkan.

    Returns:
        bool: True jika domain tampak legitimate.
    """
    legitimate_patterns = {
        "google": ["google.com", "google.co.id", "gmail.com", "youtube.com"],
        "facebook": ["facebook.com", "fb.com", "meta.com"],
        "paypal": ["paypal.com"],
        "amazon": ["amazon.com", "amazon.co.id"],
        "microsoft": ["microsoft.com", "live.com", "outlook.com"],
        "apple": ["apple.com", "icloud.com"],
        "netflix": ["netflix.com"],
    }
    patterns = legitimate_patterns.get(brand, [f"{brand}.com"])
    return any(host.endswith(p) or host == p for p in patterns)
