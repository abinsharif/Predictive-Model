import numpy as np
import pandas as pd
import networkx as nx
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from collections import defaultdict
import math
import json

class PopulationModel:
    """Comprehensive population dynamics and demographic modeling system"""
    
    def __init__(self):
        self.demographic_data = self._load_demographic_data()
        self.migration_patterns = self._load_migration_patterns()
        self.urbanization_data = self._load_urbanization_data()
        self.infrastructure_capacity = self._load_infrastructure_capacity()

    def _load_demographic_data(self):
        """Load comprehensive demographic data for different regions"""
        return {
            'country_demographics': {
                'USA': {
                    'total_population': 331900000,
                    'population_density_per_km2': 36,
                    'urban_population_percent': 82.7,
                    'age_distribution': {
                        '0-14': 18.1, '15-24': 12.9, '25-54': 39.2, '55-64': 12.8, '65+': 17.0
                    },
                    'education_levels': {
                        'primary': 15, 'secondary': 45, 'tertiary': 40
                    },
                    'economic_sectors': {
                        'agriculture': 1.3, 'industry': 19.1, 'services': 79.6
                    },
                    'income_distribution_gini': 0.434
                },
                'Pakistan': {
                    'total_population': 231402117,
                    'population_density_per_km2': 287,
                    'urban_population_percent': 37.2,
                    'age_distribution': {
                        '0-14': 35.4, '15-24': 19.4, '25-54': 35.3, '55-64': 5.6, '65+': 4.3
                    },
                    'education_levels': {
                        'primary': 58, 'secondary': 32, 'tertiary': 10
                    },
                    'economic_sectors': {
                        'agriculture': 37.4, 'industry': 18.2, 'services': 44.4
                    },
                    'income_distribution_gini': 0.331
                },
                'India': {
                    'total_population': 1428627663,
                    'population_density_per_km2': 464,
                    'urban_population_percent': 35.9,
                    'age_distribution': {
                        '0-14': 25.3, '15-24': 17.5, '25-54': 41.5, '55-64': 9.4, '65+': 6.3
                    },
                    'education_levels': {
                        'primary': 48, 'secondary': 35, 'tertiary': 17
                    },
                    'economic_sectors': {
                        'agriculture': 41.9, 'industry': 24.7, 'services': 33.4
                    },
                    'income_distribution_gini': 0.472
                }
            },
            'community_types': {
                'rural_village': {
                    'population_range': [500, 5000],
                    'density_per_km2': 50,
                    'infrastructure_score': 3.2,
                    'economic_diversity': 2.1,
                    'social_cohesion': 8.5,
                    'disaster_resilience': 4.0
                },
                'small_town': {
                    'population_range': [5000, 25000],
                    'density_per_km2': 200,
                    'infrastructure_score': 5.8,
                    'economic_diversity': 4.5,
                    'social_cohesion': 7.2,
                    'disaster_resilience': 5.5
                },
                'medium_city': {
                    'population_range': [25000, 250000],
                    'density_per_km2': 800,
                    'infrastructure_score': 7.1,
                    'economic_diversity': 6.8,
                    'social_cohesion': 6.0,
                    'disaster_resilience': 6.8
                },
                'large_city': {
                    'population_range': [250000, 1000000],
                    'density_per_km2': 2500,
                    'infrastructure_score': 8.2,
                    'economic_diversity': 8.1,
                    'social_cohesion': 5.2,
                    'disaster_resilience': 7.8
                },
                'megacity': {
                    'population_range': [1000000, 20000000],
                    'density_per_km2': 5000,
                    'infrastructure_score': 7.8,
                    'economic_diversity': 9.2,
                    'social_cohesion': 4.5,
                    'disaster_resilience': 8.5
                }
            }
        }

    def _load_migration_patterns(self):
        """Load migration pattern data"""
        return {
            'seasonal_migration': {'rate': 0.05, 'distance_km': 50},
            'economic_migration': {'rate': 0.15, 'distance_km': 200},
            'crisis_migration': {'rate': 0.35, 'distance_km': 500},
            'return_rates': {'seasonal': 0.9, 'economic': 0.4, 'crisis': 0.2}
        }

    def _load_urbanization_data(self):
        """Load urbanization trend data"""
        return {
            'urban_growth_rate': 0.025,
            'rural_urban_migration': 0.03,
            'urbanization_factors': ['economic_opportunity', 'infrastructure', 'education']
        }

    def _load_infrastructure_capacity(self):
        """Load infrastructure capacity data"""
        return {
            'housing': {'capacity_per_1000': 400, 'overcrowding_threshold': 1.5},
            'healthcare': {'beds_per_1000': 3.2, 'doctors_per_1000': 2.1},
            'education': {'schools_per_1000': 2.5, 'teachers_per_100': 5.8},
            'utilities': {'water_capacity': 150, 'power_capacity': 1.5}
        }

    def analyze_population_impact(self, location_type, population_size, impact_scenario):
        """Analyze comprehensive population impact for different community sizes"""
        # Determine community characteristics
        community_profile = self._determine_community_profile(location_type, population_size)
        
        # Calculate direct population effects
        direct_effects = self._calculate_direct_population_effects(
            community_profile, impact_scenario
        )
        
        # Calculate infrastructure strain
        infrastructure_strain = self._calculate_infrastructure_strain(
            community_profile, impact_scenario
        )
        
        # Calculate social dynamics changes
        social_dynamics = self._calculate_social_dynamics_impact(
            community_profile, impact_scenario
        )
        
        # Calculate migration and displacement
        displacement_analysis = self._calculate_displacement_patterns(
            community_profile, impact_scenario
        )
        
        # Calculate recovery capacity
        recovery_capacity = self._calculate_community_recovery_capacity(
            community_profile, impact_scenario
        )
        
        return {
            'location_type': location_type,
            'population_size': population_size,
            'community_profile': community_profile,
            'impact_scenario': impact_scenario,
            'direct_effects': direct_effects,
            'infrastructure_strain': infrastructure_strain,
            'social_dynamics': social_dynamics,
            'displacement_analysis': displacement_analysis,
            'recovery_capacity': recovery_capacity,
            'long_term_projections': self._project_long_term_effects(
                direct_effects, recovery_capacity, impact_scenario
            )
        }

    def _determine_community_profile(self, location_type, population_size):
        """Determine detailed community profile based on type and size"""
        # Get base community type data
        if location_type in self.demographic_data['community_types']:
            base_profile = self.demographic_data['community_types'][location_type].copy()
        else:
            # Interpolate based on population size
            base_profile = self._interpolate_community_profile(population_size)
        
        # Adjust for actual population size
        base_profile['actual_population'] = population_size
        base_profile['area_km2'] = population_size / base_profile['density_per_km2']
        
        # Calculate derived metrics
        base_profile['households'] = int(population_size / 3.2)  # Average household size
        base_profile['workforce'] = int(population_size * 0.62)  # Working age percentage
        base_profile['children'] = int(population_size * 0.28)  # Children percentage
        base_profile['elderly'] = int(population_size * 0.10)  # Elderly percentage
        
        # Infrastructure capacity calculations
        base_profile['hospital_capacity'] = max(10, int(population_size / 1000))
        base_profile['school_capacity'] = int(population_size * 0.18)  # School-age children
        base_profile['housing_units'] = int(population_size / 3.0)
        base_profile['water_supply_capacity'] = population_size * 150  # Liters per day
        base_profile['power_grid_capacity_mw'] = population_size * 0.0015  # MW per capita
        
        return base_profile

    def _interpolate_community_profile(self, population_size):
        """Interpolate community profile for custom population sizes"""
        community_types = self.demographic_data['community_types']
        
        # Find appropriate community type based on population
        if population_size < 5000:
            return community_types['rural_village'].copy()
        elif population_size < 25000:
            return community_types['small_town'].copy()
        elif population_size < 250000:
            return community_types['medium_city'].copy()
        elif population_size < 1000000:
            return community_types['large_city'].copy()
        else:
            return community_types['megacity'].copy()

    def _calculate_direct_population_effects(self, community_profile, impact_scenario):
        """Calculate direct effects on population"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        duration = impact_scenario.get('duration_days', 30)
        
        # Base mortality rates by scenario type and intensity
        mortality_rates = {
            'conflict': {
                'low': 0.001, 'medium': 0.005, 'high': 0.015, 'extreme': 0.040
            },
            'natural_disaster': {
                'low': 0.0005, 'medium': 0.002, 'high': 0.008, 'extreme': 0.020
            },
            'economic_collapse': {
                'low': 0.0002, 'medium': 0.001, 'high': 0.004, 'extreme': 0.012
            },
            'pandemic': {
                'low': 0.005, 'medium': 0.015, 'high': 0.035, 'extreme': 0.060
            },
            'infrastructure_failure': {
                'low': 0.0003, 'medium': 0.0015, 'high': 0.006, 'extreme': 0.015
            }
        }
        
        base_mortality_rate = mortality_rates.get(scenario_type, mortality_rates['conflict'])[intensity]
        
        # Adjust for community characteristics
        mortality_modifier = 1.0
        
        # Infrastructure quality affects casualty rates
        infra_score = community_profile['infrastructure_score']
        if infra_score < 5:
            mortality_modifier += 0.5
        elif infra_score > 8:
            mortality_modifier -= 0.3
        
        # Population density affects spread of impact
        density = community_profile['density_per_km2']
        if density > 2000:
            mortality_modifier += 0.4  # High density increases casualties
        elif density < 100:
            mortality_modifier -= 0.2  # Low density reduces casualties
        
        # Duration effects
        duration_factor = min(2.0, 1.0 + (duration - 30) / 365)  # Longer duration = more impact
        final_mortality_rate = base_mortality_rate * mortality_modifier * duration_factor
        
        # Calculate casualties by demographic group
        total_population = community_profile['actual_population']
        casualties = {
            'total_casualties': int(total_population * final_mortality_rate),
            'children_casualties': int(community_profile['children'] * final_mortality_rate * 1.2),
            'elderly_casualties': int(community_profile['elderly'] * final_mortality_rate * 1.8),
            'working_age_casualties': int(community_profile['workforce'] * final_mortality_rate * 0.8)
        }
        
        # Calculate injured (typically 3-5x casualties)
        injury_multiplier = {'low': 2, 'medium': 3.5, 'high': 4.5, 'extreme': 5.5}[intensity]
        injuries = {
            'total_injured': int(casualties['total_casualties'] * injury_multiplier),
            'severe_injuries': int(casualties['total_casualties'] * injury_multiplier * 0.3),
            'moderate_injuries': int(casualties['total_casualties'] * injury_multiplier * 0.7)
        }
        
        return {
            'casualties': casualties,
            'injuries': injuries,
            'mortality_rate': final_mortality_rate,
            'affected_population_percent': (casualties['total_casualties'] + injuries['total_injured']) / total_population * 100,
            'demographic_impact': self._calculate_demographic_impact(casualties, community_profile)
        }

    def _calculate_demographic_impact(self, casualties, community_profile):
        """Calculate demographic impact of casualties"""
        total_population = community_profile['actual_population']
        
        return {
            'population_loss_percent': casualties['total_casualties'] / total_population * 100,
            'workforce_loss_percent': casualties['working_age_casualties'] / community_profile['workforce'] * 100,
            'dependency_ratio_change': (casualties['children_casualties'] + casualties['elderly_casualties']) / casualties['working_age_casualties'] if casualties['working_age_casualties'] > 0 else 0,
            'recovery_time_estimate_years': min(10, casualties['total_casualties'] / (total_population * 0.01))
        }

    def _calculate_infrastructure_strain(self, community_profile, impact_scenario):
        """Calculate strain on community infrastructure"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        
        # Infrastructure damage rates by scenario
        damage_rates = {
            'conflict': {
                'housing': {'low': 0.05, 'medium': 0.15, 'high': 0.35, 'extreme': 0.60},
                'healthcare': {'low': 0.10, 'medium': 0.25, 'high': 0.50, 'extreme': 0.75},
                'education': {'low': 0.08, 'medium': 0.20, 'high': 0.40, 'extreme': 0.65},
                'utilities': {'low': 0.15, 'medium': 0.30, 'high': 0.55, 'extreme': 0.80}
            },
            'natural_disaster': {
                'housing': {'low': 0.10, 'medium': 0.25, 'high': 0.50, 'extreme': 0.80},
                'healthcare': {'low': 0.05, 'medium': 0.15, 'high': 0.35, 'extreme': 0.60},
                'education': {'low': 0.08, 'medium': 0.18, 'high': 0.35, 'extreme': 0.65},
                'utilities': {'low': 0.20, 'medium': 0.40, 'high': 0.70, 'extreme': 0.90}
            }
        }
        
        scenario_damage = damage_rates.get(scenario_type, damage_rates['conflict'])
        infrastructure_strain = {}
        
        # Housing strain
        housing_damage_rate = scenario_damage['housing'][intensity]
        damaged_housing = int(community_profile['housing_units'] * housing_damage_rate)
        homeless_population = damaged_housing * 3.2  # Average household size
        
        infrastructure_strain['housing'] = {
            'damaged_units': damaged_housing,
            'homeless_population': int(homeless_population),
            'housing_shortage_percent': (damaged_housing / community_profile['housing_units']) * 100,
            'temporary_shelter_needed': int(homeless_population * 0.8)
        }
        
        # Healthcare strain
        healthcare_damage = scenario_damage['healthcare'][intensity]
        remaining_capacity = community_profile['hospital_capacity'] * (1 - healthcare_damage)
        healthcare_demand_multiplier = {'low': 1.5, 'medium': 2.5, 'high': 4.0, 'extreme': 6.0}[intensity]
        
        infrastructure_strain['healthcare'] = {
            'capacity_lost_percent': healthcare_damage * 100,
            'remaining_capacity': int(remaining_capacity),
            'demand_multiplier': healthcare_demand_multiplier,
            'capacity_shortage_percent': max(0, (healthcare_demand_multiplier - (1 - healthcare_damage)) * 100),
            'medical_supplies_depletion_days': max(1, 30 / healthcare_demand_multiplier)
        }
        
        # Utilities strain
        utilities_damage = scenario_damage['utilities'][intensity]
        infrastructure_strain['utilities'] = {
            'power_outage_percent': utilities_damage * 100,
            'water_supply_disruption_percent': utilities_damage * 80,  # Water usually more resilient
            'communication_disruption_percent': utilities_damage * 90,
            'sanitation_failure_percent': utilities_damage * 70,
            'estimated_restoration_days': int(utilities_damage * 60)  # More damage = longer restoration
        }
        
        return infrastructure_strain

    def _calculate_social_dynamics_impact(self, community_profile, impact_scenario):
        """Calculate impact on social structures and community dynamics"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        base_cohesion = community_profile['social_cohesion']
        
        # Social cohesion changes by scenario type
        cohesion_impacts = {
            'conflict': {'low': -1.2, 'medium': -2.8, 'high': -4.5, 'extreme': -6.2},
            'natural_disaster': {'low': +0.8, 'medium': +1.5, 'high': +0.5, 'extreme': -1.0},
            'economic_collapse': {'low': -0.5, 'medium': -1.8, 'high': -3.2, 'extreme': -5.0},
            'pandemic': {'low': -1.0, 'medium': -2.0, 'high': -3.5, 'extreme': -4.8}
        }
        
        cohesion_change = cohesion_impacts.get(scenario_type, cohesion_impacts['conflict'])[intensity]
        new_cohesion = max(1.0, min(10.0, base_cohesion + cohesion_change))
        
        # Calculate specific social impacts
        social_dynamics = {
            'social_cohesion_change': cohesion_change,
            'new_social_cohesion_score': new_cohesion,
            'community_organization_effectiveness': max(0.1, new_cohesion / 10),
            'social_unrest_probability': max(0, (10 - new_cohesion) / 10),
            'mutual_aid_networks_strength': new_cohesion * 0.8,
            'leadership_stability': max(0.2, 1.0 - abs(cohesion_change) * 0.15)
        }
        
        # Economic activity changes
        economic_impact_multipliers = {
            'conflict': {'low': 0.85, 'medium': 0.65, 'high': 0.40, 'extreme': 0.20},
            'natural_disaster': {'low': 0.80, 'medium': 0.60, 'high': 0.35, 'extreme': 0.15},
            'economic_collapse': {'low': 0.75, 'medium': 0.50, 'high': 0.25, 'extreme': 0.10}
        }
        
        economic_multiplier = economic_impact_multipliers.get(scenario_type, economic_impact_multipliers['conflict'])[intensity]
        social_dynamics['economic_activity_factor'] = economic_multiplier
        social_dynamics['unemployment_increase_percent'] = (1 - economic_multiplier) * 80
        social_dynamics['local_business_survival_rate'] = economic_multiplier
        
        return social_dynamics

    def _calculate_displacement_patterns(self, community_profile, impact_scenario):
        """Calculate population displacement and migration patterns"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        duration = impact_scenario.get('duration_days', 30)
        
        # Displacement rates by scenario and intensity
        displacement_rates = {
            'conflict': {'low': 0.15, 'medium': 0.35, 'high': 0.65, 'extreme': 0.85},
            'natural_disaster': {'low': 0.20, 'medium': 0.45, 'high': 0.70, 'extreme': 0.90},
            'economic_collapse': {'low': 0.05, 'medium': 0.15, 'high': 0.35, 'extreme': 0.60},
            'pandemic': {'low': 0.02, 'medium': 0.08, 'high': 0.20, 'extreme': 0.45}
        }
        
        base_displacement_rate = displacement_rates.get(scenario_type, displacement_rates['conflict'])[intensity]
        
        # Adjust for community characteristics
        displacement_modifier = 1.0
        
        # Infrastructure quality affects displacement
        if community_profile['infrastructure_score'] < 5:
            displacement_modifier += 0.3
        elif community_profile['infrastructure_score'] > 8:
            displacement_modifier -= 0.2
        
        # Social cohesion affects likelihood to stay
        if community_profile['social_cohesion'] > 7:
            displacement_modifier -= 0.2
        elif community_profile['social_cohesion'] < 4:
            displacement_modifier += 0.3
        
        final_displacement_rate = min(0.95, base_displacement_rate * displacement_modifier)
        displaced_population = int(community_profile['actual_population'] * final_displacement_rate)
        
        # Calculate displacement patterns
        displacement_patterns = {
            'total_displaced': displaced_population,
            'displacement_rate_percent': final_displacement_rate * 100,
            'internal_displacement': int(displaced_population * 0.7),  # Stay within region
            'external_migration': int(displaced_population * 0.3),  # Leave region
            'temporary_displacement': int(displaced_population * 0.6),  # Expect to return
            'permanent_displacement': int(displaced_population * 0.4),  # Unlikely to return
        }
        
        # Time-based displacement patterns
        if duration < 30:
            displacement_patterns['return_probability'] = 0.8
            displacement_patterns['expected_return_months'] = 3
        elif duration < 180:
            displacement_patterns['return_probability'] = 0.6
            displacement_patterns['expected_return_months'] = 12
        else:
            displacement_patterns['return_probability'] = 0.3
            displacement_patterns['expected_return_months'] = 36
        
        # Destination analysis
        displacement_patterns['destination_analysis'] = {
            'nearby_communities': 0.4,
            'regional_cities': 0.3,
            'other_countries': 0.2,
            'refugee_camps': 0.1
        }
        
        return displacement_patterns

    def _calculate_community_recovery_capacity(self, community_profile, impact_scenario):
        """Calculate community recovery capacity"""
        return {
            'infrastructure_resilience': community_profile['disaster_resilience'] / 10,
            'social_capital': community_profile['social_cohesion'] / 10,
            'economic_diversity': community_profile['economic_diversity'] / 10,
            'institutional_capacity': community_profile['infrastructure_score'] / 10,
            'overall_recovery_score': (community_profile['disaster_resilience'] + 
                                     community_profile['social_cohesion'] + 
                                     community_profile['economic_diversity'] + 
                                     community_profile['infrastructure_score']) / 40,
            'estimated_recovery_years': max(1, 10 - (community_profile['disaster_resilience'] / 2))
        }

    def _project_long_term_effects(self, direct_effects, recovery_capacity, impact_scenario):
        """Project long-term demographic and social effects"""
        recovery_score = recovery_capacity['overall_recovery_score']
        mortality_rate = direct_effects['mortality_rate']
        
        return {
            'population_recovery_years': int(5 / max(0.1, recovery_score)),
            'demographic_shifts': {
                'aging_acceleration': mortality_rate > 0.01,
                'workforce_shortage_duration_years': int(mortality_rate * 100),
                'birth_rate_impact': -mortality_rate * 0.5
            },
            'social_fabric_recovery': {
                'social_cohesion_recovery_years': int(3 / max(0.1, recovery_score)),
                'institutional_rebuilding_years': int(5 / max(0.1, recovery_score)),
                'cultural_preservation_likelihood': max(0.3, recovery_score)
            }
        }


class PsychologicalImpactModel:
    """Comprehensive psychological and mental health impact modeling"""
    
    def __init__(self):
        self.trauma_response_patterns = self._load_trauma_patterns()
        self.resilience_factors = self._load_resilience_factors()
        self.mental_health_baselines = self._load_mental_health_baselines()

    def _load_trauma_patterns(self):
        """Load trauma response pattern data"""
        return {
            'acute_stress': {'onset_days': 1, 'duration_weeks': 4, 'severity_scale': 0.7},
            'ptsd': {'onset_days': 30, 'duration_months': 12, 'severity_scale': 0.9},
            'depression': {'onset_days': 14, 'duration_months': 6, 'severity_scale': 0.6},
            'anxiety_disorders': {'onset_days': 7, 'duration_months': 8, 'severity_scale': 0.5}
        }

    def _load_resilience_factors(self):
        """Load resilience factor data"""
        return {
            'social_support': {'weight': 0.3, 'protective_factor': 0.6},
            'prior_experience': {'weight': 0.2, 'protective_factor': 0.4},
            'cultural_resources': {'weight': 0.25, 'protective_factor': 0.5},
            'economic_stability': {'weight': 0.15, 'protective_factor': 0.3},
            'access_to_services': {'weight': 0.1, 'protective_factor': 0.7}
        }

    def _load_mental_health_baselines(self):
        """Load baseline mental health data"""
        return {
            'ptsd_baseline': 0.035,
            'depression_baseline': 0.08,
            'anxiety_baseline': 0.12,
            'substance_abuse_baseline': 0.06,
            'regional_variations': {'developed': 0.9, 'developing': 1.2, 'conflict_zone': 1.5}
        }

    def analyze_psychological_impact(self, population_profile, impact_scenario, duration_days):
        """Analyze comprehensive psychological impact on population"""
        # Calculate trauma exposure levels
        trauma_exposure = self._calculate_trauma_exposure(population_profile, impact_scenario)
        
        # Calculate mental health outcomes
        mental_health_outcomes = self._calculate_mental_health_outcomes(
            population_profile, trauma_exposure, duration_days
        )
        
        # Calculate resilience and coping mechanisms
        resilience_analysis = self._analyze_community_resilience(
            population_profile, impact_scenario
        )
        
        # Calculate long-term psychological effects
        long_term_effects = self._calculate_long_term_psychological_effects(
            trauma_exposure, resilience_analysis, duration_days
        )
        
        return {
            'trauma_exposure': trauma_exposure,
            'mental_health_outcomes': mental_health_outcomes,
            'resilience_analysis': resilience_analysis,
            'long_term_effects': long_term_effects,
            'intervention_recommendations': self._generate_intervention_recommendations(
                mental_health_outcomes, resilience_analysis
            )
        }

    def _calculate_trauma_exposure(self, population_profile, impact_scenario):
        """Calculate levels of trauma exposure across population"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        
        # Trauma exposure rates by scenario
        exposure_rates = {
            'conflict': {
                'direct_violence': {'low': 0.15, 'medium': 0.35, 'high': 0.60, 'extreme': 0.80},
                'displacement': {'low': 0.20, 'medium': 0.40, 'high': 0.65, 'extreme': 0.85},
                'loss_of_livelihood': {'low': 0.25, 'medium': 0.50, 'high': 0.75, 'extreme': 0.90}
            },
            'natural_disaster': {
                'direct_threat': {'low': 0.30, 'medium': 0.55, 'high': 0.75, 'extreme': 0.90},
                'property_loss': {'low': 0.20, 'medium': 0.45, 'high': 0.70, 'extreme': 0.85},
                'displacement': {'low': 0.15, 'medium': 0.35, 'high': 0.60, 'extreme': 0.80}
            }
        }
        
        scenario_exposures = exposure_rates.get(scenario_type, exposure_rates['conflict'])
        trauma_exposure = {}
        total_population = population_profile['actual_population']
        
        for trauma_type, intensity_rates in scenario_exposures.items():
            exposure_rate = intensity_rates[intensity]
            exposed_population = int(total_population * exposure_rate)
            
            trauma_exposure[trauma_type] = {
                'exposure_rate_percent': exposure_rate * 100,
                'exposed_population': exposed_population,
                'severity_distribution': {
                    'mild': int(exposed_population * 0.4),
                    'moderate': int(exposed_population * 0.4),
                    'severe': int(exposed_population * 0.2)
                }
            }
        
        return trauma_exposure

    def _calculate_mental_health_outcomes(self, population_profile, trauma_exposure, duration_days):
        """Calculate expected mental health outcomes"""
        # Base rates of mental health conditions
        base_rates = self.mental_health_baselines
        
        mental_health_outcomes = {}
        total_population = population_profile['actual_population']
        
        # PTSD calculation
        ptsd_multiplier = 1.0
        for trauma_type, exposure_data in trauma_exposure.items():
            severe_exposure = exposure_data['severity_distribution']['severe']
            ptsd_multiplier += (severe_exposure / total_population) * 8  # 8x increase for severe trauma
        
        ptsd_rate = min(0.25, base_rates['ptsd_baseline'] * ptsd_multiplier)  # Cap at 25%
        
        # Depression calculation
        depression_multiplier = 1.0
        for trauma_type, exposure_data in trauma_exposure.items():
            total_exposed = exposure_data['exposed_population']
            depression_multiplier += (total_exposed / total_population) * 3  # 3x increase
        
        depression_rate = min(0.35, base_rates['depression_baseline'] * depression_multiplier)
        
        # Duration effects - longer exposure increases rates
        duration_factor = min(2.0, 1.0 + (duration_days / 365))
        
        mental_health_outcomes = {
            'ptsd': {
                'prevalence_rate': ptsd_rate * duration_factor,
                'affected_population': int(total_population * ptsd_rate * duration_factor),
                'severity_mild': int(total_population * ptsd_rate * duration_factor * 0.5),
                'severity_moderate': int(total_population * ptsd_rate * duration_factor * 0.3),
                'severity_severe': int(total_population * ptsd_rate * duration_factor * 0.2)
            },
            'depression': {
                'prevalence_rate': depression_rate * duration_factor,
                'affected_population': int(total_population * depression_rate * duration_factor),
                'treatment_needs': int(total_population * depression_rate * duration_factor * 0.7)
            },
            'anxiety_disorders': {
                'prevalence_rate': min(0.4, base_rates['anxiety_baseline'] * 4 * duration_factor),
                'affected_population': int(total_population * min(0.4, base_rates['anxiety_baseline'] * 4 * duration_factor)),
                'functional_impairment': int(total_population * min(0.4, base_rates['anxiety_baseline'] * 4 * duration_factor) * 0.6)
            }
        }
        
        return mental_health_outcomes

    def _analyze_community_resilience(self, population_profile, impact_scenario):
        """Analyze community resilience factors"""
        return {
            'social_support_strength': population_profile.get('social_cohesion', 5) / 10,
            'cultural_resources_availability': 0.7,  # Default moderate availability
            'economic_stability': population_profile.get('economic_diversity', 5) / 10,
            'institutional_support': population_profile.get('infrastructure_score', 5) / 10,
            'overall_resilience_score': (population_profile.get('social_cohesion', 5) + 
                                       population_profile.get('economic_diversity', 5) + 
                                       population_profile.get('infrastructure_score', 5)) / 30,
            'protective_factors': ['community_networks', 'cultural_practices', 'local_leadership']
        }

    def _calculate_long_term_psychological_effects(self, trauma_exposure, resilience_analysis, duration_days):
        """Calculate long-term psychological effects"""
        resilience_score = resilience_analysis['overall_resilience_score']
        
        # Calculate chronic conditions likelihood
        chronic_likelihood = max(0.1, 1.0 - resilience_score)
        
        return {
            'chronic_ptsd_likelihood': chronic_likelihood * 0.6,
            'chronic_depression_likelihood': chronic_likelihood * 0.4,
            'intergenerational_trauma_risk': chronic_likelihood * 0.3,
            'community_healing_timeline_years': int(5 / max(0.1, resilience_score)),
            'social_functioning_recovery_months': int(12 / max(0.1, resilience_score)),
            'collective_trauma_indicators': duration_days > 180 and chronic_likelihood > 0.5
        }

    def _generate_intervention_recommendations(self, mental_health_outcomes, resilience_analysis):
        """Generate intervention recommendations"""
        recommendations = {
            'immediate_interventions': ['psychological_first_aid', 'crisis_counseling'],
            'short_term_programs': ['trauma_therapy', 'support_groups'],
            'long_term_services': ['mental_health_system_strengthening', 'community_programs'],
            'community_based_approaches': ['peer_support', 'cultural_healing_practices'],
            'priority_populations': ['children', 'elderly', 'first_responders']
        }
        
        # Adjust based on outcomes
        ptsd_rate = mental_health_outcomes['ptsd']['prevalence_rate']
        if ptsd_rate > 0.15:  # High PTSD rate
            recommendations['immediate_interventions'].append('specialized_ptsd_treatment')
        
        depression_rate = mental_health_outcomes['depression']['prevalence_rate']
        if depression_rate > 0.2:  # High depression rate
            recommendations['short_term_programs'].append('depression_screening_programs')
        
        return recommendations


class CulturalModel:
    """Cultural and social structure modeling system"""
    
    def __init__(self):
        self.cultural_factors = self._load_cultural_factors()
        self.social_structures = self._load_social_structures()
        self.institutional_frameworks = self._load_institutional_frameworks()

    def _load_social_structures(self):
        """Load social structure data"""
        return {
            'family_systems': {'nuclear': 0.4, 'extended': 0.6},
            'community_organizations': {'formal': 0.3, 'informal': 0.7},
            'authority_structures': {'hierarchical': 0.6, 'egalitarian': 0.4}
        }

    def _load_institutional_frameworks(self):
        """Load institutional framework data"""
        return {
            'governance': {'centralized': 0.5, 'decentralized': 0.5},
            'education': {'formal': 0.7, 'traditional': 0.3},
            'healthcare': {'modern': 0.6, 'traditional': 0.4},
            'legal_systems': {'formal': 0.8, 'customary': 0.2}
        }

    def analyze_cultural_impact(self, region, population_profile, impact_scenario):
        """Analyze impact on cultural structures and social institutions"""
        regional_culture = self.cultural_factors.get(region, self._get_default_cultural_profile())
        
        # Calculate impact on cultural institutions
        institutional_impact = self._calculate_institutional_impact(
            regional_culture, impact_scenario
        )
        
        # Calculate social structure changes
        social_structure_changes = self._calculate_social_structure_impact(
            regional_culture, population_profile, impact_scenario
        )
        
        # Calculate cultural preservation vs adaptation
        cultural_adaptation = self._calculate_cultural_adaptation(
            regional_culture, impact_scenario
        )
        
        return {
            'regional_culture': regional_culture,
            'institutional_impact': institutional_impact,
            'social_structure_changes': social_structure_changes,
            'cultural_adaptation': cultural_adaptation,
            'preservation_priorities': self._identify_preservation_priorities(regional_culture),
            'adaptation_strategies': self._identify_adaptation_strategies(regional_culture, impact_scenario)
        }

    def _get_default_cultural_profile(self):
        """Get default cultural profile for unknown regions"""
        return {
            'family_structure_importance': 7.0,
            'community_collectivism': 6.5,
            'religious_significance': 6.0,
            'traditional_authority': 6.0,
            'economic_cooperation': 6.5,
            'cultural_institutions': ['community_centers', 'local_organizations'],
            'social_safety_nets': ['family_networks', 'community_support'],
            'decision_making_style': 'mixed_consensus',
            'conflict_resolution': 'community_mediation'
        }

    def _calculate_social_structure_impact(self, cultural_profile, population_profile, impact_scenario):
        """Calculate impact on social structures"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        
        # Impact on different social structures
        structure_impacts = {
            'family_networks': {
                'disruption_level': min(0.8, intensity == 'extreme' and 0.7 or 0.4),
                'adaptation_capacity': cultural_profile['family_structure_importance'] / 10,
                'recovery_timeline_months': 6 if intensity in ['low', 'medium'] else 18
            },
            'community_organizations': {
                'disruption_level': min(0.9, intensity == 'extreme' and 0.8 or 0.5),
                'adaptation_capacity': cultural_profile['community_collectivism'] / 10,
                'recovery_timeline_months': 12 if intensity in ['low', 'medium'] else 24
            },
            'economic_systems': {
                'disruption_level': min(0.95, intensity == 'extreme' and 0.9 or 0.6),
                'adaptation_capacity': cultural_profile['economic_cooperation'] / 10,
                'recovery_timeline_months': 18 if intensity in ['low', 'medium'] else 36
            }
        }
        
        # Calculate overall social cohesion change
        disruption_avg = np.mean([s['disruption_level'] for s in structure_impacts.values()])
        social_cohesion_change = -disruption_avg * cultural_profile['community_collectivism']
        
        return {
            'structure_impacts': structure_impacts,
            'social_cohesion_change': social_cohesion_change,
            'institutional_trust_change': -disruption_avg * 0.5,
            'collective_efficacy_change': -disruption_avg * 0.6
        }

    def _calculate_cultural_adaptation(self, cultural_profile, impact_scenario):
        """Calculate cultural adaptation patterns"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        
        # Adaptation vs preservation likelihood
        traditional_strength = cultural_profile['traditional_authority'] / 10
        adaptation_pressure = {'low': 0.3, 'medium': 0.6, 'high': 0.8, 'extreme': 0.9}[intensity]
        
        return {
            'preservation_likelihood': max(0.2, traditional_strength - adaptation_pressure * 0.5),
            'adaptation_likelihood': min(0.8, adaptation_pressure),
            'cultural_innovation_potential': (1 - traditional_strength) * adaptation_pressure,
            'tradition_erosion_risk': adaptation_pressure * (1 - traditional_strength),
            'cultural_resilience_factors': ['language_maintenance', 'ritual_continuity', 'knowledge_transmission']
        }

    def _identify_preservation_priorities(self, cultural_profile):
        """Identify cultural preservation priorities"""
        priorities = []
        
        if cultural_profile['religious_significance'] > 7:
            priorities.append('religious_practices_sites')
        if cultural_profile['traditional_authority'] > 7:
            priorities.append('traditional_governance_systems')
        if cultural_profile['family_structure_importance'] > 8:
            priorities.append('family_kinship_systems')
        
        priorities.extend(['language_preservation', 'cultural_knowledge', 'community_rituals'])
        return priorities

    def _identify_adaptation_strategies(self, cultural_profile, impact_scenario):
        """Identify cultural adaptation strategies"""
        strategies = {
            'institutional_adaptation': ['flexible_governance', 'hybrid_systems'],
            'social_adaptation': ['modified_practices', 'new_solidarity_mechanisms'],
            'economic_adaptation': ['alternative_livelihoods', 'cooperative_systems'],
            'cultural_innovation': ['creative_expression', 'narrative_reconstruction']
        }
        
        scenario_type = impact_scenario.get('type', 'conflict')
        if scenario_type == 'conflict':
            strategies['conflict_specific'] = ['peace_building_practices', 'reconciliation_mechanisms']
        elif scenario_type == 'natural_disaster':
            strategies['disaster_specific'] = ['environmental_adaptation', 'risk_reduction_practices']
        
        return strategies

    def _load_cultural_factors(self):
        """Load cultural factors for different regions"""
        return {
            'south_asia': {
                'family_structure_importance': 9.2,
                'community_collectivism': 8.5,
                'religious_significance': 8.8,
                'traditional_authority': 7.5,
                'economic_cooperation': 7.8,
                'cultural_institutions': ['family_networks', 'religious_centers', 'community_councils'],
                'social_safety_nets': ['extended_family', 'community_mutual_aid', 'religious_charity'],
                'decision_making_style': 'consensus_based',
                'conflict_resolution': 'elder_mediation'
            },
            'middle_east': {
                'family_structure_importance': 9.0,
                'community_collectivism': 8.2,
                'religious_significance': 9.1,
                'traditional_authority': 8.0,
                'economic_cooperation': 7.5,
                'cultural_institutions': ['tribal_councils', 'religious_institutions', 'family_clans'],
                'social_safety_nets': ['tribal_support', 'religious_community', 'family_networks'],
                'decision_making_style': 'hierarchical_consensus',
                'conflict_resolution': 'traditional_mediation'
            },
            'western_society': {
                'family_structure_importance': 6.5,
                'community_collectivism': 5.8,
                'religious_significance': 4.2,
                'traditional_authority': 4.5,
                'economic_cooperation': 6.8,
                'cultural_institutions': ['civic_organizations', 'professional_networks', 'voluntary_associations'],
                'social_safety_nets': ['government_programs', 'insurance_systems', 'civic_organizations'],
                'decision_making_style': 'democratic_process',
                'conflict_resolution': 'legal_system'
            }
        }

    def _calculate_institutional_impact(self, cultural_profile, impact_scenario):
        """Calculate impact on cultural and social institutions"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        
        # Institution vulnerability to different scenarios
        institution_vulnerabilities = {
            'conflict': {
                'government_institutions': {'low': 0.3, 'medium': 0.6, 'high': 0.8, 'extreme': 0.95},
                'religious_institutions': {'low': 0.2, 'medium': 0.4, 'high': 0.7, 'extreme': 0.85},
                'educational_institutions': {'low': 0.4, 'medium': 0.7, 'high': 0.9, 'extreme': 0.98},
                'economic_institutions': {'low': 0.5, 'medium': 0.8, 'high': 0.9, 'extreme': 0.95}
            },
            'natural_disaster': {
                'government_institutions': {'low': 0.2, 'medium': 0.4, 'high': 0.6, 'extreme': 0.8},
                'religious_institutions': {'low': 0.1, 'medium': 0.3, 'high': 0.5, 'extreme': 0.7},
                'educational_institutions': {'low': 0.3, 'medium': 0.6, 'high': 0.8, 'extreme': 0.9},
                'economic_institutions': {'low': 0.4, 'medium': 0.7, 'high': 0.85, 'extreme': 0.9}
            }
        }
        
        vulnerabilities = institution_vulnerabilities.get(scenario_type, institution_vulnerabilities['conflict'])
        institutional_impact = {}
        
        for institution, intensity_effects in vulnerabilities.items():
            impact_level = intensity_effects[intensity]
            
            institutional_impact[institution] = {
                'disruption_level': impact_level,
                'functionality_remaining': 1 - impact_level,
                'recovery_priority': self._calculate_recovery_priority(institution, cultural_profile),
                'alternative_mechanisms': self._identify_alternative_mechanisms(institution, cultural_profile)
            }
        
        return institutional_impact

    def _calculate_recovery_priority(self, institution, cultural_profile):
        """Calculate recovery priority for institutions"""
        priority_weights = {
            'government_institutions': cultural_profile.get('traditional_authority', 5) / 10,
            'religious_institutions': cultural_profile.get('religious_significance', 5) / 10,
            'educational_institutions': 0.7,  # Generally high priority
            'economic_institutions': cultural_profile.get('economic_cooperation', 5) / 10
        }
        
        return priority_weights.get(institution, 0.5)

    def _identify_alternative_mechanisms(self, institution, cultural_profile):
        """Identify alternative mechanisms for damaged institutions"""
        alternatives = {
            'government_institutions': ['traditional_councils', 'community_leaders'],
            'religious_institutions': ['community_gatherings', 'informal_spiritual_practices'],
            'educational_institutions': ['community_teachers', 'informal_education'],
            'economic_institutions': ['barter_systems', 'mutual_aid_networks']
        }
        
        return alternatives.get(institution, ['community_self_organization'])