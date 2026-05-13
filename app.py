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
# CLEAN PREMIUM UI
# =========================================================

st.markdown("""
<style>

/* =========================================================
BACKGROUND
========================================================= */

.stApp {
    background:
    linear-gradient(
        135deg,
        #0B1120 0%,
        #111827 50%,
        #172554 100%
    );
    color: white;
}

/* =========================================================
GLOBAL
========================================================= */

html, body, [class*="css"] {
    color: white;
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1150px;
}

/* =========================================================
TITLE
========================================================= */

.hero-title {
    font-size: 4.5rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.5rem;

    background: linear-gradient(
        90deg,
        #60A5FA,
        #A78BFA
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    text-align: center;
    font-size: 1.2rem;
    color: #CBD5E1;
    margin-bottom: 3rem;
}

/* =========================================================
CARDS
========================================================= */

.card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(10px);

    border: 1px solid rgba(255,255,255,0.08);

    padding: 25px;

    border-radius: 22px;

    margin-bottom: 20px;
}

/* =========================================================
TEXT AREA
========================================================= */

textarea {
    background-color: rgba(15,23,42,0.90) !important;
    color: white !important;

    border-radius: 14px !important;

    border: 1px solid rgba(255,255,255,0.10) !important;
}

/* =========================================================
INPUTS
========================================================= */

input {
    background-color: rgba(15,23,42,0.90) !important;
    color: white !important;
}

/* =========================================================
UPLOAD BOX
========================================================= */

[data-testid="stFileUploader"] {
    background-color: rgba(15,23,42,0.75);

    border-radius: 18px;

    padding: 20px;

    border: 1px solid rgba(255,255,255,0.10);
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {

    width: 100%;

    background:
    linear-gradient(
        90deg,
        #3B82F6,
        #8B5CF6
    );

    color: white;

    border: none;

    border-radius: 14px;

    padding: 14px;

    font-size: 16px;

    font-weight: 700;

    transition: 0.25s;
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow: 0 8px 20px rgba(59,130,246,0.35);
}

/* =========================================================
METRICS
========================================================= */

[data-testid="metric-container"] {

    background: rgba(255,255,255,0.04);

    border: 1px solid rgba(255,255,255,0.08);

    padding: 20px;

    border-radius: 20px;
}

/* =========================================================
PROGRESS BAR
========================================================= */

.stProgress > div > div > div > div {

    background:
    linear-gradient(
        90deg,
        #3B82F6,
        #8B5CF6
    );
}

/* =========================================================
INFO BOXES
========================================================= */

.stInfo,
.stSuccess,
.stWarning {

    border-radius: 14px;
}

/* =========================================================
SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {

    background: #0F172A;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================

st.markdown("""
<h1 class="hero-title">
Juxtapose Merit
</h1>

<p class="hero-sub">
AI-Powered Resume Intelligence & ATS Optimization
</p>
""", unsafe_allow_html=True)

# =========================================================
# INPUT SECTION
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=300,
        placeholder="Paste the job description here..."
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ANALYSIS
# =========================================================

if uploaded_file is not None and job_description:

    resume_text = ""

    try:

        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text

        st.success("✅ Resume uploaded successfully!")

    except Exception:

        st.error("❌ Error reading PDF file.")
        st.stop()

    if not resume_text:

        st.warning("⚠️ Could not extract text from the PDF.")
        st.stop()

    # =========================================================
    # ATS ANALYSIS
    # =========================================================

    (
        match_score,
        matched_keywords,
        missing_skills,
        job_type,
        seniority
    ) = get_match_percentage(
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

    # =========================================================
    # TOP METRICS
    # =========================================================

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("🎯 Match Score", f"{match_score}%")

    with m2:
        st.metric("💼 Career Field", job_type)

    with m3:
        st.metric("📈 Seniority", seniority)

    st.progress(match_score / 100)

    st.divider()

    # =========================================================
    # SKILLS SECTION
    # =========================================================

    colA, colB = st.columns(2)

    with colA:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("✅ Matching Skills")

        if matched_keywords:
            st.write(", ".join(matched_keywords))
        else:
            st.write("No strong matches found.")

        st.markdown('</div>', unsafe_allow_html=True)

    with colB:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("⚠️ Missing Skills")

        if missing_skills:
            st.write(", ".join(missing_skills))
        else:
            st.write("🎉 No missing skills detected!")

        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # AI FEEDBACK
    # =========================================================

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("💡 AI Resume Coach Feedback")

    st.write(feedback)

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # CHAT COACH
    # =========================================================

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("💬 AI Resume Chat Coach")

    user_question = st.text_input(
        "Ask a question about your resume"
    )

    if user_question:

        response = chat_response(
            user_question,
            match_score,
            matched_keywords,
            missing_skills,
            job_type
        )

        st.write(response)

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # DOWNLOAD REPORT
    # =========================================================

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
        label="📥 Download ATS Report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain"
    )

# =========================================================
# DEFAULT STATE
# =========================================================

else:

    st.info(
        "📄 Upload your resume and paste a job description "
        "to begin ATS analysis."
    )