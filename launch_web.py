#!/usr/bin/env python3
"""
Web Interface Launcher for Rubik's Cube Solver
AeroHack 2025 - Easy startup script
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages for web interface"""
    print("🔧 Installing web interface requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "plotly", "pandas"], 
                      check=True, capture_output=True)
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def launch_web_interface():
    """Launch the Streamlit web interface"""
    print("🚀 Launching Rubik's Cube Solver Web Interface...")
    print("📱 Opening in your default browser...")
    print("🔗 URL: http://localhost:8501")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Launch streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "web_interface.py", 
                       "--server.port", "8501", "--server.headless", "false"], 
                      check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching web interface: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Web interface stopped by user")

def main():
    print("🧩 Rubik's Cube Solver - Web Interface Launcher")
    print("🏆 AeroHack 2025 - Collins Aerospace Challenge")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not os.path.exists("web_interface.py"):
        print("❌ Error: web_interface.py not found!")
        print("💡 Please run this script from the project root directory")
        return
    
    # Install requirements
    if not install_requirements():
        print("💡 Trying to continue anyway...")
    
    print("\n" + "=" * 55)
    launch_web_interface()

if __name__ == "__main__":
    main()
