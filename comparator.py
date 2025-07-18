from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Tuple
import re

class ResumeComparator:
    """
    A class to compare resumes against job roles using semantic similarity.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the comparator with a SentenceTransformer model.
        
        Args:
            model_name (str): Name of the SentenceTransformer model to use
        """
        try:
            self.model = SentenceTransformer(model_name)
            self.model_loaded = True
        except Exception as e:
            print(f"Error loading SentenceTransformer model: {e}")
            self.model_loaded = False
    
    def calculate_similarity(self, resume_text: str, job_role: str) -> float:
        """
        Calculate similarity score between resume and job role.
        
        Args:
            resume_text (str): Cleaned resume text
            job_role (str): Target job role description
            
        Returns:
            float: Similarity score between 0 and 1
        """
        if not self.model_loaded:
            # Fallback to keyword-based matching if model fails
            return self._keyword_based_similarity(resume_text, job_role)
        
        try:
            # Create embeddings for both texts
            resume_embedding = self.model.encode([resume_text])
            job_embedding = self.model.encode([job_role])
            
            # Calculate cosine similarity
            similarity = np.dot(resume_embedding[0], job_embedding[0]) / (
                np.linalg.norm(resume_embedding[0]) * np.linalg.norm(job_embedding[0])
            )
            
            return float(similarity)
            
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            # Fallback to keyword-based matching
            return self._keyword_based_similarity(resume_text, job_role)
    
    def _keyword_based_similarity(self, resume_text: str, job_role: str) -> float:
        """
        Fallback keyword-based similarity calculation.
        
        Args:
            resume_text (str): Resume text
            job_role (str): Job role
            
        Returns:
            float: Similarity score based on keyword matching
        """
        # Define skill categories and their associated keywords
        skill_categories = {
            'data_scientist': [
                'python', 'r', 'sql', 'machine learning', 'deep learning', 'statistics',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'jupyter',
                'data analysis', 'data visualization', 'matplotlib', 'seaborn', 'plotly',
                'spark', 'hadoop', 'tableau', 'power bi', 'excel', 'regression',
                'classification', 'clustering', 'neural network', 'ai', 'artificial intelligence'
            ],
            'software_engineer': [
                'python', 'java', 'javascript', 'c++', 'c#', 'programming', 'software development',
                'git', 'github', 'api', 'rest', 'database', 'sql', 'html', 'css', 'react',
                'angular', 'vue', 'node.js', 'spring', 'django', 'flask', 'agile', 'scrum'
            ],
            'product_manager': [
                'product management', 'roadmap', 'stakeholder', 'agile', 'scrum', 'analytics',
                'user experience', 'market research', 'competitive analysis', 'kpi', 'metrics',
                'a/b testing', 'product strategy', 'feature', 'requirements', 'jira', 'confluence'
            ],
            'data_analyst': [
                'excel', 'sql', 'tableau', 'power bi', 'data analysis', 'statistics',
                'reporting', 'dashboard', 'visualization', 'python', 'r', 'analytics',
                'kpi', 'metrics', 'business intelligence', 'data mining'
            ],
            'web_developer': [
                'html', 'css', 'javascript', 'react', 'angular', 'vue', 'node.js',
                'web development', 'frontend', 'backend', 'responsive design', 'bootstrap',
                'jquery', 'php', 'mysql', 'mongodb', 'api', 'rest'
            ]
        }
        
        # Determine which category the job role belongs to
        job_role_lower = job_role.lower()
        relevant_keywords = []
        
        for category, keywords in skill_categories.items():
            if any(word in job_role_lower for word in category.split('_')):
                relevant_keywords.extend(keywords)
                break
        
        # If no specific category found, use general tech keywords
        if not relevant_keywords:
            relevant_keywords = [
                'programming', 'software', 'development', 'technology', 'computer',
                'technical', 'analysis', 'problem solving', 'team', 'project'
            ]
        
        # Count keyword matches
        resume_lower = resume_text.lower()
        matches = 0
        total_keywords = len(relevant_keywords)
        
        for keyword in relevant_keywords:
            if keyword in resume_lower:
                matches += 1
        
        # Calculate similarity as percentage of keywords found
        similarity = matches / total_keywords if total_keywords > 0 else 0
        
        # Add bonus for exact job role mention
        if job_role_lower in resume_lower:
            similarity += 0.2
        
        # Cap at 1.0
        return min(similarity, 1.0)
    
    def get_detailed_analysis(self, resume_text: str, job_role: str) -> Dict:
        """
        Get detailed analysis of resume vs job role match.
        
        Args:
            resume_text (str): Resume text
            job_role (str): Job role
            
        Returns:
            Dict: Detailed analysis including strengths and gaps
        """
        overall_score = self.calculate_similarity(resume_text, job_role)
        
        # Extract key sections from resume
        skills = self._extract_skills_from_text(resume_text)
        experience_indicators = self._extract_experience_indicators(resume_text)
        education_indicators = self._extract_education_indicators(resume_text)
        
        # Analyze against job requirements
        required_skills = self._get_required_skills_for_role(job_role)
        missing_skills = [skill for skill in required_skills if skill.lower() not in resume_text.lower()]
        present_skills = [skill for skill in required_skills if skill.lower() in resume_text.lower()]
        
        return {
            'overall_score': overall_score,
            'present_skills': present_skills,
            'missing_skills': missing_skills,
            'identified_skills': skills,
            'experience_indicators': experience_indicators,
            'education_indicators': education_indicators,
            'strengths': self._identify_strengths(resume_text, job_role),
            'recommendations': self._generate_recommendations(missing_skills, job_role)
        }
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from text."""
        # This is a simplified version - you could expand this
        common_skills = [
            'python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'angular',
            'machine learning', 'data analysis', 'statistics', 'excel', 'tableau'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_experience_indicators(self, text: str) -> List[str]:
        """Extract experience indicators from text."""
        indicators = []
        
        # Look for year patterns
        year_pattern = r'\b(\d{4})\s*[-–]\s*(\d{4}|present|current)\b'
        year_matches = re.findall(year_pattern, text, re.IGNORECASE)
        
        if year_matches:
            indicators.append(f"Work history spans {len(year_matches)} positions")
        
        # Look for experience statements
        exp_pattern = r'(\d+)\+?\s*years?\s*(?:of\s*)?experience'
        exp_matches = re.findall(exp_pattern, text, re.IGNORECASE)
        
        if exp_matches:
            indicators.append(f"Mentions {exp_matches[0]} years of experience")
        
        return indicators
    
    def _extract_education_indicators(self, text: str) -> List[str]:
        """Extract education indicators from text."""
        indicators = []
        text_lower = text.lower()
        
        education_levels = ['phd', 'doctorate', 'master', 'bachelor', 'associate']
        
        for level in education_levels:
            if level in text_lower:
                indicators.append(f"Has {level.title()} level education")
                break
        
        return indicators
    
    def _get_required_skills_for_role(self, job_role: str) -> List[str]:
        """Get commonly required skills for a job role."""
        role_skills = {
            'data scientist': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'NumPy'],
            'software engineer': ['Programming', 'Git', 'APIs', 'Databases', 'Testing', 'Debugging'],
            'product manager': ['Product Strategy', 'Analytics', 'Stakeholder Management', 'Agile', 'Roadmapping'],
            'data analyst': ['SQL', 'Excel', 'Tableau', 'Statistics', 'Data Visualization'],
            'web developer': ['HTML', 'CSS', 'JavaScript', 'React', 'APIs', 'Responsive Design']
        }
        
        job_role_lower = job_role.lower()
        
        for role, skills in role_skills.items():
            if role in job_role_lower:
                return skills
        
        # Default skills for unknown roles
        return ['Communication', 'Problem Solving', 'Team Collaboration', 'Technical Skills']
    
    def _identify_strengths(self, resume_text: str, job_role: str) -> List[str]:
        """Identify strengths in the resume for the target role."""
        strengths = []
        text_lower = resume_text.lower()
        
        # Check for leadership indicators
        leadership_keywords = ['lead', 'manage', 'supervise', 'mentor', 'team lead']
        if any(keyword in text_lower for keyword in leadership_keywords):
            strengths.append("Leadership experience demonstrated")
        
        # Check for project management
        pm_keywords = ['project', 'delivered', 'implemented', 'launched']
        if any(keyword in text_lower for keyword in pm_keywords):
            strengths.append("Project management and delivery experience")
        
        # Check for technical depth
        tech_keywords = ['developed', 'built', 'created', 'designed', 'architected']
        if any(keyword in text_lower for keyword in tech_keywords):
            strengths.append("Hands-on technical development experience")
        
        # Check for results/metrics
        results_pattern = r'\d+%|\$\d+|increased|improved|reduced|optimized'
        if re.search(results_pattern, text_lower):
            strengths.append("Quantifiable achievements and results")
        
        return strengths if strengths else ["General relevant experience"]
    
    def _generate_recommendations(self, missing_skills: List[str], job_role: str) -> List[str]:
        """Generate recommendations based on missing skills."""
        if not missing_skills:
            return ["Strong skill alignment with target role"]
        
        recommendations = []
        
        if len(missing_skills) <= 2:
            recommendations.append("Consider gaining experience in: " + ", ".join(missing_skills))
        else:
            recommendations.append("Focus on developing key missing skills, starting with the most critical ones")
        
        recommendations.append("Look for projects or courses to demonstrate these skills")
        recommendations.append("Consider highlighting transferable skills that relate to the target role")
        
        return recommendations
