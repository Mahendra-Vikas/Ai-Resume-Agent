"""
🚀 Resume Comparator & Career Advisor Launcher
Simple script to start the application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pdfplumber', 
        'sentence_transformers',
        'requests',
        'pandas',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    return missing_packages

def main():
    print("🚀 RESUME COMPARATOR & CAREER ADVISOR")
    print("=" * 50)
    print()
    
    print("📦 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("💡 Run: pip install -r requirements.txt")
        return
    
    print("\n✅ All dependencies found!")
    print()
    print("🌐 Starting Streamlit application...")
    print("📍 This will open in your web browser at: http://localhost:8501")
    print()
    print("🔄 Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Start Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Try running manually: streamlit run app.py")

if __name__ == "__main__":
    main()
