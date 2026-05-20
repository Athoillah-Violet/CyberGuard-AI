"""
app.py — CyberGuard AI
Aplikasi utama Streamlit: UI, navigasi, dashboard, dan integrasi modul.
Jalankan: streamlit run app.py
"""

import streamlit as st
from pathlib import Path

import engine
import fms

# ---------------------------------------------------------------------------
# Konfigurasi Halaman (harus pertama)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="CyberGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Load Custom CSS (path relatif — kompatibel Streamlit Cloud)
# ---------------------------------------------------------------------------

def load_css() -> None:
    """
    Memuat file style.css ke halaman Streamlit.

    Menggunakan Path(__file__) agar path selalu relatif terhadap
    lokasi app.py — aman untuk deploy lokal maupun cloud.
    """
    css_path = Path(__file__).parent / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


# ---------------------------------------------------------------------------
# Inisialisasi Session State
# ---------------------------------------------------------------------------

def init_session_state() -> None:
    """
    Menginisialisasi variabel session_state untuk chat history
    dan navigasi halaman.
    """
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if "chat_initialized" not in st.session_state:
        st.session_state.chat_initialized = False


init_session_state()


# ---------------------------------------------------------------------------
# Helper UI Functions
# ---------------------------------------------------------------------------

def render_badge(level: str) -> str:
    """
    Membuat HTML badge berdasarkan level keamanan.

    Args:
        level: Level status (Safe, Suspicious, Dangerous, Weak, Medium, Strong).

    Returns:
        str: HTML string badge.
    """
    level_lower = level.lower()
    css_class = f"cg-badge cg-badge-{level_lower}"
    return f'<span class="{css_class}">{level}</span>'


def render_progress_bar(score: int, level: str) -> str:
    """
    Membuat HTML progress bar untuk skor keamanan password.

    Args:
        score: Skor 0-100.
        level: Level (Weak, Medium, Strong).

    Returns:
        str: HTML progress bar.
    """
    level_class = level.lower()
    return (
        f'<div class="cg-progress-track">'
        f'<div class="cg-progress-fill cg-progress-{level_class}" '
        f'style="width: {score}%;"></div></div>'
    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_sidebar() -> str:
    """
    Merender sidebar navigasi dan mengembalikan halaman yang dipilih.

    Returns:
        str: Nama halaman aktif.
    """
    with st.sidebar:
        st.markdown(
            """
            <div class="cg-sidebar-logo">
                <div class="logo-icon">🛡️</div>
                <h2>CyberGuard AI</h2>
                <p class="tagline">Security Assistant</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("##### 📍 Navigasi")
        page = st.radio(
            "Menu",
            [
                "Dashboard",
                "AI Chatbot",
                "Password Checker",
                "URL Scanner",
                "Security Tips",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        st.markdown("##### 🔒 Status Keamanan")
        st.markdown(
            """
            <p style="font-size:0.85rem;color:#94a3b8;">
                <span class="cg-status-dot cg-status-active"></span>
                Sistem Aktif & Terlindungi
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        st.markdown("##### ⚡ Quick Tools")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💬 Chat", use_container_width=True):
                st.session_state.current_page = "AI Chatbot"
        with col2:
            if st.button("🔑 Pass", use_container_width=True):
                st.session_state.current_page = "Password Checker"

        st.markdown("---")

        st.markdown("##### ℹ️ About")
        st.markdown(
            """
            <p style="font-size:0.78rem;color:#64748b;line-height:1.5;">
            <b>CyberGuard AI</b> v1.0<br>
            AI Cyber Security Assistant<br>
            Edukasi • Analisis • Proteksi<br><br>
            <i>Bukan tools hacking — fokus edukasi & awareness.</i>
            </p>
            """,
            unsafe_allow_html=True,
        )

    return page


# ---------------------------------------------------------------------------
# Dashboard / Welcome Screen
# ---------------------------------------------------------------------------

def render_dashboard() -> None:
    """
    Merender halaman dashboard utama dengan welcome screen,
    metric cards, quick start, dan penjelasan fitur.
    """
    st.markdown(
        """
        <div class="cg-hero">
            <div class="cg-hero-icon">🛡️</div>
            <h1>CyberGuard AI</h1>
            <p>Asisten Keamanan Siber Profesional — Edukasi, Analisis, dan Proteksi Digital Anda</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Metric cards
    cols = st.columns(4)
    metrics = [
        ("🎯", "Threat Detection", "Active"),
        ("🔐", "Password Security", "Enabled"),
        ("🔗", "Link Safety", "Monitoring"),
        ("🤖", "AI Protection", "Online"),
    ]
    for col, (icon, label, value) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="cg-metric">
                    <div class="cg-metric-icon">{icon}</div>
                    <div class="cg-metric-value">{value}</div>
                    <div class="cg-metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="cg-section-title">🚀 <span>Quick Start</span></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(
            """
            <div class="cg-card">
                <h3>📋 Petunjuk Penggunaan</h3>
                <ol class="cg-steps">
                    <li>Gunakan <b>AI Chatbot</b> untuk bertanya tentang cyber security</li>
                    <li>Gunakan <b>Password Checker</b> untuk mengecek keamanan password</li>
                    <li>Gunakan <b>URL Scanner</b> untuk mendeteksi link phishing</li>
                    <li>Gunakan <b>sidebar</b> untuk navigasi antar fitur</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            """
            <div class="cg-card">
                <h3>✨ Fitur Utama</h3>
                <ul>
                    <li><b>AI Chatbot</b> — Tanya jawab keamanan siber interaktif</li>
                    <li><b>Password Checker</b> — Analisis kekuatan password real-time</li>
                    <li><b>URL Scanner</b> — Deteksi indikasi phishing pada link</li>
                    <li><b>Security Tips</b> — Tips keamanan digital terkini</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="cg-section-title">💡 <span>Tip Hari Ini</span></div>', unsafe_allow_html=True)
    tip = fms.get_random_tip()
    st.markdown(f'<div class="cg-tip-box">💡 {tip}</div>', unsafe_allow_html=True)

    st.markdown('<div class="cg-section-title">🎯 <span>Mulai Sekarang</span></div>', unsafe_allow_html=True)
    btn_cols = st.columns(4)
    actions = [
        ("💬 Buka Chatbot", "AI Chatbot"),
        ("🔑 Cek Password", "Password Checker"),
        ("🔗 Scan URL", "URL Scanner"),
        ("📚 Lihat Tips", "Security Tips"),
    ]
    for col, (label, target_page) in zip(btn_cols, actions):
        with col:
            if st.button(label, use_container_width=True, key=f"dash_{target_page}"):
                st.session_state.current_page = target_page
                st.rerun()


# ---------------------------------------------------------------------------
# AI Chatbot Page
# ---------------------------------------------------------------------------

def render_chatbot() -> None:
    """
    Merender halaman chatbot AI dengan history dan input pengguna.
    """
    st.markdown('<div class="cg-section-title">💬 <span>AI Cyber Security Chatbot</span></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="cg-card">
            <p>Tanyakan apa saja tentang phishing, malware, ransomware, password security,
            social engineering, dan topik cyber lainnya.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.chat_initialized:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": engine.get_welcome_message(),
        })
        st.session_state.chat_initialized = True

    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div class="cg-chat-user">
                        <div class="cg-chat-label">Anda</div>
                        {msg["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(msg["content"])
                st.markdown(
                    '<div style="margin-bottom:0.75rem;"></div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.chat_input("Ketik pertanyaan cyber security Anda...")
    with col_send:
        send_clicked = st.button("Kirim 📤", use_container_width=True)

    message = user_input if user_input else None

    if send_clicked:
        quick = st.session_state.get("quick_question", "")
        if quick:
            message = quick
            st.session_state.quick_question = ""

    if message:
        st.session_state.chat_history.append({
            "role": "user",
            "content": message,
        })

        result = engine.process_message(
            message,
            st.session_state.chat_history,
        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": result["response"],
        })

        st.rerun()

    st.markdown("##### 💡 Pertanyaan Cepat")
    quick_cols = st.columns(4)
    quick_questions = [
        "Apa itu phishing?",
        "Tips password aman?",
        "Apa itu ransomware?",
        "Cara aktifkan 2FA?",
    ]
    for col, q in zip(quick_cols, quick_questions):
        with col:
            if st.button(q, use_container_width=True, key=f"quick_{q}"):
                st.session_state.quick_question = q
                st.session_state.chat_history.append({"role": "user", "content": q})
                result = engine.process_message(q, st.session_state.chat_history)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result["response"],
                })
                st.rerun()

    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.chat_history = []
        st.session_state.chat_initialized = False
        st.rerun()


# ---------------------------------------------------------------------------
# Password Checker Page
# ---------------------------------------------------------------------------

def render_password_checker() -> None:
    """
    Merender halaman analisis kekuatan password.
    """
    st.markdown('<div class="cg-section-title">🔑 <span>Password Strength Checker</span></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="cg-card">
            <p>Masukkan password untuk dianalisis. Password <b>tidak disimpan</b>
            dan hanya diproses di session Anda.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    password = st.text_input(
        "Masukkan Password",
        type="password",
        placeholder="Ketik password untuk dianalisis...",
    )

    if password:
        result = fms.check_password_strength(password)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f'<div style="text-align:center;margin:1rem 0;">'
                f'{render_badge(result["level"])}</div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.metric("Security Score", f'{result["score"]}/100')
        with col3:
            st.metric("Estimasi Crack", result["crack_estimate"])

        st.markdown(render_progress_bar(result["score"], result["level"]), unsafe_allow_html=True)

        st.markdown("##### 📊 Detail Analisis")
        check_labels = {
            "length_8": "Panjang ≥ 8 karakter",
            "length_12": "Panjang ≥ 12 karakter",
            "uppercase": "Huruf besar (A-Z)",
            "lowercase": "Huruf kecil (a-z)",
            "digit": "Angka (0-9)",
            "symbol": "Simbol khusus",
            "no_common": "Bukan password umum",
            "no_sequence": "Tanpa urutan sederhana",
        }
        check_cols = st.columns(2)
        checks = result["checks"]
        items = list(check_labels.items())
        for i, (key, label) in enumerate(items):
            with check_cols[i % 2]:
                status = "✅" if checks.get(key, False) else "❌"
                st.markdown(f"{status} {label}")

        st.markdown("##### 💡 Rekomendasi")
        for rec in result["recommendations"]:
            st.markdown(f'<div class="cg-finding">→ {rec}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# URL Scanner Page
# ---------------------------------------------------------------------------

def render_url_scanner() -> None:
    """
    Merender halaman deteksi URL/phishing.
    """
    st.markdown('<div class="cg-section-title">🔗 <span>URL / Phishing Detector</span></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="cg-card">
            <p>Masukkan URL untuk dianalisis indikasi phishing.
            Analisis berbasis heuristik — verifikasi manual tetap disarankan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    url_input = st.text_input(
        "Masukkan URL",
        placeholder="https://example.com atau example.com",
    )

    if st.button("🔍 Scan URL", use_container_width=False):
        if not url_input:
            st.warning("Masukkan URL terlebih dahulu.")
        else:
            result = fms.analyze_url(url_input)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    f'<div style="text-align:center;margin:1rem 0;">'
                    f'{render_badge(result["status"])}</div>',
                    unsafe_allow_html=True,
                )
            with col2:
                st.metric("Risk Score", f'{result["risk_score"]}/100')

            st.markdown(f'<div class="cg-tip-box">{result["summary"]}</div>', unsafe_allow_html=True)

            st.markdown("##### 🔎 Temuan Analisis")
            for finding in result["findings"]:
                st.markdown(f'<div class="cg-finding">⚠️ {finding}</div>', unsafe_allow_html=True)

            st.markdown(f'<p style="color:#64748b;font-size:0.8rem;">URL diperiksa: {result.get("url_checked", url_input)}</p>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Security Tips Page
# ---------------------------------------------------------------------------

def render_security_tips() -> None:
    """
    Merender halaman tips keamanan siber.
    """
    st.markdown('<div class="cg-section-title">📚 <span>Cyber Security Tips</span></div>', unsafe_allow_html=True)

    tip = fms.get_random_tip()
    st.markdown(f'<div class="cg-tip-box">💡 <b>Tip Acak:</b> {tip}</div>', unsafe_allow_html=True)

    if st.button("🔄 Tip Baru", use_container_width=False):
        st.rerun()

    st.markdown("##### 📋 Semua Tips Keamanan")
    for i, tip_text in enumerate(fms.get_all_tips(), 1):
        st.markdown(
            f'<div class="cg-card" style="padding:0.75rem 1rem;">'
            f'<p style="margin:0;"><b>{i}.</b> {tip_text}</p></div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Main Router
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Entry point aplikasi — mengatur routing halaman berdasarkan sidebar.
    """
    page = render_sidebar()

    if st.session_state.get("current_page") and st.session_state.current_page != page:
        override = st.session_state.current_page
        if override in ["AI Chatbot", "Password Checker", "URL Scanner", "Security Tips", "Dashboard"]:
            page = override
            st.session_state.current_page = page

    pages = {
        "Dashboard": render_dashboard,
        "AI Chatbot": render_chatbot,
        "Password Checker": render_password_checker,
        "URL Scanner": render_url_scanner,
        "Security Tips": render_security_tips,
    }

    render_fn = pages.get(page, render_dashboard)
    render_fn()


if __name__ == "__main__":
    main()
