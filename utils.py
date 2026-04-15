# utils.py

def extract_keywords(text):
    return set(text.lower().split())


def get_similarity(resume_text, job_text):
    resume_words = extract_keywords(resume_text)
    job_words = extract_keywords(job_text)

    matched = resume_words & job_words

    if len(job_words) == 0:
        return 0

    score = (len(matched) / len(job_words)) * 100
    return int(score)


def get_keyword_match(resume_text, job_text):
    resume_words = extract_keywords(resume_text)
    job_words = extract_keywords(job_text)

    return list(resume_words & job_words)


def get_missing_skills(resume_text, job_text):
    resume_words = extract_keywords(resume_text)
    job_words = extract_keywords(job_text)

    return list(job_words - resume_words)


def get_ai_feedback(score):
    if score > 75:
        return "Strong match! Your resume aligns well with this job."
    elif score > 50:
        return "Decent match, but you are missing some important keywords."
    else:
        return "Low match. Tailor your resume to better fit this job description."