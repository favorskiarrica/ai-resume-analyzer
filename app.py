import streamlit as st
import PyPDF2

from utils import (
    get_match_percentage,
    generate_ai_suggestions,
    chat_response,
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Juxtapose Merit",
    page_icon="⚡",
    layout="wide"
)

# =========================================================
# SAFE INLINE CSS (NO FILE DEPENDENCY)
# =========================================================

st.markdown("""
<style>

/* =========================
BASE DARK BACKGROUND
========================= */

.stApp {
    background: radial-gradient(circle at top,
        #070A12 0%,
        #05060B 60%,
        #02030A 100%);
    color: #E5E7EB;
}

/* subtle neon glow */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 20% 20%, rgba(0,255,200,0.06), transparent 45%),
        radial-gradient(circle at 80% 30%, rgba(56,189,248,0.05), transparent 45%);
    pointer-events: none;
}

/* =========================
TEXT
========================= */

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
    color: #E5E7EB;
}

/* =========================
TITLE (YC STYLE)
========================= */

.hero-title {
    font-size: 3.8rem;
    font-weight: 900;
    text-align: center;

    background: linear-gradient(90deg, #00FFC6, #38BDF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    text-align: center;
    color: #94A3B8;
    margin-bottom: 2rem;
}

/* =========================
CARDS (SAFE STREAMLIT VERSION)
========================= */

div[data-testid="stVerticalBlock"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,255,200,0.10) !important;
    border-radius: 14px;
    padding: 12px;
}

/* =========================
FILE UPLOADER (FIXED WHITE BOX)
========================= */

section[data-testid="stFileUploader"] {
    background: rgba(2,6,23,0.9) !important;
    border: 1px solid rgba(0,255,200,0.15) !important;
    border-radius: 12px;
    padding: 10px;
}

/* =========================
TEXT INPUTS
========================= */

textarea,
input {
    background: rgba(2,6,23,0.85) !important;
    color: #E5E7EB !important;
    border: 1px solid rgba(0,255,200,0.15) !important;
    border-radius: 10px !important;
}

/* =========================
BUTTONS (NEON CYAN GREEN)
========================= */

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #00FFC6, #38BDF8);
    color: #05060B;
    border: none;
    border-radius: 10px;
    font-weight: 800;
    padding: 10px;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 18px rgba(0,255,200,0.25);
}

/* =========================
METRICS
========================= */

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,255,200,0.10) !important;
    border-radius: 12px;
}

/* =========================
PROGRESS BAR
========================= */

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00FFC6, #38BDF8);
}

/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background: rgba(2,6,23,0.95);
    border-right: 1px solid rgba(0,255,200,0.10);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<h1 class="hero-title">Juxtapose Merit</h1>
<p class="hero-sub">AI Resume Intelligence • ATS Optimization Engine</p>
""", unsafe_allow_html=True)

# =========================================================
# INPUTS
# =========================================================

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

with col2:
    job_description = st.text_area(
        "💼 Paste Job Description",
        height=260,
        placeholder="Paste job description here..."
    )

# =========================================================
# ANALYSIS ENGINE
# =========================================================

if uploaded_file and job_description:

    resume_text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

    except Exception:
        st.error("Could not read PDF.")
        st.stop()

    if not resume_text:
        st.warning("No readable text found in PDF.")
        st.stop()

    # AI ANALYSIS
    match_score, matched_keywords, missing_skills, job_type, seniority = get_match_percentage(
        resume_text,
        job_description
    )

    feedback = generate_ai_suggestions(
        match_score,
        matched_keywords,
        missing_skills,
        job_type
    )

    st.divider()

    # =====================================================
    # METRICS
    # =====================================================

    m1, m2, m3 = st.columns(3)

    m1.metric("⚡ Match Score", f"{match_score}%")
    m2.metric("🧠 Role", job_type)
    m3.metric("📊 Level", seniority)

    st.progress(match_score / 100)

    st.divider()

    # =====================================================
    # SKILLS
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Matched Skills")
        st.write(", ".join(matched_keywords) if matched_keywords else "None")

    with c2:
        st.subheader("Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "Fully aligned")

    st.divider()

    # =====================================================
    # AI FEEDBACK
    # =====================================================

    st.subheader("AI Feedback")
    st.write(feedback)

    st.divider()

    # =====================================================
    # CHAT
    # =====================================================

    st.subheader("AI Career Chat")

    user_question = st.text_input("Ask a question")

    if user_question:
        response = chat_response(
            user_question,
            match_score,
            matched_keywords,
            missing_skills,
            job_type
        )
        st.write(response)

    st.divider()

    # =====================================================
    # DOWNLOAD
    # =====================================================

    report = f"""
Resume Analysis Report

Role: {job_type}
Level: {seniority}
Score: {match_score}%

Matched:
{', '.join(matched_keywords)}

Missing:
{', '.join(missing_skills)}

Feedback:
{feedback}
"""

    st.download_button(
        "Download Report",
        report,
        file_name="resume_report.txt"
    )

else:
    st.info("Upload resume + job description to begin.")