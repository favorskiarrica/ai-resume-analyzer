import re

# ---------------- STOPWORDS ---------------- #

STOPWORDS = {
    "the","and","is","in","to","of","a","for","on","with","as","by","an","at","from",
    "this","that","be","are","or","it","your","will","we","our",
    "you","they","their","them",
    "experience","job","role","responsibilities","requirements",
    "candidate","ideal","seeking","join","description","position","work"
}

# ---------------- TEXT CLEANING ---------------- #

def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text.lower())
    words = text.split()

    normalized = []

    for w in words:
        if w.startswith("treat"):
            normalized.append("treat")
        elif w.startswith("diagnos"):
            normalized.append("diagnose")
        elif w.startswith("evaluat"):
            normalized.append("evaluate")
        elif w.startswith("perform"):
            normalized.append("perform")
        elif w.startswith("develop"):
            normalized.append("develop")
        else:
            normalized.append(w)

    return [w for w in normalized if len(w) > 2 and w not in STOPWORDS]


# ---------------- JOB TYPE DETECTION ---------------- #

JOB_CATEGORIES = {
    "Data Analyst": ["data", "analysis", "sql", "excel", "tableau", "power", "dashboard", "statistics"],
    "Software Engineer": ["python", "java", "api", "backend", "frontend", "git", "debugging", "algorithms"],
    "Healthcare": ["patient", "clinical", "medical", "diagnosis", "treatment", "care"],
    "Chiropractor": ["chiropractic", "spinal", "adjustment", "therapy", "musculoskeletal"]
}

def detect_job_type(job_text):
    words = set(clean_text(job_text))

    scores = {}

    for job, keywords in JOB_CATEGORIES.items():
        scores[job] = len(words & set(keywords))

    best_match = max(scores, key=scores.get)

    return best_match


# ---------------- KEYWORD EXTRACTION ---------------- #

IMPORTANT_VERBS = {
    "diagnose", "treat", "evaluate", "perform", "develop"
}

def extract_job_keywords(job_text):
    words = clean_text(job_text)

    freq = {}

    for word in words:
        freq[word] = freq.get(word, 0) + 1

    # boost important verbs
    for word in IMPORTANT_VERBS:
        if word in freq:
            freq[word] += 2

    sorted_words = sorted(freq, key=freq.get, reverse=True)

    return set(sorted_words[:20])


# ---------------- MATCHING ENGINE ---------------- #

def get_match_percentage(resume_text, job_text):
    resume_words = set(clean_text(resume_text))
    job_keywords = extract_job_keywords(job_text)

    matched = resume_words & job_keywords
    missing = job_keywords - resume_words

    score = (len(matched) / len(job_keywords)) * 100 if job_keywords else 0

    job_type = detect_job_type(job_text)

    return int(score), list(matched), list(missing), job_type


# ---------------- CHATGPT-STYLE FEEDBACK ---------------- #

def generate_ai_suggestions(score, matched, missing, job_type):

    matched = list(matched)
    missing = list(missing)

    response = []

    response.append("🧠 AI Resume Coach Analysis\n")

    # Score logic
    if score >= 80:
        response.append(f"Your resume is highly competitive for a {job_type} role.")
    elif score >= 60:
        response.append(f"Good foundation for a {job_type} role, but improvements are needed.")
    elif score >= 40:
        response.append(f"Moderate match for a {job_type} role. Key gaps exist.")
    else:
        response.append(f"Low match for a {job_type} role. Major improvements required.")

    # Missing skills
    if missing:
        response.append("\n📌 Missing Key Skills:")
        response.append(", ".join(missing[:6]))

    # Strengths
    if matched:
        response.append("\n✅ Your Strengths:")
        response.append(", ".join(matched[:6]))

    # Advice
    response.append("\n🚀 Improvement Tips:")
    response.append("• Add missing skills into experience section")
    response.append("• Use job keywords naturally (not just lists)")
    response.append("• Quantify achievements (e.g. improved efficiency by 20%)")

    return "\n".join(response)


# ---------------- CHAT SYSTEM (NO API NEEDED) ---------------- #

def chat_response(user_input, score, matched, missing, job_type):

    user_input = user_input.lower()

    if "improve" in user_input:
        return f"""
🧠 To improve your resume for a {job_type} role:

📌 Focus on: {', '.join(list(missing)[:5])}

📊 Your current match score is {score}%.

💡 Add these skills into real experience examples, not just a list.
"""

    elif "missing" in user_input:
        return f"""
⚠️ Missing Skills:
{', '.join(list(missing)[:8])}
"""

    elif "strength" in user_input:
        return f"""
✅ Strengths:
{', '.join(list(matched)[:8])}
"""

    elif "score" in user_input:
        return f"""
📊 Your match score is {score}%.
"""

    else:
        return """
💬 Ask me:
• How can I improve my resume?
• What am I missing?
• What are my strengths?
• What is my score?
"""