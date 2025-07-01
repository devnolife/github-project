#!/usr/bin/env python3
"""
Web launcher for GitHub Proposal Generator
"""

import sys
import os
import webbrowser
import time
from threading import Timer

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src'))

def open_browser():
    """Open browser after a short delay."""
    webbrowser.open('http://localhost:5000')

def main():
    """Main web launcher function."""
    print("🚀 Starting GitHub Proposal Generator Web Interface...")
    print("=" * 60)
    
    try:
        # Import and run the Flask app
        from web.app import app
        
        # Open browser after 2 seconds
        timer = Timer(2.0, open_browser)
        timer.start()
        
        print("🌐 Web interface will open in your browser automatically")
        print("📡 Server running at: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Start the Flask development server
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
        
    except ImportError as e:
        print(f"❌ Error importing Flask modules: {e}")
        print("💡 Please install the required dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Web server stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
