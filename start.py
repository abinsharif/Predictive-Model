#!/usr/bin/env python3
"""
Quick startup script for Comprehensive Predictive Modeling Platform
"""

import os
import sys
import subprocess

def main():
    print("🚀 Comprehensive Predictive Modeling Platform - Quick Start")
    print("=" * 60)

    # Check if database exists
    if not os.path.exists('comprehensive_analysis.db'):
        print("📊 Initializing database...")
        subprocess.run([sys.executable, 'init_database.py'])

    # Start the application
    print("🌐 Starting web application...")
    print("📍 Open your browser to: http://localhost:5000")
    print("⚠️  Configure API key in ai_config.py for AI features")
    print("-" * 60)

    subprocess.run([sys.executable, 'app.py'])

if __name__ == '__main__':
    main()
