import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import tempfile
import os
from typing import List, Dict, Tuple

# Import our custom modules
from resume_utils import extract_resume_text, clean_text
from comparator import ResumeComparator
from advisor import CareerAdvisor

# Page configuration
st.set_page_config(
    page_title="Resume Comparator & Career Advisor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e86ab;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .recommendation-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<h1 class="main-header">🎯 Multi-Resume Comparator & Career Advisor</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    mode = st.sidebar.selectbox(
        "Choose Mode",
        ["Resume Comparison", "Personal Career Advisor"]
    )
    
    if mode == "Resume Comparison":
        resume_comparison_mode()
    else:
        career_advisor_mode()

def resume_comparison_mode():
    """Mode for comparing multiple resumes against a job role"""
    
    st.markdown('<h2 class="section-header">📊 Resume Comparison Mode</h2>', unsafe_allow_html=True)
    
    # Job role input
    col1, col2 = st.columns([2, 1])
    with col1:
        target_job = st.text_input(
            "Enter Target Job Role",
            placeholder="e.g., Data Scientist, Software Engineer, Product Manager",
            help="Specify the job role you want to match resumes against"
        )
    
    with col2:
        st.markdown("### Upload Resumes")
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type="pdf",
            accept_multiple_files=True,
            help="Upload multiple resume PDF files to compare"
        )
    
    if target_job and uploaded_files:
        if st.button("🔍 Analyze Resumes", type="primary"):
            analyze_resumes(uploaded_files, target_job)

def analyze_resumes(uploaded_files: List, target_job: str):
    """Analyze and compare multiple resumes"""
    
    with st.spinner("Processing resumes... This may take a moment."):
        # Initialize comparator
        comparator = ResumeComparator()
        
        # Process each resume
        resumes_data = []
        progress_bar = st.progress(0)
        
        for i, uploaded_file in enumerate(uploaded_files):
            # Extract text from PDF
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            
            try:
                resume_text = extract_resume_text(tmp_file_path)
                cleaned_text = clean_text(resume_text)
                
                # Calculate similarity score
                score = comparator.calculate_similarity(cleaned_text, target_job)
                
                resumes_data.append({
                    'filename': uploaded_file.name,
                    'text': cleaned_text,
                    'score': score,
                    'word_count': len(cleaned_text.split())
                })
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            finally:
                os.unlink(tmp_file_path)
            
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        # Sort by score (descending)
        resumes_data.sort(key=lambda x: x['score'], reverse=True)
        
        # Display results
        display_comparison_results(resumes_data, target_job)

def display_comparison_results(resumes_data: List[Dict], target_job: str):
    """Display the comparison results in a nice format"""
    
    st.markdown('<h2 class="section-header">📈 Comparison Results</h2>', unsafe_allow_html=True)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Resumes", len(resumes_data))
    with col2:
        st.metric("Best Match Score", f"{max(r['score'] for r in resumes_data):.1%}")
    with col3:
        st.metric("Average Score", f"{sum(r['score'] for r in resumes_data) / len(resumes_data):.1%}")
    with col4:
        st.metric("Target Role", target_job)
    
    # Create visualization
    df = pd.DataFrame(resumes_data)
    df['rank'] = range(1, len(df) + 1)
    
    # Bar chart
    fig = px.bar(
        df, 
        x='filename', 
        y='score',
        title=f'Resume Match Scores for {target_job}',
        labels={'score': 'Match Score', 'filename': 'Resume'},
        color='score',
        color_continuous_scale='viridis'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed results table
    st.markdown("### 📋 Detailed Rankings")
    
    for i, resume in enumerate(resumes_data):
        with st.expander(f"#{i+1} - {resume['filename']} (Score: {resume['score']:.1%})"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**Statistics:**")
                st.write(f"• Match Score: {resume['score']:.1%}")
                st.write(f"• Word Count: {resume['word_count']}")
                st.write(f"• Rank: {i+1}/{len(resumes_data)}")
            
            with col2:
                st.markdown("**Resume Preview:**")
                st.text_area(
                    "Content", 
                    resume['text'][:500] + "..." if len(resume['text']) > 500 else resume['text'],
                    height=150,
                    key=f"preview_{i}"
                )
    
    # Download results
    if st.button("📥 Download Results as CSV"):
        csv_data = pd.DataFrame([
            {
                'Rank': i+1,
                'Filename': r['filename'],
                'Match_Score': f"{r['score']:.3f}",
                'Word_Count': r['word_count']
            }
            for i, r in enumerate(resumes_data)
        ])
        
        csv_buffer = BytesIO()
        csv_data.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        st.download_button(
            label="Download CSV Report",
            data=csv_buffer,
            file_name=f"resume_comparison_{target_job.replace(' ', '_')}.csv",
            mime="text/csv"
        )

def career_advisor_mode():
    """Mode for personal career advice"""
    
    st.markdown('<h2 class="section-header">🎓 Personal Career Advisor</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        target_role = st.text_input(
            "Target Job Role",
            placeholder="e.g., Senior Data Scientist",
            help="What role are you aiming for?"
        )
        
        experience_level = st.selectbox(
            "Current Experience Level",
            ["Entry Level (0-2 years)", "Mid Level (3-5 years)", "Senior Level (6-10 years)", "Lead/Expert (10+ years)"]
        )
    
    with col2:
        st.markdown("### Upload Your Resume")
        user_resume = st.file_uploader(
            "Upload your resume (PDF)",
            type="pdf",
            help="Upload your current resume for personalized advice"
        )
    
    if target_role and user_resume:
        if st.button("🚀 Get Career Advice", type="primary"):
            get_career_advice(user_resume, target_role, experience_level)

def get_career_advice(resume_file, target_role: str, experience_level: str):
    """Generate personalized career advice"""
    
    with st.spinner("Analyzing your resume and generating personalized advice..."):
        # Extract resume text
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(resume_file.read())
            tmp_file_path = tmp_file.name
        
        try:
            resume_text = extract_resume_text(tmp_file_path)
            cleaned_text = clean_text(resume_text)
            
            # Initialize advisor
            advisor = CareerAdvisor()
            
            # Get comprehensive advice
            advice_data = advisor.get_comprehensive_advice(
                resume_text=cleaned_text,
                target_role=target_role,
                experience_level=experience_level
            )
            
            # Display advice
            display_career_advice(advice_data, target_role)
            
        except Exception as e:
            st.error(f"Error processing resume: {str(e)}")
        finally:
            os.unlink(tmp_file_path)

def display_career_advice(advice_data: Dict, target_role: str):
    """Display comprehensive career advice"""
    
    st.markdown('<h2 class="section-header">💡 Your Personalized Career Roadmap</h2>', unsafe_allow_html=True)
    
    # Overall assessment
    if 'overall_score' in advice_data:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Resume Strength", f"{advice_data['overall_score']}/10")
        with col2:
            st.metric("Target Role", target_role)
        with col3:
            readiness = advice_data.get('readiness_level', 'Developing')
            st.metric("Readiness Level", readiness)
    
    # Strengths and improvements
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Your Strengths")
        if 'strengths' in advice_data:
            for strength in advice_data['strengths']:
                st.markdown(f"• {strength}")
        else:
            st.info("Analyzing your strengths...")
    
    with col2:
        st.markdown("### 🎯 Areas for Improvement")
        if 'improvements' in advice_data:
            for improvement in advice_data['improvements']:
                st.markdown(f"• {improvement}")
        else:
            st.info("Identifying improvement areas...")
    
    # Skills analysis
    if 'missing_skills' in advice_data:
        st.markdown("### 🔧 Missing Technical Skills")
        missing_skills = advice_data['missing_skills']
        if missing_skills:
            skills_df = pd.DataFrame([{'Skill': skill, 'Priority': 'High'} for skill in missing_skills])
            st.dataframe(skills_df, use_container_width=True)
        else:
            st.success("Great! You seem to have most of the required technical skills.")
    
    # Roadmap
    if 'roadmap' in advice_data:
        st.markdown("### 🗺️ Your Learning Roadmap")
        roadmap_steps = advice_data['roadmap']
        for i, step in enumerate(roadmap_steps, 1):
            st.markdown(f"**Step {i}:** {step}")
    
    # Course recommendations
    if 'courses' in advice_data:
        st.markdown("### 📚 Recommended Courses & Resources")
        for course in advice_data['courses']:
            st.markdown(f"• {course}")
    
    # Action items
    if 'action_items' in advice_data:
        st.markdown("### 📝 Immediate Action Items")
        for action in advice_data['action_items']:
            st.markdown(f"☐ {action}")

if __name__ == "__main__":
    main()
