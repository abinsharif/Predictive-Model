# Create the complete project zip file
import zipfile
import os

# List all files to include in the zip
files_to_zip = [
    # Root files
    ('app.py', 'app.py'),
    ('ai_config.py', 'ai_config.py'),
    ('config.py', 'config.py'),
    ('init_database.py', 'init_database.py'), 
    ('requirements.txt', 'requirements.txt'),
    ('start.py', 'start.py'),
    ('README.md', 'README.md'),
    
    # Models
    ('models/military_models.py', 'models/military_models.py'),
    ('models/economic_models.py', 'models/economic_models.py'),
    ('models/social_models.py', 'models/social_models.py'),
    ('models/environmental_models.py', 'models/environmental_models.py'),
    ('models/composite_models.py', 'models/composite_models.py'),
    
    # AI Assistant
    ('ai_assistant/chat_assistant.py', 'ai_assistant/chat_assistant.py'),
    
    # Utils
    ('utils/data_manager.py', 'utils/data_manager.py'),
    ('utils/visualization_engine.py', 'utils/visualization_engine.py'),
    
    # Templates
    ('templates/base.html', 'templates/base.html'),
    ('templates/dashboard.html', 'templates/dashboard.html'),
    ('templates/scenario_builder.html', 'templates/scenario_builder.html'),
    ('templates/ai_assistant.html', 'templates/ai_assistant.html'),
    ('templates/results.html', 'templates/results.html'),
    ('templates/error.html', 'templates/error.html'),
    
    # Static files
    ('static/css/main.css', 'static/css/main.css'),
    ('static/js/main.js', 'static/js/main.js'),
    ('static/js/scenario_builder.js', 'static/js/scenario_builder.js'),
    
    # Data
    ('data/database_schema.sql', 'data/database_schema.sql')
]

# Create the zip file
zip_filename = 'comprehensive-predictive-modeling-platform.zip'
print(f"📦 Creating comprehensive project archive: {zip_filename}")

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for source_file, zip_path in files_to_zip:
        if os.path.exists(source_file):
            zipf.write(source_file, zip_path)
            print(f"   ✅ Added: {zip_path}")
        else:
            print(f"   ⚠️  Missing: {source_file}")

print(f"\n🎉 Successfully created: {zip_filename}")
print(f"📊 Archive contains {len(files_to_zip)} files")

# Get file size
file_size = os.path.getsize(zip_filename)
print(f"💾 Archive size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")


# Display final instructions
print("\n" + "="*60)
print("🚀 COMPREHENSIVE PREDICTIVE MODELING PLATFORM")
print("="*60)
print("\n📋 INSTALLATION INSTRUCTIONS:")
print("1. Extract: comprehensive-predictive-modeling-platform.zip")
print("2. Configure API: Edit ai_config.py (line 4)")
print("3. Install: pip install -r requirements.txt")
print("4. Run: python start.py")
print("5. Open: http://localhost:5000")

print("\n🔑 API CONFIGURATION:")
print("📁 File: ai_config.py")
print("📍 Location: Root directory, line 4")
print("✏️  Change: OPENAI_API_KEY = 'your-openai-api-key-here'")

print("\n🎯 KEY FEATURES:")
print("• Advanced Military Analysis (missile trajectories, casualties)")
print("• Economic Impact Modeling (GDP effects, supply chains)")
print("• Population Dynamics (displacement, psychological impact)")
print("• Infrastructure Analysis (cascade failures, recovery)")
print("• AI Assistant (natural language scenario building)")
print("• 3D Visualizations (abstract geometric representations)")
print("• Built-in Experiments (India-Pakistan, China-Taiwan, etc.)")
print("• SQLite Database (persistent, no random data generation)")

print("\n📊 TECHNICAL SPECIFICATIONS:")
print("• Deterministic Models (consistent results)")
print("• SQLite Database (all data saved)")
print("• User-Friendly Interface (responsive design)")
print("• No Random Data Generation (realistic, consistent models)")
print("• Thread-Safe Analysis (background processing)")
print("• Comprehensive Logging (full audit trail)")

print("\n⚡ QUICK START:")
print("1. Extract zip file")
print("2. python start.py")
print("3. Open browser to http://localhost:5000")

print("\n✨ The platform is now complete and ready for deployment!")
#print(f"📦 Download: {zip_filename}")
print("📖 Full documentation included in README.md")