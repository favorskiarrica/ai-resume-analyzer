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

/* FORCE APP BACKGROUND */
.stApp {
    background: #05060B !important;
    color: #E5E7EB !important;
}

/* REMOVE STREAMLIT DEFAULT SURFACES */
section, div {
    background: transparent !important;
}

/* TEXT FIX (PURPLE REMOVAL) */
h1, h2, h3, p, span, label {
    color: #E5E7EB !important;
}

/* FILE UPLOADER FIX */
[data-testid="stFileUploader"] {
    background: #0B1220 !important;
    border: 1px solid #00FFC6 !important;
    border-radius: 12px !important;
}

/* INPUT FIELDS */
textarea, input {
    background: #0B1220 !important;
    color: white !important;
    border: 1px solid #00FFC6 !important;
}

/* METRICS */
[data-testid="metric-container"] {
    background: #0B1220 !important;
    border: 1px solid #00FFC6 !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(90deg, #00FFC6, #38BDF8) !important;
    color: #05060B !important;
    font-weight: 800 !important;
}

/* PROGRESS BAR */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00FFC6, #38BDF8) !important;
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