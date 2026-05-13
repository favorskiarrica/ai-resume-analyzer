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
# CYBER NEON UI THEME
# =========================================================

st.markdown("""
<style>

/* =========================================================
DARK CYBER BACKGROUND
========================================================= */

.stApp {
    background: radial-gradient(circle at top, #0B1220 0%, #05070F 50%, #02040A 100%);
    color: #E5E7EB;
}

/* moving glow overlay */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 20% 20%, rgba(0,255,200,0.08), transparent 40%),
                radial-gradient(circle at 80% 30%, rgba(0,120,255,0.08), transparent 40%),
                radial-gradient(circle at 50% 80%, rgba(168,85,247,0.06), transparent 50%);
    pointer-events: none;
}

/* =========================================================
GLOBAL TEXT
========================================================= */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #E5E7EB;
}

/* =========================================================
MAIN CONTAINER
========================================================= */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* =========================================================
CYBER GLASS CARDS
========================================================= */

div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,255,200,0.12);
    border-radius: 18px;

    box-shadow:
        0 0 20px rgba(0,255,200,0.05),
        inset 0 0 20px rgba(0,120,255,0.03);

    padding: 18px;
}

/* =========================================================
TITLE (NEON CYBER GLOW)
========================================================= */

.hero-title {
    font-size: 4.2rem;
    font-weight: 900;
    text-align: center;

    background: linear-gradient(90deg, #00FFC6, #38BDF8, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 20px rgba(0,255,198,0.15),
        0 0 40px rgba(56,189,248,0.10);
}

.hero-sub {
    text-align: center;
    font-size: 1.1rem;
    color: #94A3B8;
    margin-bottom: 2.5rem;
}

/* =========================================================
INPUTS (CYBER TERMINAL STYLE)
========================================================= */

textarea,
input {
    background: rgba(2,6,23,0.8) !important;
    color: #E5E7EB !important;

    border: 1px solid rgba(0,255,200,0.15) !important;
    border-radius: 12px !important;

    box-shadow: inset 0 0 10px rgba(0,255,200,0.05);
}

/* =========================================================
FILE UPLOADER
========================================================= */

[data-testid="stFileUploader"] {
    background: rgba(2,6,23,0.7) !important;
    border: 1px solid rgba(0,255,200,0.15);
    border-radius: 16px;
    padding: 18px;
}

/* =========================================================
METRICS (NEON PANELS)
========================================================= */

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,255,200,0.12) !important;
    border-radius: 16px;
    padding: 16px;

    box-shadow: 0 0 15px rgba(0,255,200,0.05);
}

/* metric values glow */
[data-testid="metric-container"] label {
    color: #94A3B8 !important;
}

/* =========================================================
BUTTONS (NEON CYBER CORE)
========================================================= */

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #00FFC6, #38BDF8, #A78BFA);
    color: #0B0F1A;

    border: none;
    border-radius: 12px;

    font-weight: 800;

    padding: 14px;

    box-shadow:
        0 0 15px rgba(0,255,198,0.25),
        0 0 30px rgba(56,189,248,0.15);

    transition: 0.2s ease-in-out;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 0 25px rgba(0,255,198,0.35),
        0 0 50px rgba(56,189,248,0.25);
}

/* =========================================================
PROGRESS BAR (CYBER ENERGY BAR)
========================================================= */

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00FFC6, #38BDF8);
    box-shadow: 0 0 10px rgba(0,255,198,0.4);
}

/* =========================================================
INFO BOXES
========================================================= */

.stAlert {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,255,200,0.12) !important;
    border-radius: 12px;
}

/* =========================================================
SIDEBAR CYBER STYLE
========================================================= */

section[data-testid="stSidebar"] {
    background: rgba(2,6,23,0.9);
    border-right: 1px solid rgba(0,255,200,0.15);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<h1 class="hero-title">Juxtapose Merit</h1>
<p class="hero-sub">AI Resume Intelligence • ATS Optimization • Cyber Analysis Engine</p>
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
        height=280,
        placeholder="Analyze a job role..."
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
        st.error("PDF parsing failed.")
        st.stop()

    if not resume_text:
        st.warning("No readable text found.")
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
    # DASHBOARD METRICS
    # =====================================================

    m1, m2, m3 = st.columns(3)

    m1.metric("⚡ Match Score", f"{match_score}%")
    m2.metric("🧠 Role Type", job_type)
    m3.metric("📊 Seniority", seniority)

    st.progress(match_score / 100)

    st.divider()

    # =====================================================
    # SKILL MATRIX
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("✅ Matched Signals")
        st.write(", ".join(matched_keywords) if matched_keywords else "No strong matches detected.")

    with c2:
        st.subheader("⚠️ Missing Signals")
        st.write(", ".join(missing_skills) if missing_skills else "Fully aligned.")

    st.divider()

    # =====================================================
    # AI ENGINE OUTPUT
    # =====================================================

    st.subheader("🧠 AI Strategy Output")
    st.write(feedback)

    st.divider()

    # =====================================================
    # CHAT COACH
    # =====================================================

    st.subheader("💬 AI Career Terminal")

    user_question = st.text_input("Ask the system")

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
    # EXPORT
    # =====================================================

    report = f"""
JUXTAPOSE MERIT CYBER REPORT

Role: {job_type}
Seniority: {seniority}
Match Score: {match_score}%

Matched:
{', '.join(matched_keywords)}

Missing:
{', '.join(missing_skills)}

AI OUTPUT:
{feedback}
"""

    st.download_button(
        "⬇ Download Report",
        report,
        file_name="cyber_resume_report.txt"
    )

else:
    st.info("Upload a resume + job description to initialize the analysis engine.")