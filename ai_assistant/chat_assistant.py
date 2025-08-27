
import json
import re
import numpy as np
from datetime import datetime, timedelta
import requests
import os
from typing import Dict, List, Any, Optional

class AIAssistant:
    """Advanced AI Assistant for natural language scenario building and analysis"""

    def __init__(self):
        self.openai_api_key = os.environ.get('OPENAI_API_KEY', '')
        self.conversation_history = {}
        self.scenario_templates = self._load_scenario_templates()
        self.country_data = self._load_country_data()
        self.model_capabilities = self._load_model_capabilities()

    def _load_scenario_templates(self):
        """Load scenario templates for different types of analysis"""
        return {
            'military_conflict': {
                'required_fields': ['attacker_country', 'defender_country', 'intensity'],
                'optional_fields': ['duration_days', 'escalation_level', 'nuclear_escalation'],
                'default_values': {
                    'duration_days': 30,
                    'intensity': 'medium',
                    'escalation_level': 'limited',
                    'nuclear_escalation': False
                }
            },
            'economic_warfare': {
                'required_fields': ['target_country', 'warfare_type'],
                'optional_fields': ['attacker_country', 'intensity', 'duration_days'],
                'default_values': {
                    'intensity': 'medium',
                    'duration_days': 180,
                    'warfare_type': 'sanctions'
                }
            },
            'natural_disaster': {
                'required_fields': ['location', 'disaster_type'],
                'optional_fields': ['intensity', 'population_affected'],
                'default_values': {
                    'intensity': 'medium',
                    'population_affected': 100000
                }
            },
            'pandemic_scenario': {
                'required_fields': ['region', 'pathogen_type'],
                'optional_fields': ['mortality_rate', 'transmission_rate', 'duration_days'],
                'default_values': {
                    'mortality_rate': 0.02,
                    'transmission_rate': 2.5,
                    'duration_days': 365
                }
            },
            'climate_impact': {
                'required_fields': ['region', 'time_horizon_years'],
                'optional_fields': ['emission_scenario', 'population_size'],
                'default_values': {
                    'emission_scenario': 'rcp45',
                    'population_size': 1000000
                }
            },
            'supply_chain_crisis': {
                'required_fields': ['affected_materials', 'affected_regions'],
                'optional_fields': ['disruption_intensity', 'duration_days'],
                'default_values': {
                    'disruption_intensity': 0.7,
                    'duration_days': 90
                }
            }
        }

    def _load_country_data(self):
        """Load country data for scenario building"""
        return {
            'USA': {
                'region': 'north_america',
                'neighbors': ['Canada', 'Mexico'],
                'allies': ['UK', 'France', 'Germany', 'Japan', 'Australia'],
                'rivals': ['China', 'Russia', 'Iran'],
                'population': 331900000,
                'gdp_trillion': 26.9,
                'military_strength': 10,
                'nuclear_weapons': True
            },
            'China': {
                'region': 'east_asia',
                'neighbors': ['Russia', 'India', 'North Korea', 'Vietnam'],
                'allies': ['Russia', 'Pakistan', 'Iran'],
                'rivals': ['USA', 'India', 'Japan'],
                'population': 1425671352,
                'gdp_trillion': 17.9,
                'military_strength': 9,
                'nuclear_weapons': True
            },
            'India': {
                'region': 'south_asia',
                'neighbors': ['Pakistan', 'China', 'Bangladesh', 'Myanmar'],
                'allies': ['USA', 'Russia', 'Israel'],
                'rivals': ['Pakistan', 'China'],
                'population': 1428627663,
                'gdp_trillion': 3.74,
                'military_strength': 7,
                'nuclear_weapons': True
            },
            'Pakistan': {
                'region': 'south_asia',
                'neighbors': ['India', 'China', 'Iran', 'Afghanistan'],
                'allies': ['China', 'Saudi Arabia', 'Turkey'],
                'rivals': ['India'],
                'population': 231402117,
                'gdp_trillion': 0.35,
                'military_strength': 5,
                'nuclear_weapons': True
            },
            'Russia': {
                'region': 'eurasia',
                'neighbors': ['China', 'Ukraine', 'Belarus', 'Kazakhstan'],
                'allies': ['China', 'Iran', 'Belarus'],
                'rivals': ['USA', 'NATO', 'Ukraine'],
                'population': 144713314,
                'gdp_trillion': 1.83,
                'military_strength': 8,
                'nuclear_weapons': True
            },
            'Iran': {
                'region': 'middle_east',
                'neighbors': ['Iraq', 'Afghanistan', 'Pakistan', 'Turkey'],
                'allies': ['Russia', 'China', 'Syria'],
                'rivals': ['USA', 'Israel', 'Saudi Arabia'],
                'population': 85028759,
                'gdp_trillion': 0.23,
                'military_strength': 4,
                'nuclear_weapons': False
            }
        }

    def _load_model_capabilities(self):
        """Load information about available models and their capabilities"""
        return {
            'military_analysis': {
                'description': 'Analyzes military conflicts, missile trajectories, casualty estimates, and defense system effectiveness',
                'inputs': ['countries', 'weapon_types', 'defense_systems', 'geographic_location'],
                'outputs': ['casualty_estimates', 'interception_probabilities', 'economic_damage']
            },
            'nuclear_warfare': {
                'description': 'Models nuclear weapon exchanges, escalation dynamics, and global consequences',
                'inputs': ['nuclear_powers', 'escalation_level', 'first_strike_capability'],
                'outputs': ['casualty_projections', 'fallout_patterns', 'global_climate_effects']
            },
            'economic_impact': {
                'description': 'Analyzes economic warfare, sanctions, market disruptions, and GDP impacts',
                'inputs': ['countries', 'economic_measures', 'trade_relationships'],
                'outputs': ['gdp_impact', 'unemployment_effects', 'market_volatility']
            },
            'supply_chain_analysis': {
                'description': 'Models supply chain disruptions, cascade effects, and alternative routing',
                'inputs': ['supply_chains', 'disrupted_nodes', 'critical_materials'],
                'outputs': ['shortage_predictions', 'price_impacts', 'recovery_timelines']
            },
            'population_impact': {
                'description': 'Analyzes demographic impacts, displacement, and social dynamics',
                'inputs': ['population_size', 'community_type', 'impact_scenario'],
                'outputs': ['displacement_patterns', 'social_cohesion_changes', 'demographic_shifts']
            },
            'psychological_impact': {
                'description': 'Models mental health effects, trauma responses, and psychological resilience',
                'inputs': ['trauma_exposure', 'population_characteristics', 'duration'],
                'outputs': ['ptsd_prevalence', 'depression_rates', 'community_resilience']
            },
            'infrastructure_analysis': {
                'description': 'Analyzes infrastructure damage, cascade failures, and recovery requirements',
                'inputs': ['infrastructure_types', 'damage_scenarios', 'interdependencies'],
                'outputs': ['service_disruptions', 'repair_costs', 'recovery_timelines']
            },
            'climate_modeling': {
                'description': 'Models long-term climate impacts, environmental changes, and adaptation needs',
                'inputs': ['emission_scenarios', 'time_horizons', 'regional_factors'],
                'outputs': ['temperature_changes', 'precipitation_patterns', 'adaptation_requirements']
            }
        }

    def process_message(self, message: str, conversation_id: str) -> Dict[str, Any]:
        """Process user message and generate appropriate response"""

        # Initialize conversation if new
        if conversation_id not in self.conversation_history:
            self.conversation_history[conversation_id] = {
                'messages': [],
                'scenario_config': {},
                'context': {},
                'stage': 'initial'
            }

        conversation = self.conversation_history[conversation_id]
        conversation['messages'].append({'role': 'user', 'content': message, 'timestamp': datetime.now().isoformat()})

        # Analyze user intent
        intent_analysis = self._analyze_user_intent(message, conversation)

        # Generate response based on intent
        if intent_analysis['intent'] == 'scenario_request':
            response = self._handle_scenario_request(message, conversation, intent_analysis)
        elif intent_analysis['intent'] == 'parameter_clarification':
            response = self._handle_parameter_clarification(message, conversation, intent_analysis)
        elif intent_analysis['intent'] == 'run_analysis':
            response = self._handle_run_analysis_request(message, conversation)
        elif intent_analysis['intent'] == 'model_explanation':
            response = self._handle_model_explanation_request(message, conversation, intent_analysis)
        elif intent_analysis['intent'] == 'modify_scenario':
            response = self._handle_scenario_modification(message, conversation, intent_analysis)
        else:
            response = self._handle_general_query(message, conversation)

        conversation['messages'].append({'role': 'assistant', 'content': response['message'], 'timestamp': datetime.now().isoformat()})

        return response

    def _analyze_user_intent(self, message: str, conversation: Dict) -> Dict[str, Any]:
        """Analyze user intent from message"""

        message_lower = message.lower()

        # Scenario creation patterns
        scenario_patterns = [
            r'what if.* attack.*',
            r'analyze.*conflict.*',
            r'model.*scenario.*',
            r'simulate.*war.*',
            r'predict.*impact.*',
            r'economic.*warfare.*',
            r'nuclear.*exchange.*',
            r'supply.*chain.*disruption.*'
        ]

        # Parameter clarification patterns
        parameter_patterns = [
            r'set.*intensity.*',
            r'change.*duration.*',
            r'use.*country.*',
            r'modify.*parameter.*',
            r'adjust.*setting.*'
        ]

        # Run analysis patterns
        run_patterns = [
            r'run.*analysis.*',
            r'execute.*scenario.*',
            r'start.*simulation.*',
            r'analyze.*now.*',
            r'run.*model.*'
        ]

        # Model explanation patterns
        explain_patterns = [
            r'how.*work.*',
            r'explain.*model.*',
            r'what.*does.*do.*',
            r'describe.*analysis.*'
        ]

        # Check patterns
        for pattern in scenario_patterns:
            if re.search(pattern, message_lower):
                return {
                    'intent': 'scenario_request',
                    'confidence': 0.9,
                    'extracted_entities': self._extract_entities(message)
                }

        for pattern in parameter_patterns:
            if re.search(pattern, message_lower):
                return {
                    'intent': 'parameter_clarification',
                    'confidence': 0.8,
                    'extracted_entities': self._extract_entities(message)
                }

        for pattern in run_patterns:
            if re.search(pattern, message_lower):
                return {
                    'intent': 'run_analysis',
                    'confidence': 0.9,
                    'extracted_entities': {}
                }

        for pattern in explain_patterns:
            if re.search(pattern, message_lower):
                return {
                    'intent': 'model_explanation',
                    'confidence': 0.7,
                    'extracted_entities': self._extract_entities(message)
                }

        return {
            'intent': 'general_query',
            'confidence': 0.5,
            'extracted_entities': self._extract_entities(message)
        }

    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """Extract relevant entities from user message"""

        entities = {
            'countries': [],
            'numbers': [],
            'time_periods': [],
            'intensity_levels': [],
            'scenario_types': []
        }

        message_lower = message.lower()

        # Extract countries
        for country in self.country_data.keys():
            if country.lower() in message_lower:
                entities['countries'].append(country)

        # Common country name variations
        country_variations = {
            'us': 'USA', 'america': 'USA', 'united states': 'USA',
            'china': 'China', 'prc': 'China',
            'india': 'India',
            'pakistan': 'Pakistan',
            'russia': 'Russia', 'russian': 'Russia',
            'iran': 'Iran', 'persia': 'Iran'
        }

        for variation, country in country_variations.items():
            if variation in message_lower and country not in entities['countries']:
                entities['countries'].append(country)

        # Extract numbers
        import re
        numbers = re.findall(r'\d+', message)
        entities['numbers'] = [int(n) for n in numbers]

        # Extract intensity levels
        intensity_keywords = ['low', 'medium', 'high', 'extreme', 'severe', 'mild', 'intense']
        for keyword in intensity_keywords:
            if keyword in message_lower:
                entities['intensity_levels'].append(keyword)

        # Extract scenario types
        scenario_keywords = {
            'conflict': ['war', 'conflict', 'attack', 'invasion', 'military'],
            'economic': ['economic', 'sanctions', 'trade', 'market', 'financial'],
            'nuclear': ['nuclear', 'atomic', 'warhead', 'fallout'],
            'natural_disaster': ['earthquake', 'tsunami', 'hurricane', 'flood', 'disaster'],
            'pandemic': ['pandemic', 'virus', 'disease', 'outbreak', 'epidemic'],
            'cyber': ['cyber', 'hacking', 'digital', 'internet']
        }

        for scenario_type, keywords in scenario_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    entities['scenario_types'].append(scenario_type)
                    break

        return entities

    def _handle_scenario_request(self, message: str, conversation: Dict, intent_analysis: Dict) -> Dict[str, Any]:
        """Handle scenario creation request"""

        entities = intent_analysis['extracted_entities']

        # Determine scenario type
        scenario_types = entities.get('scenario_types', [])
        if not scenario_types:
            # Try to infer from context
            if any(keyword in message.lower() for keyword in ['attack', 'war', 'military', 'missile']):
                scenario_type = 'military_conflict'
            elif any(keyword in message.lower() for keyword in ['economic', 'sanctions', 'trade']):
                scenario_type = 'economic_warfare'
            else:
                scenario_type = 'military_conflict'  # Default
        else:
            scenario_type = scenario_types[0] if scenario_types[0] in self.scenario_templates else 'military_conflict'

        # Get template for scenario type  
        template = self.scenario_templates[scenario_type]

        # Build scenario configuration
        scenario_config = template['default_values'].copy()
        scenario_config['type'] = scenario_type.replace('_', '')

        # Fill in extracted information
        countries = entities.get('countries', [])
        if len(countries) >= 2:
            scenario_config['attacker_country'] = countries[0]
            scenario_config['defender_country'] = countries[1]
            scenario_config['countries_involved'] = countries
        elif len(countries) == 1:
            scenario_config['target_country'] = countries[0]
            scenario_config['countries_involved'] = countries

        # Set intensity if specified
        intensity_levels = entities.get('intensity_levels', [])
        if intensity_levels:
            intensity_map = {'mild': 'low', 'severe': 'high', 'intense': 'extreme'}
            intensity = intensity_levels[0]
            scenario_config['intensity'] = intensity_map.get(intensity, intensity)

        # Set duration if numbers present
        numbers = entities.get('numbers', [])
        if numbers:
            # Assume first number is duration in days
            scenario_config['duration_days'] = numbers[0]

        # Store in conversation
        conversation['scenario_config'] = scenario_config
        conversation['stage'] = 'scenario_built'

        # Generate response
        response_message = f"""I've created a {scenario_type.replace('_', ' ')} scenario with the following configuration:

**Scenario Type**: {scenario_type.replace('_', ' ').title()}
"""

        if 'attacker_country' in scenario_config:
            response_message += f"**Attacker**: {scenario_config['attacker_country']}\n"
        if 'defender_country' in scenario_config:
            response_message += f"**Defender**: {scenario_config['defender_country']}\n"
        if 'target_country' in scenario_config:
            response_message += f"**Target Country**: {scenario_config['target_country']}\n"

        response_message += f"""**Intensity**: {scenario_config.get('intensity', 'medium').title()}
**Duration**: {scenario_config.get('duration_days', 30)} days

Would you like me to:
1. Run the analysis with these settings
2. Modify any parameters
3. Add more specific details (population size, geographic location, etc.)

Just let me know what you'd like to do next!"""

        return {
            'message': response_message,
            'scenario_config': scenario_config,
            'action': 'scenario_configured'
        }

    def _handle_run_analysis_request(self, message: str, conversation: Dict) -> Dict[str, Any]:
        """Handle request to run analysis"""

        if 'scenario_config' not in conversation or not conversation['scenario_config']:
            return {
                'message': "I don't have a scenario configured yet. Please describe what scenario you'd like me to analyze first.",
                'action': 'need_scenario'
            }

        scenario_config = conversation['scenario_config']

        # Add any missing required fields with defaults
        self._fill_missing_scenario_fields(scenario_config)

        response_message = f"""Starting comprehensive analysis of your scenario...

**Scenario Summary:**
- Type: {scenario_config.get('type', 'Unknown')}
- Countries: {', '.join(scenario_config.get('countries_involved', ['Unknown']))}
- Intensity: {scenario_config.get('intensity', 'medium')}
- Duration: {scenario_config.get('duration_days', 30)} days

**Analysis will include:**
- Military impact assessment
- Economic damage modeling
- Population and infrastructure effects
- Psychological and social impacts
- Global response modeling
- Timeline projections

This analysis typically takes 45-90 seconds to complete. You'll receive detailed results with interactive visualizations once finished."""

        return {
            'message': response_message,
            'scenario_config': scenario_config,
            'action': 'run_analysis'
        }

    def _fill_missing_scenario_fields(self, scenario_config: Dict):
        """Fill in missing required fields with intelligent defaults"""

        # Add unique ID
        scenario_config['id'] = f"ai_scenario_{int(datetime.now().timestamp())}"

        # Add population size based on countries involved
        if 'population_size' not in scenario_config:
            countries = scenario_config.get('countries_involved', [])
            if countries:
                # Estimate affected population based on country
                total_pop = sum(self.country_data.get(country, {}).get('population', 10000000) for country in countries)
                scenario_config['population_size'] = min(50000000, int(total_pop * 0.1))  # 10% of total population affected
            else:
                scenario_config['population_size'] = 1000000

        # Add geographic details
        if 'location' not in scenario_config:
            countries = scenario_config.get('countries_involved', [])
            if countries:
                scenario_config['location'] = countries[0]  # Primary country

        if 'terrain_type' not in scenario_config:
            scenario_config['terrain_type'] = 'urban_medium'

        if 'climate_zone' not in scenario_config:
            scenario_config['climate_zone'] = 'temperate'

        if 'elevation_m' not in scenario_config:
            scenario_config['elevation_m'] = 200

        # Add cultural region
        if 'cultural_region' not in scenario_config:
            countries = scenario_config.get('countries_involved', [])
            if countries:
                country = countries[0]
                country_info = self.country_data.get(country, {})
                scenario_config['cultural_region'] = country_info.get('region', 'western_society')

        # Add military details for conflict scenarios
        if scenario_config.get('type') in ['conflict', 'military', 'war']:
            if 'missile_threat' not in scenario_config:
                countries = scenario_config.get('countries_involved', [])
                if len(countries) >= 2:
                    attacker = countries[0]
                    defender = countries[1]

                    # Add realistic coordinates (simplified)
                    coords_map = {
                        'USA': [39.8283, -98.5795],
                        'China': [35.8617, 104.1954],
                        'India': [20.5937, 78.9629],
                        'Pakistan': [30.3753, 69.3451],
                        'Russia': [61.5240, 105.3188],
                        'Iran': [32.4279, 53.6880]
                    }

                    scenario_config['missile_threat'] = {
                        'launch_coords': coords_map.get(attacker, [35.0, 50.0]),
                        'target_coords': coords_map.get(defender, [40.0, 55.0]),
                        'missile_type': 'ballistic_missiles',
                        'missile_subtype': 'IRBM',
                        'weapon_type': 'conventional'
                    }

            if 'defense_systems' not in scenario_config:
                defender = scenario_config.get('defender_country', 'USA')
                defense_map = {
                    'USA': ['Patriot PAC-3', 'THAAD', 'Aegis SM-3'],
                    'India': ['S-400', 'Akash', 'Iron Dome'],
                    'China': ['HQ-9', 'HQ-19'],
                    'Russia': ['S-400', 'S-500', 'Pantsir'],
                    'Israel': ['Iron Dome', 'David Sling', 'Arrow-3']
                }
                scenario_config['defense_systems'] = defense_map.get(defender, ['Patriot PAC-3'])

        # Add economic warfare details
        if 'economic_warfare' not in scenario_config and scenario_config.get('type') == 'economic':
            scenario_config['economic_warfare'] = True

        # Add infrastructure impact details
        if 'infrastructure_impact' not in scenario_config:
            scenario_config['infrastructure_impact'] = {
                'profile': {
                    'transportation': 0.7,
                    'energy': 0.8,
                    'telecommunications': 0.6,
                    'water_systems': 0.5
                }
            }

class ScenarioBuilder:
    """Advanced scenario builder with natural language processing"""

    def __init__(self):
        self.predefined_scenarios = self._load_predefined_scenarios()
        self.parameter_validators = self._load_parameter_validators()

    def _load_predefined_scenarios(self):
        """Load predefined scenario configurations"""
        return {
            'india_pakistan_nuclear': {
                'type': 'conflict',
                'attacker_country': 'Pakistan',
                'defender_country': 'India',
                'duration_days': 21,
                'intensity': 'extreme',
                'escalation_level': 'strategic',
                'nuclear_escalation': True,
                'population_size': 25000000,
                'location': 'Kashmir',
                'cultural_region': 'south_asia'
            },
            'china_taiwan_invasion': {
                'type': 'conflict',
                'attacker_country': 'China', 
                'defender_country': 'Taiwan',
                'duration_days': 60,
                'intensity': 'extreme',
                'escalation_level': 'strategic',
                'nuclear_escalation': False,
                'population_size': 23500000,
                'location': 'Taiwan',
                'allies_involved': ['USA', 'Japan', 'Australia']
            },
            'global_supply_chain_collapse': {
                'type': 'economic',
                'affected_regions': ['China', 'Taiwan', 'Southeast Asia'],
                'affected_materials': ['semiconductors', 'rare_earth_elements', 'pharmaceuticals'],
                'disruption_intensity': 0.9,
                'duration_days': 180,
                'population_size': 500000000
            },
            'middle_east_oil_shock': {
                'type': 'economic',
                'affected_regions': ['Saudi Arabia', 'Iran', 'UAE'],
                'affected_materials': ['oil_gas', 'petrochemicals'],
                'disruption_intensity': 0.8,
                'duration_days': 90,
                'global_impact': True
            }
        }

    def build_scenario_from_description(self, description: str) -> Dict[str, Any]:
        """Build comprehensive scenario from natural language description"""

        # Use AI assistant to parse description
        ai_assistant = AIAssistant()

        # Process the description
        result = ai_assistant.process_message(description, 'scenario_builder')

        if 'scenario_config' in result:
            scenario_config = result['scenario_config']

            # Add comprehensive default configurations
            self._add_comprehensive_defaults(scenario_config)

            return {
                'scenario_config': scenario_config,
                'confidence': 0.85,
                'interpretation': result.get('message', ''),
                'suggested_modifications': self._suggest_modifications(scenario_config)
            }
        else:
            return {
                'error': 'Could not parse scenario description',
                'suggestion': 'Please provide more specific details about the scenario'
            }

    def _add_comprehensive_defaults(self, scenario_config: Dict):
        """Add comprehensive default configurations for all aspects of scenario"""

        # Ensure all required fields are present
        defaults = {
            'id': f"scenario_{int(datetime.now().timestamp())}",
            'created_at': datetime.now().isoformat(),
            'type': 'conflict',
            'intensity': 'medium',
            'duration_days': 30,
            'population_size': 1000000,
            'location': 'Unknown',
            'terrain_type': 'urban_medium',
            'climate_zone': 'temperate',
            'elevation_m': 100,
            'cultural_region': 'western_society'
        }

        for key, value in defaults.items():
            if key not in scenario_config:
                scenario_config[key] = value

        # Add detailed target area data for military scenarios
        if scenario_config.get('type') in ['conflict', 'military', 'war']:
            if 'target_area_data' not in scenario_config:
                scenario_config['target_area_data'] = {
                    'population_density': 5000,
                    'area_type': 'urban',
                    'protection_level': 0.2,
                    'building_density': 0.65,
                    'time_of_day': 'day'
                }

        # Add supply chain disruption details for economic scenarios
        if scenario_config.get('type') == 'economic':
            if 'supply_chain_disruption' not in scenario_config:
                scenario_config['supply_chain_disruption'] = {
                    'affected_nodes': scenario_config.get('countries_involved', ['Global']),
                    'affected_materials': ['manufactured_goods', 'raw_materials'],
                    'disruption_intensity': 0.6
                }

    def _suggest_modifications(self, scenario_config: Dict) -> List[str]:
        """Suggest potential modifications to improve scenario realism"""

        suggestions = []

        # Check for unrealistic parameters
        if scenario_config.get('duration_days', 0) > 365:
            suggestions.append("Consider shorter duration - conflicts rarely last over a year without major changes")

        if scenario_config.get('intensity') == 'extreme' and scenario_config.get('duration_days', 0) > 90:
            suggestions.append("Extreme intensity conflicts typically don't sustain for very long periods")

        # Check for missing important factors
        if scenario_config.get('type') == 'conflict' and not scenario_config.get('nuclear_escalation'):
            nuclear_countries = ['USA', 'Russia', 'China', 'India', 'Pakistan', 'Israel', 'North Korea']
            involved_countries = scenario_config.get('countries_involved', [])
            if any(country in nuclear_countries for country in involved_countries):
                suggestions.append("Consider nuclear escalation risk given nuclear-armed countries involved")

        if scenario_config.get('population_size', 0) > 50000000:
            suggestions.append("Very large affected populations may be unrealistic - consider regional focus")

        return suggestions
