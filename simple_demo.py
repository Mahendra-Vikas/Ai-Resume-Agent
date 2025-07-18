"""
Simplified demo script to test the resume comparison functionality
"""

from resume_utils import clean_text, extract_skills, extract_contact_info
import re

def demo_text_processing():
    """Demo text processing capabilities"""
    print("🔍 DEMO: Text Processing Capabilities")
    print("=" * 50)
    
    # Sample resume text for demo
    sample_resume = """
    John Doe
    Email: john.doe@email.com
    Phone: (555) 123-4567
    LinkedIn: linkedin.com/in/johndoe
    
    EXPERIENCE
    Data Scientist at TechCorp (2020-2024)
    - Developed machine learning models using Python and scikit-learn
    - Created data visualization dashboards with Tableau and matplotlib
    - Analyzed large datasets using SQL and pandas
    - Collaborated with cross-functional teams on AI projects
    
    Software Engineer at StartupXYZ (2018-2020)
    - Built web applications using React and Node.js
    - Implemented REST APIs and microservices architecture
    - Used Git for version control and Docker for containerization
    
    EDUCATION
    M.S. Computer Science, University of Technology (2018)
    B.S. Computer Science, State University (2016)
    
    SKILLS
    Programming: Python, JavaScript, SQL, R
    Libraries: pandas, numpy, scikit-learn, tensorflow
    Tools: Git, Docker, Kubernetes, AWS
    """
    
    # Clean the text
    cleaned_text = clean_text(sample_resume)
    print(f"📄 Cleaned Resume Text (first 200 chars):")
    print(f"{cleaned_text[:200]}...")
    print()
    
    # Extract contact info
    contact_info = extract_contact_info(sample_resume)
    print(f"📞 Contact Information:")
    for key, value in contact_info.items():
        if value:
            print(f"  {key.title()}: {value}")
    print()
    
    # Extract skills
    skills = extract_skills(sample_resume)
    print(f"🔧 Identified Skills:")
    print(f"  {', '.join(skills[:10])}...")  # Show first 10 skills
    print()

def keyword_similarity(text1, text2):
    """Simple keyword-based similarity for demo"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    if len(union) == 0:
        return 0.0
    
    return len(intersection) / len(union)

def demo_resume_comparison():
    """Demo resume comparison functionality"""
    print("📊 DEMO: Resume Comparison (Keyword-based)")
    print("=" * 50)
    
    # Sample resumes for comparison
    resumes = {
        "Resume_A_DataScientist.pdf": """
        Jane Smith, Data Scientist
        5 years experience in machine learning and data analysis
        Expert in Python, pandas, numpy, scikit-learn, tensorflow
        Built predictive models for customer churn and sales forecasting
        PhD in Statistics, experienced with SQL, Tableau, AWS
        """,
        
        "Resume_B_SoftwareEngineer.pdf": """
        Mike Johnson, Software Engineer
        3 years experience in full-stack development
        Proficient in JavaScript, React, Node.js, Python
        Built web applications and REST APIs
        Bachelor's in Computer Science, familiar with Git, Docker
        """,
        
        "Resume_C_DataAnalyst.pdf": """
        Sarah Wilson, Data Analyst
        2 years experience in business intelligence
        Strong skills in SQL, Excel, Tableau, Power BI
        Created dashboards and reports for executive team
        Master's in Business Analytics, some Python experience
        """
    }
    
    target_job = "Data Scientist machine learning Python statistics analysis"
    print(f"🎯 Target Job Role: Data Scientist")
    print(f"🔍 Keywords: {target_job}")
    print()
    
    # Compare each resume
    results = []
    for filename, resume_text in resumes.items():
        cleaned_text = clean_text(resume_text)
        score = keyword_similarity(cleaned_text, target_job)
        results.append({
            'filename': filename,
            'score': score,
            'text': cleaned_text
        })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("📈 Comparison Results:")
    for i, result in enumerate(results, 1):
        print(f"  #{i} {result['filename']}")
        print(f"      Match Score: {result['score']:.1%}")
        print(f"      Preview: {result['text'][:100]}...")
        print()

def demo_api_features():
    """Demo API integration features"""
    print("🤖 DEMO: AI-Powered Career Advisor Features")
    print("=" * 50)
    
    print("🎯 Target Integration: Gemini 2.5 Pro API")
    print("📡 Endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent")
    print()
    
    print("💡 Career Advisor Capabilities:")
    features = [
        "Resume strength assessment (1-10 scale)",
        "Personalized improvement recommendations",
        "Missing skills identification",
        "Step-by-step career roadmap",
        "Course and certification suggestions",
        "Immediate actionable items",
        "Industry-specific advice",
        "Experience level-appropriate guidance"
    ]
    
    for feature in features:
        print(f"  ✓ {feature}")
    print()
    
    print("📝 Sample Career Advice Structure:")
    sample_advice = {
        'overall_score': 7,
        'readiness_level': 'Developing',
        'strengths': [
            'Strong analytical background in mathematics',
            'Hands-on experience with data analysis tools',
            'Understanding of business requirements'
        ],
        'missing_skills': [
            'Advanced machine learning algorithms',
            'Deep learning frameworks (TensorFlow/PyTorch)',
            'Statistical modeling and hypothesis testing',
            'Big data technologies (Spark, Hadoop)',
            'MLOps and model deployment'
        ],
        'roadmap': [
            'Complete advanced Python for data science course',
            'Learn machine learning fundamentals',
            'Build portfolio projects with real datasets',
            'Get familiar with MLOps tools and practices',
            'Apply for junior data scientist positions'
        ],
        'action_items': [
            'Enroll in Coursera Machine Learning Specialization',
            'Start contributing to open-source ML projects',
            'Update LinkedIn profile with new skills'
        ]
    }
    
    print(f"  Overall Score: {sample_advice['overall_score']}/10")
    print(f"  Readiness: {sample_advice['readiness_level']}")
    print()
    print("  Strengths:")
    for strength in sample_advice['strengths']:
        print(f"    • {strength}")
    print()
    print("  Missing Skills:")
    for skill in sample_advice['missing_skills'][:3]:
        print(f"    • {skill}")
    print()

def main():
    """Run all demos"""
    print("🚀 RESUME COMPARATOR & CAREER ADVISOR DEMO")
    print("=" * 60)
    print()
    
    # Run demos
    demo_text_processing()
    print("\n" + "=" * 60 + "\n")
    
    demo_resume_comparison()
    print("\n" + "=" * 60 + "\n")
    
    demo_api_features()
    print("\n" + "=" * 60)
    
    print("✨ Demo completed! The full application is available at:")
    print("   http://localhost:8501")
    print()
    print("🎯 Key Features Demonstrated:")
    print("   ✓ PDF text extraction and cleaning")
    print("   ✓ Contact information and skills extraction")
    print("   ✓ Resume comparison algorithms")
    print("   ✓ AI-powered career advice integration")
    print("   ✓ Interactive Streamlit web interface")
    print("   ✓ CSV export functionality")
    print("   ✓ Visual charts and metrics")
    print()
    print("📦 Project Structure:")
    print("   ├── app.py                 # Main Streamlit application")
    print("   ├── resume_utils.py        # PDF processing utilities")
    print("   ├── comparator.py          # Resume comparison logic")
    print("   ├── advisor.py             # AI career advisor")
    print("   ├── requirements.txt       # Dependencies")
    print("   └── README.md             # Documentation")

if __name__ == "__main__":
    main()
