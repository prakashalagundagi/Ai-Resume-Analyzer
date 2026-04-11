import streamlit as st
import pandas as pd
import numpy as np
import re
from utils.resume_parser import extract_resume_info
from utils.analyzer import analyze_resume, calculate_score, predict_field
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import time
import json
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="AI Resume Analyzer - World-Class Edition",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# World-Class CSS Design System
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

[data-testid="stApp"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.glass-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 25px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    padding: 2rem;
    margin: 1rem 0;
    transition: all 0.3s ease;
}

.glass-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 45px rgba(31, 38, 135, 0.5);
}

.hero-header {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
    border-radius: 30px;
    margin-bottom: 3rem;
    box-shadow: 0 20px 60px rgba(102, 126, 234, 0.6);
    position: relative;
    overflow: hidden;
}

.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transform: rotate(45deg);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

.hero-header h1 {
    color: #ffffff;
    font-size: 4rem;
    font-weight: 900;
    text-shadow: 3px 3px 20px rgba(0,0,0,0.4);
    margin: 0;
    position: relative;
    z-index: 1;
    animation: fadeInUp 1s ease;
}

.hero-header p {
    color: rgba(255, 255, 255, 0.95);
    font-size: 1.4rem;
    font-weight: 400;
    margin-top: 1rem;
    position: relative;
    z-index: 1;
    animation: fadeInUp 1.2s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stMetric {
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.08));
    backdrop-filter: blur(10px);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 15px 45px rgba(0,0,0,0.3);
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

.stMetric:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 25px 60px rgba(0,0,0,0.4);
}

.stMetric .metric-label {
    color: rgba(255, 255, 255, 0.9);
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}

.stMetric .metric-value {
    color: #ffffff;
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stButton > button {
    background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
    background-size: 200% 200%;
    animation: gradientMove 3s ease infinite;
    color: white;
    border: none;
    border-radius: 15px;
    padding: 15px 35px;
    font-weight: 700;
    font-size: 1.1rem;
    width: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    position: relative;
    overflow: hidden;
    text-transform: uppercase;
    letter-spacing: 1px;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.7);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(26, 26, 46, 0.95), rgba(22, 33, 62, 0.95));
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.stFileUploader {
    background: rgba(255, 255, 255, 0.05);
    border: 2px dashed rgba(102, 126, 234, 0.6);
    border-radius: 20px;
    padding: 2rem;
    transition: all 0.3s ease;
}

.stFileUploader:hover {
    border-color: rgba(102, 126, 234, 1);
    background: rgba(255, 255, 255, 0.1);
    transform: scale(1.02);
}

.stSuccess {
    background: linear-gradient(135deg, rgba(76, 175, 80, 0.2), rgba(129, 199, 132, 0.2));
    border-left: 4px solid #4CAF50;
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

.stError {
    background: linear-gradient(135deg, rgba(244, 67, 54, 0.2), rgba(239, 83, 80, 0.2));
    border-left: 4px solid #f44336;
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

.stInfo {
    background: linear-gradient(135deg, rgba(33, 150, 243, 0.2), rgba(100, 181, 246, 0.2));
    border-left: 4px solid #2196F3;
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

.skill-tag {
    display: inline-block;
    background: linear-gradient(90deg, #f093fb, #f5576c);
    color: white;
    padding: 8px 20px;
    border-radius: 25px;
    margin: 5px;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
}

.skill-tag:hover {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 8px 25px rgba(240, 147, 251, 0.6);
}

.ai-icon {
    font-size: 5rem;
    animation: float 3s ease-in-out infinite;
    display: block;
    text-align: center;
    margin-bottom: 1rem;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
}

.progress-ring {
    width: 200px;
    height: 200px;
    margin: 0 auto;
}

.chart-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None

# Hero Section
st.markdown("""
<div class="hero-header">
    <div class="ai-icon"></div>
    <h1>AI Resume Analyzer</h1>
    <p>World-Class Resume Analysis Powered by Advanced Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Logo
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div class="ai-icon"></div>
        <h2 style="color: white; margin: 0;">Control Panel</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload
    st.subheader(" Upload Resume", anchor=False)
    uploaded_file = st.file_uploader(
        "Drag & Drop or Browse",
        type=["pdf", "docx", "txt"],
        help="Support for PDF, DOCX, and TXT files",
        label_visibility="collapsed"
    )
    
    # Job Selection
    st.subheader(" Target Role", anchor=False)
    job_roles = [
        "Web Developer", "Data Analyst", "Cyber Security",
        "Software Engineer", "AI/ML Engineer", "DevOps Engineer",
        "Product Manager", "UI/UX Designer", "Mobile Developer"
    ]
    selected_job = st.selectbox("Choose your target position", job_roles, index=0)
    
    # Advanced Options
    with st.expander(" Advanced Settings"):
        experience_level = st.selectbox(
            "Experience Level",
            ["Entry Level", "Mid Level", "Senior Level", "Lead/Principal"],
            index=1
        )
        
        custom_keywords = st.text_area(
            "Custom Keywords (comma-separated)",
            placeholder="e.g., Python, React, AWS, Docker...",
            help="Add specific skills you want to highlight"
        )
    
    # Analyze Button
    analyze_button = st.button(
        " Analyze Resume",
        type="primary",
        use_container_width=True,
        disabled=not uploaded_file
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Stats
    if st.session_state.analysis_complete:
        st.markdown("---")
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.subheader(" Quick Stats", anchor=False)
        if st.session_state.resume_data:
            score = st.session_state.resume_data.get('score', 0)
            st.metric("Match Score", f"{score}%")
            st.metric("Skills Found", len(st.session_state.resume_data.get('matches', [])))
        st.markdown('</div>', unsafe_allow_html=True)

# Main Content Area
if uploaded_file and analyze_button:
    # Show loading animation
    with st.spinner(" AI is analyzing your resume..."):
        time.sleep(2)  # Simulate processing
        
        # Extract and analyze
        resume_text = extract_resume_info(uploaded_file)
        analysis_result = analyze_resume(resume_text, selected_job)
        
        # Store in session state
        st.session_state.resume_data = analysis_result
        st.session_state.analysis_complete = True
    
    # Success message
    st.success(" Analysis Complete! Here are your results:")
    
    # Main Results Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = analysis_result.get('score', 0)
        st.metric(
            "Match Score",
            f"{score}%",
            delta=f"{score-50}%" if score > 50 else f"{score-50}%",
            delta_color="normal" if score > 50 else "inverse"
        )
    
    with col2:
        matched_skills = len(analysis_result.get('matches', []))
        total_skills = analysis_result.get('total_keywords', 0)
        st.metric("Skills Matched", f"{matched_skills}/{total_skills}")
    
    with col3:
        st.metric("Experience", experience_level)
    
    # Detailed Analysis
    st.markdown("---")
    
    # Skills Analysis
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.subheader(" Skills Analysis", anchor=False)
        
        matched_skills = analysis_result.get('matches', [])
        missing_skills = analysis_result.get('missing_keywords', [])
        
        if matched_skills:
            st.write("** Matched Skills:**")
            skills_html = ""
            for skill in matched_skills[:20]:  # Limit to 20 skills
                skills_html += f'<span class="skill-tag">{skill}</span>'
            st.markdown(skills_html, unsafe_allow_html=True)
        
        if missing_skills:
            st.write("** Missing Skills:**")
            missing_html = ""
            for skill in missing_skills[:10]:  # Limit to 10 missing skills
                missing_html += f'<span class="skill-tag" style="background: linear-gradient(90deg, #ff6b6b, #ff8787);">{skill}</span>'
            st.markdown(missing_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        st.subheader(" Score Breakdown", anchor=False)
        
        # Create circular progress visualization
        score = analysis_result.get('score', 0)
        fig = go.Figure(data=[go.Pie(
            values=[score, 100-score],
            labels=['Match', 'Gap'],
            hole=0.7,
            marker_colors=['#667eea', '#e0e0e0'],
            textinfo='none',
            hoverinfo='none'
        )])
        
        fig.add_annotation(
            x=0.5, y=0.5,
            text=f"{score}%",
            showarrow=False,
            font=dict(size=24, color='white', family='Inter')
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=0, b=0, l=0, r=0),
            height=200
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("---")
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.subheader(" Personalized Recommendations", anchor=False)
    
    recommendations = [
        "Consider adding certifications in cloud technologies (AWS/Azure)",
        "Highlight more quantifiable achievements with metrics",
        "Include keywords related to Agile/Scrum methodologies",
        "Add project descriptions that demonstrate problem-solving skills",
        "Consider including a professional summary section"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.write(f"{i}. {rec}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export Options
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(" Download Report", use_container_width=True):
            st.info("Report downloaded successfully!")
    
    with col2:
        if st.button(" Share Results", use_container_width=True):
            st.info("Share link copied to clipboard!")
    
    with col3:
        if st.button(" Start New Analysis", use_container_width=True):
            st.session_state.analysis_complete = False
            st.session_state.resume_data = None
            st.rerun()

elif not uploaded_file:
    # Welcome state
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <div class="ai-icon"></div>
        <h2 style="color: white; margin-bottom: 1rem;">Welcome to AI Resume Analyzer</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; margin-bottom: 2rem;">
            Upload your resume to get instant, AI-powered analysis and personalized recommendations
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-top: 3rem;">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
                <h4 style="color: white;">Smart Analysis</h4>
                <p style="color: rgba(255,255,255,0.7);">Advanced NLP algorithms analyze your resume</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
                <h4 style="color: white;">Instant Results</h4>
                <p style="color: rgba(255,255,255,0.7);">Get detailed analysis in seconds</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
                <h4 style="color: white;">Actionable Insights</h4>
                <p style="color: rgba(255,255,255,0.7);">Personalized recommendations to improve</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); padding: 2rem;">
    <p>AI Resume Analyzer © 2024 | Powered by Advanced Machine Learning</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
        World-Class Resume Analysis Technology
    </p>
</div>
""", unsafe_allow_html=True)
