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
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# GLOBAL STYLES (FULL FIXED UI THEME)
# =========================================================

st.markdown("""
<style>

/* =========================================================
BACKGROUND
========================================================= */

.stApp {
    background: linear-gradient(
        135deg,
        #0B1120 0%,
        #111827 50%,
        #172554 100%
    );
    color: white;
}

/* =========================================================
GLOBAL TEXT
========================================================= */

html, body, [class*="css"] {
    color: white;
    font-family: Inter, sans-serif;
}

/* =========================================================
MAIN CONTAINER
========================================================= */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1150px;
}

/* =========================================================
GLASS CARD (UNIVERSAL FIX)
THIS FIXES YOUR "WHITE BOX PROBLEM"
========================================================= */

div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"] {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 18px;
}

/* =========================================================
HERO TITLE
========================================================= */

.hero-title {
    font-size: 4.5rem;
    font-weight: 800;
    text-align: center;

    background: linear-gradient(90deg, #60A5FA, #10B981);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    text-align: center;
    font-size: 1.2rem;
    color: #CBD5E1;
    margin-bottom: 2.5rem;
}

/* =========================================================
INPUTS (FIX WHITE BOXES)
========================================================= */

textarea,
input {
    background-color: rgba(15,23,42,0.85) !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
}

/* =========================================================
FILE UPLOADER FIX
========================================================= */

[data-testid="stFileUploader"] {
    background: rgba(15,23,42,0.65) !important;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.10);
    padding: 20px;
}

/* =========================================================
METRICS FIX
========================================================= */

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 18px;
    padding: 16px;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #3B82F6, #10B981);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px;
    font-weight: 700;
    transition: 0.25s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(59,130,246,0.35);
}

/* =========================================================
PROGRESS BAR
========================================================= */

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #3B82F6, #10B981);
}

/* =========================================================
SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.85);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<h1 class="hero-title">Juxtapose Merit</h1>
<p class="hero-sub">AI-Powered Resume Intelligence & ATS Optimization</p>
""", unsafe_allow_html=True)

# =========================================================
# INPUT SECTION
# =========================================================

col1, col2 = st.columns(2)

with col1:
    st.file_uploader("📄 Upload Resume", type=["pdf"])

with col2:
    job_description = st.text_area(
        "💼 Paste Job Description",
        height=300,
        placeholder="Paste the job description here..."
    )

# =========================================================
# ANALYSIS
# =========================================================

uploaded_file = st.session_state.get("file_uploader")

if uploaded_file and job_description:

    resume_text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        st.success("Resume uploaded successfully!")

    except Exception:
        st.error("Error reading PDF.")
        st.stop()

    if not resume_text:
        st.warning("No text found in PDF.")
        st.stop()

    # =====================================================
    # AI ENGINE
    # =====================================================

    (
        match_score,
        matched_keywords,
        missing_skills,
        job_type,
        seniority
    ) = get_match_percentage(resume_text, job_description)

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

    m1.metric("🎯 Match Score", f"{match_score}%")
    m2.metric("💼 Career Field", job_type)
    m3.metric("📈 Seniority", seniority)

    st.progress(match_score / 100)

    st.divider()

    # =====================================================
    # SKILLS
    # =====================================================

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("✅ Matching Skills")
        st.write(", ".join(matched_keywords) if matched_keywords else "No strong matches found.")

    with c2:
        st.subheader("⚠️ Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "No missing skills detected!")

    st.divider()

    # =====================================================
    # AI FEEDBACK
    # =====================================================

    st.subheader("💡 AI Resume Coach Feedback")
    st.write(feedback)

    st.divider()

    # =====================================================
    # CHAT COACH
    # =====================================================

    st.subheader("💬 AI Resume Chat Coach")

    user_question = st.text_input("Ask a question about your resume")

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
    # DOWNLOAD REPORT
    # =====================================================

    report = f"""
Juxtapose Merit - ATS Report

Career Field: {job_type}
Seniority: {seniority}
Match Score: {match_score}%

Matching Skills:
{', '.join(matched_keywords)}

Missing Skills:
{', '.join(missing_skills)}

AI Feedback:
{feedback}
"""

    st.download_button(
        "📥 Download ATS Report",
        report,
        file_name="resume_analysis_report.txt"
    )

# =========================================================
# DEFAULT STATE
# =========================================================

else:
    st.info("Upload your resume and paste a job description to begin analysis.")