
import sqlite3
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid
import os
def log_error_to_file(error_message):
    with open(os.path.join(os.path.dirname(__file__), '../error.log'), 'a', encoding='utf-8') as f:
        f.write(error_message + '\n')

class DataManager:
    """Comprehensive data management system for all model data"""

    def __init__(self, db_path: str = 'comprehensive_analysis.db'):
        self.db_path = db_path
        self.experiment_configs = self._load_experiment_configs()
        self.environment_types = self._load_environment_types()
        self.model_info = self._load_model_information()

    def _load_experiment_configs(self):
        """Load built-in experiment configurations"""
        return {
            'india_pakistan_conflict': {
                'name': 'India-Pakistan Conflict Escalation',
                'description': 'Comprehensive analysis of potential conflict between India and Pakistan',
                'config': {
                    'type': 'conflict',
                    'attacker_country': 'Pakistan',
                    'defender_country': 'India',
                    'duration_days': 45,
                    'intensity': 'high',
                    'escalation_level': 'strategic',
                    'nuclear_escalation': True,
                    'population_size': 50000000,
                    'location': 'Kashmir',
                    'countries_involved': ['India', 'Pakistan', 'China', 'USA']
                }
            },
            'china_taiwan_scenario': {
                'name': 'China-Taiwan Military Scenario',
                'description': 'Analysis of potential Chinese military action against Taiwan',
                'config': {
                    'type': 'conflict',
                    'attacker_country': 'China',
                    'defender_country': 'Taiwan',
                    'duration_days': 60,
                    'intensity': 'extreme',
                    'population_size': 23500000,
                    'location': 'Taiwan',
                    'allies_involved': ['USA', 'Japan', 'Australia']
                }
            }
        }

    def _load_environment_types(self):
        """Load environment type definitions"""
        return {
            'village': {
                'name': 'Rural Village',
                'population_range': [500, 5000],
                'characteristics': ['agricultural', 'low_infrastructure', 'high_cohesion']
            },
            'medium_city': {
                'name': 'Medium City', 
                'population_range': [25000, 250000],
                'characteristics': ['urban', 'good_infrastructure', 'diverse_economy']
            },
            'megacity': {
                'name': 'Megacity',
                'population_range': [1000000, 20000000],
                'characteristics': ['mega_metropolitan', 'complex_infrastructure', 'global_economy']
            }
        }

    def _load_model_information(self):
        """Load detailed model information"""
        return {
            'military_analysis': {
                'name': 'Military Conflict Analysis',
                'description': 'Comprehensive analysis of military conflicts',
                'complexity': 'Very High',
                'runtime_seconds': [30, 60]
            },
            'economic_impact': {
                'name': 'Economic Impact Assessment',
                'description': 'Detailed economic warfare analysis',
                'complexity': 'High',
                'runtime_seconds': [20, 45]
            }
        }

    def get_experiment_config(self, experiment_id: str) -> Dict[str, Any]:
        """Get configuration for built-in experiment"""
        try:
            return self.experiment_configs.get(experiment_id, {})
        except Exception as e:
            error_msg = f"DataManager.get_experiment_config error: {str(e)}"
            log_error_to_file(error_msg)
            return {}

    def get_environment_types(self) -> Dict[str, Any]:
        """Get all environment type definitions"""
        try:
            return self.environment_types
        except Exception as e:
            error_msg = f"DataManager.get_environment_types error: {str(e)}"
            log_error_to_file(error_msg)
            return {}

    def get_model_info(self, model_type: str) -> Dict[str, Any]:
        """Get detailed information about specific model"""
        try:
            return self.model_info.get(model_type, {})
        except Exception as e:
            error_msg = f"DataManager.get_model_info error: {str(e)}"
            log_error_to_file(error_msg)
            return {}

    def load_country_data(self):
        """Load country data into database"""
        conn = sqlite3.connect(self.db_path)
        countries_data = [
            ('USA', 'North America', 331900000, 26.9, 10, True),
            ('China', 'East Asia', 1425671352, 17.9, 9, True),
            ('India', 'South Asia', 1428627663, 3.74, 7, True)
        ]
        conn.executemany('INSERT OR REPLACE INTO countries VALUES (?, ?, ?, ?, ?, ?)', countries_data)
        conn.commit()
        conn.close()

class CountryDataManager:
    """Specialized manager for country-specific data"""

    def __init__(self):
        self.countries = {
            'USA': {
                'name': 'United States of America',
                'population': 331900000,
                'gdp_trillion_usd': 26.9,
                'nuclear_weapons': True,
                'allies': ['NATO', 'Japan', 'South Korea']
            },
            'China': {
                'name': "People's Republic of China",
                'population': 1425671352,
                'gdp_trillion_usd': 17.9,
                'nuclear_weapons': True,
                'allies': ['Russia', 'Pakistan']
            },
            'India': {
                'name': 'Republic of India',
                'population': 1428627663,
                'gdp_trillion_usd': 3.74,
                'nuclear_weapons': True,
                'allies': ['USA', 'Russia', 'Israel']
            },
            'Pakistan': {
                'name': 'Islamic Republic of Pakistan',
                'population': 231402117,
                'gdp_trillion_usd': 0.35,
                'nuclear_weapons': True,
                'allies': ['China', 'Saudi Arabia', 'Turkey']
            }
        }

    def get_all_countries(self) -> List[str]:
        """Get list of all available countries"""
        return list(self.countries.keys())

    def get_country_details(self, country_code: str) -> Dict[str, Any]:
        """Get detailed information for specific country"""
        return self.countries.get(country_code, {})

class ScenarioManager:
    """Manager for scenario execution and results storage"""

    def __init__(self, db_path: str = 'comprehensive_analysis.db'):
        self.db_path = db_path
        self.active_scenarios = {}

    def create_scenario(self, scenario_id: str, scenario_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create and initialize new scenario"""
        scenario = {
            'id': scenario_id,
            'config': scenario_config,
            'status': 'initialized',
            'created_at': datetime.now().isoformat(),
            'progress': 0
        }
        self.active_scenarios[scenario_id] = scenario
        return scenario

    def store_results(self, scenario_id: str, results: Dict[str, Any]):
        """Store scenario results"""
        if scenario_id in self.active_scenarios:
            self.active_scenarios[scenario_id]['results'] = results
            self.active_scenarios[scenario_id]['status'] = 'completed'

    def get_scenario(self, scenario_id: str) -> Dict[str, Any]:
        """Get scenario by ID"""
        return self.active_scenarios.get(scenario_id, {})

    def get_recent_scenarios(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent scenarios"""
        scenarios = list(self.active_scenarios.values())[-limit:]
        return scenarios

    def get_available_models(self) -> List[str]:
        """Get list of available model types"""
        return [
            'military_analysis',
            'economic_impact',
            'population_impact',
            'infrastructure_analysis'
        ]

    def get_detailed_model_info(self) -> Dict[str, Any]:
        """Get detailed information about all models"""
        data_manager = DataManager()
        return data_manager.model_info
