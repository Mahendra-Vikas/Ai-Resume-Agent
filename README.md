# Multi-Resume Comparator & Career Resume Advisor

A comprehensive AI-powered Streamlit web application that helps compare multiple resumes against target job roles and provides personalized career advice using advanced semantic analysis and Gemini 2.5 Pro API.

## 🎯 Features

### Resume Comparison Mode
- **Multi-Resume Upload**: Upload multiple PDF resumes simultaneously
- **Semantic Similarity Analysis**: Uses SentenceTransformers for intelligent resume-job matching
- **Interactive Rankings**: Visual rankings with match scores and detailed analysis
- **Downloadable Reports**: Export comparison results as CSV
- **Advanced Visualization**: Interactive charts and metrics

### Personal Career Advisor Mode
- **AI-Powered Resume Analysis**: Comprehensive resume evaluation using Gemini 2.5 Pro
- **Personalized Roadmap**: Step-by-step career development plan
- **Skill Gap Analysis**: Identifies missing technical and soft skills
- **Course Recommendations**: Specific learning resources and certifications
- **Actionable Feedback**: Immediate steps to improve your candidacy

## 🚀 Technology Stack

- **Frontend**: Streamlit with custom CSS styling
- **PDF Processing**: pdfplumber for accurate text extraction
- **AI/ML**: 
  - SentenceTransformers for semantic similarity
  - Gemini 2.5 Pro API for career advice
- **Visualization**: Plotly for interactive charts
- **Data Processing**: Pandas, NumPy

## 📁 Project Structure

```
ResumeAgent/
├── app.py                 # Main Streamlit application
├── resume_utils.py        # PDF processing and text extraction
├── comparator.py          # Resume comparison and ranking logic
├── advisor.py             # Gemini API integration for career advice
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## 🛠️ Installation & Setup

1. **Clone or download the project**
   ```bash
   cd ResumeAgent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the app**
   - Open your browser and go to `http://localhost:8501`

## 📖 How to Use

### Resume Comparison Mode

1. **Select "Resume Comparison"** from the sidebar
2. **Enter target job role** (e.g., "Data Scientist", "Software Engineer")
3. **Upload multiple PDF resumes** using the file uploader
4. **Click "Analyze Resumes"** to start the comparison
5. **View results**:
   - Overall metrics and summary
   - Interactive visualization of match scores
   - Detailed rankings with resume previews
   - Download CSV report

### Personal Career Advisor Mode

1. **Select "Personal Career Advisor"** from the sidebar
2. **Enter your target role** and experience level
3. **Upload your resume** (PDF format)
4. **Click "Get Career Advice"** for analysis
5. **Review comprehensive feedback**:
   - Resume strength assessment
   - Identified strengths and improvement areas
   - Missing skills analysis
   - Personalized learning roadmap
   - Course and certification recommendations
   - Immediate action items

## 🔧 Configuration

### API Configuration
The application uses Gemini 2.5 Pro API for advanced career advice. The API key is configured in `advisor.py`:

```python
self.api_key = "AIzaSyDVEE344Kj_5nZkWWJqYKwLaRahybAXLwk"
self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent"
```

### Model Configuration
SentenceTransformer model can be changed in `comparator.py`:

```python
def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
```

## 🎨 Features Detail

### Advanced Resume Processing
- **Smart Text Extraction**: Handles various PDF formats and layouts
- **Text Cleaning**: Removes artifacts and normalizes content
- **Contact Information Extraction**: Automatically identifies emails, phones, LinkedIn
- **Skills Recognition**: Identifies technical and soft skills
- **Experience Analysis**: Estimates years of experience and role progression

### Intelligent Comparison
- **Semantic Understanding**: Goes beyond keyword matching
- **Role-Specific Analysis**: Tailored evaluation for different job categories
- **Fallback Mechanisms**: Keyword-based matching when AI models unavailable
- **Detailed Scoring**: Multiple factors contribute to final match score

### AI-Powered Career Advice
- **Comprehensive Analysis**: 10+ aspects of career readiness
- **Structured Feedback**: Organized recommendations and action items
- **Personalized Roadmaps**: Step-by-step career development plans
- **Industry-Specific Advice**: Tailored to target role requirements

## 🔍 Example Use Cases

1. **Hiring Managers**: Quickly rank candidate resumes against job requirements
2. **Recruiters**: Efficiently screen large volumes of applications
3. **Job Seekers**: Get personalized feedback on resume strength
4. **Career Counselors**: Provide data-driven career guidance
5. **HR Teams**: Standardize resume evaluation processes

## 🚧 Troubleshooting

### Common Issues

1. **PDF Reading Errors**
   - Ensure PDFs are text-based (not scanned images)
   - Try re-saving PDFs if extraction fails

2. **Model Loading Issues**
   - First run may take time to download SentenceTransformer models
   - Ensure stable internet connection

3. **API Errors**
   - Check Gemini API key validity
   - Verify API quota and usage limits

## 🔮 Future Enhancements

- **Multi-language Support**: Resume analysis in multiple languages
- **Advanced Visualizations**: More detailed comparison charts
- **Interview Preparation**: AI-generated interview questions
- **Resume Builder**: AI-assisted resume creation
- **Company-Specific Analysis**: Tailored advice for specific companies
- **Batch Processing**: Command-line interface for large-scale processing

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Support

For questions or support, please create an issue in the project repository.

---

**Built with ❤️ using Streamlit, SentenceTransformers, and Gemini 2.5 Pro API**
