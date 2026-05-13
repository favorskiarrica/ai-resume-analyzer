import streamlit as st
import PyPDF2

from utils import (
    get_match_percentage,
    generate_ai_suggestions,
    chat_response,
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Juxtapose Merit",
    page_icon="⚡",
    layout="wide"
)

# =========================
# CSS (SAFE + SIMPLE + STABLE)
# =========================

st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background: #05060B;
    color: #E5E7EB;
}

/* REMOVE DEFAULT WHITE AREAS */
section, div {
    background: transparent !important;
}

/* HERO */
.hero-title {
    font-size: 4rem;
    font-weight: 800;
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

/* FILE UPLOAD */
[data-testid="stFileUploader"] {
    background: #0B1220 !important;
    border: 1px solid #00FFC6 !important;
    border-radius: 12px !important;
}

/* INPUTS */
textarea, input {
    background: #0B1220 !important;
    color: white !important;
    border: 1px solid #00FFC6 !important;
    border-radius: 10px !important;
}

/* METRICS */
[data-testid="metric-container"] {
    background: #0B1220 !important;
    border: 1px solid #00FFC6 !important;
    border-radius: 12px !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(90deg, #00FFC6, #38BDF8) !important;
    color: #05060B !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
}

/* PROGRESS */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00FFC6, #38BDF8) !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================

st.markdown("""
<h1 class="hero-title">Juxtapose Merit</h1>
<p class="hero-sub">AI Resume Intelligence • ATS Optimization Engine</p>
""", unsafe_allow_html=True)

# =========================
# INPUTS
# =========================

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

with col2:
    job_description = st.text_area("💼 Paste Job Description", height=250)

# =========================
# ANALYSIS
# =========================

if uploaded_file and job_description:

    resume_text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

    except Exception:
        st.error("PDF read error")
        st.stop()

    if not resume_text:
        st.warning("No text found in PDF")
        st.stop()

    # AI
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

    # METRICS
    c1, c2, c3 = st.columns(3)

    c1.metric("Match Score", f"{match_score}%")
    c2.metric("Role", job_type)
    c3.metric("Level", seniority)

    st.progress(match_score / 100)

    st.divider()

    # SKILLS
    c4, c5 = st.columns(2)

    c4.subheader("Matched Skills")
    c4.write(", ".join(matched_keywords) or "None")

    c5.subheader("Missing Skills")
    c5.write(", ".join(missing_skills) or "Fully aligned")

    st.divider()

    # FEEDBACK
    st.subheader("AI Feedback")
    st.write(feedback)

    st.divider()

    # CHAT
    st.subheader("AI Chat Coach")

    q = st.text_input("Ask something")

    if q:
        st.write(chat_response(
            q,
            match_score,
            matched_keywords,
            missing_skills,
            job_type
        ))

    st.divider()

    # DOWNLOAD
    report = f"""
Role: {job_type}
Level: {seniority}
Score: {match_score}%

Matched: {', '.join(matched_keywords)}
Missing: {', '.join(missing_skills)}

Feedback:
{feedback}
"""

    st.download_button("Download Report", report)

else:
    st.info("Upload resume + job description to start")