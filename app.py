"""
app.py — CyberGuard AI
Aplikasi utama Streamlit: UI, navigasi, dashboard, onboarding, dan integrasi modul.
Jalankan: streamlit run app.py
"""

import streamlit as st
from pathlib import Path

import engine
import fms

# ---------------------------------------------------------------------------
# Konstanta navigasi — daftar halaman yang valid di aplikasi
# ---------------------------------------------------------------------------

VALID_PAGES = [
    "Dashboard",
    "AI Chatbot",
    "Password Checker",
    "URL Scanner",
    "Security Tips",
]

# Metadata halaman untuk tampilan dekoratif sidebar
PAGE_META = {
    "Dashboard": ("🏠", "Dashboard"),
    "AI Chatbot": ("💬", "AI Chatbot"),
    "Password Checker": ("🔑", "Password Checker"),
    "URL Scanner": ("🔗", "URL Scanner"),
    "Security Tips": ("📚", "Security Tips"),
}

# ---------------------------------------------------------------------------
# Konfigurasi Halaman (harus dipanggil pertama oleh Streamlit)
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

_LIGHT_THEME_CSS = """
:root {
    --cg-bg-primary: #f8fafc;
    --cg-bg-secondary: #f1f5ff;
    --cg-bg-card: rgba(255, 255, 255, 0.92);
    --cg-blue-neon: #0ea5e9;
    --cg-blue-electric: #2563eb;
    --cg-blue-glow: rgba(14, 165, 233, 0.18);
    --cg-accent: #2563eb;
    --cg-text-primary: #0b1220;
    --cg-text-muted: #64748b;
    --cg-border: rgba(37, 99, 235, 0.14);
    --cg-shadow: 0 10px 26px rgba(15, 23, 42, 0.10);
}

.stApp {
    background: radial-gradient(900px circle at 20% 0%, rgba(14, 165, 233, 0.16), transparent 55%),
        radial-gradient(900px circle at 80% 20%, rgba(37, 99, 235, 0.12), transparent 50%),
        linear-gradient(160deg, #f8fafc 0%, #f1f5ff 40%, #ffffff 100%) !important;
    color: var(--cg-text-primary) !important;
}

section[data-testid="stSidebar"] {
    background: radial-gradient(500px circle at 30% 0%, rgba(14, 165, 233, 0.12), transparent 55%),
        linear-gradient(180deg, #ffffff 0%, #f1f5ff 100%) !important;
    border-right: 1px solid var(--cg-border) !important;
}

.cg-sidebar-deco {
    background: linear-gradient(160deg, rgba(14, 165, 233, 0.10), rgba(255, 255, 255, 0.95)) !important;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08) !important;
}

.cg-onboarding-card {
    background: linear-gradient(160deg, rgba(14, 165, 233, 0.10), rgba(255, 255, 255, 0.95)) !important;
    box-shadow: var(--cg-shadow), 0 0 24px var(--cg-blue-glow) !important;
}

.cg-hero {
    background: linear-gradient(135deg, rgba(14, 165, 233, 0.14) 0%, rgba(255, 255, 255, 0.96) 100%) !important;
    box-shadow: var(--cg-shadow), 0 0 22px var(--cg-blue-glow) !important;
}

.cg-metric {
    background: linear-gradient(145deg, rgba(14, 165, 233, 0.08), rgba(255, 255, 255, 0.96)) !important;
    box-shadow: 0 10px 22px rgba(15, 23, 42, 0.08) !important;
}

.cg-chat-user {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.16), rgba(37, 99, 235, 0.06)) !important;
}

.cg-chat-assistant {
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06) !important;
}

.cg-scan-result,
.cg-websec-result {
    background: linear-gradient(145deg, rgba(14, 165, 233, 0.10), rgba(255, 255, 255, 0.96)) !important;
    box-shadow: var(--cg-shadow), 0 0 18px var(--cg-blue-glow) !important;
}

.cg-scan-metric,
.cg-websec-metric {
    background: rgba(255, 255, 255, 0.92) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255, 255, 255, 0.92) !important;
    color: var(--cg-text-primary) !important;
}

.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.92) !important;
}

div[data-testid="stChatInput"] textarea {
    background: rgba(255, 255, 255, 0.92) !important;
    color: var(--cg-text-primary) !important;
    border: 1px solid var(--cg-border) !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--cg-text-muted) !important;
}

div[data-testid="stChatInput"] {
    background: rgba(255, 255, 255, 0.92) !important;
    border: 1px solid var(--cg-border) !important;
    border-radius: 14px !important;
    padding: 0.35rem 0.4rem !important;
    box-shadow: 0 12px 26px rgba(15, 23, 42, 0.10) !important;
}

div[data-testid="stChatInput"] > div {
    background: transparent !important;
}

div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
}

div[data-testid="stBottomBlockContainer"],
div[data-testid="stBottom"] {
    background: transparent !important;
}

div[data-testid="stExpander"] details {
    background: rgba(255, 255, 255, 0.92) !important;
    border: 1px solid var(--cg-border) !important;
    border-radius: 12px !important;
}

div[data-testid="stExpander"] summary {
    color: var(--cg-text-primary) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #2563eb) !important;
    box-shadow: 0 8px 18px rgba(37, 99, 235, 0.20) !important;
}

.stButton > button:hover {
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.28) !important;
}
"""


def load_css() -> None:
    """
    Memuat file style.css ke halaman Streamlit.

    Menggunakan Path(__file__) agar path selalu relatif terhadap
    lokasi app.py — aman untuk deploy lokal maupun cloud.
    """
    css_path = Path(__file__).parent / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            theme = st.session_state.get("theme", "dark")
            css = f.read()
            if theme == "light":
                css += _LIGHT_THEME_CSS
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


load_css()


# ---------------------------------------------------------------------------
# Inisialisasi Session State
# ---------------------------------------------------------------------------

def init_session_state() -> None:
    """
    Menginisialisasi variabel session_state untuk chat, navigasi,
    onboarding, dan hasil scan URL.
    """
    # State chatbot
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_initialized" not in st.session_state:
        st.session_state.chat_initialized = False

    # State navigasi halaman
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    if "cg_theme_toggle" not in st.session_state:
        st.session_state.cg_theme_toggle = st.session_state.theme == "light"
    else:
        st.session_state.theme = "light" if st.session_state.cg_theme_toggle else "dark"

    # State onboarding — muncul sekali per sesi browser
    if "onboarding_done" not in st.session_state:
        st.session_state.onboarding_done = False
    if "onboarding_step" not in st.session_state:
        st.session_state.onboarding_step = 0

    # State URL Scanner — menyimpan hasil agar tidak hilang setelah rerun
    if "url_scan_result" not in st.session_state:
        st.session_state.url_scan_result = None


init_session_state()


# ---------------------------------------------------------------------------
# Helper UI Functions
# ---------------------------------------------------------------------------

def navigate_to(page: str) -> None:
    """
    Mengarahkan pengguna ke halaman tertentu dan me-refresh UI.

    Args:
        page: Nama halaman tujuan (harus ada di VALID_PAGES).
    """
    if page in VALID_PAGES:
        st.session_state.current_page = page
        st.rerun()


def sync_theme() -> None:
    st.session_state.theme = "light" if st.session_state.get("cg_theme_toggle") else "dark"


def render_badge(level: str) -> str:
    """
    Membuat HTML badge berdasarkan level keamanan.

    Args:
        level: Level status (Safe, Suspicious, Dangerous, Weak, Medium, Strong).

    Returns:
        str: HTML string badge.
    """
    level_lower = level.lower()
    # Alias: CSS menggunakan .cg-badge-danger untuk status Dangerous
    if level_lower == "dangerous":
        level_lower = "danger"
    css_class = f"cg-badge cg-badge-{level_lower}"
    return f'<span class="{css_class}">{level}</span>'


def render_progress_bar(score: int, level: str) -> str:
    """
    Membuat HTML progress bar untuk skor keamanan.

    Args:
        score: Skor 0-100.
        level: Level visual (Weak, Medium, Strong).

    Returns:
        str: HTML progress bar.
    """
    level_class = level.lower()
    return (
        f'<div class="cg-progress-track">'
        f'<div class="cg-progress-fill cg-progress-{level_class}" '
        f'style="width: {score}%;"></div></div>'
    )


def render_url_analysis_result(result: dict, show_title: bool = True) -> None:
    """
    Menampilkan hasil analisis URL secara konsisten di seluruh halaman.

    Args:
        result: Dict dari fms.analyze_url().
        show_title: Tampilkan judul section hasil atau tidak.
    """
    status = result.get("status", "Suspicious")
    risk_score = result.get("risk_score", 0)
    summary = result.get("summary", "")
    findings = result.get("findings", [])
    url_checked = result.get("url_checked", "")

    # Tentukan warna progress bar berdasarkan skor risiko
    if risk_score < 30:
        bar_level = "Strong"
    elif risk_score < 60:
        bar_level = "Medium"
    else:
        bar_level = "Weak"

    if show_title:
        st.markdown("##### 📊 Hasil Analisis")

    st.markdown(
        f"""
        <div class="cg-scan-result">
            <div class="cg-scan-result-header">
                <span>Status Keamanan</span>
                {render_badge(status)}
            </div>
            <div class="cg-scan-metrics">
                <div class="cg-scan-metric">
                    <span class="cg-scan-metric-label">Risk Score</span>
                    <span class="cg-scan-metric-value">{risk_score}/100</span>
                </div>
            </div>
            <div class="cg-scan-risk-label">Tingkat risiko</div>
            {render_progress_bar(risk_score, bar_level)}
            <div class="cg-scan-summary">
                <span class="cg-scan-summary-label">Ringkasan</span>
                <p>{summary}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if findings:
        st.markdown("##### 🔎 Temuan Analisis")
        for finding in findings:
            st.markdown(
                f'<div class="cg-finding">⚠️ {finding}</div>',
                unsafe_allow_html=True,
            )

    if url_checked:
        st.markdown(
            f'<p class="cg-url-checked">URL diperiksa: {url_checked}</p>',
            unsafe_allow_html=True,
        )


def send_chat_message(message: str) -> None:
    """
    Mengirim pesan ke chatbot dan menyimpan respons ke history.

    Args:
        message: Pertanyaan pengguna.
    """
    st.session_state.chat_history.append({"role": "user", "content": message})
    result = engine.process_message(message, st.session_state.chat_history)
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result["response"],
    })
    st.rerun()


# ---------------------------------------------------------------------------
# Welcome Tour / Onboarding
# ---------------------------------------------------------------------------

# Konten tiap langkah panduan pengguna baru
ONBOARDING_STEPS = [
    {
        "title": "Selamat Datang di CyberGuard AI",
        "icon": "🛡️",
        "body": """
        <p>CyberGuard AI adalah <b>asisten keamanan siber</b> yang membantu pengguna
        memahami ancaman digital dan meningkatkan keamanan akun mereka.</p>
        <p>Panduan singkat ini akan memperkenalkan fitur utama aplikasi.
        Tekan <b>Next</b> untuk melanjutkan atau <b>Lewati</b> untuk langsung masuk.</p>
        """,
    },
    {
        "title": "💬 AI Chatbot",
        "icon": "💬",
        "body": """
        <p><b>Yang bisa Anda lakukan:</b></p>
        <ul class="cg-onboard-list">
            <li>Bertanya tentang cyber security</li>
            <li>Phishing, Malware, Ransomware</li>
            <li>VPN, Firewall, Password Security</li>
            <li>2FA, Scam dan penipuan online</li>
        </ul>
        """,
    },
    {
        "title": "🔑 Password Checker",
        "icon": "🔑",
        "body": """
        <p><b>Yang bisa Anda lakukan:</b></p>
        <ul class="cg-onboard-list">
            <li>Mengecek kekuatan password</li>
            <li>Mengetahui tingkat keamanan password</li>
            <li>Mendapatkan rekomendasi perbaikan password</li>
        </ul>
        """,
    },
    {
        "title": "🔗 URL Scanner",
        "icon": "🔗",
        "body": """
        <p><b>Yang bisa Anda lakukan:</b></p>
        <ul class="cg-onboard-list">
            <li>Memeriksa keamanan website</li>
            <li>Mendeteksi indikasi phishing</li>
            <li>Menampilkan tingkat risiko website</li>
        </ul>
        """,
    },
    {
        "title": "📚 Security Tips",
        "icon": "📚",
        "body": """
        <p><b>Yang bisa Anda lakukan:</b></p>
        <ul class="cg-onboard-list">
            <li>Mendapatkan tips keamanan digital</li>
            <li>Membangun awareness keamanan siber</li>
            <li>Belajar praktik terbaik proteksi data</li>
        </ul>
        """,
    },
    {
        "title": "Anda Siap Menggunakan CyberGuard AI",
        "icon": "🚀",
        "body": """
        <p>Anda sudah memahami fitur utama aplikasi.
        Mulai eksplorasi CyberGuard AI dan tingkatkan keamanan digital Anda.</p>
        <p>Tekan tombol di bawah untuk langsung membuka <b>AI Chatbot</b>.</p>
        """,
        "is_final": True,
    },
]


def finish_onboarding(go_to_chatbot: bool = False) -> None:
    """
    Menutup panduan onboarding untuk sesi ini.

    Args:
        go_to_chatbot: True jika pengguna menekan Mulai Sekarang.
    """
    st.session_state.onboarding_done = True
    if go_to_chatbot:
        st.session_state.current_page = "AI Chatbot"
    st.rerun()


def render_onboarding() -> None:
    """
    Merender kartu Welcome Guide / Onboarding untuk pengguna baru.
    Hanya muncul sekali per sesi hingga Lewati atau Mulai Sekarang ditekan.
    """
    step_idx = st.session_state.onboarding_step
    step = ONBOARDING_STEPS[step_idx]
    total_steps = len(ONBOARDING_STEPS)
    is_final = step.get("is_final", False)

    # Progress indicator langkah panduan
    progress_pct = int(((step_idx + 1) / total_steps) * 100)

    st.markdown(
        f"""
        <div class="cg-onboarding-wrap">
            <div class="cg-onboarding-card">
                <div class="cg-onboarding-icon">{step["icon"]}</div>
                <h2 class="cg-onboarding-title">{step["title"]}</h2>
                <div class="cg-onboarding-progress">
                    <div class="cg-onboarding-progress-fill" style="width:{progress_pct}%;"></div>
                </div>
                <p class="cg-onboarding-step-label">Langkah {step_idx + 1} dari {total_steps}</p>
                <div class="cg-onboarding-body">{step["body"]}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tombol navigasi panduan
    if is_final:
        col_skip, col_start = st.columns([1, 2])
        with col_skip:
            if st.button("Lewati", key="onboard_skip_final", use_container_width=True):
                finish_onboarding(go_to_chatbot=False)
        with col_start:
            if st.button("🚀 Mulai Sekarang", key="onboard_start", use_container_width=True):
                finish_onboarding(go_to_chatbot=True)
    else:
        col_skip, col_next = st.columns([1, 2])
        with col_skip:
            if st.button("Lewati", key=f"onboard_skip_{step_idx}", use_container_width=True):
                finish_onboarding(go_to_chatbot=False)
        with col_next:
            if st.button("Next →", key=f"onboard_next_{step_idx}", use_container_width=True):
                st.session_state.onboarding_step += 1
                st.rerun()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_sidebar() -> str:
    """
    Merender sidebar dengan panel dekoratif dan Quick Tools.
    Navigasi radio dihapus — halaman aktif diatur via session_state.

    Returns:
        str: Nama halaman aktif saat ini.
    """
    # Pastikan halaman aktif selalu valid
    if st.session_state.current_page not in VALID_PAGES:
        st.session_state.current_page = "Dashboard"

    current_page = st.session_state.current_page
    page_icon, page_label = PAGE_META.get(current_page, ("🛡️", "Dashboard"))

    with st.sidebar:
        # Logo dan branding aplikasi
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

        # Panel dekoratif — menggantikan menu radio/checkbox
        st.markdown(
            f"""
            <div class="cg-sidebar-deco">
                <div class="cg-sidebar-deco-glow"></div>
                <p class="cg-sidebar-deco-label">Halaman Aktif</p>
                <div class="cg-sidebar-active-page">
                    <span class="cg-sidebar-active-icon">{page_icon}</span>
                    <span class="cg-sidebar-active-text">{page_label}</span>
                </div>
                <div class="cg-sidebar-deco-divider"></div>
                <div class="cg-sidebar-shield-row">
                    <span class="cg-status-dot cg-status-active"></span>
                    <span class="cg-sidebar-shield-text">Secure Session Active</span>
                </div>
                <div class="cg-sidebar-bars">
                    <div class="cg-sidebar-bar" style="width:92%;"></div>
                    <div class="cg-sidebar-bar" style="width:78%;"></div>
                    <div class="cg-sidebar-bar" style="width:85%;"></div>
                </div>
                <p class="cg-sidebar-deco-tagline">
                    Proteksi digital • Edukasi • Awareness
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Quick Tools — navigasi utama antar halaman
        st.markdown("##### ⚡ Quick Tools")
        qcol1, qcol2 = st.columns(2)
        with qcol1:
            if st.button("🏠 Home", key="qt_home", use_container_width=True):
                navigate_to("Dashboard")
        with qcol2:
            if st.button("💬 Chat", key="qt_chat", use_container_width=True):
                navigate_to("AI Chatbot")

        qcol3, qcol4 = st.columns(2)
        with qcol3:
            if st.button("🔑 Pass", key="qt_pass", use_container_width=True):
                navigate_to("Password Checker")
        with qcol4:
            if st.button("🔗 URL", key="qt_url", use_container_width=True):
                navigate_to("URL Scanner")

        if st.button("📚 Tips", key="qt_tips", use_container_width=True):
            navigate_to("Security Tips")

        st.markdown("---")

        st.markdown("##### 🎨 Tema")
        st.toggle("🌞 Tema Terang", key="cg_theme_toggle", on_change=sync_theme)
        st.markdown("---")

        # Informasi singkat aplikasi
        st.markdown("##### ℹ️ About")
        st.markdown(
            """
            <p style="font-size:0.78rem;color:var(--cg-text-muted);line-height:1.5;">
            <b>CyberGuard AI</b> v1.1<br>
            Edukasi &amp; awareness keamanan siber.<br><br>
            <i>Bukan tools hacking.</i>
            </p>
            """,
            unsafe_allow_html=True,
        )

    return current_page


# ---------------------------------------------------------------------------
# Dashboard — tampilan bersih (Less is More)
# ---------------------------------------------------------------------------

def render_dashboard() -> None:
    """
    Merender dashboard utama yang ringkas dan profesional.
    Menghapus elemen dekoratif tanpa fungsi (metric palsu, duplikasi konten).
    """
    # Hero section — pesan utama aplikasi
    st.markdown(
        """
        <div class="cg-hero cg-hero-compact">
            <div class="cg-hero-icon">🛡️</div>
            <h1>CyberGuard AI</h1>
            <p>Asisten keamanan siber untuk edukasi, analisis, dan proteksi digital Anda.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="cg-section-title">🧭 <span>Fitur Utama</span></div>',
        unsafe_allow_html=True,
    )

    # Grid fitur — setiap kartu punya fungsi navigasi nyata
    features = [
        ("💬", "AI Chatbot", "Tanya jawab seputar keamanan siber", "AI Chatbot"),
        ("🔑", "Password Checker", "Cek kekuatan & rekomendasi password", "Password Checker"),
        ("🔗", "URL Scanner", "Deteksi indikasi phishing pada link", "URL Scanner"),
        ("📚", "Security Tips", "Tips keamanan digital terkini", "Security Tips"),
    ]

    fcols = st.columns(2)
    for i, (icon, title, desc, target) in enumerate(features):
        with fcols[i % 2]:
            st.markdown(
                f"""
                <div class="cg-feature-card">
                    <div class="cg-feature-icon">{icon}</div>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Buka {title}", key=f"feat_{target}", use_container_width=True):
                navigate_to(target)


# ---------------------------------------------------------------------------
# Website Security Check (embedded in AI Chatbot page)
# ---------------------------------------------------------------------------

def render_website_security_check() -> None:
    """
    Merender section Website Security Check pada halaman AI Chatbot.
    Menggunakan fms.analyze_url() — tanpa membuat fungsi analisis baru.
    """
    st.markdown(
        '<div class="cg-section-title cg-websec-section-title">'
        '🌐 <span>Website Security Check</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="cg-card cg-websec-card">
            <p>Periksa keamanan website secara instan tanpa harus chat terlebih dahulu.
            Analisis berbasis heuristik — verifikasi manual tetap disarankan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    websec_url = st.text_input(
        "URL Website",
        placeholder="Masukkan URL website yang ingin dianalisis...",
        key="websec_url_input",
        label_visibility="collapsed",
    )

    if st.button("🔍 Analisis Website", key="websec_analyze_btn", use_container_width=True):
        if not websec_url or not websec_url.strip():
            st.warning("Masukkan URL terlebih dahulu.")
        else:
            with st.spinner("Menganalisis keamanan website..."):
                result = fms.analyze_url(websec_url)
            render_url_analysis_result(result)


# ---------------------------------------------------------------------------
# AI Chatbot Page
# ---------------------------------------------------------------------------

# Daftar contoh pertanyaan untuk panduan pengguna
CHAT_EXAMPLE_QUESTIONS = [
    "Apa itu phishing?",
    "Bagaimana cara membuat password yang aman?",
    "Apa itu ransomware?",
    "Bagaimana cara mengaktifkan 2FA?",
    "Apa fungsi VPN?",
    "Apa itu firewall?",
]

# Pertanyaan cepat (tombol shortcut di bawah chat)
CHAT_QUICK_QUESTIONS = [
    "Apa itu phishing?",
    "Tips password aman?",
    "Apa itu ransomware?",
    "Cara aktifkan 2FA?",
]


def render_chatbot() -> None:
    """
    Merender halaman chatbot AI yang modern dengan panduan contoh pertanyaan.
    """
    st.markdown(
        '<div class="cg-section-title">💬 <span>AI Cyber Security Chatbot</span></div>',
        unsafe_allow_html=True,
    )

    # Card contoh pertanyaan — membantu pengguna baru
    examples_html = "".join(
        f"<li>{q}</li>" for q in CHAT_EXAMPLE_QUESTIONS
    )
    st.markdown(
        f"""
        <div class="cg-card cg-chat-guide">
            <h3>💡 Contoh Pertanyaan</h3>
            <p>Klik salah satu pertanyaan cepat di bawah chat, atau ketik sendiri di kolom chat.</p>
            <ul class="cg-example-list">{examples_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Inisialisasi pesan sambutan chatbot sekali per sesi
    if not st.session_state.chat_initialized:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": engine.get_welcome_message(),
        })
        st.session_state.chat_initialized = True

    # Area riwayat percakapan
    st.markdown('<div class="cg-chat-area">', unsafe_allow_html=True)
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
            st.markdown(
                f"""
                <div class="cg-chat-assistant">
                    <div class="cg-chat-label">CyberGuard AI</div>
                    {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Input chat pengguna
    user_input = st.chat_input("Ketik pertanyaan cyber security Anda...")

    if user_input:
        send_chat_message(user_input)

    with st.expander("⚡ Pertanyaan Cepat", expanded=False):
        qcols = st.columns(2)
        for i, question in enumerate(CHAT_QUICK_QUESTIONS):
            with qcols[i % 2]:
                if st.button(question, key=f"quick_{i}", use_container_width=True):
                    send_chat_message(question)

    # Tombol reset riwayat chat
    if st.button("🗑️ Hapus Riwayat Chat", key="clear_chat"):
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
    st.markdown(
        '<div class="cg-section-title">🔑 <span>Password Strength Checker</span></div>',
        unsafe_allow_html=True,
    )

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

# Contoh URL edukatif untuk panduan pengguna
SAFE_URL_EXAMPLES = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.microsoft.com",
]

RISKY_URL_EXAMPLES = [
    "http://free-gift-login.xyz",
    "http://secure-bank-verification.net",
    "http://claim-prize-now.click",
]


def fill_url_scan_input(url: str) -> None:
    """
    Callback untuk mengisi kolom URL Scanner dari tombol contoh URL.

    Args:
        url: URL contoh yang dipilih pengguna.
    """
    st.session_state.url_scan_input = url


def render_url_scanner() -> None:
    """
    Merender halaman URL Scanner dengan panduan, contoh URL, dan hasil analisis.
    Hasil disimpan di session_state agar tidak hilang setelah rerun Streamlit.
    """
    st.markdown(
        '<div class="cg-section-title">🔗 <span>URL / Phishing Detector</span></div>',
        unsafe_allow_html=True,
    )

    # Card petunjuk penggunaan
    st.markdown(
        """
        <div class="cg-card cg-url-guide">
            <h3>📖 Cara Menggunakan URL Scanner</h3>
            <ol class="cg-url-steps">
                <li>Salin alamat website yang ingin diperiksa.</li>
                <li>Tempelkan URL ke kolom input.</li>
                <li>Klik <b>Scan URL</b>.</li>
                <li>Tunggu hasil analisis.</li>
                <li>Perhatikan status dan tingkat risiko.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Input URL — key tetap agar nilai tidak hilang saat rerun
    url_input = st.text_input(
        "Masukkan URL",
        placeholder="https://example.com atau example.com",
        key="url_scan_input",
    )

    # Tombol scan dengan spinner dan penyimpanan hasil ke session_state
    scan_clicked = st.button("🔍 Scan URL", key="url_scan_btn", use_container_width=True)

    if scan_clicked:
        if not url_input or not url_input.strip():
            st.warning("Masukkan URL terlebih dahulu.")
            st.session_state.url_scan_result = None
        else:
            with st.spinner("Memindai URL..."):
                st.session_state.url_scan_result = fms.analyze_url(url_input)

    # Tampilkan hasil scan terakhir (persisten selama sesi)
    if st.session_state.url_scan_result:
        render_url_analysis_result(st.session_state.url_scan_result)

    st.markdown("---")

    # Contoh URL aman — klik untuk mengisi kolom input
    st.markdown("##### ✅ Contoh URL Aman")
    safe_cols = st.columns(3)
    for i, example_url in enumerate(SAFE_URL_EXAMPLES):
        with safe_cols[i]:
            st.button(
                example_url,
                key=f"safe_url_{i}",
                use_container_width=True,
                on_click=fill_url_scan_input,
                args=(example_url,),
            )

    # Contoh URL berisiko — hanya untuk edukasi
    st.markdown("##### ⚠️ Contoh URL yang Perlu Diwaspadai")
    risky_cols = st.columns(3)
    for i, example_url in enumerate(RISKY_URL_EXAMPLES):
        with risky_cols[i]:
            st.button(
                example_url,
                key=f"risky_url_{i}",
                use_container_width=True,
                on_click=fill_url_scan_input,
                args=(example_url,),
            )

    st.markdown(
        """
        <p class="cg-url-disclaimer">
        <i>Contoh URL berisiko hanya untuk simulasi edukasi dan bukan hasil analisis nyata.</i>
        </p>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Security Tips Page
# ---------------------------------------------------------------------------

def render_security_tips() -> None:
    """
    Merender halaman tips keamanan siber.
    """
    st.markdown(
        '<div class="cg-section-title">📚 <span>Cyber Security Tips</span></div>',
        unsafe_allow_html=True,
    )

    tip = fms.get_random_tip()
    st.markdown(f'<div class="cg-tip-box">💡 <b>Tip Acak:</b> {tip}</div>', unsafe_allow_html=True)

    if st.button("🔄 Tip Baru", key="new_tip", use_container_width=False):
        st.rerun()

    st.markdown("##### 📋 Semua Tips Keamanan")
    for i, tip_text in enumerate(fms.get_all_tips(), 1):
        st.markdown(
            f'<div class="cg-card cg-tip-item">'
            f'<p><b>{i}.</b> {tip_text}</p></div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Main Router
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Entry point aplikasi — onboarding, sidebar, dan routing halaman.
    """
    # Sidebar mengembalikan halaman aktif dari session_state
    page = render_sidebar()

    # Tampilkan onboarding sekali per sesi sebelum konten utama
    if not st.session_state.onboarding_done:
        render_onboarding()
        return

    # Render halaman sesuai navigasi Quick Tools / dashboard / onboarding
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
