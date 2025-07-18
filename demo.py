"""
Demo script to test the resume comparison functionality without Streamlit UI
"""

from resume_utils import extract_resume_text, clean_text, extract_skills, extract_contact_info
from comparator import ResumeComparator
from advisor import CareerAdvisor
import os

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

def demo_resume_comparison():
    """Demo resume comparison functionality"""
    print("📊 DEMO: Resume Comparison")
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
    
    target_job = "Data Scientist"
    print(f"🎯 Target Job Role: {target_job}")
    print()
    
    # Initialize comparator
    comparator = ResumeComparator()
    
    # Compare each resume
    results = []
    for filename, resume_text in resumes.items():
        cleaned_text = clean_text(resume_text)
        score = comparator.calculate_similarity(cleaned_text, target_job)
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

def demo_career_advisor():
    """Demo career advisor functionality"""
    print("🎓 DEMO: Career Advisor")
    print("=" * 50)
    
    # Sample resume for career advice
    user_resume = """
    Alex Thompson
    Junior Data Analyst with 1 year experience
    
    EXPERIENCE
    Data Analyst at Business Corp (2023-2024)
    - Created basic reports using Excel and SQL
    - Assisted with data cleaning and preparation
    - Learned Python basics for data manipulation
    
    EDUCATION
    B.S. in Mathematics (2023)
    
    SKILLS
    - Excel (Advanced)
    - SQL (Intermediate)
    - Python (Beginner)
    - Basic statistics knowledge
    """
    
    target_role = "Senior Data Scientist"
    experience_level = "Entry Level (0-2 years)"
    
    print(f"👤 Current Role: Junior Data Analyst")
    print(f"🎯 Target Role: {target_role}")
    print(f"📊 Experience Level: {experience_level}")
    print()
    
    # Initialize advisor
    advisor = CareerAdvisor()
    
    print("🤖 Getting AI-powered career advice...")
    print("(Note: This is connecting to Gemini 2.5 Pro API)")
    print()
    
    try:
        # Get comprehensive advice
        advice = advisor.get_comprehensive_advice(
            resume_text=clean_text(user_resume),
            target_role=target_role,
            experience_level=experience_level
        )
        
        print("💡 Career Advice Results:")
        print(f"Overall Score: {advice.get('overall_score', 'N/A')}/10")
        print(f"Readiness Level: {advice.get('readiness_level', 'N/A')}")
        print()
        
        if 'strengths' in advice:
            print("✅ Strengths:")
            for strength in advice['strengths'][:3]:  # Show first 3
                print(f"  • {strength}")
            print()
        
        if 'missing_skills' in advice:
            print("🎯 Missing Skills:")
            for skill in advice['missing_skills'][:5]:  # Show first 5
                print(f"  • {skill}")
            print()
        
        if 'action_items' in advice:
            print("📝 Immediate Action Items:")
            for action in advice['action_items'][:3]:  # Show first 3
                print(f"  • {action}")
            print()
            
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        print("This might be due to API limits or network issues.")
        print("In a real application, you would see personalized career advice here.")

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
    
    demo_career_advisor()
    print("\n" + "=" * 60)
    
    print("✨ Demo completed! The full application is available at:")
    print("   http://localhost:8501")
    print()
    print("🎯 Key Features Demonstrated:")
    print("   ✓ PDF text extraction and cleaning")
    print("   ✓ Contact information and skills extraction")
    print("   ✓ Semantic similarity comparison")
    print("   ✓ AI-powered career advice (Gemini 2.5 Pro)")
    print("   ✓ Interactive Streamlit web interface")

if __name__ == "__main__":
    main()
