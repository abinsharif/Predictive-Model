import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import time
import uuid

from .military_models import MilitaryAnalyzer, NuclearWarfareModel, DefenseSystemModel
from .economic_models import EconomicImpactModel, SupplyChainModel, MarketDisruptionModel
from .social_models import PopulationModel, PsychologicalImpactModel, CulturalModel
from .environmental_models import GeographicModel, ClimateImpactModel, InfrastructureModel

class CompositeScenarioModel:
    """Master composite model that orchestrates all individual models for complex scenarios"""

    def __init__(self):
        # Initialize all component models
        self.military_analyzer = MilitaryAnalyzer()
        self.nuclear_model = NuclearWarfareModel()
        self.defense_model = DefenseSystemModel()
        self.economic_model = EconomicImpactModel()
        self.supply_chain_model = SupplyChainModel()
        self.market_model = MarketDisruptionModel()
        self.population_model = PopulationModel()
        self.psychological_model = PsychologicalImpactModel()
        self.cultural_model = CulturalModel()
        self.geographic_model = GeographicModel()
        self.climate_model = ClimateImpactModel()
        self.infrastructure_model = InfrastructureModel()

        # Initialize escalation and response models
        self.escalation_model = EscalationModel()
        self.global_response_model = GlobalResponseModel()
        self.scenario_cache = {}

    def run_comprehensive_analysis(self, scenario_config):
        """Run comprehensive analysis using multiple interconnected models"""
        scenario_id = scenario_config.get('id', str(uuid.uuid4()))
        scenario_type = scenario_config.get('type', 'conflict')

        print(f"Starting comprehensive analysis for scenario: {scenario_id}")

        # Initialize results structure
        comprehensive_results = {
            'scenario_id': scenario_id,
            'scenario_config': scenario_config,
            'analysis_start_time': datetime.now().isoformat(),
            'model_results': {},
            'integrated_analysis': {},
            'timeline_projections': {},
            'risk_assessment': {},
            'policy_recommendations': {}
        }

        try:
            # Phase 1: Run all individual model analyses
            print("Phase 1: Running individual model analyses...")
            comprehensive_results['model_results'] = self._run_individual_models(scenario_config)

            # Phase 2: Integrate results across models
            print("Phase 2: Integrating cross-model interactions...")
            comprehensive_results['integrated_analysis'] = self._integrate_model_results(
                comprehensive_results['model_results'], scenario_config
            )

            # Phase 3: Generate timeline projections
            print("Phase 3: Generating timeline projections...")
            comprehensive_results['timeline_projections'] = self._generate_timeline_projections(
                comprehensive_results['integrated_analysis'], scenario_config
            )

            # Phase 4: Assess overall risks and uncertainties
            print("Phase 4: Assessing risks and uncertainties...")
            comprehensive_results['risk_assessment'] = self._assess_comprehensive_risks(
                comprehensive_results['integrated_analysis']
            )

            # Phase 5: Generate policy recommendations
            print("Phase 5: Generating policy recommendations...")
            comprehensive_results['policy_recommendations'] = self._generate_policy_recommendations(
                comprehensive_results['integrated_analysis'], comprehensive_results['risk_assessment']
            )

            # Phase 6: Calculate confidence levels
            comprehensive_results['confidence_analysis'] = self._calculate_confidence_levels(
                comprehensive_results['model_results']
            )

            comprehensive_results['analysis_end_time'] = datetime.now().isoformat()
            comprehensive_results['status'] = 'completed'

            # Cache results
            self.scenario_cache[scenario_id] = comprehensive_results

            print(f"Comprehensive analysis completed for scenario: {scenario_id}")
            return comprehensive_results

        except Exception as e:
            error_msg = f"Error in comprehensive analysis: {str(e)}"
            comprehensive_results['status'] = 'error'
            comprehensive_results['error'] = str(e)
            comprehensive_results['analysis_end_time'] = datetime.now().isoformat()
            print(error_msg)
            import os
            def log_error_to_file(error_message):
                with open(os.path.join(os.path.dirname(__file__), '../error.log'), 'a', encoding='utf-8') as f:
                    f.write(error_message + '\n')
            log_error_to_file(error_msg)
            return comprehensive_results

    def _run_individual_models(self, scenario_config):
        """Run all individual models based on scenario configuration"""
        model_results = {}
        scenario_type = scenario_config.get('type', 'conflict')

        # Geographic and environmental analysis (always runs first)
        print("  Running geographic analysis...")
        if 'location' in scenario_config:
            model_results['geographic'] = self.geographic_model.analyze_geographic_impact(
                scenario_config['location'],
                scenario_config.get('terrain_type', 'urban_medium'),
                scenario_config.get('climate_zone', 'temperate'),
                scenario_config.get('elevation_m', 100),
                scenario_config
            )

        # Population and demographic analysis
        print("  Running population analysis...")
        if 'population_size' in scenario_config:
            model_results['population'] = self.population_model.analyze_population_impact(
                scenario_config.get('location_type', 'medium_city'),
                scenario_config['population_size'],
                scenario_config
            )

        # Military analysis (if conflict scenario)
        if scenario_type in ['conflict', 'military', 'war']:
            print("  Running military analysis...")
            # Basic military analysis
            if 'missile_threat' in scenario_config:
                missile_config = scenario_config['missile_threat']
                trajectory = self.military_analyzer.calculate_missile_trajectory(
                    missile_config['launch_coords'],
                    missile_config['target_coords'],
                    missile_config['missile_type'],
                    missile_config['missile_subtype']
                )

                defense_analysis = self.military_analyzer.calculate_defense_interception_probability(
                    trajectory,
                    scenario_config.get('defense_systems', ['Patriot PAC-3', 'THAAD']),
                    missile_config['target_coords']
                )

                casualty_analysis = self.military_analyzer.estimate_casualties_comprehensive(
                    trajectory,
                    scenario_config.get('target_area_data', {}),
                    missile_config.get('weapon_type', 'conventional')
                )

                model_results['military'] = {
                    'trajectory': trajectory,
                    'defense_analysis': defense_analysis,
                    'casualty_analysis': casualty_analysis
                }

            # Nuclear analysis (if nuclear scenario)
            if scenario_config.get('nuclear_escalation', False):
                print("  Running nuclear warfare analysis...")
                model_results['nuclear'] = self.nuclear_model.calculate_nuclear_exchange_scenario(
                    scenario_config['attacker_country'],
                    scenario_config['defender_country'],
                    scenario_config.get('escalation_level', 'limited'),
                    scenario_config.get('first_strike', False)
                )

        # Economic analysis
        print("  Running economic analysis...")
        if 'economic_warfare' in scenario_config or scenario_type == 'economic':
            model_results['economic'] = self.economic_model.calculate_economic_warfare_impact(
                scenario_config.get('attacker_country', 'Unknown'),
                scenario_config.get('target_country', 'USA'),
                scenario_config.get('warfare_type', 'sanctions'),
                scenario_config.get('intensity', 'medium'),
                scenario_config.get('duration_days', 180)
            )

        # Supply chain analysis
        if 'supply_chain_disruption' in scenario_config:
            print("  Running supply chain analysis...")
            model_results['supply_chain'] = self.supply_chain_model.analyze_supply_chain_disruption(
                scenario_config['supply_chain_disruption']['affected_nodes'],
                scenario_config['supply_chain_disruption']['affected_materials'],
                scenario_config['supply_chain_disruption']['disruption_intensity']
            )

        # Infrastructure analysis
        if 'infrastructure_impact' in scenario_config:
            print("  Running infrastructure analysis...")
            model_results['infrastructure'] = self.infrastructure_model.analyze_infrastructure_impact(
                scenario_config['infrastructure_impact']['profile'],
                scenario_config,
                model_results.get('geographic', {})
            )

        # Psychological impact analysis
        if 'population_size' in scenario_config:
            print("  Running psychological impact analysis...")
            model_results['psychological'] = self.psychological_model.analyze_psychological_impact(
                model_results.get('population', {}),
                scenario_config,
                scenario_config.get('duration_days', 30)
            )

        # Cultural impact analysis
        if 'cultural_region' in scenario_config:
            print("  Running cultural impact analysis...")
            model_results['cultural'] = self.cultural_model.analyze_cultural_impact(
                scenario_config['cultural_region'],
                model_results.get('population', {}),
                scenario_config
            )

        # Climate impact analysis (if long-term scenario)
        if scenario_config.get('time_horizon_years', 0) > 5:
            print("  Running climate impact analysis...")
            model_results['climate'] = self.climate_model.model_climate_impact_scenario(
                scenario_config.get('region', 'global'),
                scenario_config['time_horizon_years'],
                scenario_config.get('emission_scenario', 'rcp45'),
                model_results.get('population', {})
            )

        return model_results

    def _integrate_model_results(self, model_results, scenario_config):
        """Integrate results across all models to identify interactions and compound effects"""
        integrated_analysis = {
            'cross_model_interactions': {},
            'compound_effects': {},
            'feedback_loops': {},
            'system_vulnerabilities': {},
            'resilience_factors': {}
        }

        # Identify cross-model interactions
        integrated_analysis['cross_model_interactions'] = self._identify_cross_model_interactions(model_results)

        # Calculate compound effects
        integrated_analysis['compound_effects'] = self._calculate_compound_effects(model_results)

        # Identify feedback loops
        integrated_analysis['feedback_loops'] = self._identify_feedback_loops(model_results)

        # Assess system vulnerabilities
        integrated_analysis['system_vulnerabilities'] = self._assess_system_vulnerabilities(model_results)

        # Evaluate resilience factors
        integrated_analysis['resilience_factors'] = self._evaluate_resilience_factors(model_results)

        return integrated_analysis

    def _calculate_compound_effects(self, model_results):
        """Calculate compound effects where multiple factors amplify each other"""
        compound_effects = {}

        # Calculate total casualty burden (direct + indirect)
        total_casualties = 0
        casualty_sources = []

        if 'military' in model_results:
            military_casualties = model_results['military'].get('casualty_analysis', {}).get('immediate_casualties', 0)
            total_casualties += military_casualties
            casualty_sources.append({'source': 'military', 'casualties': int(military_casualties)})

        if 'infrastructure' in model_results:
            # Infrastructure failures cause indirect casualties
            infrastructure_casualties = self._estimate_infrastructure_casualties(model_results['infrastructure'])
            total_casualties += infrastructure_casualties
            casualty_sources.append({'source': 'infrastructure', 'casualties': int(infrastructure_casualties)})

        if 'psychological' in model_results:
            # Mental health impacts lead to additional mortality
            psychological_mortality = self._estimate_psychological_mortality(model_results['psychological'])
            total_casualties += psychological_mortality
            casualty_sources.append({'source': 'psychological', 'casualties': int(psychological_mortality)})

        compound_effects['total_casualty_burden'] = {
            'total_casualties': int(total_casualties),
            'casualty_sources': casualty_sources,
            'casualty_multiplier': float(total_casualties / max(1, casualty_sources[0]['casualties'] if casualty_sources else 1))
        }

        # Calculate compound economic impact
        total_economic_damage = 0.0
        economic_sources = []

        if 'economic' in model_results:
            direct_economic = model_results['economic'].get('economic_damage', {}).get('total_damage_usd', 0)
            total_economic_damage += direct_economic
            economic_sources.append({'source': 'direct_economic_warfare', 'damage': float(direct_economic)})

        if 'supply_chain' in model_results:
            supply_chain_damage = model_results['supply_chain'].get('global_impact_summary', {}).get('total_economic_impact_billion', 0) * 1e9
            total_economic_damage += supply_chain_damage
            economic_sources.append({'source': 'supply_chain', 'damage': float(supply_chain_damage)})

        if 'infrastructure' in model_results:
            infrastructure_economic = model_results['infrastructure'].get('economic_impact', {}).get('total_damage_usd', 0)
            total_economic_damage += infrastructure_economic
            economic_sources.append({'source': 'infrastructure', 'damage': float(infrastructure_economic)})

        compound_effects['total_economic_impact'] = {
            'total_damage_usd': float(total_economic_damage),
            'economic_sources': economic_sources,
            'gdp_impact_percent': float((total_economic_damage / 25000000000000) * 100)  # Global GDP rough estimate
        }

        # Calculate compound social disruption
        social_disruption_score = 0.0
        disruption_factors = []

        if 'population' in model_results:
            displacement_factor = model_results['population'].get('displacement_analysis', {}).get('displacement_rate_percent', 0) / 100
            social_disruption_score += displacement_factor * 0.4
            disruption_factors.append({'factor': 'displacement', 'score': float(displacement_factor)})

        if 'psychological' in model_results:
            mental_health_factor = model_results['psychological'].get('mental_health_outcomes', {}).get('ptsd', {}).get('prevalence_rate', 0)
            social_disruption_score += mental_health_factor * 0.3
            disruption_factors.append({'factor': 'mental_health', 'score': float(mental_health_factor)})

        if 'cultural' in model_results:
            cultural_disruption = model_results['cultural'].get('social_structure_changes', {}).get('social_cohesion_change', 0)
            cultural_factor = abs(cultural_disruption) / 10  # Normalize
            social_disruption_score += cultural_factor * 0.3
            disruption_factors.append({'factor': 'cultural_disruption', 'score': float(cultural_factor)})

        compound_effects['social_disruption'] = {
            'total_disruption_score': float(min(1.0, social_disruption_score)),
            'disruption_factors': disruption_factors,
            'social_cohesion_remaining': float(max(0, 1.0 - social_disruption_score))
        }

        return compound_effects

    def _assess_comprehensive_risks(self, integrated_analysis):
        """Assess comprehensive risks across all model domains"""
        risk_assessment = {
            'overall_risk_score': 0.0,
            'risk_categories': {},
            'critical_vulnerabilities': [],
            'risk_mitigation_priorities': [],
            'uncertainty_factors': []
        }

        # Assess risks by category
        risk_categories = {
            'military_risk': 0.0,
            'economic_risk': 0.0,
            'social_risk': 0.0,
            'infrastructure_risk': 0.0,
            'systemic_risk': 0.0
        }

        # Calculate compound effects risk
        compound_effects = integrated_analysis.get('compound_effects', {})
        if 'total_casualty_burden' in compound_effects:
            total_casualties = compound_effects['total_casualty_burden'].get('total_casualties', 0)
            risk_categories['military_risk'] = float(min(1.0, total_casualties / 100000))

        if 'total_economic_impact' in compound_effects:
            economic_damage = compound_effects['total_economic_impact'].get('gdp_impact_percent', 0)
            risk_categories['economic_risk'] = float(min(1.0, economic_damage / 20))

        if 'social_disruption' in compound_effects:
            social_score = compound_effects['social_disruption'].get('total_disruption_score', 0)
            risk_categories['social_risk'] = float(social_score)

        # Assess system vulnerabilities
        vulnerabilities = integrated_analysis.get('system_vulnerabilities', {})
        risk_categories['systemic_risk'] = float(vulnerabilities.get('cascade_vulnerability', 0.5))

        # Calculate overall risk score
        risk_assessment['overall_risk_score'] = float(np.mean(list(risk_categories.values())))
        risk_assessment['risk_categories'] = risk_categories

        # Identify critical vulnerabilities
        critical_threshold = 0.7
        risk_assessment['critical_vulnerabilities'] = [
            category for category, score in risk_categories.items() if score > critical_threshold
        ]

        # Generate risk mitigation priorities
        risk_assessment['risk_mitigation_priorities'] = self._generate_risk_mitigation_priorities(risk_categories)

        # Assess uncertainty factors
        risk_assessment['uncertainty_factors'] = self._assess_uncertainty_factors(integrated_analysis)

        return risk_assessment

    def _generate_policy_recommendations(self, integrated_analysis, risk_assessment):
        """Generate comprehensive policy recommendations"""
        recommendations = {
            'immediate_actions': [],
            'short_term_strategies': [],
            'long_term_policies': [],
            'international_coordination': [],
            'resource_allocation': {}
        }

        overall_risk = risk_assessment.get('overall_risk_score', 0.5)
        critical_vulnerabilities = risk_assessment.get('critical_vulnerabilities', [])

        # Immediate actions based on risk level
        if overall_risk > 0.8:
            recommendations['immediate_actions'].extend([
                'Activate emergency response protocols',
                'Establish crisis command center',
                'Initiate evacuation procedures for high-risk areas',
                'Deploy emergency medical resources'
            ])
        elif overall_risk > 0.6:
            recommendations['immediate_actions'].extend([
                'Heighten alert status for relevant agencies',
                'Pre-position emergency resources',
                'Increase intelligence gathering'
            ])

        # Recommendations based on specific vulnerabilities
        if 'military_risk' in critical_vulnerabilities:
            recommendations['immediate_actions'].append('Activate missile defense systems')
            recommendations['short_term_strategies'].append('Strengthen defense capabilities')

        if 'economic_risk' in critical_vulnerabilities:
            recommendations['immediate_actions'].append('Implement economic stabilization measures')
            recommendations['short_term_strategies'].append('Diversify supply chains')

        if 'social_risk' in critical_vulnerabilities:
            recommendations['immediate_actions'].append('Enhance social support systems')
            recommendations['short_term_strategies'].append('Strengthen community resilience programs')

        # Long-term policy recommendations
        recommendations['long_term_policies'] = [
            'Develop comprehensive national resilience strategy',
            'Invest in critical infrastructure hardening',
            'Establish international cooperation frameworks',
            'Create adaptive governance mechanisms'
        ]

        # International coordination needs
        if overall_risk > 0.6:
            recommendations['international_coordination'] = [
                'Engage multilateral organizations',
                'Coordinate with regional allies',
                'Establish information sharing protocols',
                'Develop joint response capabilities'
            ]

        # Resource allocation recommendations
        recommendations['resource_allocation'] = self._generate_resource_allocation_recommendations(
            risk_assessment, integrated_analysis
        )

        return recommendations

    def _calculate_confidence_levels(self, model_results):
        """Calculate confidence levels for model predictions"""
        confidence_analysis = {
            'overall_confidence': 0.0,
            'model_confidence': {},
            'data_quality_scores': {},
            'uncertainty_sources': []
        }

        model_confidences = {}

        # Assess confidence for each model
        for model_name, results in model_results.items():
            if model_name == 'military':
                # Military model confidence based on data completeness
                confidence = 0.8  # High confidence for well-established models
                if 'trajectory' in results and 'casualty_analysis' in results:
                    confidence = min(0.9, confidence + 0.1)
            elif model_name == 'economic':
                # Economic model confidence
                confidence = 0.7  # Moderate confidence due to complexity
            elif model_name == 'population':
                # Population model confidence
                confidence = 0.8  # Good confidence for demographic data
            elif model_name == 'infrastructure':
                # Infrastructure model confidence
                confidence = 0.6  # Lower confidence due to system complexity
            else:
                confidence = 0.6  # Default moderate confidence

            model_confidences[model_name] = confidence

        # Calculate overall confidence
        if model_confidences:
            confidence_analysis['overall_confidence'] = float(np.mean(list(model_confidences.values())))
        else:
            confidence_analysis['overall_confidence'] = 0.5

        confidence_analysis['model_confidence'] = model_confidences

        # Assess data quality
        confidence_analysis['data_quality_scores'] = self._assess_data_quality(model_results)

        # Identify uncertainty sources
        confidence_analysis['uncertainty_sources'] = [
            'Model parameter uncertainty',
            'Scenario complexity',
            'Data limitations',
            'Model interaction effects'
        ]

        return confidence_analysis

    def _identify_cross_model_interactions(self, model_results):
        """Identify significant interactions between different model results"""
        interactions = {}

        # Military-Economic interactions
        if 'military' in model_results and 'economic' in model_results:
            military_casualties = model_results['military'].get('casualty_analysis', {}).get('immediate_casualties', 0)
            economic_damage = model_results['economic'].get('economic_damage', {}).get('total_damage_usd', 0)

            # Military action amplifies economic damage
            amplification_factor = 1 + (military_casualties / 100000) * 0.5
            adjusted_economic_damage = economic_damage * amplification_factor

            interactions['military_economic'] = {
                'casualty_economic_multiplier': float(amplification_factor),
                'adjusted_economic_damage': float(adjusted_economic_damage),
                'confidence_in_economic_systems': float(max(0.1, 1.0 - (military_casualties / 1000000)))
            }

        # Population-Infrastructure interactions
        if 'population' in model_results and 'infrastructure' in model_results:
            displaced_population = model_results['population'].get('displacement_analysis', {}).get('total_displaced', 0)
            infrastructure_damage = model_results['infrastructure'].get('service_disruptions', {})

            # Population displacement affects infrastructure recovery
            recovery_delay_factor = 1 + (displaced_population / 100000) * 0.3

            interactions['population_infrastructure'] = {
                'displacement_recovery_delay': float(recovery_delay_factor),
                'workforce_availability': float(max(0.2, 1.0 - (displaced_population / 500000))),
                'infrastructure_maintenance_capacity': float(max(0.1, 1.0 - (displaced_population / 200000)))
            }

        # Economic-Social interactions
        if 'economic' in model_results and ('population' in model_results or 'psychological' in model_results):
            economic_damage_percent = 0
            if 'economic' in model_results:
                economic_damage_percent = model_results['economic'].get('economic_damage', {}).get('gdp_impact_percent', 0)

            # Economic damage affects social cohesion
            social_stress_multiplier = 1 + (economic_damage_percent / 10) * 0.8

            interactions['economic_social'] = {
                'economic_social_stress_multiplier': float(social_stress_multiplier),
                'unemployment_social_impact': float(economic_damage_percent * 2.5),
                'social_unrest_probability': float(min(0.8, economic_damage_percent / 20))
            }

        # Geographic-All Models interactions
        if 'geographic' in model_results:
            geographic_factors = model_results['geographic']
            terrain_accessibility = geographic_factors.get('logistics_factors', {}).get('accessibility_factor', 1.0)

            interactions['geographic_amplifiers'] = {
                'terrain_difficulty_multiplier': float(2.0 - terrain_accessibility),
                'logistics_constraint_factor': float(terrain_accessibility),
                'evacuation_difficulty': float(2.0 - terrain_accessibility),
                'recovery_access_factor': float(terrain_accessibility)
            }

        return interactions

    def _identify_feedback_loops(self, model_results):
        """Identify feedback loops between different systems"""
        feedback_loops = {}

        # Economic-Social feedback loop
        if 'economic' in model_results and 'population' in model_results:
            economic_impact = model_results['economic'].get('economic_damage', {}).get('gdp_impact_percent', 0)
            social_displacement = model_results['population'].get('displacement_analysis', {}).get('displacement_rate_percent', 0)

            # Economic damage causes social displacement, which further damages economy
            loop_strength = min(1.0, (economic_impact + social_displacement) / 50)
            feedback_loops['economic_social_loop'] = {
                'initial_economic_impact': float(economic_impact),
                'induced_social_displacement': float(social_displacement),
                'feedback_economic_damage': float(social_displacement * 0.5),  # Additional economic damage
                'loop_strength': float(loop_strength),
                'stabilization_time_months': int(12 * loop_strength)
            }

        # Infrastructure-Economic feedback loop
        if 'infrastructure' in model_results and 'economic' in model_results:
            infrastructure_disruption = float(np.mean([
                service.get('disruption_rate', 0) 
                for service in model_results['infrastructure'].get('service_disruptions', {}).values()
            ]) if model_results['infrastructure'].get('service_disruptions') else 0)

            feedback_loops['infrastructure_economic_loop'] = {
                'infrastructure_disruption': float(infrastructure_disruption),
                'economic_recovery_delay': float(infrastructure_disruption * 0.8),
                'infrastructure_investment_shortage': float(infrastructure_disruption * 0.6),
                'loop_strength': float(infrastructure_disruption)
            }

        # Population-Security feedback loop
        if 'population' in model_results and 'military' in model_results:
            population_stress = model_results['population'].get('stress_indicators', {}).get('overall_stress', 0)

            feedback_loops['population_security_loop'] = {
                'population_stress': float(population_stress),
                'security_deterioration': float(population_stress * 0.4),
                'increased_military_response': float(population_stress * 0.3),
                'civilian_military_tension': float(population_stress * 0.5)
            }

        return feedback_loops

    def _assess_system_vulnerabilities(self, model_results):
        """Assess system-wide vulnerabilities"""
        vulnerabilities = {
            'cascade_vulnerability': 0.0,
            'single_point_failures': [],
            'critical_dependencies': [],
            'resilience_gaps': []
        }

        # Assess cascade vulnerability
        cascade_factors = []

        if 'infrastructure' in model_results:
            infrastructure_interconnection = 0.8  # High infrastructure interconnection
            cascade_factors.append(infrastructure_interconnection)

        if 'economic' in model_results:
            economic_interdependence = 0.7  # High economic interdependence
            cascade_factors.append(economic_interdependence)

        if 'supply_chain' in model_results:
            supply_chain_concentration = 0.9  # High supply chain concentration
            cascade_factors.append(supply_chain_concentration)

        if cascade_factors:
            vulnerabilities['cascade_vulnerability'] = float(np.mean(cascade_factors))

        # Identify single point failures
        vulnerabilities['single_point_failures'] = [
            'Critical infrastructure nodes',
            'Key transportation hubs',
            'Essential supply chain links',
            'Financial system components'
        ]

        # Identify critical dependencies
        vulnerabilities['critical_dependencies'] = [
            'Energy supply systems',
            'Communication networks',
            'Water distribution systems',
            'Food supply chains'
        ]

        # Identify resilience gaps
        vulnerabilities['resilience_gaps'] = [
            'Insufficient backup systems',
            'Limited alternative supply routes',
            'Inadequate emergency reserves',
            'Weak coordination mechanisms'
        ]

        return vulnerabilities

    def _evaluate_resilience_factors(self, model_results):
        """Evaluate factors that contribute to system resilience"""
        resilience_factors = {
            'overall_resilience_score': 0.0,
            'structural_resilience': 0.0,
            'social_resilience': 0.0,
            'economic_resilience': 0.0,
            'adaptive_capacity': 0.0
        }

        # Assess structural resilience
        if 'infrastructure' in model_results:
            infrastructure_redundancy = 0.6  # Moderate infrastructure redundancy
            resilience_factors['structural_resilience'] = float(infrastructure_redundancy)

        # Assess social resilience
        if 'population' in model_results:
            social_cohesion = model_results['population'].get('social_cohesion', {}).get('cohesion_index', 0.7)
            resilience_factors['social_resilience'] = float(social_cohesion)

        # Assess economic resilience
        if 'economic' in model_results:
            economic_diversity = 0.7  # Moderate economic diversity
            resilience_factors['economic_resilience'] = float(economic_diversity)

        # Assess adaptive capacity
        adaptive_factors = [
            0.8,  # Institutional capacity
            0.6,  # Learning capability
            0.7,  # Innovation capacity
            0.5   # Flexibility
        ]
        resilience_factors['adaptive_capacity'] = float(np.mean(adaptive_factors))

        # Calculate overall resilience
        resilience_scores = [score for score in resilience_factors.values() if isinstance(score, (int, float))]
        if resilience_scores:
            resilience_factors['overall_resilience_score'] = float(np.mean(resilience_scores))

        return resilience_factors

    def _estimate_infrastructure_casualties(self, infrastructure_results):
        """Estimate casualties from infrastructure failures"""
        total_casualties = 0

        service_disruptions = infrastructure_results.get('service_disruptions', {})

        # Estimate casualties from different infrastructure failures
        if 'healthcare' in service_disruptions:
            healthcare_disruption = service_disruptions['healthcare'].get('disruption_rate', 0)
            healthcare_casualties = int(healthcare_disruption * 10000)  # Rough estimate
            total_casualties += healthcare_casualties

        if 'water_systems' in service_disruptions:
            water_disruption = service_disruptions['water_systems'].get('disruption_rate', 0)
            water_casualties = int(water_disruption * 5000)  # Rough estimate
            total_casualties += water_casualties

        if 'energy' in service_disruptions:
            energy_disruption = service_disruptions['energy'].get('disruption_rate', 0)
            energy_casualties = int(energy_disruption * 3000)  # Rough estimate
            total_casualties += energy_casualties

        return total_casualties

    def _estimate_psychological_mortality(self, psychological_results):
        """Estimate mortality from psychological impacts"""
        psychological_mortality = 0

        mental_health = psychological_results.get('mental_health_outcomes', {})

        # Estimate mortality from severe mental health impacts
        if 'ptsd' in mental_health:
            ptsd_prevalence = mental_health['ptsd'].get('prevalence_rate', 0)
            ptsd_mortality = int(ptsd_prevalence * 1000)  # Rough estimate
            psychological_mortality += ptsd_mortality

        if 'depression' in mental_health:
            depression_severity = mental_health['depression'].get('severity_score', 0)
            depression_mortality = int(depression_severity * 500)  # Rough estimate
            psychological_mortality += depression_mortality

        return psychological_mortality

    def _generate_timeline_projections(self, integrated_analysis, scenario_config):
        """Generate timeline projections for scenario development"""
        duration_days = scenario_config.get('duration_days', 30)
        scenario_type = scenario_config.get('type', 'conflict')

        # Create timeline phases
        timeline_phases = self._define_timeline_phases(scenario_type, duration_days)

        # Project key metrics over time
        timeline_projections = {
            'phases': timeline_phases,
            'casualty_timeline': self._project_casualty_timeline(integrated_analysis, timeline_phases),
            'economic_impact_timeline': self._project_economic_timeline(integrated_analysis, timeline_phases),
            'infrastructure_recovery_timeline': self._project_infrastructure_timeline(integrated_analysis, timeline_phases),
            'social_recovery_timeline': self._project_social_timeline(integrated_analysis, timeline_phases),
            'escalation_probability_timeline': self._project_escalation_timeline(integrated_analysis, timeline_phases)
        }

        return timeline_projections

    def _project_casualty_timeline(self, integrated_analysis, timeline_phases):
        """Project casualty progression over time"""
        casualty_timeline = []

        compound_effects = integrated_analysis.get('compound_effects', {})
        total_casualties = compound_effects.get('total_casualty_burden', {}).get('total_casualties', 0)

        cumulative_casualties = 0
        for phase in timeline_phases:
            phase_duration = phase['end_day'] - phase['start_day']

            # Different casualty rates for different phases
            if phase['phase'] == 'initial_impact':
                phase_casualty_rate = 0.6  # 60% of casualties in initial impact
            elif phase['phase'] == 'escalation':
                phase_casualty_rate = 0.3  # 30% in escalation
            else:
                phase_casualty_rate = 0.1  # 10% in later phases

            phase_casualties = int(total_casualties * phase_casualty_rate)
            cumulative_casualties += phase_casualties

            casualty_timeline.append({
                'phase': phase['phase'],
                'day': int(phase['end_day']),
                'phase_casualties': int(phase_casualties),
                'cumulative_casualties': int(cumulative_casualties),
                'casualty_rate_per_day': float(phase_casualties / max(1, phase_duration))
            })

        return casualty_timeline

    def _project_economic_timeline(self, integrated_analysis, timeline_phases):
        """Project economic impact progression over time"""
        economic_timeline = []

        compound_effects = integrated_analysis.get('compound_effects', {})
        total_economic_damage = compound_effects.get('total_economic_impact', {}).get('total_damage_usd', 0)

        cumulative_damage = 0.0
        for phase in timeline_phases:
            # Different economic damage rates for different phases
            if phase['phase'] == 'initial_impact':
                phase_damage_rate = 0.4  # 40% of damage in initial impact
            elif phase['phase'] == 'escalation':
                phase_damage_rate = 0.4  # 40% in escalation
            else:
                phase_damage_rate = 0.2  # 20% in later phases

            phase_damage = total_economic_damage * phase_damage_rate
            cumulative_damage += phase_damage

            economic_timeline.append({
                'phase': phase['phase'],
                'day': int(phase['end_day']),
                'phase_damage_usd': float(phase_damage),
                'cumulative_damage_usd': float(cumulative_damage),
                'gdp_impact_percent': float((cumulative_damage / 25000000000000) * 100)  # Rough global GDP
            })

        return economic_timeline

    def _project_infrastructure_timeline(self, integrated_analysis, timeline_phases):
        """Project infrastructure recovery timeline"""
        infrastructure_timeline = []

        # Assume initial infrastructure damage
        initial_damage_rate = 0.7
        current_damage_rate = initial_damage_rate

        for phase in timeline_phases:
            # Recovery rates vary by phase
            if phase['phase'] in ['recovery', 'rebuilding']:
                recovery_rate = 0.1  # 10% recovery per phase
                current_damage_rate = max(0.1, current_damage_rate - recovery_rate)
            elif phase['phase'] == 'stabilization':
                recovery_rate = 0.05  # 5% recovery per phase
                current_damage_rate = max(0.1, current_damage_rate - recovery_rate)
            else:
                recovery_rate = 0.0  # No recovery during conflict

            infrastructure_timeline.append({
                'phase': phase['phase'],
                'day': int(phase['end_day']),
                'damage_rate': float(current_damage_rate),
                'operational_capacity': float(1.0 - current_damage_rate),
                'recovery_rate': float(recovery_rate)
            })

        return infrastructure_timeline

    def _project_social_timeline(self, integrated_analysis, timeline_phases):
        """Project social recovery timeline"""
        social_timeline = []

        compound_effects = integrated_analysis.get('compound_effects', {})
        initial_social_disruption = compound_effects.get('social_disruption', {}).get('total_disruption_score', 0.5)

        current_disruption = initial_social_disruption

        for phase in timeline_phases:
            # Social recovery rates
            if phase['phase'] in ['recovery', 'rebuilding']:
                recovery_rate = 0.08  # 8% recovery per phase
                current_disruption = max(0.1, current_disruption - recovery_rate)
            elif phase['phase'] == 'stabilization':
                recovery_rate = 0.04  # 4% recovery per phase
                current_disruption = max(0.1, current_disruption - recovery_rate)
            else:
                recovery_rate = 0.0  # No recovery during active conflict

            social_timeline.append({
                'phase': phase['phase'],
                'day': int(phase['end_day']),
                'social_disruption_score': float(current_disruption),
                'social_cohesion': float(1.0 - current_disruption),
                'recovery_rate': float(recovery_rate)
            })

        return social_timeline

    def _project_escalation_timeline(self, integrated_analysis, timeline_phases):
        """Project escalation probability timeline"""
        escalation_timeline = []

        base_escalation_prob = 0.3  # Base escalation probability

        for phase in timeline_phases:
            # Escalation probability varies by phase
            if phase['phase'] == 'initial_impact':
                phase_escalation_prob = base_escalation_prob * 0.8
            elif phase['phase'] == 'escalation':
                phase_escalation_prob = base_escalation_prob * 1.5
            elif phase['phase'] == 'sustained_conflict':
                phase_escalation_prob = base_escalation_prob * 1.2
            else:
                phase_escalation_prob = base_escalation_prob * 0.5

            escalation_timeline.append({
                'phase': phase['phase'],
                'day': int(phase['end_day']),
                'escalation_probability': float(min(0.9, phase_escalation_prob)),
                'de_escalation_opportunities': float(1.0 - phase_escalation_prob)
            })

        return escalation_timeline

    def _define_timeline_phases(self, scenario_type, duration_days):
        """Define timeline phases based on scenario type"""
        if scenario_type in ['conflict', 'war', 'military']:
            return [
                {'phase': 'initial_impact', 'start_day': 0, 'end_day': min(7, int(duration_days * 0.1))},
                {'phase': 'escalation', 'start_day': min(7, int(duration_days * 0.1)), 'end_day': min(30, int(duration_days * 0.3))},
                {'phase': 'sustained_conflict', 'start_day': min(30, int(duration_days * 0.3)), 'end_day': min(int(duration_days * 0.8), duration_days - 30)},
                {'phase': 'resolution_phase', 'start_day': max(duration_days - 30, int(duration_days * 0.8)), 'end_day': duration_days},
                {'phase': 'immediate_aftermath', 'start_day': duration_days, 'end_day': duration_days + 90},
                {'phase': 'recovery', 'start_day': duration_days + 90, 'end_day': duration_days + 365}
            ]
        elif scenario_type == 'economic':
            return [
                {'phase': 'initial_shock', 'start_day': 0, 'end_day': 14},
                {'phase': 'market_adjustment', 'start_day': 14, 'end_day': 60},
                {'phase': 'structural_adaptation', 'start_day': 60, 'end_day': duration_days},
                {'phase': 'recovery_phase', 'start_day': duration_days, 'end_day': duration_days + 180}
            ]
        else:  # Natural disaster or other
            return [
                {'phase': 'immediate_impact', 'start_day': 0, 'end_day': 3},
                {'phase': 'emergency_response', 'start_day': 3, 'end_day': 14},
                {'phase': 'stabilization', 'start_day': 14, 'end_day': 60},
                {'phase': 'recovery', 'start_day': 60, 'end_day': 365},
                {'phase': 'rebuilding', 'start_day': 365, 'end_day': 1095}  # 3 years
            ]

    def _generate_risk_mitigation_priorities(self, risk_categories):
        """Generate prioritized risk mitigation recommendations"""
        priorities = []

        # Sort risks by severity
        sorted_risks = sorted(risk_categories.items(), key=lambda x: x[1], reverse=True)

        for risk_type, risk_score in sorted_risks:
            if risk_score > 0.7:
                priorities.append(f"Critical: Address {risk_type} (score: {risk_score:.2f})")
            elif risk_score > 0.5:
                priorities.append(f"High: Mitigate {risk_type} (score: {risk_score:.2f})")
            elif risk_score > 0.3:
                priorities.append(f"Medium: Monitor {risk_type} (score: {risk_score:.2f})")

        return priorities

    def _assess_uncertainty_factors(self, integrated_analysis):
        """Assess factors contributing to uncertainty"""
        uncertainty_factors = [
            {'factor': 'Model complexity', 'impact': 0.3},
            {'factor': 'Data limitations', 'impact': 0.4},
            {'factor': 'Human behavior unpredictability', 'impact': 0.5},
            {'factor': 'External intervention probability', 'impact': 0.3},
            {'factor': 'Technological factors', 'impact': 0.2}
        ]

        return uncertainty_factors

    def _generate_resource_allocation_recommendations(self, risk_assessment, integrated_analysis):
        """Generate resource allocation recommendations"""
        total_budget = 1000000000  # Example: $1B budget

        allocations = {}
        risk_categories = risk_assessment.get('risk_categories', {})

        # Allocate based on risk severity
        total_risk_score = sum(risk_categories.values()) or 1

        for category, risk_score in risk_categories.items():
            proportion = risk_score / total_risk_score
            allocations[category] = {
                'budget_allocation': int(total_budget * proportion),
                'priority_level': 'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.4 else 'Low'
            }

        return allocations

    def _assess_data_quality(self, model_results):
        """Assess quality of data used in models"""
        quality_scores = {}

        for model_name in model_results.keys():
            # Simplified quality assessment
            if model_name in ['military', 'nuclear']:
                quality_scores[model_name] = 0.8  # High quality defense data
            elif model_name in ['economic', 'supply_chain']:
                quality_scores[model_name] = 0.7  # Good economic data
            else:
                quality_scores[model_name] = 0.6  # Moderate quality

        return quality_scores

    def run_experiment(self, experiment_id, experiment_config):
        """Run a built-in experiment scenario"""
        if experiment_id == 'india_pakistan_conflict':
            return self._run_india_pakistan_experiment(experiment_config)
        elif experiment_id == 'china_taiwan_scenario':
            return self._run_china_taiwan_experiment(experiment_config)
        elif experiment_id == 'middle_east_oil_crisis':
            return self._run_oil_crisis_experiment(experiment_config)
        elif experiment_id == 'pandemic_economic_collapse':
            return self._run_pandemic_experiment(experiment_config)
        elif experiment_id == 'cyber_warfare_escalation':
            return self._run_cyber_warfare_experiment(experiment_config)
        elif experiment_id == 'climate_refugee_crisis':
            return self._run_climate_refugee_experiment(experiment_config)
        else:
            raise ValueError(f"Unknown experiment ID: {experiment_id}")

    def _run_india_pakistan_experiment(self, config):
        """Run comprehensive India-Pakistan conflict scenario"""
        scenario_config = {
            'id': f'india_pakistan_{int(time.time())}',
            'type': 'conflict',
            'attacker_country': 'Pakistan',
            'defender_country': 'India',
            'countries_involved': ['India', 'Pakistan', 'China', 'USA'],
            'duration_days': 45,
            'intensity': 'high',
            'escalation_level': 'strategic',
            'nuclear_escalation': True,
            'population_size': 50000000,  # Affected population in border regions
            'location': 'Kashmir',
            'location_type': 'mountainous',
            'terrain_type': 'mountainous',
            'climate_zone': 'continental',
            'elevation_m': 2500,
            'cultural_region': 'south_asia',
            'missile_threat': {
                'launch_coords': [33.7782, 73.0610],  # Islamabad area
                'target_coords': [28.6139, 77.2090],  # Delhi area
                'missile_type': 'ballistic_missiles',
                'missile_subtype': 'IRBM',
                'weapon_type': 'nuclear'
            },
            'defense_systems': ['S-400', 'Akash', 'Iron Dome'],
            'target_area_data': {
                'population_density': 25000,
                'area_type': 'urban',
                'protection_level': 0.15,
                'building_density': 0.7,
                'time_of_day': 'day'
            },
            'economic_warfare': True,
            'supply_chain_disruption': {
                'affected_nodes': ['India', 'Pakistan', 'China'],
                'affected_materials': ['textiles', 'agriculture', 'pharmaceuticals'],
                'disruption_intensity': 0.8
            },
            'infrastructure_impact': {
                'profile': {
                    'transportation': 0.6,
                    'energy': 0.8,
                    'telecommunications': 0.7,
                    'water_systems': 0.5
                }
            }
        }

        return self.run_comprehensive_analysis(scenario_config)

    def _run_china_taiwan_experiment(self, config):
        """Run comprehensive China-Taiwan scenario"""
        scenario_config = {
            'id': f'china_taiwan_{int(time.time())}',
            'type': 'conflict',
            'attacker_country': 'China',
            'defender_country': 'Taiwan',
            'countries_involved': ['China', 'Taiwan', 'USA', 'Japan'],
            'duration_days': 60,
            'intensity': 'extreme',
            'escalation_level': 'strategic',
            'nuclear_escalation': False,
            'population_size': 23000000,
            'location': 'Taiwan',
            'location_type': 'island',
            'terrain_type': 'coastal',
            'climate_zone': 'subtropical',
            'elevation_m': 200,
            'cultural_region': 'east_asia'
        }

        return self.run_comprehensive_analysis(scenario_config)

    def _run_oil_crisis_experiment(self, config):
        """Run Middle East oil crisis scenario"""
        scenario_config = {
            'id': f'oil_crisis_{int(time.time())}',
            'type': 'economic',
            'warfare_type': 'supply_chain_disruption',
            'intensity': 'extreme',
            'duration_days': 180,
            'supply_chain_disruption': {
                'affected_nodes': ['Saudi Arabia', 'Iran', 'Iraq'],
                'affected_materials': ['oil_gas'],
                'disruption_intensity': 0.9
            }
        }

        return self.run_comprehensive_analysis(scenario_config)

    def _run_pandemic_experiment(self, config):
        """Run pandemic economic collapse scenario"""
        scenario_config = {
            'id': f'pandemic_{int(time.time())}',
            'type': 'health_crisis',
            'population_size': 7800000000,  # Global population
            'duration_days': 365,
            'economic_warfare': True,
            'warfare_type': 'supply_chain_disruption',
            'intensity': 'high'
        }

        return self.run_comprehensive_analysis(scenario_config)

    def _run_cyber_warfare_experiment(self, config):
        """Run cyber warfare escalation scenario"""
        scenario_config = {
            'id': f'cyber_warfare_{int(time.time())}',
            'type': 'cyber',
            'warfare_type': 'cyber_warfare',
            'intensity': 'high',
            'duration_days': 90,
            'infrastructure_impact': {
                'profile': {
                    'telecommunications': 0.8,
                    'energy': 0.6,
                    'finance': 0.9,
                    'transportation': 0.4
                }
            }
        }

        return self.run_comprehensive_analysis(scenario_config)

    def _run_climate_refugee_experiment(self, config):
        """Run climate refugee crisis scenario"""
        scenario_config = {
            'id': f'climate_refugee_{int(time.time())}',
            'type': 'climate',
            'population_size': 200000000,  # Potential climate refugees
            'time_horizon_years': 30,
            'duration_days': 10950,  # 30 years
            'location': 'South Asia',
            'climate_zone': 'tropical'
        }

        return self.run_comprehensive_analysis(scenario_config)


class EscalationModel:
    """Model for analyzing escalation dynamics and probability"""

    def __init__(self):
        self.escalation_triggers = self._load_escalation_triggers()
        self.de_escalation_factors = self._load_de_escalation_factors()
        self.threshold_models = self._load_threshold_models()

    def _load_escalation_triggers(self):
        """Load escalation trigger mechanisms"""
        return {
            'military': {
                'casualty_threshold': 1000,
                'infrastructure_damage_threshold': 0.3,
                'territory_loss_threshold': 0.1,
                'civilian_casualties_threshold': 500
            },
            'economic': {
                'gdp_impact_threshold': 0.05,
                'unemployment_threshold': 0.08,
                'inflation_threshold': 0.15,
                'currency_devaluation_threshold': 0.25
            },
            'political': {
                'regime_stability_threshold': 0.6,
                'public_support_threshold': 0.4,
                'international_isolation_threshold': 0.7,
                'internal_cohesion_threshold': 0.5
            },
            'social': {
                'displacement_threshold': 0.2,
                'social_unrest_threshold': 0.3,
                'institutional_breakdown_threshold': 0.4,
                'ethnic_tension_threshold': 0.6
            }
        }

    def _load_de_escalation_factors(self):
        """Load de-escalation factor mechanisms"""
        return {
            'diplomatic': {
                'international_mediation': 0.3,
                'bilateral_dialogue': 0.2,
                'regional_organizations': 0.25,
                'economic_incentives': 0.15
            },
            'economic': {
                'economic_interdependence': 0.4,
                'trade_relationships': 0.3,
                'investment_ties': 0.2,
                'development_aid': 0.1
            },
            'military': {
                'deterrence_capability': 0.5,
                'alliance_support': 0.3,
                'peacekeeping_forces': 0.2
            },
            'social': {
                'civil_society_pressure': 0.3,
                'public_opinion': 0.4,
                'cultural_ties': 0.2,
                'humanitarian_concerns': 0.1
            }
        }

    def _load_threshold_models(self):
        """Load threshold models for escalation"""
        return {
            'linear': {'type': 'linear', 'sensitivity': 1.0},
            'exponential': {'type': 'exponential', 'sensitivity': 1.5},
            'step_function': {'type': 'step', 'sensitivity': 0.8},
            'logarithmic': {'type': 'log', 'sensitivity': 0.6}
        }

    def calculate_escalation_probability(self, current_state, scenario_config, time_period_days):
        """Calculate probability of scenario escalation"""
        escalation_factors = {}

        # Analyze each category of escalation triggers
        for category, thresholds in self.escalation_triggers.items():
            category_risk = self._assess_category_escalation_risk(
                category, thresholds, current_state
            )
            escalation_factors[category] = category_risk

        # Calculate base escalation probability
        base_escalation_prob = sum(factor['risk_level'] for factor in escalation_factors.values()) / len(escalation_factors)

        # Apply time-dependent factors
        time_factor = self._calculate_time_escalation_factor(time_period_days)

        # Apply scenario-specific modifiers
        scenario_modifier = self._calculate_scenario_escalation_modifier(scenario_config)

        # Calculate final escalation probability
        final_escalation_prob = min(0.95, base_escalation_prob * time_factor * scenario_modifier)

        return {
            'escalation_probability': final_escalation_prob,
            'escalation_factors': escalation_factors,
            'time_factor': time_factor,
            'scenario_modifier': scenario_modifier,
            'escalation_triggers_activated': [
                category for category, factor in escalation_factors.items()
                if factor['risk_level'] > 0.7
            ],
            'de_escalation_opportunities': self._identify_de_escalation_opportunities(escalation_factors)
        }

    def _assess_category_escalation_risk(self, category, thresholds, current_state):
        """Assess escalation risk for a specific category"""
        risk_level = 0.0
        triggered_thresholds = []

        # Check each threshold in the category
        for threshold_name, threshold_value in thresholds.items():
            current_value = current_state.get(threshold_name, 0)

            if isinstance(threshold_value, (int, float)):
                if current_value > threshold_value:
                    risk_level += 0.25  # Each triggered threshold adds 25% risk
                    triggered_thresholds.append(threshold_name)

        return {
            'risk_level': min(1.0, risk_level),
            'triggered_thresholds': triggered_thresholds,
            'category': category
        }

    def _calculate_time_escalation_factor(self, time_period_days):
        """Calculate time-dependent escalation factor"""
        # Escalation probability increases with time but plateaus
        if time_period_days <= 7:
            return 0.8  # Lower probability in first week
        elif time_period_days <= 30:
            return 1.0  # Baseline probability in first month
        elif time_period_days <= 90:
            return 1.2  # Higher probability as conflict continues
        else:
            return 1.1  # Slightly lower as situations stabilize

    def _calculate_scenario_escalation_modifier(self, scenario_config):
        """Calculate scenario-specific escalation modifier"""
        modifier = 1.0

        scenario_type = scenario_config.get('type', 'conflict')
        intensity = scenario_config.get('intensity', 'medium')

        # Scenario type modifiers
        if scenario_type == 'nuclear':
            modifier *= 1.5
        elif scenario_type == 'conflict':
            modifier *= 1.2
        elif scenario_type == 'economic':
            modifier *= 0.8

        # Intensity modifiers
        intensity_modifiers = {
            'low': 0.7,
            'medium': 1.0,
            'high': 1.3,
            'extreme': 1.6
        }
        modifier *= intensity_modifiers.get(intensity, 1.0)

        # Nuclear escalation modifier
        if scenario_config.get('nuclear_escalation', False):
            modifier *= 1.4

        return modifier

    def _identify_de_escalation_opportunities(self, escalation_factors):
        """Identify opportunities for de-escalation"""
        opportunities = []

        # Check overall escalation level
        avg_escalation = np.mean([factor['risk_level'] for factor in escalation_factors.values()])

        if avg_escalation < 0.5:
            opportunities.extend([
                'Diplomatic engagement window available',
                'Economic incentives could be effective',
                'Civil society pressure could influence decision-makers'
            ])
        elif avg_escalation < 0.7:
            opportunities.extend([
                'International mediation recommended',
                'Alliance pressure could be effective',
                'Economic costs argument could work'
            ])
        else:
            opportunities.extend([
                'Urgent international intervention needed',
                'Military deterrence may be only option',
                'Humanitarian concerns could provide leverage'
            ])

        return opportunities


class GlobalResponseModel:
    """Model for international and global response to scenarios"""

    def __init__(self):
        self.country_relationships = self._load_country_relationships()
        self.international_organizations = self._load_international_organizations()
        self.response_mechanisms = self._load_response_mechanisms()

    def _load_country_relationships(self):
        """Load country relationship data"""
        return {
            'USA': {
                'allies': ['NATO', 'Japan', 'Australia', 'South Korea'],
                'rivals': ['China', 'Russia', 'Iran'],
                'neutral': ['India', 'Brazil', 'South Africa'],
                'influence_score': 0.9
            },
            'China': {
                'allies': ['Russia', 'Pakistan', 'North Korea'],
                'rivals': ['USA', 'India', 'Japan'],
                'neutral': ['EU', 'Brazil', 'ASEAN'],
                'influence_score': 0.8
            },
            'Russia': {
                'allies': ['China', 'Belarus', 'Kazakhstan'],
                'rivals': ['USA', 'NATO', 'Ukraine'],
                'neutral': ['India', 'Turkey', 'Iran'],
                'influence_score': 0.6
            }
        }

    def _load_international_organizations(self):
        """Load international organization data"""
        return {
            'UN_Security_Council': {
                'response_speed': 'slow',
                'effectiveness': 0.6,
                'veto_powers': ['USA', 'Russia', 'China', 'UK', 'France']
            },
            'NATO': {
                'response_speed': 'fast',
                'effectiveness': 0.8,
                'members': ['USA', 'UK', 'France', 'Germany', 'Turkey']
            },
            'EU': {
                'response_speed': 'medium',
                'effectiveness': 0.7,
                'economic_leverage': 0.9
            },
            'G20': {
                'response_speed': 'slow',
                'effectiveness': 0.5,
                'economic_coordination': 0.8
            }
        }

    def _load_response_mechanisms(self):
        """Load response mechanism data"""
        return {
            'diplomatic': {
                'bilateral_talks': {'speed': 'fast', 'effectiveness': 0.6},
                'multilateral_mediation': {'speed': 'medium', 'effectiveness': 0.7},
                'international_arbitration': {'speed': 'slow', 'effectiveness': 0.8}
            },
            'economic': {
                'sanctions': {'speed': 'fast', 'effectiveness': 0.7},
                'trade_restrictions': {'speed': 'medium', 'effectiveness': 0.6},
                'financial_isolation': {'speed': 'fast', 'effectiveness': 0.8}
            },
            'military': {
                'deterrence': {'speed': 'fast', 'effectiveness': 0.8},
                'peacekeeping': {'speed': 'slow', 'effectiveness': 0.6},
                'intervention': {'speed': 'medium', 'effectiveness': 0.9}
            }
        }

    def model_global_response(self, scenario_config, scenario_results):
        """Model comprehensive global response to scenario"""
        primary_actors = scenario_config.get('countries_involved', [])
        scenario_type = scenario_config.get('type', 'conflict')
        scenario_severity = self._assess_scenario_severity(scenario_results)

        global_response = {
            'immediate_responses': {},
            'diplomatic_initiatives': {},
            'economic_measures': {},
            'military_responses': {},
            'humanitarian_aid': {},
            'long_term_implications': {}
        }

        # Analyze immediate international responses
        global_response['immediate_responses'] = self._model_immediate_responses(
            primary_actors, scenario_type, scenario_severity
        )

        # Model diplomatic initiatives
        global_response['diplomatic_initiatives'] = self._model_diplomatic_responses(
            primary_actors, scenario_type, scenario_severity
        )

        # Analyze economic response measures
        global_response['economic_measures'] = self._model_economic_responses(
            primary_actors, scenario_type, scenario_severity, scenario_results
        )

        # Model potential military responses
        if scenario_type in ['conflict', 'military', 'war']:
            global_response['military_responses'] = self._model_military_responses(
                primary_actors, scenario_severity
            )

        # Calculate humanitarian aid requirements and responses
        global_response['humanitarian_aid'] = self._model_humanitarian_response(
            scenario_results, scenario_severity
        )

        # Assess long-term geopolitical implications
        global_response['long_term_implications'] = self._assess_long_term_implications(
            primary_actors, scenario_type, scenario_results
        )

        return global_response

    def _assess_scenario_severity(self, scenario_results):
        """Assess overall severity of scenario for international response"""
        severity_factors = {
            'casualty_severity': 0.0,
            'economic_severity': 0.0,
            'infrastructure_severity': 0.0,
            'social_severity': 0.0,
            'regional_stability_impact': 0.0
        }

        # Assess casualty severity
        if 'model_results' in scenario_results:
            model_results = scenario_results['model_results']

            if 'military' in model_results:
                casualties = model_results['military'].get('casualty_analysis', {}).get('immediate_casualties', 0)
                severity_factors['casualty_severity'] = float(min(1.0, casualties / 100000))  # Scale to 100k casualties = max

            if 'economic' in model_results:
                economic_damage = model_results['economic'].get('economic_damage', {}).get('gdp_impact_percent', 0)
                severity_factors['economic_severity'] = float(min(1.0, economic_damage / 20))  # Scale to 20% GDP impact = max

            if 'infrastructure' in model_results:
                infrastructure_impact = model_results['infrastructure'].get('service_disruptions', {})
                avg_disruption = float(np.mean([
                    service.get('disruption_rate', 0)
                    for service in infrastructure_impact.values()
                ]) if infrastructure_impact else 0)
                severity_factors['infrastructure_severity'] = avg_disruption

            if 'population' in model_results:
                displacement_rate = model_results['population'].get('displacement_analysis', {}).get('displacement_rate_percent', 0)
                severity_factors['social_severity'] = float(min(1.0, displacement_rate / 50))  # Scale to 50% displacement = max

        # Calculate regional stability impact
        severity_factors['regional_stability_impact'] = float(np.mean(list(severity_factors.values())))

        # Calculate overall severity score
        overall_severity = float(np.mean(list(severity_factors.values())))

        return {
            'overall_severity_score': overall_severity,
            'severity_factors': severity_factors,
            'severity_category': self._categorize_severity(overall_severity)
        }

    def _categorize_severity(self, severity_score):
        """Categorize severity score into levels"""
        if severity_score < 0.2:
            return 'low'
        elif severity_score < 0.4:
            return 'moderate'
        elif severity_score < 0.6:
            return 'high'
        elif severity_score < 0.8:
            return 'severe'
        else:
            return 'extreme'

    def _model_immediate_responses(self, primary_actors, scenario_type, scenario_severity):
        """Model immediate international responses"""
        responses = {}

        severity_category = scenario_severity['severity_category']

        # Major power responses
        major_powers = ['USA', 'China', 'Russia', 'EU']

        for power in major_powers:
            if power not in primary_actors:  # Neutral powers
                if severity_category in ['severe', 'extreme']:
                    responses[power] = {
                        'diplomatic_engagement': 'high',
                        'economic_measures': 'medium',
                        'military_posturing': 'medium',
                        'humanitarian_aid': 'high'
                    }
                elif severity_category == 'high':
                    responses[power] = {
                        'diplomatic_engagement': 'medium',
                        'economic_measures': 'low',
                        'military_posturing': 'low',
                        'humanitarian_aid': 'medium'
                    }
                else:
                    responses[power] = {
                        'diplomatic_engagement': 'low',
                        'economic_measures': 'none',
                        'military_posturing': 'none',
                        'humanitarian_aid': 'low'
                    }

        return responses

    def _model_diplomatic_responses(self, primary_actors, scenario_type, scenario_severity):
        """Model diplomatic response initiatives"""
        diplomatic_responses = {
            'un_security_council_action': False,
            'regional_organization_involvement': [],
            'bilateral_mediation_efforts': [],
            'international_arbitration': False
        }

        severity_category = scenario_severity['severity_category']

        # UN Security Council involvement
        if severity_category in ['high', 'severe', 'extreme']:
            diplomatic_responses['un_security_council_action'] = True

        # Regional organization involvement
        if any(actor in ['India', 'Pakistan'] for actor in primary_actors):
            diplomatic_responses['regional_organization_involvement'].append('SAARC')
        if any(actor in ['China', 'Taiwan', 'Japan'] for actor in primary_actors):
            diplomatic_responses['regional_organization_involvement'].append('ASEAN')

        # Bilateral mediation
        if severity_category in ['severe', 'extreme']:
            diplomatic_responses['bilateral_mediation_efforts'] = ['USA', 'EU', 'UN']

        # International arbitration
        if scenario_type in ['territorial', 'resource']:
            diplomatic_responses['international_arbitration'] = True

        return diplomatic_responses

    def _model_economic_responses(self, primary_actors, scenario_type, scenario_severity, scenario_results):
        """Model economic response measures"""
        economic_responses = {
            'sanctions_regime': {},
            'trade_restrictions': {},
            'financial_measures': {},
            'development_aid': {}
        }

        severity_category = scenario_severity['severity_category']

        # Sanctions
        if severity_category in ['severe', 'extreme']:
            for actor in primary_actors:
                if actor in ['Russia', 'China', 'Iran']:  # Typical sanction targets
                    economic_responses['sanctions_regime'][actor] = {
                        'type': 'comprehensive',
                        'sectors': ['finance', 'energy', 'technology', 'defense'],
                        'international_coordination': 'high'
                    }

        # Trade restrictions
        if scenario_type == 'economic':
            economic_responses['trade_restrictions'] = {
                'tariffs': 'increased',
                'export_controls': 'enhanced',
                'investment_screening': 'strengthened'
            }

        return economic_responses

    def _model_military_responses(self, primary_actors, scenario_severity):
        """Model military response measures"""
        military_responses = {
            'deterrence_measures': [],
            'alliance_activation': [],
            'peacekeeping_deployment': False,
            'military_aid': {}
        }

        severity_category = scenario_severity['severity_category']

        # Deterrence measures
        if severity_category in ['severe', 'extreme']:
            military_responses['deterrence_measures'] = [
                'Increased military exercises',
                'Enhanced force readiness',
                'Strategic asset deployment'
            ]

        # Alliance activation
        if any(actor in ['NATO', 'USA', 'EU'] for actor in primary_actors):
            military_responses['alliance_activation'].append('NATO Article 5 consideration')

        # Peacekeeping
        if severity_category == 'extreme':
            military_responses['peacekeeping_deployment'] = True

        return military_responses

    def _model_humanitarian_response(self, scenario_results, scenario_severity):
        """Model humanitarian aid response"""
        humanitarian_response = {
            'aid_requirement_usd': 0,
            'refugee_assistance': {},
            'medical_aid': {},
            'food_security': {}
        }

        # Calculate aid requirements based on casualties and displacement
        if 'model_results' in scenario_results:
            model_results = scenario_results['model_results']

            total_affected = 0
            if 'military' in model_results:
                total_affected += model_results['military'].get('casualty_analysis', {}).get('total_affected', 0)

            if 'population' in model_results:
                total_affected += model_results['population'].get('displacement_analysis', {}).get('total_displaced', 0)

            # Calculate aid requirement ($500 per affected person)
            humanitarian_response['aid_requirement_usd'] = int(total_affected * 500)

        return humanitarian_response

    def _assess_long_term_implications(self, primary_actors, scenario_type, scenario_results):
        """Assess long-term geopolitical implications"""
        implications = {
            'power_balance_shifts': {},
            'alliance_changes': [],
            'new_security_arrangements': [],
            'economic_realignments': []
        }

        # Power balance implications
        if 'USA' in primary_actors and 'China' in primary_actors:
            implications['power_balance_shifts']['us_china_competition'] = 'intensified'

        # Alliance implications
        if scenario_type == 'military':
            implications['alliance_changes'] = [
                'Strengthened regional alliances',
                'New defense partnerships',
                'Enhanced intelligence sharing'
            ]

        # Security arrangements
        implications['new_security_arrangements'] = [
            'Updated defense strategies',
            'New deterrence concepts',
            'Enhanced crisis management'
        ]

        # Economic realignments
        if 'economic' in scenario_type or 'supply_chain' in str(scenario_results):
            implications['economic_realignments'] = [
                'Supply chain diversification',
                'Strategic autonomy initiatives',
                'New trade partnerships'
            ]

        return implications
