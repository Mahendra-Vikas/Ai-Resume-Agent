# 🚀 Quick Start Guide

## Running the Application

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Open in browser**:
   ```
   http://localhost:8501
   ```

## How to Use

### 📊 Resume Comparison Mode
1. Select "Resume Comparison" in the sidebar
2. Enter target job role (e.g., "Data Scientist")
3. Upload multiple PDF resumes
4. Click "Analyze Resumes"
5. View ranked results and download CSV report

### 🎓 Personal Career Advisor Mode  
1. Select "Personal Career Advisor" in the sidebar
2. Enter your target job role
3. Select your experience level
4. Upload your resume (PDF)
5. Click "Get Career Advice"
6. Review personalized recommendations

## Demo Scripts

- **`simple_demo.py`** - Run core functionality demo
- **`test_api.py`** - Test AI API connectivity
- **`demo.py`** - Full feature demonstration

## Features Available

✅ **Working Features**:
- PDF text extraction and cleaning
- Contact information extraction
- Technical skills identification
- Resume comparison (keyword + semantic)
- Interactive web interface
- Visual charts and rankings
- CSV export functionality
- Responsive design

🤖 **AI Features**:
- Career advice (when API is available)
- Personalized recommendations
- Learning roadmaps
- Skill gap analysis

## Technology Stack

- **Frontend**: Streamlit with custom CSS
- **PDF Processing**: pdfplumber
- **AI/ML**: SentenceTransformers, Gemini 2.5 Pro API
- **Visualization**: Plotly
- **Data**: Pandas, NumPy

## File Structure

```
ResumeAgent/
├── app.py                 # Main Streamlit app
├── resume_utils.py        # PDF processing
├── comparator.py          # Resume comparison
├── advisor.py             # AI career advisor
├── requirements.txt       # Dependencies
├── README.md             # Documentation
├── simple_demo.py        # Demo script
└── test_api.py           # API testing
```

## Troubleshooting

**PDF Reading Issues**:
- Ensure PDFs contain extractable text (not scanned images)
- Try different PDF files if extraction fails

**API Rate Limits**:
- The app gracefully degrades to keyword-based comparison
- All core features work without AI API

**Dependencies**:
- Run `pip install -r requirements.txt` if packages are missing
- Python 3.8+ recommended

## Next Steps

1. **Add Sample PDFs** - Test with real resume files
2. **Customize Skills Database** - Add industry-specific skills
3. **Enhance UI** - Add more visualization options
4. **Deploy** - Host on Streamlit Cloud or Heroku
5. **Extend API** - Add more AI providers for redundancy

---
**Built with ❤️ using Streamlit, SentenceTransformers, and Gemini 2.5 Pro API**
