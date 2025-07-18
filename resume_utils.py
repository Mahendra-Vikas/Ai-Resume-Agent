import pdfplumber
import re
from typing import Optional

def extract_resume_text(pdf_path: str) -> str:
    """
    Extract text content from a PDF resume file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content
    """
    try:
        text_content = ""
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract text from the page
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
        
        return text_content.strip()
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def clean_text(text: str) -> str:
    """
    Clean and preprocess extracted resume text.
    
    Args:
        text (str): Raw extracted text
        
    Returns:
        str: Cleaned and processed text
    """
    if not text:
        return ""
    
    # Remove extra whitespaces and normalize
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep important punctuation
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]]', ' ', text)
    
    # Remove multiple consecutive punctuation marks
    text = re.sub(r'[\.]{2,}', '.', text)
    text = re.sub(r'[\-]{2,}', '-', text)
    
    # Remove extra spaces around punctuation
    text = re.sub(r'\s+([\.,:;!?])', r'\1', text)
    text = re.sub(r'([\.,:;!?])\s+', r'\1 ', text)
    
    # Convert to lowercase for better processing
    text = text.lower()
    
    # Remove common PDF artifacts
    text = re.sub(r'\bpage \d+\b', '', text)
    text = re.sub(r'\b\d+/\d+/\d+\b', '', text)  # Remove dates in format mm/dd/yyyy
    
    # Final cleanup
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_contact_info(text: str) -> dict:
    """
    Extract contact information from resume text.
    
    Args:
        text (str): Resume text
        
    Returns:
        dict: Extracted contact information
    """
    contact_info = {
        'email': None,
        'phone': None,
        'linkedin': None,
        'github': None
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        contact_info['email'] = emails[0]
    
    # Phone pattern (various formats)
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\+\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            contact_info['phone'] = phones[0]
            break
    
    # LinkedIn pattern
    linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
    linkedin_matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
    if linkedin_matches:
        contact_info['linkedin'] = linkedin_matches[0]
    
    # GitHub pattern
    github_pattern = r'github\.com/[\w\-]+'
    github_matches = re.findall(github_pattern, text, re.IGNORECASE)
    if github_matches:
        contact_info['github'] = github_matches[0]
    
    return contact_info

def extract_skills(text: str) -> list:
    """
    Extract technical skills from resume text.
    
    Args:
        text (str): Resume text
        
    Returns:
        list: List of identified skills
    """
    # Common technical skills (this is a basic implementation)
    # In production, you might want a more comprehensive skills database
    
    technical_skills = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust', 'swift',
        'kotlin', 'scala', 'r', 'matlab', 'sql', 'php', 'perl', 'bash', 'powershell',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
        'spring', 'laravel', 'bootstrap', 'jquery', 'webpack', 'sass', 'less',
        
        # Databases
        'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'oracle',
        'sqlite', 'dynamodb', 'firebase', 'neo4j',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
        'circleci', 'terraform', 'ansible', 'puppet', 'chef', 'vagrant',
        
        # Data Science & ML
        'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'matplotlib',
        'seaborn', 'plotly', 'jupyter', 'spark', 'hadoop', 'tableau', 'power bi',
        
        # Mobile Development
        'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic',
        
        # Other Technologies
        'linux', 'unix', 'windows', 'mac', 'api', 'rest', 'graphql', 'microservices',
        'agile', 'scrum', 'kanban', 'jira', 'confluence', 'slack'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in technical_skills:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill.title())
    
    return list(set(found_skills))  # Remove duplicates

def extract_education(text: str) -> list:
    """
    Extract education information from resume text.
    
    Args:
        text (str): Resume text
        
    Returns:
        list: List of education entries
    """
    education_keywords = [
        'bachelor', 'master', 'phd', 'doctorate', 'degree', 'university', 'college',
        'institute', 'school', 'education', 'graduated', 'gpa'
    ]
    
    education_entries = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in education_keywords):
            # Try to capture the education entry and potentially the next line
            entry = line.strip()
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if len(next_line) < 100:  # Likely part of the same entry
                    entry += " " + next_line
            
            if len(entry) > 10:  # Filter out very short entries
                education_entries.append(entry)
    
    return education_entries[:3]  # Return up to 3 entries

def extract_experience_years(text: str) -> Optional[int]:
    """
    Try to extract years of experience from resume text.
    
    Args:
        text (str): Resume text
        
    Returns:
        Optional[int]: Estimated years of experience
    """
    # Look for patterns like "5 years experience", "3+ years", etc.
    experience_patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'(\d+)\+?\s*years?\s*in\s*\w+',
        r'experience\s*:\s*(\d+)\+?\s*years?'
    ]
    
    for pattern in experience_patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            return int(matches[0])
    
    # Try to estimate based on date ranges in work experience
    # This is a simple heuristic and may not be very accurate
    year_pattern = r'\b(19|20)\d{2}\b'
    years = re.findall(year_pattern, text)
    
    if len(years) >= 4:  # Need at least 2 date ranges
        years = [int(year) for year in years]
        years.sort()
        # Estimate experience as difference between latest and earliest year
        estimated_experience = years[-1] - years[0]
        return min(estimated_experience, 50)  # Cap at 50 years
    
    return None
