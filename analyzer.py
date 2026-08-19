import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# SKILLS DATABASE
# ============================================================

SKILLS = [
    "python", "java", "c", "c++", "c#", "javascript",
    "typescript", "html", "css", "react", "angular",
    "node.js", "nodejs", "flask", "django", "fastapi",
    "sql", "mysql", "postgresql", "mongodb", "firebase",
    "git", "github", "docker", "aws", "azure", "google cloud",
    "machine learning", "deep learning", "artificial intelligence",
    "data science", "data analysis", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "opencv", "nlp",
    "power bi", "tableau", "excel", "streamlit", "spring boot",
    "php", "bootstrap", "tailwind", "linux", "rest api", "api",
    "data structures", "algorithms", "oop", "agile", "scrum"
]


# ============================================================
# RESUME SECTIONS
# ============================================================

SECTION_KEYWORDS = {

    "Contact Information": [
        "email", "phone", "mobile", "linkedin", "github"
    ],

    "Education": [
        "education", "academic", "degree", "university",
        "college", "bachelor", "b.tech", "b.e"
    ],

    "Skills": [
        "skills", "technical skills", "technologies",
        "technical expertise"
    ],

    "Projects": [
        "projects", "project experience", "academic projects"
    ],

    "Experience": [
        "experience", "work experience", "employment",
        "internship", "internships"
    ],

    "Certifications": [
        "certifications", "certificates", "certification"
    ],

    "Achievements": [
        "achievements", "awards", "accomplishments"
    ],

    "Summary": [
        "summary", "profile", "objective",
        "career objective", "professional summary"
    ]
}


# ============================================================
# JOB ROLES
# ============================================================

JOB_ROLES = {

    "Python Developer": [
        "python", "flask", "django", "fastapi"
    ],

    "Web Developer": [
        "html", "css", "javascript", "react"
    ],

    "Full Stack Developer": [
        "html", "css", "javascript",
        "react", "node.js", "sql"
    ],

    "Data Analyst": [
        "python", "pandas", "numpy",
        "excel", "sql", "power bi"
    ],

    "Data Scientist": [
        "python", "pandas", "numpy",
        "machine learning", "scikit-learn"
    ],

    "Machine Learning Engineer": [
        "python", "machine learning",
        "scikit-learn", "tensorflow", "pytorch"
    ],

    "AI Engineer": [
        "python", "artificial intelligence",
        "machine learning", "deep learning",
        "tensorflow", "pytorch"
    ],

    "Cloud Engineer": [
        "aws", "azure", "docker", "linux"
    ],

    "Backend Developer": [
        "python", "java", "flask", "django",
        "fastapi", "sql", "mongodb"
    ]
}


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# FIND SKILLS
# ============================================================

def find_skills(text):

    text_lower = clean_text(text)

    detected = []

    for skill in SKILLS:

        if skill.lower() in text_lower:
            detected.append(skill)

    return sorted(set(detected))


# ============================================================
# ANALYZE RESUME SECTIONS
# ============================================================

def analyze_sections(text):

    text_lower = clean_text(text)

    results = {}

    for section, keywords in SECTION_KEYWORDS.items():

        found = any(
            keyword.lower() in text_lower
            for keyword in keywords
        )

        results[section] = found

    return results


# ============================================================
# ATS STATUS
# ============================================================

def get_ats_status(score):

    if score >= 85:
        return "Excellent ATS Compatibility"

    elif score >= 70:
        return "Good ATS Compatibility"

    elif score >= 50:
        return "Average ATS Compatibility"

    else:
        return "Needs ATS Improvement"


# ============================================================
# EXTRACT JOB KEYWORDS
# ============================================================

def extract_job_keywords(job_description):

    if not job_description.strip():
        return []

    text = clean_text(job_description)

    detected_skills = find_skills(text)

    common_keywords = [
        "communication",
        "leadership",
        "teamwork",
        "problem solving",
        "problem-solving",
        "analytical",
        "analytical skills",
        "project management",
        "time management",
        "collaboration",
        "debugging",
        "testing",
        "development",
        "software development",
        "web development",
        "api",
        "rest api",
        "restful",
        "database",
        "data structures",
        "algorithms",
        "object oriented programming",
        "oop",
        "version control",
        "agile",
        "scrum",
        "deployment",
        "automation",
        "security",
        "cloud",
        "documentation",
        "critical thinking"
    ]

    found_common = []

    for keyword in common_keywords:

        if keyword in text:
            found_common.append(keyword)

    all_keywords = detected_skills + found_common

    return list(dict.fromkeys(all_keywords))


# ============================================================
# KEYWORD ANALYSIS
# ============================================================

def analyze_keywords(
    resume_text,
    job_description
):

    if not job_description.strip():

        return {
            "job_keywords": [],
            "found_keywords": [],
            "missing_keywords": [],
            "keyword_score": None
        }

    job_keywords = extract_job_keywords(
        job_description
    )

    resume_lower = clean_text(
        resume_text
    )

    found_keywords = []
    missing_keywords = []

    for keyword in job_keywords:

        if keyword.lower() in resume_lower:
            found_keywords.append(keyword)

        else:
            missing_keywords.append(keyword)

    if job_keywords:

        keyword_score = round(
            len(found_keywords)
            / len(job_keywords)
            * 100,
            2
        )

    else:

        keyword_score = 0

    return {

        "job_keywords": job_keywords,

        "found_keywords": found_keywords,

        "missing_keywords": missing_keywords,

        "keyword_score": keyword_score
    }


# ============================================================
# JOB MATCH
# ============================================================

def calculate_job_match(
    resume_text,
    job_description
):

    if not job_description.strip():

        return (
            None,
            None,
            [],
            [],
            None
        )

    resume_skills = set(
        find_skills(resume_text)
    )

    job_skills = set(
        find_skills(job_description)
    )

    if job_skills:

        matching = resume_skills.intersection(
            job_skills
        )

        missing = job_skills - resume_skills

        skill_score = (
            len(matching) /
            len(job_skills)
        ) * 100

    else:

        matching = set()
        missing = set()
        skill_score = 0

    try:

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform([
            resume_text,
            job_description
        ])

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        nlp_score = round(
            similarity * 100,
            2
        )

    except Exception:

        nlp_score = 0

    if job_skills:

        final_match = (
            skill_score * 0.7 +
            nlp_score * 0.3
        )

    else:

        final_match = nlp_score

    final_match = round(
        final_match,
        2
    )

    if final_match >= 85:
        status = "Excellent Job Match"

    elif final_match >= 70:
        status = "Strong Job Match"

    elif final_match >= 50:
        status = "Moderate Job Match"

    else:
        status = "Low Job Match"

    return (
        final_match,
        status,
        sorted(matching),
        sorted(missing),
        nlp_score
    )


# ============================================================
# CAREER RECOMMENDATIONS
# ============================================================

def career_recommendations(detected_skills):

    detected = set(
        skill.lower()
        for skill in detected_skills
    )

    recommendations = []

    for role, required_skills in JOB_ROLES.items():

        matched = len(
            detected.intersection(
                required_skills
            )
        )

        total = len(required_skills)

        score = round(
            matched / total * 100
        )

        if score > 0:

            recommendations.append({
                "role": role,
                "match": score
            })

    recommendations.sort(
        key=lambda x: x["match"],
        reverse=True
    )

    return recommendations[:5]


# ============================================================
# STRENGTHS
# ============================================================

def generate_strengths(
    skills,
    sections,
    ats_score
):

    strengths = []

    if len(skills) >= 8:

        strengths.append(
            f"Strong technical skill coverage with "
            f"{len(skills)} detected skills."
        )

    elif len(skills) >= 4:

        strengths.append(
            f"Good technical foundation with "
            f"{len(skills)} detected skills."
        )

    elif skills:

        strengths.append(
            f"Technical skills are present with "
            f"{len(skills)} detected skills."
        )

    if sections.get("Projects"):

        strengths.append(
            "Projects section is present and demonstrates practical work."
        )

    if sections.get("Education"):

        strengths.append(
            "Education information is clearly represented."
        )

    if sections.get("Experience"):

        strengths.append(
            "Experience or internship information is included."
        )

    if sections.get("Certifications"):

        strengths.append(
            "Certifications are included in the resume."
        )

    if sections.get("Achievements"):

        strengths.append(
            "Achievements are included."
        )

    if ats_score >= 80:

        strengths.append(
            "The resume has strong ATS-friendly characteristics."
        )

    if sections.get("Contact Information"):

        strengths.append(
            "Professional contact information is available."
        )

    if not strengths:

        strengths.append(
            "The resume contains useful information "
            "that can be improved further."
        )

    return strengths


# ============================================================
# WEAKNESSES
# ============================================================

def generate_weaknesses(
    skills,
    sections,
    ats_score,
    job_description,
    missing_skills,
    missing_keywords
):

    weaknesses = []

    if len(skills) < 5:

        weaknesses.append(
            "The resume contains relatively few detectable technical skills."
        )

    if not sections.get("Summary"):

        weaknesses.append(
            "A professional summary or career objective is missing."
        )

    if not sections.get("Projects"):

        weaknesses.append(
            "A dedicated Projects section is missing."
        )

    if not sections.get("Experience"):

        weaknesses.append(
            "Experience or internship information is missing."
        )

    if not sections.get("Certifications"):

        weaknesses.append(
            "Certifications are not clearly mentioned."
        )

    if not sections.get("Achievements"):

        weaknesses.append(
            "Achievements or measurable accomplishments are missing."
        )

    if ats_score < 70:

        weaknesses.append(
            "ATS compatibility needs improvement."
        )

    if job_description and missing_skills:

        weaknesses.append(
            f"{len(missing_skills)} technical skills from the "
            f"job description were not detected."
        )

    if job_description and missing_keywords:

        weaknesses.append(
            f"{len(missing_keywords)} important job keywords "
            f"were not detected."
        )

    if not sections.get("Contact Information"):

        weaknesses.append(
            "Contact information or professional links "
            "are not clearly detected."
        )

    if not weaknesses:

        weaknesses.append(
            "No major weaknesses were detected."
        )

    return weaknesses


# ============================================================
# STEP 24 - SMART IMPROVEMENT SUGGESTIONS
# ============================================================

def generate_improvement_suggestions(
    ats_score,
    keyword_score,
    job_match_score,
    nlp_score,
    skills,
    section_results,
    missing_skills,
    missing_keywords
):

    suggestions = []

    if ats_score < 50:

        suggestions.append(
            "🚨 Your ATS score is low. Use standard section headings, "
            "simple formatting, readable fonts, and relevant keywords."
        )

    elif ats_score < 70:

        suggestions.append(
            "📈 Improve ATS compatibility by using clearer section "
            "headings and adding relevant technical keywords."
        )

    elif ats_score < 85:

        suggestions.append(
            "🎯 Your ATS score is good. Fine-tune formatting and "
            "job-specific keywords to push it higher."
        )

    else:

        suggestions.append(
            "⭐ Excellent ATS compatibility. Maintain a clean, "
            "simple and recruiter-friendly format."
        )

    if keyword_score is not None:

        if keyword_score < 50:

            suggestions.append(
                "🔑 Your keyword match is low. Review the job description "
                "and naturally include relevant skills and terminology "
                "that genuinely match your experience."
            )

        elif keyword_score < 75:

            suggestions.append(
                "🔑 Your keyword coverage is moderate. Add relevant "
                "job-specific terminology where truthful."
            )

        else:

            suggestions.append(
                "🔑 Strong keyword coverage. Continue tailoring the "
                "resume for each individual job."
            )

    if job_match_score is not None:

        if job_match_score < 50:

            suggestions.append(
                "💼 The resume has a low match with this job. "
                "Highlight relevant projects, skills and experience "
                "that directly relate to the role."
            )

        elif job_match_score < 75:

            suggestions.append(
                "💼 Your job compatibility is moderate. "
                "Strengthen the resume around the employer's "
                "most important requirements."
            )

        else:

            suggestions.append(
                "💼 Strong job compatibility. Keep the resume "
                "focused on the target position."
            )

    if nlp_score is not None and nlp_score < 50:

        suggestions.append(
            "🧠 The resume has low semantic similarity to the job "
            "description. Rewrite your summary and project "
            "descriptions using relevant terminology."
        )

    if len(skills) < 4:

        suggestions.append(
            "🛠️ Add more relevant technical skills that you genuinely know."
        )

    elif len(skills) < 8:

        suggestions.append(
            "🛠️ Consider expanding your technical skills section "
            "with relevant tools, frameworks and technologies."
        )

    else:

        suggestions.append(
            "🛠️ Your technical skill coverage is strong. "
            "Prioritize the most relevant skills for each application."
        )

    if missing_skills:

        suggestions.append(
            "🎯 Review the missing job skills. Learn them if they "
            "are relevant to your career goals, then add them only "
            "after you have genuine knowledge or experience."
        )

    if missing_keywords:

        suggestions.append(
            "🔍 Review the missing keywords and naturally incorporate "
            "the ones that accurately describe your experience."
        )

    if not section_results.get("Summary"):

        suggestions.append(
            "📝 Add a concise professional summary tailored to your target role."
        )

    if not section_results.get("Projects"):

        suggestions.append(
            "💻 Add 2–3 relevant projects with technologies used, "
            "your contribution and measurable outcomes."
        )

    if not section_results.get("Experience"):

        suggestions.append(
            "🏢 Include internships, freelance work, volunteering "
            "or practical experience when applicable."
        )

    if not section_results.get("Certifications"):

        suggestions.append(
            "🏆 Add relevant certifications with the issuing "
            "organization and completion details."
        )

    if not section_results.get("Achievements"):

        suggestions.append(
            "📈 Add measurable achievements such as awards, "
            "rankings, competition results or performance improvements."
        )

    if not suggestions:

        suggestions.append(
            "🎉 Your resume is in good shape. Continue tailoring "
            "it to each target job."
        )

    return list(dict.fromkeys(suggestions))


# ============================================================
# ACTION PLAN
# ============================================================

def generate_action_plan(
    ats_score,
    keyword_score,
    job_match_score,
    missing_skills,
    missing_keywords,
    section_results
):

    actions = []

    if ats_score < 70:

        actions.append(
            "Improve ATS compatibility using clean formatting "
            "and standard headings."
        )

    if keyword_score is not None and keyword_score < 75:

        actions.append(
            "Add relevant job-specific keywords where they "
            "truthfully represent your skills."
        )

    if job_match_score is not None and job_match_score < 70:

        actions.append(
            "Tailor your summary and project descriptions "
            "toward the target job."
        )

    if missing_skills:

        actions.append(
            "Work on the missing technical skills that are "
            "relevant to your career goal."
        )

    if missing_keywords:

        actions.append(
            "Review the missing keywords and include "
            "appropriate ones naturally."
        )

    if not section_results.get("Summary"):

        actions.append(
            "Create a 2–4 line professional summary."
        )

    if not section_results.get("Projects"):

        actions.append(
            "Add 2–3 strong projects with technologies "
            "and measurable results."
        )

    if not section_results.get("Experience"):

        actions.append(
            "Add relevant internships, practical experience "
            "or freelance work."
        )

    if not section_results.get("Achievements"):

        actions.append(
            "Add measurable achievements and accomplishments."
        )

    if not actions:

        actions.append(
            "Continue tailoring your resume to each target job."
        )

    return list(dict.fromkeys(actions))


# ============================================================
# STEP 26 - SCORE EXPLANATION
# ============================================================

def generate_score_explanation(
    overall_score,
    ats_score,
    job_match_score,
    keyword_score,
    nlp_score,
    skills,
    section_results
):

    explanations = []

    # Overall score

    if overall_score >= 85:

        summary = (
            "Excellent! Your resume is highly competitive and "
            "has strong overall quality."
        )

    elif overall_score >= 70:

        summary = (
            "Good resume! You have a solid foundation, but a few "
            "targeted improvements can make it significantly stronger."
        )

    elif overall_score >= 50:

        summary = (
            "Your resume has a reasonable foundation, but several "
            "areas should be improved before applying to competitive roles."
        )

    else:

        summary = (
            "Your resume needs significant improvement. Focus on "
            "structure, skills, keywords and relevant experience."
        )


    # Score-specific explanations

    if ats_score >= 85:

        explanations.append(
            "Your ATS compatibility is excellent, meaning your resume "
            "has a strong structure for automated screening systems."
        )

    elif ats_score >= 70:

        explanations.append(
            "Your ATS compatibility is good, but clearer headings, "
            "better keyword usage and simpler formatting could improve it."
        )

    else:

        explanations.append(
            "Your ATS compatibility is limiting your score. Improve "
            "section structure, contact details, skills and job-relevant keywords."
        )


    if job_match_score is not None:

        if job_match_score >= 85:

            explanations.append(
                "Your resume strongly matches the provided job description."
            )

        elif job_match_score >= 70:

            explanations.append(
                "Your resume has a good match with the target job, "
                "but some requirements are still missing."
            )

        elif job_match_score >= 50:

            explanations.append(
                "Your resume has a moderate job match. Tailoring "
                "your skills and project descriptions would help."
            )

        else:

            explanations.append(
                "Your resume currently has a low match with this job. "
                "Focus on relevant skills, projects and terminology."
            )


    if keyword_score is not None:

        if keyword_score >= 80:

            explanations.append(
                "Your keyword coverage is strong."
            )

        elif keyword_score >= 50:

            explanations.append(
                "Your keyword coverage is moderate. Add relevant "
                "job-specific terms where they truthfully apply."
            )

        else:

            explanations.append(
                "Your keyword coverage is low. Carefully review the "
                "job description and tailor your resume."
            )


    if nlp_score is not None:

        if nlp_score >= 70:

            explanations.append(
                "The resume content is semantically well aligned "
                "with the job description."
            )

        elif nlp_score >= 40:

            explanations.append(
                "The resume has moderate semantic similarity with "
                "the job description."
            )

        else:

            explanations.append(
                "The resume content has low semantic similarity "
                "with the target job."
            )


    if len(skills) >= 8:

        explanations.append(
            f"You have strong technical coverage with {len(skills)} "
            "detected skills."
        )

    elif len(skills) >= 4:

        explanations.append(
            f"You have a reasonable technical foundation with "
            f"{len(skills)} detected skills."
        )

    else:

        explanations.append(
            "Your detected technical skill count is low. Add relevant "
            "skills that you genuinely know."
        )


    missing_sections = [
        section
        for section, found in section_results.items()
        if not found
    ]

    if missing_sections:

        important = ", ".join(
            missing_sections[:3]
        )

        explanations.append(
            f"Some resume sections could be strengthened or added, "
            f"including: {important}."
        )

    return {
        "summary": summary,
        "details": explanations
    }


# ============================================================
# STEP 26 - SCORE CATEGORY BREAKDOWN
# ============================================================

def generate_score_factors(
    ats_score,
    job_match_score,
    keyword_score,
    nlp_score,
    skills,
    section_results
):

    factors = []

    factors.append({
        "name": "ATS Compatibility",
        "score": round(ats_score),
        "description": (
            "Measures resume structure, detected skills "
            "and contact information."
        )
    })

    factors.append({
        "name": "Technical Skills",
        "score": min(len(skills) * 8, 100),
        "description": (
            "Based on the number of recognized technical skills."
        )
    })

    factors.append({
        "name": "Resume Structure",
        "score": round(
            sum(section_results.values())
            / len(section_results) * 100
        ),
        "description": (
            "Checks important resume sections such as education, "
            "projects, experience and certifications."
        )
    })

    if keyword_score is not None:

        factors.append({
            "name": "Keyword Match",
            "score": round(keyword_score),
            "description": (
                "Measures important keywords shared with the job description."
            )
        })

    if job_match_score is not None:

        factors.append({
            "name": "Job Compatibility",
            "score": round(job_match_score),
            "description": (
                "Combines skill matching and NLP similarity."
            )
        })

    if nlp_score is not None:

        factors.append({
            "name": "NLP Similarity",
            "score": round(nlp_score),
            "description": (
                "Measures semantic similarity between resume "
                "and job description."
            )
        })

    return factors


# ============================================================
# OVERALL SCORE
# ============================================================

def calculate_overall_score(
    ats_score,
    job_match_score,
    keyword_score,
    section_results,
    skills
):

    section_score = (
        sum(section_results.values())
        /
        len(section_results)
    ) * 100

    skill_score = min(
        len(skills) * 8,
        100
    )

    if job_match_score is not None:

        keyword_component = (
            keyword_score
            if keyword_score is not None
            else 0
        )

        overall = (
            ats_score * 0.30
            +
            job_match_score * 0.30
            +
            keyword_component * 0.15
            +
            section_score * 0.15
            +
            skill_score * 0.10
        )

    else:

        overall = (
            ats_score * 0.55
            +
            section_score * 0.25
            +
            skill_score * 0.20
        )

    return round(
        min(overall, 100),
        2
    )


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze_resume(
    text,
    job_description=""
):

    clean_resume = clean_text(text)

    skills = find_skills(
        clean_resume
    )

    section_results = analyze_sections(
        clean_resume
    )

    section_score = (
        sum(section_results.values())
        /
        len(section_results)
    ) * 100

    skill_score = min(
        len(skills) * 8,
        100
    )

    contact_score = (
        100
        if section_results["Contact Information"]
        else 0
    )

    ats_score = round(
        section_score * 0.50
        +
        skill_score * 0.30
        +
        contact_score * 0.20,
        2
    )

    ats_status = get_ats_status(
        ats_score
    )

    (
        job_match_score,
        job_match_status,
        matching_job_skills,
        missing_job_skills,
        nlp_score
    ) = calculate_job_match(
        clean_resume,
        job_description
    )

    keyword_analysis = analyze_keywords(
        clean_resume,
        job_description
    )

    keyword_score = keyword_analysis[
        "keyword_score"
    ]

    overall_score = calculate_overall_score(
        ats_score,
        job_match_score,
        keyword_score,
        section_results,
        skills
    )

    quality = {

        "Technical Skills":
            round(skill_score),

        "Resume Structure":
            round(section_score),

        "Contact Information":
            round(contact_score),

        "ATS Compatibility":
            round(ats_score)
    }

    strengths = generate_strengths(
        skills,
        section_results,
        ats_score
    )

    weaknesses = generate_weaknesses(
        skills,
        section_results,
        ats_score,
        job_description,
        missing_job_skills,
        keyword_analysis["missing_keywords"]
    )

    improvement_suggestions = generate_improvement_suggestions(
        ats_score,
        keyword_score,
        job_match_score,
        nlp_score,
        skills,
        section_results,
        missing_job_skills,
        keyword_analysis["missing_keywords"]
    )

    action_plan = generate_action_plan(
        ats_score,
        keyword_score,
        job_match_score,
        missing_job_skills,
        keyword_analysis["missing_keywords"],
        section_results
    )

    job_recommendations = career_recommendations(
        skills
    )

    # ========================================================
    # STEP 26 DATA
    # ========================================================

    score_explanation = generate_score_explanation(
        overall_score,
        ats_score,
        job_match_score,
        keyword_score,
        nlp_score,
        skills,
        section_results
    )

    score_factors = generate_score_factors(
        ats_score,
        job_match_score,
        keyword_score,
        nlp_score,
        skills,
        section_results
    )

    return {

        "overall_score":
            overall_score,

        "ats_score":
            ats_score,

        "ats_status":
            ats_status,

        "job_match_score":
            job_match_score,

        "job_match_status":
            job_match_status,

        "nlp_score":
            nlp_score,

        "skills":
            skills,

        "matching_job_skills":
            matching_job_skills,

        "missing_job_skills":
            missing_job_skills,

        "section_results":
            section_results,

        "quality":
            quality,

        "job_recommendations":
            job_recommendations,

        "suggestions":
            improvement_suggestions,

        "improvement_suggestions":
            improvement_suggestions,

        "strengths":
            strengths,

        "weaknesses":
            weaknesses,

        "action_plan":
            action_plan,

        # STEP 26

        "score_explanation":
            score_explanation,

        "score_factors":
            score_factors,

        # Keywords

        "job_keywords":
            keyword_analysis["job_keywords"],

        "found_keywords":
            keyword_analysis["found_keywords"],

        "missing_keywords":
            keyword_analysis["missing_keywords"],

        "keyword_score":
            keyword_score
    }