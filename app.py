import os
def log_error_to_file(error_message):
    with open(os.path.join(os.path.dirname(__file__), 'error.log'), 'a', encoding='utf-8') as f:
        f.write(error_message + '\n')
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from datetime import datetime, timedelta
import sqlite3
import json
import uuid
from functools import wraps
import threading
import queue
import time

from models.composite_models import CompositeScenarioModel
from utils.data_manager import DataManager, CountryDataManager, ScenarioManager
from utils.visualization_engine import VisualizationEngine
from ai_assistant.chat_assistant import AIAssistant
from ai_config import OPENAI_API_KEY, AI_PROVIDER

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Initialize managers
data_manager = DataManager()
country_manager = CountryDataManager()
scenario_manager = ScenarioManager()
visualization_engine = VisualizationEngine()
composite_model = CompositeScenarioModel()
ai_assistant = AIAssistant()

# Thread-safe queue for long-running analyses
analysis_queue = queue.Queue()
active_analyses = {}

def init_database():
    """Initialize the database with schema and sample data"""
    conn = sqlite3.connect('comprehensive_analysis.db')

    # Read and execute schema
    with open('data/database_schema.sql', 'r') as f:
        schema = f.read()

    conn.executescript(schema)
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('comprehensive_analysis.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    """Main dashboard page"""
    try:
        # Get dashboard statistics
        conn = get_db()

        # Count countries
        total_countries = conn.execute('SELECT COUNT(*) FROM countries').fetchone()[0]

        # Get recent scenarios
        recent_scenarios = conn.execute(
            'SELECT id, config, status, created_at, completed_at FROM scenarios ORDER BY created_at DESC LIMIT 10'
        ).fetchall()

        # Format recent scenarios
        formatted_scenarios = []
        for scenario in recent_scenarios:
            try:
                config = json.loads(scenario['config']) if scenario['config'] else {}
                formatted_scenarios.append({
                    'id': scenario['id'],
                    'name': config.get('name', f"Scenario {scenario['id'][:8]}"),
                    'type': config.get('type', 'unknown'),
                    'status': scenario['status'],
                    'created_at': scenario['created_at'],
                    'completed_at': scenario['completed_at']
                })
            except json.JSONDecodeError:
                continue

        conn.close()

        return render_template('dashboard.html',
                             total_countries=total_countries,
                             total_models=8,
                             recent_scenarios=formatted_scenarios)

    except Exception as e:
        error_msg = f"Dashboard error: {str(e)}"
        app.logger.error(error_msg)
        log_error_to_file(error_msg)
        flash('Error loading dashboard data', 'error')
        return render_template('dashboard.html',
                             total_countries=0,
                             total_models=8,
                             recent_scenarios=[])

@app.route('/scenario-builder')
def scenario_builder():
    """Scenario builder page"""
    try:
        countries = country_manager.get_all_countries()
        environment_types = data_manager.get_environment_types()
        model_types = scenario_manager.get_available_models()

        return render_template('scenario_builder.html',
                             countries=countries,
                             environment_types=environment_types,
                             model_types=model_types)

    except Exception as e:
        error_msg = f"Scenario builder error: {str(e)}"
        app.logger.error(error_msg)
        log_error_to_file(error_msg)
        flash('Error loading scenario builder', 'error')
        return redirect(url_for('dashboard'))

@app.route('/models-overview')
def models_overview():
    """Models overview page"""
    try:
        model_info = scenario_manager.get_detailed_model_info()
        return render_template('models_overview.html', models=model_info)

    except Exception as e:
        error_msg = f"Models overview error: {str(e)}"
        app.logger.error(error_msg)
        log_error_to_file(error_msg)
        flash('Error loading models overview', 'error')
        return redirect(url_for('dashboard'))

@app.route('/built-in-experiments')
def built_in_experiments():
    """Built-in experiments page"""
    try:
        experiments = {
            'india_pakistan_conflict': {
                'name': 'India-Pakistan Conflict Escalation',
                'description': 'Comprehensive analysis of potential conflict between India and Pakistan',
                'complexity': 'Very High',
                'estimated_runtime': '60-90 seconds'
            },
            'china_taiwan_scenario': {
                'name': 'China-Taiwan Military Scenario',
                'description': 'Analysis of potential Chinese military action against Taiwan',
                'complexity': 'Extreme',
                'estimated_runtime': '75-120 seconds'
            }
        }

        return render_template('experiments.html', experiments=experiments)

    except Exception as e:
        error_msg = f"Built-in experiments error: {str(e)}"
        app.logger.error(error_msg)
        log_error_to_file(error_msg)
        flash('Error loading experiments', 'error')
        return redirect(url_for('dashboard'))

@app.route('/ai-assistant')
def ai_assistant_page():
    """AI assistant chat page"""
    try:
        api_configured = OPENAI_API_KEY and OPENAI_API_KEY != "your-openai-api-key-here"
        if not api_configured:
            flash('AI Assistant requires API key configuration in ai_config.py', 'warning')

        return render_template('ai_assistant.html', api_configured=api_configured)

    except Exception as e:
        app.logger.error(f"AI assistant error: {str(e)}")
        flash('Error loading AI assistant', 'error')
        return redirect(url_for('dashboard'))

# API Routes
@app.route('/api/run-scenario', methods=['POST'])
def run_scenario():
    """Start scenario analysis"""
    try:
        scenario_data = request.get_json()

        if not scenario_data:
            return jsonify({'error': 'No scenario data provided'}), 400

        # Generate consistent scenario ID based on configuration
        scenario_config_str = json.dumps(scenario_data, sort_keys=True)
        scenario_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, scenario_config_str))

        # Check if this exact scenario was already run
        conn = get_db()
        existing = conn.execute('SELECT id FROM scenarios WHERE id = ?', (scenario_id,)).fetchone()

        if existing:
            return jsonify({
                'status': 'success',
                'scenario_id': scenario_id,
                'message': 'Using existing analysis results'
            })

        # Create scenario in database
        conn.execute(
            'INSERT INTO scenarios (id, config, status, created_at) VALUES (?, ?, ?, ?)',
            (scenario_id, json.dumps(scenario_data), 'initialized', datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

        # Start analysis in background thread
        analysis_thread = threading.Thread(
            target=run_scenario_analysis,
            args=(scenario_id, scenario_data)
        )
        analysis_thread.daemon = True
        analysis_thread.start()

        # Track active analysis
        active_analyses[scenario_id] = {
            'status': 'running',
            'progress': 0,
            'current_phase': 'initialization',
            'started_at': datetime.now()
        }

        return jsonify({
            'status': 'success',
            'scenario_id': scenario_id,
            'message': 'Analysis started successfully'
        })

    except Exception as e:
        app.logger.error(f"Run scenario error: {str(e)}")
        return jsonify({'error': str(e)}), 500

def run_scenario_analysis(scenario_id, scenario_data):
    """Run scenario analysis in background thread with deterministic results"""
    try:
        # Update status
        update_scenario_status(scenario_id, 'running', 10, 'Starting analysis')

        # Add deterministic configuration to prevent random data generation
        scenario_data['use_deterministic_models'] = True
        scenario_data['random_seed'] = abs(hash(scenario_id)) % (2**31)
        scenario_data['disable_random_variation'] = True

        # Run comprehensive analysis with consistent data
        update_scenario_status(scenario_id, 'running', 30, 'Running models')
        results = composite_model.run_comprehensive_analysis(scenario_data)

        # Generate visualizations
        update_scenario_status(scenario_id, 'running', 80, 'Generating visualizations')
        visualization_data = visualization_engine.generate_comprehensive_visualization(results)
        results['visualization_data'] = visualization_data

        # Save results to database
        update_scenario_status(scenario_id, 'running', 95, 'Saving results')
        conn = get_db()
        conn.execute(
            'UPDATE scenarios SET results = ?, status = ?, completed_at = ? WHERE id = ?',
            (json.dumps(results), 'completed', datetime.now().isoformat(), scenario_id)
        )
        conn.commit()
        conn.close()

        # Complete analysis
        update_scenario_status(scenario_id, 'completed', 100, 'Analysis completed')

        # Remove from active analyses
        if scenario_id in active_analyses:
            del active_analyses[scenario_id]

    except Exception as e:
        app.logger.error(f"Scenario analysis error for {scenario_id}: {str(e)}")
        update_scenario_status(scenario_id, 'error', 0, f'Error: {str(e)}')

        if scenario_id in active_analyses:
            del active_analyses[scenario_id]

def update_scenario_status(scenario_id, status, progress, phase):
    """Update scenario status in database and active analyses"""
    try:
        # Update database
        conn = get_db()
        conn.execute(
            'UPDATE scenarios SET status = ?, updated_at = ? WHERE id = ?',
            (status, datetime.now().isoformat(), scenario_id)
        )
        conn.commit()
        conn.close()

        # Update active analyses
        if scenario_id in active_analyses:
            active_analyses[scenario_id].update({
                'status': status,
                'progress': progress,
                'current_phase': phase,
                'updated_at': datetime.now()
            })

    except Exception as e:
        app.logger.error(f"Status update error for {scenario_id}: {str(e)}")

@app.route('/api/scenario-status/<scenario_id>')
def get_scenario_status(scenario_id):
    """Get scenario status"""
    try:
        # Check active analyses first
        if scenario_id in active_analyses:
            return jsonify(active_analyses[scenario_id])

        # Check database
        conn = get_db()
        result = conn.execute(
            'SELECT status, created_at, updated_at, completed_at FROM scenarios WHERE id = ?',
            (scenario_id,)
        ).fetchone()
        conn.close()

        if result:
            return jsonify({
                'status': result['status'],
                'progress': 100 if result['status'] == 'completed' else 0,
                'current_phase': 'completed' if result['status'] == 'completed' else 'unknown',
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'completed_at': result['completed_at']
            })

        return jsonify({'error': 'Scenario not found'}), 404

    except Exception as e:
        app.logger.error(f"Get scenario status error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/results/<scenario_id>')
def results_viewer(scenario_id):
    """Results viewer page"""
    try:
        # Get scenario results from database
        conn = get_db()
        result = conn.execute(
            'SELECT config, results, status, created_at, completed_at FROM scenarios WHERE id = ?',
            (scenario_id,)
        ).fetchone()
        conn.close()

        if not result:
            flash('Scenario not found', 'error')
            return redirect(url_for('dashboard'))

        if result['status'] != 'completed':
            flash('Scenario analysis not completed', 'warning')
            return redirect(url_for('dashboard'))

        # Parse results
        config = json.loads(result['config']) if result['config'] else {}
        results = json.loads(result['results']) if result['results'] else {}

        return render_template('results.html',
                             scenario_id=scenario_id,
                             config=config,
                             results=results,
                             created_at=result['created_at'],
                             completed_at=result['completed_at'])

    except Exception as e:
        app.logger.error(f"Results viewer error: {str(e)}")
        flash('Error loading results', 'error')
        return redirect(url_for('dashboard'))

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """Chat with AI assistant"""
    try:
        if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
            return jsonify({'error': 'AI Assistant requires API key configuration'}), 400

        data = request.get_json()
        message = data.get('message', '')
        conversation_id = data.get('conversation_id', str(uuid.uuid4()))

        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Process message with AI assistant
        response = ai_assistant.process_message(message, conversation_id)

        return jsonify(response)

    except Exception as e:
        app.logger.error(f"AI chat error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/countries')
def get_countries():
    """Get all countries"""
    try:
        conn = get_db()
        countries = conn.execute('SELECT code, name FROM countries ORDER BY name').fetchall()
        conn.close()

        return jsonify([{'code': c['code'], 'name': c['name']} for c in countries])

    except Exception as e:
        app.logger.error(f"Get countries error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal server error: {str(error)}")
    return render_template('error.html', error='Internal server error'), 500

if __name__ == '__main__':
    # Initialize database on startup
    if not os.path.exists('comprehensive_analysis.db'):
        init_database()
        print("✅ Database initialized successfully")

    print("🚀 Starting Comprehensive Predictive Modeling Platform...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔧 Scenario Builder: http://localhost:5000/scenario-builder")
    print("🤖 AI Assistant: http://localhost:5000/ai-assistant")
    print("⚠️  Configure AI API key in ai_config.py for full functionality")

    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
