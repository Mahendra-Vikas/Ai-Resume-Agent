import requests
import json
from typing import Dict, List, Optional
import re

class CareerAdvisor:
    """
    A class to provide career advice using Gemini 2.5 Pro API.
    """
    
    def __init__(self):
        """Initialize the Career Advisor with Gemini API configuration."""
        self.api_key = "AIzaSyDVEE344Kj_5nZkWWJqYKwLaRahybAXLwk"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def _make_api_request(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Make a request to the Gemini API.
        
        Args:
            prompt (str): The prompt to send to the API
            max_tokens (int): Maximum tokens in the response
            
        Returns:
            str: The API response text
        """
        url = f"{self.base_url}?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": max_tokens,
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            response_data = response.json()
            
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                return response_data['candidates'][0]['content']['parts'][0]['text']
            else:
                return "Unable to generate response. Please try again."
                
        except requests.exceptions.RequestException as e:
            return f"Error communicating with API: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"Error parsing API response: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def get_comprehensive_advice(self, resume_text: str, target_role: str, experience_level: str) -> Dict:
        """
        Get comprehensive career advice including all aspects.
        
        Args:
            resume_text (str): The candidate's resume text
            target_role (str): Target job role
            experience_level (str): Current experience level
            
        Returns:
            Dict: Comprehensive advice data
        """
        # Create comprehensive prompt
        prompt = self._create_comprehensive_prompt(resume_text, target_role, experience_level)
        
        # Get response from Gemini
        response = self._make_api_request(prompt, max_tokens=3000)
        
        # Parse the structured response
        advice_data = self._parse_comprehensive_response(response)
        
        # Add some basic scoring if not provided
        if 'overall_score' not in advice_data:
            advice_data['overall_score'] = self._calculate_basic_score(resume_text, target_role)
        
        return advice_data
    
    def _create_comprehensive_prompt(self, resume_text: str, target_role: str, experience_level: str) -> str:
        """Create a comprehensive prompt for career advice."""
        
        prompt = f"""
You are an expert career advisor and resume consultant. Analyze the following resume for someone targeting a {target_role} position at the {experience_level} level.

RESUME TEXT:
{resume_text[:4000]}  # Limit text to avoid token limits

TARGET ROLE: {target_role}
EXPERIENCE LEVEL: {experience_level}

Please provide a comprehensive analysis in the following structured format. Use exactly these section headers:

OVERALL_SCORE: [Rate from 1-10 how well this resume matches the target role]

READINESS_LEVEL: [Choose one: Ready, Nearly Ready, Developing, Needs Significant Work]

STRENGTHS:
- [List 3-5 key strengths this candidate has for the target role]
- [Focus on specific skills, experiences, or achievements]
- [Be specific and actionable]

IMPROVEMENTS:
- [List 3-5 specific areas that need improvement]
- [Be constructive and specific]
- [Focus on gaps relevant to the target role]

MISSING_SKILLS:
- [List 3-7 technical skills missing for the target role]
- [Focus on skills commonly required for {target_role}]
- [Prioritize the most important ones]

ROADMAP:
- [Provide 4-6 step roadmap to reach the target role]
- [Make steps specific and actionable]
- [Order from most important to least important]

COURSES:
- [Recommend 4-6 specific courses, certifications, or resources]
- [Include both technical and soft skills]
- [Mention specific platforms when helpful]

ACTION_ITEMS:
- [List 3-5 immediate action items they can take this week]
- [Make them very specific and actionable]
- [Focus on quick wins and important gaps]

Please be specific, actionable, and encouraging in your advice. Focus on practical steps they can take to improve their candidacy for the target role.
"""
        
        return prompt
    
    def _parse_comprehensive_response(self, response: str) -> Dict:
        """Parse the structured response from Gemini."""
        
        advice_data = {}
        
        try:
            # Extract overall score
            score_match = re.search(r'OVERALL_SCORE:\s*(\d+)', response, re.IGNORECASE)
            if score_match:
                advice_data['overall_score'] = int(score_match.group(1))
            
            # Extract readiness level
            readiness_match = re.search(r'READINESS_LEVEL:\s*([^\n]+)', response, re.IGNORECASE)
            if readiness_match:
                advice_data['readiness_level'] = readiness_match.group(1).strip()
            
            # Extract sections
            sections = {
                'strengths': r'STRENGTHS:(.*?)(?=IMPROVEMENTS:|$)',
                'improvements': r'IMPROVEMENTS:(.*?)(?=MISSING_SKILLS:|$)',
                'missing_skills': r'MISSING_SKILLS:(.*?)(?=ROADMAP:|$)',
                'roadmap': r'ROADMAP:(.*?)(?=COURSES:|$)',
                'courses': r'COURSES:(.*?)(?=ACTION_ITEMS:|$)',
                'action_items': r'ACTION_ITEMS:(.*?)(?=$)'
            }
            
            for key, pattern in sections.items():
                match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    # Split by bullet points and clean up
                    items = [item.strip() for item in re.split(r'[-•*]\s*', content) if item.strip()]
                    advice_data[key] = items[1:] if items and not items[0] else items  # Remove empty first item
            
        except Exception as e:
            print(f"Error parsing response: {e}")
            # Fallback to basic parsing
            advice_data = self._fallback_parsing(response)
        
        return advice_data
    
    def _fallback_parsing(self, response: str) -> Dict:
        """Fallback parsing if structured parsing fails."""
        
        # Basic fallback - split response into sections
        lines = response.split('\n')
        
        return {
            'overall_score': 7,  # Default score
            'readiness_level': 'Developing',
            'strengths': ["Experience in relevant field", "Good technical background"],
            'improvements': ["Enhance technical skills", "Improve resume formatting"],
            'missing_skills': ["Advanced technical skills", "Industry-specific knowledge"],
            'roadmap': ["Identify skill gaps", "Take relevant courses", "Build portfolio projects", "Apply for positions"],
            'courses': ["Online technical courses", "Industry certifications", "Soft skills training"],
            'action_items': ["Update resume", "Build portfolio", "Apply to relevant positions"]
        }
    
    def _calculate_basic_score(self, resume_text: str, target_role: str) -> int:
        """Calculate a basic score if not provided by API."""
        
        # Simple keyword matching scoring
        role_keywords = {
            'data scientist': ['python', 'machine learning', 'statistics', 'sql', 'data'],
            'software engineer': ['programming', 'software', 'development', 'coding', 'git'],
            'product manager': ['product', 'management', 'strategy', 'stakeholder', 'roadmap'],
            'data analyst': ['analysis', 'excel', 'sql', 'reporting', 'dashboard'],
            'web developer': ['web', 'html', 'css', 'javascript', 'frontend']
        }
        
        resume_lower = resume_text.lower()
        target_lower = target_role.lower()
        
        # Find relevant keywords
        relevant_keywords = []
        for role, keywords in role_keywords.items():
            if any(word in target_lower for word in role.split()):
                relevant_keywords = keywords
                break
        
        # Count matches
        matches = sum(1 for keyword in relevant_keywords if keyword in resume_lower)
        total_keywords = len(relevant_keywords) if relevant_keywords else 5
        
        # Calculate score out of 10
        score = min(10, max(3, int((matches / total_keywords) * 10) + 3))
        
        return score
    
    def get_resume_feedback(self, resume_text: str) -> Dict:
        """
        Get specific feedback on resume quality and formatting.
        
        Args:
            resume_text (str): Resume text to analyze
            
        Returns:
            Dict: Resume feedback and suggestions
        """
        
        prompt = f"""
Analyze this resume and provide specific feedback on its quality, formatting, and content. 
Focus on actionable improvements.

RESUME TEXT:
{resume_text[:3000]}

Please provide feedback in these areas:

FORMATTING:
- [Comment on structure, organization, readability]

CONTENT_QUALITY:
- [Assess the quality of descriptions and achievements]

MISSING_ELEMENTS:
- [What important sections or information is missing]

IMPROVEMENTS:
- [Specific suggestions to make the resume stronger]

Keep feedback constructive and actionable.
"""
        
        response = self._make_api_request(prompt, max_tokens=1500)
        
        # Parse response into categories
        feedback = {
            'formatting': [],
            'content_quality': [],
            'missing_elements': [],
            'improvements': []
        }
        
        # Simple parsing - could be improved
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'FORMATTING:' in line.upper():
                current_section = 'formatting'
            elif 'CONTENT_QUALITY:' in line.upper():
                current_section = 'content_quality'
            elif 'MISSING_ELEMENTS:' in line.upper():
                current_section = 'missing_elements'
            elif 'IMPROVEMENTS:' in line.upper():
                current_section = 'improvements'
            elif line.startswith('-') and current_section:
                feedback[current_section].append(line[1:].strip())
        
        return feedback
    
    def get_skill_recommendations(self, current_skills: List[str], target_role: str) -> Dict:
        """
        Get specific skill recommendations for career growth.
        
        Args:
            current_skills (List[str]): Current skills from resume
            target_role (str): Target job role
            
        Returns:
            Dict: Skill recommendations and learning paths
        """
        
        skills_text = ", ".join(current_skills) if current_skills else "No specific skills identified"
        
        prompt = f"""
Given these current skills: {skills_text}
Target role: {target_role}

Recommend specific skills to develop for this career path:

TECHNICAL_SKILLS:
- [List 5-7 technical skills to develop]
- [Prioritize by importance for the role]

SOFT_SKILLS:
- [List 3-5 soft skills to develop]

LEARNING_PATH:
- [Suggest a 6-month learning plan]
- [Order by priority and dependencies]

CERTIFICATIONS:
- [Recommend relevant certifications]

Be specific about technologies, tools, and methodologies.
"""
        
        response = self._make_api_request(prompt, max_tokens=1200)
        
        # Parse the response
        recommendations = {
            'technical_skills': [],
            'soft_skills': [],
            'learning_path': [],
            'certifications': []
        }
        
        # Simple parsing
        current_section = None
        for line in response.split('\n'):
            line = line.strip()
            if 'TECHNICAL_SKILLS:' in line.upper():
                current_section = 'technical_skills'
            elif 'SOFT_SKILLS:' in line.upper():
                current_section = 'soft_skills'
            elif 'LEARNING_PATH:' in line.upper():
                current_section = 'learning_path'
            elif 'CERTIFICATIONS:' in line.upper():
                current_section = 'certifications'
            elif line.startswith('-') and current_section:
                recommendations[current_section].append(line[1:].strip())
        
        return recommendations
