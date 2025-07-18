# 🎯 HOW TO RUN THE RESUME COMPARATOR PROJECT

## ✅ **CURRENT STATUS: RUNNING SUCCESSFULLY!**
Your application is live at: **http://localhost:8502**

---

## 🚀 **QUICK START (3 Methods)**

### **Method 1: Easy Launcher (Recommended)**
```bash
python start.py
```
✅ **Currently Running** - This automatically checks dependencies and starts the app!

### **Method 2: Direct Streamlit**
```bash
streamlit run app.py
```

### **Method 3: Alternative Port**
```bash
streamlit run app.py --server.port 8503
```

---

## 🌐 **ACCESSING THE APPLICATION**

**Primary URL**: http://localhost:8502
**Alternative**: http://localhost:8501 (if port 8502 is busy)

### **What You'll See:**
1. **Beautiful web interface** with sidebar navigation
2. **Two main modes** to choose from:
   - 📊 **Resume Comparison** 
   - 🎓 **Personal Career Advisor**

---

## 📊 **HOW TO USE: RESUME COMPARISON MODE**

### **Step 1:** Select Mode
- Choose "Resume Comparison" from the sidebar

### **Step 2:** Enter Job Role
- Type target job (e.g., "Data Scientist", "Software Engineer")

### **Step 3:** Upload Resumes
- Click "Choose PDF files"
- Select multiple resume PDFs
- Support for various PDF formats

### **Step 4:** Analyze
- Click "🔍 Analyze Resumes"
- Wait for processing (10-30 seconds)

### **Step 5:** View Results
- See ranked resumes with match scores
- Interactive charts and visualizations
- Detailed breakdown for each resume
- Download CSV report

---

## 🎓 **HOW TO USE: CAREER ADVISOR MODE**

### **Step 1:** Select Mode
- Choose "Personal Career Advisor" from sidebar

### **Step 2:** Enter Details
- Target job role
- Current experience level
- Upload your resume (PDF)

### **Step 3:** Get Advice
- Click "🚀 Get Career Advice"
- AI analyzes your resume vs target role

### **Step 4:** Review Feedback
- Resume strength score (1-10)
- Personalized improvement suggestions
- Missing skills identification
- Learning roadmap
- Course recommendations
- Immediate action items

---

## 🛠 **TESTING THE APPLICATION**

### **Demo with Sample Data**
```bash
python simple_demo.py
```
This runs a demonstration with sample resumes and shows all features.

### **Test AI Integration**
```bash
python test_api.py
```
This tests the Gemini API connectivity for AI features.

---

## 📁 **SAMPLE WORKFLOW**

1. **Create Test Resumes**: 
   - Use any PDF resume files you have
   - Or create simple text PDFs for testing

2. **Test Resume Comparison**:
   - Upload 2-3 different resumes
   - Try job roles like "Data Scientist", "Web Developer"
   - See how scores differ

3. **Test Career Advisor**:
   - Upload your own resume
   - Set a target role you're interested in
   - Get personalized feedback

---

## 🔧 **TROUBLESHOOTING**

### **If App Won't Start**
```bash
# Check dependencies
pip install -r requirements.txt

# Try alternative port
streamlit run app.py --server.port 8504
```

### **If PDF Upload Fails**
- Ensure PDFs contain text (not just images)
- Try different PDF files
- Check file size (should be < 10MB)

### **If AI Features Don't Work**
- App still works with keyword-based comparison
- All core features remain functional
- AI provides enhanced recommendations when available

### **Port Conflicts**
If localhost:8502 is busy:
- App will automatically try 8501, 8503, etc.
- Check terminal output for actual URL

---

## 📊 **WHAT TO EXPECT**

### **Resume Comparison Results**
- **Match scores** (0-100%)
- **Visual rankings** with charts
- **Detailed breakdowns** per resume
- **Export functionality** (CSV download)

### **Career Advisor Results**
- **Overall assessment** (1-10 scale)
- **Strengths identification**
- **Skill gap analysis**
- **Personalized roadmap**
- **Actionable recommendations**

---

## 🎯 **NEXT STEPS**

1. **Try Different Job Roles**:
   - Data Scientist
   - Software Engineer  
   - Product Manager
   - Web Developer

2. **Upload Various Resumes**:
   - Different experience levels
   - Different industries
   - Compare results

3. **Explore All Features**:
   - Download CSV reports
   - View interactive charts
   - Get career advice
   - Test with your own resume

---

## 🆘 **NEED HELP?**

### **Check Status**
- Terminal should show: "You can now view your Streamlit app..."
- Browser should load the interface

### **Common Issues**
- **Port busy**: Try different URL in terminal output
- **Dependencies**: Run `pip install -r requirements.txt`
- **PDF issues**: Use text-based PDFs

### **Quick Reset**
```bash
# Stop current app (Ctrl+C in terminal)
# Restart with:
python start.py
```

---

**🎉 ENJOY YOUR RESUME COMPARATOR & CAREER ADVISOR!**

The application is designed to be intuitive and user-friendly. Start with uploading a few sample resumes to see the comparison in action!
