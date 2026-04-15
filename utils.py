from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ---- LOAD MODEL ----
model = SentenceTransformer('all-MiniLM-L6-v2')

# ---- FILTERS ----
STOPWORDS = {
    "the","and","for","with","this","that","from","you","your","are",
    "will","can","our","job","role","work","team","using","use","used",
    "help","join","person","people","working","support","including",
    "ability","skills","requirements","preferred"
}

WEAK_WORDS = {
    "motivated","passionate","detailoriented",
    "responsible","dynamic","hardworking","excellent","strong"
}

CONNECTORS = {
    "by","with","or","and","of","to","for","in","on","such","as"
}

# ---- INDUSTRY SKILLS ----
TECH_SKILLS = {
    "python","sql","excel","tableau","machine learning","data analysis",
    "data visualization","statistics","pandas","numpy","power bi",
    "dashboard","analytics","deep learning"
}

HEALTHCARE_SKILLS = {
    "patient care","diagnosis","treatment planning","clinical experience",
    "medical records","xray","radiology","therapy","nursing","chiropractic"
}

BUSINESS_SKILLS = {
    "project management","communication","leadership","strategy",
    "marketing","sales","business analysis","customer service",
    "operations","management","finance"
}

# ---- DETECT JOB TYPE ----
def detect_job_type(text):
    text = text.lower()

    tech_score = sum(1 for skill in TECH_SKILLS if skill in text)
    health_score = sum(1 for skill in HEALTHCARE_SKILLS if skill in text)
    business_score = sum(1 for skill in BUSINESS_SKILLS if skill in text)

    scores = {
        "tech": tech_score,
        "healthcare": health_score,
        "business": business_score
    }

    return max(scores, key=scores.get)


# ---- GET SKILLS FOR JOB TYPE ----
def get_relevant_skills(job):
    job_type = detect_job_type(job)

    if job_type == "tech":
        return TECH_SKILLS, job_type
    elif job_type == "healthcare":
        return HEALTHCARE_SKILLS, job_type
    else:
        return BUSINESS_SKILLS, job_type


# ---- CLEAN TEXT ----
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9+#\s]', '', text)
    return text


# ---- EXTRACT KEYWORDS (FILTERED BY INDUSTRY) ----
def extract_keywords(text, allowed_skills):
    text = clean_text(text)

    found_skills = set()

    for skill in allowed_skills:
        if skill in text:
            found_skills.add(skill)

    return found_skills


# ---- SEMANTIC SIMILARITY ----
def get_similarity(resume, job):
    embeddings = model.encode([resume, job])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(score * 100, 2)


# ---- KEYWORD MATCH (INDUSTRY-AWARE) ----
def get_keyword_match(resume, job):
    relevant_skills, job_type = get_relevant_skills(job)

    resume_keywords = extract_keywords(resume, relevant_skills)
    job_keywords = extract_keywords(job, relevant_skills)

    matched = resume_keywords.intersection(job_keywords)
    missing = job_keywords - resume_keywords

    match_percent = (len(matched) / len(job_keywords)) * 100 if job_keywords else 0

    return round(match_percent, 2), list(missing)[:10], job_type


# ---- AI FEEDBACK ----
def get_ai_feedback(resume, job):
    feedback = []

    keyword_score, missing, job_type = get_keyword_match(resume, job)

    feedback.append(f"🧠 Detected Job Type: {job_type.upper()}")

    if keyword_score < 50:
        feedback.append("🚨 Your resume is not well aligned with this job.")

    elif keyword_score < 75:
        feedback.append("⚠️ You're somewhat aligned, but missing key skills.")

    if missing:
        feedback.append(f"🔑 Missing important skills: {', '.join(missing[:5])}")

    if "experience" not in resume.lower():
        feedback.append("📌 Add an Experience section.")

    if "skills" not in resume.lower():
        feedback.append("🛠 Include a Skills section.")

    if "education" not in resume.lower():
        feedback.append("🎓 Include your Education background.")

    if len(resume) < 300:
        feedback.append("📏 Your resume is too short.")

    if not feedback:
        feedback.append("🔥 Strong resume! Well aligned.")

    return "\n\n".join(feedback)