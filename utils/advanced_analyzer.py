import re
import random
from datetime import datetime, timedelta
from collections import Counter

# Advanced skill database with learning paths
SKILL_DATABASE = {
    'Web Developer': {
        'skills': ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'node.js', 'python', 'django', 'flask', 'mongodb', 'mysql', 'git', 'docker', 'aws', 'rest api'],
        'learning_paths': {
            'beginner': ['HTML5', 'CSS3', 'JavaScript Basics', 'Git', 'Responsive Design'],
            'intermediate': ['React/Vue.js', 'Node.js', 'Database Design', 'API Development'],
            'advanced': ['Microservices', 'Cloud Deployment', 'Performance Optimization', 'Security']
        },
        'courses': {
            'HTML/CSS': ['FreeCodeCamp', 'Codecademy', 'Coursera - HTML/CSS'],
            'JavaScript': ['JavaScript.info', 'Udemy - JS Complete Guide', 'Eloquent JavaScript'],
            'React': ['React Official Docs', 'Udemy - React Complete', 'Scrimba React Course'],
            'Backend': ['Node.js Docs', 'Django Tutorial', 'MongoDB University']
        },
        'salary_range': {'entry': 60000, 'mid': 85000, 'senior': 120000, 'lead': 150000}
    },
    'Data Analyst': {
        'skills': ['python', 'r', 'sql', 'excel', 'tableau', 'power bi', 'pandas', 'numpy', 'statistics', 'machine learning', 'data visualization', 'etl', 'business intelligence'],
        'learning_paths': {
            'beginner': ['Excel Advanced', 'SQL Basics', 'Statistics Fundamentals', 'Tableau'],
            'intermediate': ['Python for Data', 'Advanced SQL', 'Power BI', 'Statistical Analysis'],
            'advanced': ['Machine Learning', 'Big Data Technologies', 'Predictive Modeling', 'Data Engineering']
        },
        'courses': {
            'SQL': ['SQLBolt', 'Mode Analytics SQL', 'Coursera - SQL for Data Science'],
            'Python': ['Python for Data Analysis', 'DataCamp Python', 'Real Python'],
            'Tableau': ['Tableau Public', 'Udemy Tableau', 'Tableau Training'],
            'Statistics': ['Khan Academy Stats', 'Coursera Statistics', 'Statistics.com']
        },
        'salary_range': {'entry': 55000, 'mid': 75000, 'senior': 95000, 'lead': 120000}
    },
    'Cyber Security': {
        'skills': ['network security', 'penetration testing', 'ethical hacking', 'firewall', 'vpn', 'encryption', 'malware analysis', 'vulnerability assessment', 'siem', 'incident response', 'compliance', 'risk management'],
        'learning_paths': {
            'beginner': ['Network Fundamentals', 'Security Basics', 'Linux', 'Python for Security'],
            'intermediate': ['Penetration Testing', 'Security Tools', 'Cryptography', 'Incident Response'],
            'advanced': ['Advanced Penetration Testing', 'Malware Analysis', 'Security Architecture', 'Compliance']
        },
        'courses': {
            'Security Fundamentals': ['CompTIA Security+', 'Cybrary', 'Coursera Security'],
            'Penetration Testing': ['TryHackMe', 'HackTheBox', 'Offensive Security'],
            'Compliance': ['ISO 27001', 'GDPR Training', 'HIPAA Security']
        },
        'salary_range': {'entry': 65000, 'mid': 90000, 'senior': 130000, 'lead': 160000}
    }
}

# ATS keywords and formatting rules
ATS_RULES = {
    'keywords': {
        'action_verbs': ['managed', 'developed', 'implemented', 'created', 'led', 'designed', 'optimized', 'improved', 'achieved', 'launched'],
        'technical_skills': ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes', 'react', 'node.js'],
        'soft_skills': ['communication', 'leadership', 'teamwork', 'problem-solving', 'analytical', 'creative']
    },
    'formatting': {
        'file_types': ['.pdf', '.docx'],
        'font_recommendations': ['Calibri', 'Arial', 'Georgia', 'Times New Roman'],
        'font_size_range': (10, 12),
        'max_pages': 2
    }
}

def advanced_skill_gap_analysis(resume_text, job_role):
    """Perform comprehensive skill gap analysis with learning recommendations"""
    if job_role not in SKILL_DATABASE:
        return {"error": "Job role not supported"}
    
    job_data = SKILL_DATABASE[job_role]
    required_skills = job_data['skills']
    
    # Extract skills from resume
    found_skills = []
    missing_skills = []
    
    resume_lower = resume_text.lower()
    
    for skill in required_skills:
        if skill.lower() in resume_lower:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    # Determine experience level from resume
    experience_level = extract_experience_level(resume_text)
    
    # Generate personalized learning path
    learning_recommendations = generate_learning_path(missing_skills, experience_level, job_data)
    
    # Calculate skill gap percentage
    skill_gap_percentage = (len(missing_skills) / len(required_skills)) * 100
    
    return {
        'found_skills': found_skills,
        'missing_skills': missing_skills,
        'skill_gap_percentage': round(skill_gap_percentage, 1),
        'experience_level': experience_level,
        'learning_path': learning_recommendations,
        'total_skills': len(required_skills),
        'skills_covered': len(found_skills)
    }

def generate_learning_path(missing_skills, experience_level, job_data):
    """Generate personalized learning recommendations"""
    recommendations = []
    
    # Get appropriate learning path based on experience
    if experience_level == 'Entry Level':
        path_skills = job_data['learning_paths']['beginner']
    elif experience_level == 'Mid Level':
        path_skills = job_data['learning_paths']['intermediate']
    else:
        path_skills = job_data['learning_paths']['advanced']
    
    # Map missing skills to courses
    for skill in missing_skills[:5]:  # Limit to top 5 missing skills
        skill_category = categorize_skill(skill, job_data)
        if skill_category in job_data['courses']:
            courses = job_data['courses'][skill_category]
            recommendations.append({
                'skill': skill,
                'category': skill_category,
                'recommended_courses': random.sample(courses, min(2, len(courses))),
                'difficulty': experience_level,
                'estimated_time': f"{random.randint(2, 8)} weeks"
            })
    
    return recommendations

def categorize_skill(skill, job_data):
    """Categorize skill for learning recommendations"""
    skill_lower = skill.lower()
    
    for category, course_list in job_data['courses'].items():
        for course in course_list:
            if any(word in course.lower() for word in skill_lower.split()):
                return category
    
    return 'General'

def extract_experience_level(text):
    """Extract experience level from resume text"""
    text_lower = text.lower()
    
    # Look for explicit years of experience
    year_matches = re.findall(r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)', text_lower)
    if year_matches:
        years = int(year_matches[0])
        if years < 2:
            return 'Entry Level'
        elif years < 5:
            return 'Mid Level'
        elif years < 10:
            return 'Senior Level'
        else:
            return 'Lead/Principal'
    
    # Look for level indicators
    if any(word in text_lower for word in ['entry level', 'junior', 'fresher', 'recent graduate', 'intern']):
        return 'Entry Level'
    elif any(word in text_lower for word in ['mid level', 'intermediate', 'associate']):
        return 'Mid Level'
    elif any(word in text_lower for word in ['senior', 'lead', 'principal', 'head', 'manager']):
        return 'Senior Level'
    
    return 'Mid Level'  # Default assumption

def salary_estimation(found_skills, job_role, experience_level):
    """Estimate salary based on skills and experience"""
    if job_role not in SKILL_DATABASE:
        return {"error": "Job role not supported"}
    
    salary_data = SKILL_DATABASE[job_role]['salary_range']
    
    # Base salary based on experience
    exp_mapping = {
        'Entry Level': 'entry',
        'Mid Level': 'mid',
        'Senior Level': 'senior',
        'Lead/Principal': 'lead'
    }
    
    base_salary = salary_data.get(exp_mapping.get(experience_level, 'mid'), 75000)
    
    # Adjust based on skills coverage
    total_skills = len(SKILL_DATABASE[job_role]['skills'])
    skill_coverage = len(found_skills) / total_skills
    
    # Salary adjustment based on skill coverage (±20%)
    salary_adjustment = 1 + (skill_coverage - 0.5) * 0.4
    estimated_salary = int(base_salary * salary_adjustment)
    
    # Create salary range
    salary_range = {
        'min': int(estimated_salary * 0.9),
        'estimated': estimated_salary,
        'max': int(estimated_salary * 1.1),
        'currency': 'USD',
        'period': 'annual'
    }
    
    return salary_range

def ats_compatibility_check(resume_text, file_name=None):
    """Check ATS compatibility and provide optimization suggestions"""
    issues = []
    suggestions = []
    score = 100
    
    # Check file format
    if file_name:
        file_ext = file_name.lower().split('.')[-1]
        if file_ext not in ['pdf', 'docx']:
            issues.append("File format not ATS-friendly")
            suggestions.append("Save resume as PDF or DOCX format")
            score -= 10
    
    # Check for action verbs
    action_verbs = ATS_RULES['keywords']['action_verbs']
    found_action_verbs = [verb for verb in action_verbs if verb.lower() in resume_text.lower()]
    
    if len(found_action_verbs) < 5:
        issues.append("Insufficient action verbs")
        suggestions.append("Add more action verbs like 'managed', 'developed', 'implemented'")
        score -= 15
    
    # Check for contact information
    contact_patterns = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'linkedin\.com',  # LinkedIn
    ]
    
    contact_found = any(re.search(pattern, resume_text, re.IGNORECASE) for pattern in contact_patterns)
    if not contact_found:
        issues.append("Missing contact information")
        suggestions.append("Add phone, email, and LinkedIn profile")
        score -= 20
    
    # Check resume length (estimated by word count)
    word_count = len(resume_text.split())
    if word_count < 300:
        issues.append("Resume too short")
        suggestions.append("Add more detail to your experience")
        score -= 10
    elif word_count > 800:
        issues.append("Resume too long")
        suggestions.append("Condense content to 1-2 pages")
        score -= 10
    
    # Check for keywords
    tech_keywords = ATS_RULES['keywords']['technical_skills']
    found_keywords = [kw for kw in tech_keywords if kw.lower() in resume_text.lower()]
    
    if len(found_keywords) < 3:
        issues.append("Insufficient technical keywords")
        suggestions.append("Add more relevant technical skills and keywords")
        score -= 15
    
    # Check formatting issues
    if re.search(r'[^\x00-\x7F]', resume_text):
        issues.append("Special characters detected")
        suggestions.append("Remove special characters and use standard fonts")
        score -= 5
    
    return {
        'score': max(0, score),
        'issues': issues,
        'suggestions': suggestions,
        'found_action_verbs': found_action_verbs,
        'found_keywords': found_keywords,
        'word_count': word_count
    }

def job_description_match(resume_text, job_description):
    """Compare resume against specific job description"""
    # Extract keywords from job description
    job_keywords = extract_keywords(job_description)
    
    # Calculate match percentage
    resume_lower = resume_text.lower()
    matched_keywords = [kw for kw in job_keywords if kw.lower() in resume_lower]
    
    match_percentage = (len(matched_keywords) / len(job_keywords)) * 100 if job_keywords else 0
    
    # Generate improvement suggestions
    missing_keywords = [kw for kw in job_keywords if kw.lower() not in resume_lower]
    
    return {
        'match_percentage': round(match_percentage, 1),
        'matched_keywords': matched_keywords,
        'missing_keywords': missing_keywords[:10],  # Top 10 missing
        'total_keywords': len(job_keywords),
        'recommendations': generate_job_recommendations(missing_keywords)
    }

def extract_keywords(text):
    """Extract important keywords from text"""
    # Simple keyword extraction (can be enhanced with NLP)
    common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'}
    
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    word_freq = Counter(words)
    
    # Filter out common words and return top keywords
    keywords = [word for word, freq in word_freq.most_common(20) if word not in common_words]
    return keywords

def generate_job_recommendations(missing_keywords):
    """Generate recommendations based on missing keywords"""
    recommendations = []
    
    for keyword in missing_keywords[:5]:
        if len(keyword) > 3:
            recommendations.append(f"Highlight experience with {keyword}")
    
    if len(missing_keywords) > 10:
        recommendations.append("Consider tailoring your resume more specifically to this role")
    
    return recommendations

def interview_preparation(job_role, found_skills):
    """Generate interview preparation questions and tips"""
    questions = {
        'Web Developer': [
            "Explain the difference between let, const, and var in JavaScript",
            "How do you optimize website performance?",
            "Describe RESTful API design principles",
            "What is the difference between synchronous and asynchronous programming?",
            "How do you handle state management in React?"
        ],
        'Data Analyst': [
            "How do you handle missing data in a dataset?",
            "Explain the difference between correlation and causation",
            "What data visualization tools have you used?",
            "How do you ensure data quality and accuracy?",
            "Describe a complex data analysis project you've worked on"
        ],
        'Cyber Security': [
            "How do you stay updated with the latest security threats?",
            "Explain the difference between symmetric and asymmetric encryption",
            "Describe your approach to vulnerability assessment",
            "How would you respond to a security breach?",
            "What security frameworks are you familiar with?"
        ]
    }
    
    job_questions = questions.get(job_role, [
        "Tell me about your experience in this field",
        "How do you stay current with industry trends?",
        "Describe a challenging project you've worked on"
    ])
    
    # Add skill-specific questions
    skill_questions = []
    for skill in found_skills[:3]:
        skill_questions.append(f"How have you used {skill} in your previous roles?")
    
    return {
        'technical_questions': job_questions[:5],
        'skill_questions': skill_questions,
        'behavioral_questions': [
            "Tell me about a time you had to learn a new technology quickly",
            "Describe a situation where you had to work with a difficult team member",
            "How do you prioritize tasks when facing multiple deadlines?"
        ],
        'preparation_tips': [
            "Research the company and role thoroughly",
            "Prepare specific examples using the STAR method",
            "Practice explaining your projects clearly",
            "Have thoughtful questions ready for the interviewer"
        ]
    }
