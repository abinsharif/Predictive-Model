import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
from collections import defaultdict
import json

class GeographicModel:
    """Comprehensive geographic and terrain modeling system"""
    
    def __init__(self):
        self.terrain_data = self._load_terrain_data()
        self.climate_zones = self._load_climate_zones()
        self.elevation_effects = self._load_elevation_effects()
        self.geographic_vulnerabilities = self._load_geographic_vulnerabilities()

    def _load_terrain_data(self):
        """Load comprehensive terrain type data and characteristics"""
        return {
            'urban_dense': {
                'population_capacity_per_km2': 15000,
                'infrastructure_density': 0.95,
                'building_height_avg_m': 45,
                'green_space_percent': 12,
                'water_access_reliability': 0.92,
                'transportation_density': 0.88,
                'disaster_vulnerability': {
                    'earthquake': 0.85,
                    'flood': 0.75,
                    'fire': 0.90,
                    'conflict': 0.80
                },
                'economic_productivity': 2.8,
                'resource_dependencies': ['external_food', 'external_energy', 'external_materials']
            },
            'urban_medium': {
                'population_capacity_per_km2': 8000,
                'infrastructure_density': 0.78,
                'building_height_avg_m': 25,
                'green_space_percent': 25,
                'water_access_reliability': 0.88,
                'transportation_density': 0.72,
                'disaster_vulnerability': {
                    'earthquake': 0.70,
                    'flood': 0.65,
                    'fire': 0.75,
                    'conflict': 0.65
                },
                'economic_productivity': 2.2,
                'resource_dependencies': ['external_food', 'partial_energy']
            },
            'suburban': {
                'population_capacity_per_km2': 2500,
                'infrastructure_density': 0.62,
                'building_height_avg_m': 8,
                'green_space_percent': 45,
                'water_access_reliability': 0.82,
                'transportation_density': 0.55,
                'disaster_vulnerability': {
                    'earthquake': 0.45,
                    'flood': 0.50,
                    'fire': 0.60,
                    'conflict': 0.40
                },
                'economic_productivity': 1.5,
                'resource_dependencies': ['external_food', 'partial_energy']
            },
            'rural_agricultural': {
                'population_capacity_per_km2': 150,
                'infrastructure_density': 0.35,
                'building_height_avg_m': 4,
                'green_space_percent': 75,
                'water_access_reliability': 0.65,
                'transportation_density': 0.25,
                'disaster_vulnerability': {
                    'earthquake': 0.30,
                    'flood': 0.70,
                    'drought': 0.85,
                    'conflict': 0.50
                },
                'economic_productivity': 0.8,
                'resource_dependencies': ['weather_dependent'],
                'food_production_capacity': 2.5
            },
            'mountainous': {
                'population_capacity_per_km2': 80,
                'infrastructure_density': 0.25,
                'building_height_avg_m': 3,
                'green_space_percent': 85,
                'water_access_reliability': 0.75,
                'transportation_density': 0.15,
                'disaster_vulnerability': {
                    'earthquake': 0.80,
                    'landslide': 0.90,
                    'avalanche': 0.70,
                    'conflict': 0.35
                },
                'economic_productivity': 0.5,
                'resource_dependencies': ['external_food', 'external_materials'],
                'defensive_advantage': 2.2,
                'accessibility_factor': 0.3
            },
            'coastal': {
                'population_capacity_per_km2': 3500,
                'infrastructure_density': 0.68,
                'building_height_avg_m': 15,
                'green_space_percent': 35,
                'water_access_reliability': 0.85,
                'transportation_density': 0.78,
                'disaster_vulnerability': {
                    'tsunami': 0.95,
                    'hurricane': 0.88,
                    'sea_level_rise': 0.75,
                    'flood': 0.82
                },
                'economic_productivity': 2.1,
                'resource_dependencies': ['storm_protection'],
                'maritime_access': True,
                'fishing_capacity': 1.5
            },
            'desert': {
                'population_capacity_per_km2': 25,
                'infrastructure_density': 0.15,
                'building_height_avg_m': 2,
                'green_space_percent': 5,
                'water_access_reliability': 0.35,
                'transportation_density': 0.10,
                'disaster_vulnerability': {
                    'drought': 0.95,
                    'extreme_heat': 0.90,
                    'sandstorm': 0.75,
                    'conflict': 0.60
                },
                'economic_productivity': 0.3,
                'resource_dependencies': ['external_water', 'external_food'],
                'solar_energy_potential': 3.5,
                'mineral_extraction_potential': 2.0
            },
            'forest': {
                'population_capacity_per_km2': 60,
                'infrastructure_density': 0.20,
                'building_height_avg_m': 2,
                'green_space_percent': 92,
                'water_access_reliability': 0.80,
                'transportation_density': 0.12,
                'disaster_vulnerability': {
                    'wildfire': 0.90,
                    'flooding': 0.60,
                    'insect_outbreak': 0.70
                },
                'economic_productivity': 0.6,
                'resource_dependencies': ['fire_management'],
                'timber_production': 2.8,
                'carbon_sequestration': 3.2,
                'biodiversity_index': 4.5
            }
        }

    def _load_climate_zones(self):
        """Load climate zone characteristics and impacts"""
        return {
            'tropical': {
                'temperature_range_c': [20, 35],
                'humidity_avg_percent': 80,
                'precipitation_mm_year': 2500,
                'seasonal_variation': 'wet_dry',
                'agricultural_productivity': 2.2,
                'disease_risk_factor': 1.8,
                'construction_challenges': 1.4,
                'energy_cooling_demand': 2.5
            },
            'subtropical': {
                'temperature_range_c': [10, 30],
                'humidity_avg_percent': 65,
                'precipitation_mm_year': 1200,
                'seasonal_variation': 'moderate',
                'agricultural_productivity': 2.0,
                'disease_risk_factor': 1.2,
                'construction_challenges': 1.0,
                'energy_cooling_demand': 1.8
            },
            'temperate': {
                'temperature_range_c': [-5, 25],
                'humidity_avg_percent': 55,
                'precipitation_mm_year': 800,
                'seasonal_variation': 'four_seasons',
                'agricultural_productivity': 1.8,
                'disease_risk_factor': 1.0,
                'construction_challenges': 0.8,
                'energy_heating_demand': 1.5
            },
            'continental': {
                'temperature_range_c': [-20, 30],
                'humidity_avg_percent': 50,
                'precipitation_mm_year': 600,
                'seasonal_variation': 'extreme',
                'agricultural_productivity': 1.5,
                'disease_risk_factor': 0.8,
                'construction_challenges': 1.2,
                'energy_heating_demand': 2.5
            },
            'arid': {
                'temperature_range_c': [5, 45],
                'humidity_avg_percent': 25,
                'precipitation_mm_year': 200,
                'seasonal_variation': 'minimal',
                'agricultural_productivity': 0.3,
                'disease_risk_factor': 0.6,
                'construction_challenges': 1.6,
                'water_scarcity_factor': 3.5
            },
            'arctic': {
                'temperature_range_c': [-40, 10],
                'humidity_avg_percent': 70,
                'precipitation_mm_year': 400,
                'seasonal_variation': 'extreme_light',
                'agricultural_productivity': 0.1,
                'disease_risk_factor': 0.5,
                'construction_challenges': 2.8,
                'energy_heating_demand': 4.0
            }
        }

    def _load_elevation_effects(self):
        """Load elevation-based effect modifiers"""
        return {
            'lowland': {'accessibility_factor': 1.0, 'construction_difficulty': 1.0},
            'highland': {'accessibility_factor': 0.8, 'construction_difficulty': 1.3},
            'mountain': {'accessibility_factor': 0.5, 'construction_difficulty': 1.8},
            'high_mountain': {'accessibility_factor': 0.2, 'construction_difficulty': 2.5}
        }

    def _load_geographic_vulnerabilities(self):
        """Load geographic vulnerability factors"""
        return {
            'seismic_zones': {'very_high': 0.9, 'high': 0.7, 'moderate': 0.5, 'low': 0.2},
            'flood_zones': {'100_year': 0.8, '500_year': 0.6, '1000_year': 0.4, 'minimal': 0.1},
            'wildfire_zones': {'extreme': 0.9, 'high': 0.7, 'moderate': 0.5, 'low': 0.2}
        }

    def analyze_geographic_impact(self, location, terrain_type, climate_zone, elevation_m, impact_scenario):
        """Analyze comprehensive geographic impact on scenarios"""
        terrain_profile = self.terrain_data.get(terrain_type, self.terrain_data['suburban'])
        climate_profile = self.climate_zones.get(climate_zone, self.climate_zones['temperate'])
        
        elevation_effects = self._calculate_elevation_effects(elevation_m)
        terrain_vulnerabilities = self._calculate_terrain_vulnerabilities(terrain_profile, impact_scenario)
        climate_impacts = self._calculate_climate_impacts(climate_profile, impact_scenario)
        logistics_factors = self._calculate_logistics_factors(terrain_profile, elevation_effects, climate_profile)
        resource_analysis = self._calculate_resource_constraints(terrain_profile, climate_profile, elevation_effects)
        
        return {
            'location': location,
            'terrain_type': terrain_type,
            'climate_zone': climate_zone,
            'elevation_m': elevation_m,
            'terrain_profile': terrain_profile,
            'climate_profile': climate_profile,
            'elevation_effects': elevation_effects,
            'terrain_vulnerabilities': terrain_vulnerabilities,
            'climate_impacts': climate_impacts,
            'logistics_factors': logistics_factors,
            'resource_analysis': resource_analysis,
            'strategic_assessment': self._generate_strategic_assessment(terrain_profile, climate_profile, elevation_effects, impact_scenario)
        }

    def _calculate_elevation_effects(self, elevation_m):
        """Calculate effects of elevation on various factors"""
        if elevation_m < 500:
            category = 'lowland'
            accessibility_factor = 1.0
            construction_difficulty = 1.0
        elif elevation_m < 1500:
            category = 'highland'
            accessibility_factor = 0.8
            construction_difficulty = 1.3
        elif elevation_m < 3000:
            category = 'mountain'
            accessibility_factor = 0.5
            construction_difficulty = 1.8
        else:
            category = 'high_mountain'
            accessibility_factor = 0.2
            construction_difficulty = 2.5

        return {
            'elevation_category': category,
            'accessibility_factor': accessibility_factor,
            'construction_difficulty': construction_difficulty,
            'air_density_factor': math.exp(-elevation_m / 8400),
            'temperature_reduction_c': elevation_m * 0.0065
        }

    def _calculate_logistics_factors(self, terrain_profile, elevation_effects, climate_profile):
        """Calculate logistics and accessibility factors"""
        return {
            'road_accessibility': terrain_profile['transportation_density'] * elevation_effects['accessibility_factor'],
            'supply_line_vulnerability': 1.0 - terrain_profile['transportation_density'],
            'equipment_transport_difficulty': elevation_effects['construction_difficulty'],
            'seasonal_access_variation': climate_profile.get('seasonal_variation', 'moderate')
        }

    def _calculate_resource_constraints(self, terrain_profile, climate_profile, elevation_effects):
        """Calculate resource availability and constraints"""
        return {
            'water_availability': terrain_profile['water_access_reliability'] * (1 - climate_profile.get('water_scarcity_factor', 1.0) * 0.2),
            'food_security': terrain_profile.get('food_production_capacity', 0.5),
            'energy_potential': terrain_profile.get('solar_energy_potential', 1.0),
            'construction_materials': terrain_profile.get('mineral_extraction_potential', 0.5)
        }

    def _generate_strategic_assessment(self, terrain_profile, climate_profile, elevation_effects, impact_scenario):
        """Generate strategic assessment of geographic factors"""
        return {
            'overall_suitability': (terrain_profile['infrastructure_density'] + elevation_effects['accessibility_factor']) / 2,
            'key_advantages': ['Infrastructure density'] if terrain_profile['infrastructure_density'] > 0.7 else [],
            'critical_vulnerabilities': [f'{k} risk' for k, v in terrain_profile.get('disaster_vulnerability', {}).items() if v > 0.7],
            'mitigation_strategies': ['Strengthen infrastructure', 'Develop evacuation plans']
        }

    def _calculate_terrain_vulnerabilities(self, terrain_profile, impact_scenario):
        """Calculate terrain-specific vulnerabilities to impact scenario"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        
        disaster_vulnerabilities = terrain_profile.get('disaster_vulnerability', {})
        vulnerability_factors = {}
        
        if scenario_type == 'conflict':
            vulnerability_factors['military_accessibility'] = 1.0 - terrain_profile.get('defensive_advantage', 1.0) / 3.0
            vulnerability_factors['civilian_exposure'] = terrain_profile['infrastructure_density']
        elif scenario_type == 'natural_disaster':
            for disaster_type, vulnerability in disaster_vulnerabilities.items():
                vulnerability_factors[disaster_type] = vulnerability
        
        # Apply intensity multipliers
        intensity_multipliers = {'low': 0.6, 'medium': 1.0, 'high': 1.4, 'extreme': 1.8}
        multiplier = intensity_multipliers[intensity]
        
        for factor, value in vulnerability_factors.items():
            vulnerability_factors[factor] = min(1.0, value * multiplier)
        
        return vulnerability_factors

    def _calculate_climate_impacts(self, climate_profile, impact_scenario):
        """Calculate climate-related impacts on scenario"""
        climate_impacts = {}
        temp_range = climate_profile['temperature_range_c']
        avg_temp = (temp_range[0] + temp_range[1]) / 2
        
        if avg_temp > 30:  # Hot climate
            climate_impacts['heat_stress_factor'] = 1.8
            climate_impacts['equipment_degradation'] = 1.4
        elif avg_temp < 5:  # Cold climate
            climate_impacts['cold_stress_factor'] = 1.6
            climate_impacts['equipment_challenges'] = 1.5
        else:
            climate_impacts['temperature_stress'] = 1.0
        
        humidity = climate_profile['humidity_avg_percent']
        if humidity > 75:
            climate_impacts['disease_risk_multiplier'] = climate_profile.get('disease_risk_factor', 1.0)
        
        return climate_impacts


class ClimateImpactModel:
    """Climate change impact and environmental degradation modeling"""
    
    def __init__(self):
        self.climate_scenarios = self._load_climate_scenarios()
        self.environmental_thresholds = self._load_environmental_thresholds()
        self.adaptation_measures = self._load_adaptation_measures()

    def _load_climate_scenarios(self):
        """Load climate change scenario projections"""
        return {
            'rcp26': {
                'global_temp_increase_c': 1.8,
                'sea_level_rise_cm': 43,
                'precipitation_change_percent': {'global_avg': 2.5, 'variability_increase': 15},
                'extreme_weather_frequency_multiplier': 1.4,
                'agricultural_productivity_change': -0.05,
                'water_stress_regions_percent': 25
            },
            'rcp45': {
                'global_temp_increase_c': 2.4,
                'sea_level_rise_cm': 56,
                'precipitation_change_percent': {'global_avg': 3.8, 'variability_increase': 25},
                'extreme_weather_frequency_multiplier': 2.1,
                'agricultural_productivity_change': -0.12,
                'water_stress_regions_percent': 35
            },
            'rcp60': {
                'global_temp_increase_c': 3.2,
                'sea_level_rise_cm': 72,
                'precipitation_change_percent': {'global_avg': 5.1, 'variability_increase': 35},
                'extreme_weather_frequency_multiplier': 2.8,
                'agricultural_productivity_change': -0.22,
                'water_stress_regions_percent': 48
            },
            'rcp85': {
                'global_temp_increase_c': 4.3,
                'sea_level_rise_cm': 98,
                'precipitation_change_percent': {'global_avg': 7.2, 'variability_increase': 45},
                'extreme_weather_frequency_multiplier': 3.6,
                'agricultural_productivity_change': -0.35,
                'water_stress_regions_percent': 65
            }
        }

    def _load_environmental_thresholds(self):
        """Load environmental threshold data"""
        return {
            'temperature_thresholds': {'heat_stress_days': 35.0, 'extreme_heat_days': 40.0},
            'water_stress_thresholds': {'moderate_stress': 1700, 'high_stress': 1000},
            'sea_level_thresholds': {'coastal_infrastructure_risk': 30, 'major_displacement_risk': 50}
        }

    def _load_adaptation_measures(self):
        """Load adaptation measure data"""
        return {
            'infrastructure_adaptation': {
                'sea_walls': {'cost_per_km': 50000000, 'effectiveness': 0.8},
                'flood_barriers': {'cost_per_km': 10000000, 'effectiveness': 0.7}
            },
            'agricultural_adaptation': {
                'drought_resistant_crops': {'cost_per_hectare': 1000, 'effectiveness': 0.6}
            }
        }

    def model_climate_impact_scenario(self, region, time_horizon_years, emission_scenario, population_profile):
        """Model comprehensive climate impact scenario"""
        climate_projection = self.climate_scenarios.get(emission_scenario, self.climate_scenarios['rcp45'])
        
        # Scale projections to time horizon
        time_scale_factor = time_horizon_years / 80
        scaled_projection = {}
        for key, value in climate_projection.items():
            if isinstance(value, (int, float)):
                scaled_projection[key] = value * time_scale_factor
            else:
                scaled_projection[key] = value
        
        regional_impacts = self._calculate_regional_climate_impacts(region, scaled_projection, population_profile)
        infrastructure_impacts = self._calculate_infrastructure_climate_impacts(scaled_projection, population_profile)
        human_impacts = self._calculate_human_climate_impacts(regional_impacts, infrastructure_impacts, population_profile)
        economic_impacts = self._calculate_economic_climate_impacts(regional_impacts, time_horizon_years, population_profile)
        adaptation_needs = self._calculate_adaptation_requirements(regional_impacts, human_impacts, economic_impacts)
        
        return {
            'emission_scenario': emission_scenario,
            'time_horizon_years': time_horizon_years,
            'climate_projection': scaled_projection,
            'regional_impacts': regional_impacts,
            'infrastructure_impacts': infrastructure_impacts,
            'human_impacts': human_impacts,
            'economic_impacts': economic_impacts,
            'adaptation_needs': adaptation_needs,
            'migration_pressure': self._calculate_climate_migration(regional_impacts, population_profile),
            'conflict_risk': self._calculate_climate_conflict_risk(regional_impacts, human_impacts)
        }

    def _calculate_human_climate_impacts(self, regional_impacts, infrastructure_impacts, population_profile):
        """Calculate climate impacts on human populations"""
        population = population_profile.get('actual_population', 1000000)
        
        human_impacts = {
            'health_impacts': {'heat_related_deaths_per_year': 0, 'vector_borne_disease_increase': 0},
            'displacement_projections': {'temporary_displacement': 0, 'permanent_displacement': 0},
            'livelihood_impacts': {'agricultural_job_losses': 0, 'infrastructure_job_losses': 0}
        }
        
        if 'temperature' in regional_impacts:
            temp_increase = regional_impacts['temperature']['increase_c']
            human_impacts['health_impacts']['heat_related_deaths_per_year'] = int(population * temp_increase * 0.001)
        
        if 'sea_level' in regional_impacts:
            sea_level_rise = regional_impacts['sea_level']['rise_cm']
            if sea_level_rise > 50:
                displacement_rate = min(0.3, sea_level_rise / 200)
                human_impacts['displacement_projections']['permanent_displacement'] = int(population * displacement_rate)
        
        return human_impacts

    def _calculate_economic_climate_impacts(self, regional_impacts, time_horizon_years, population_profile):
        """Calculate economic impacts of climate change"""
        population = population_profile.get('actual_population', 1000000)
        gdp_per_capita = population_profile.get('gdp_per_capita', 10000)
        total_gdp = population * gdp_per_capita
        
        economic_impacts = {
            'direct_damage_costs': {'infrastructure_adaptation': 0, 'agricultural_losses': 0},
            'productivity_losses': {'heat_stress_productivity_loss': 0},
            'adaptation_investment_needs': {'infrastructure_hardening': 0},
            'total_economic_impact': 0
        }
        
        if 'temperature' in regional_impacts:
            temp_increase = regional_impacts['temperature']['increase_c']
            economic_impacts['direct_damage_costs']['infrastructure_adaptation'] = int(total_gdp * temp_increase * 0.02)
        
        economic_impacts['total_economic_impact'] = sum(economic_impacts['direct_damage_costs'].values())
        return economic_impacts

    def _calculate_adaptation_requirements(self, regional_impacts, human_impacts, economic_impacts):
        """Calculate adaptation requirements and priorities"""
        adaptation_requirements = {
            'priority_level': 'medium',
            'required_measures': [],
            'cost_estimates': {}
        }
        
        if 'sea_level' in regional_impacts and regional_impacts['sea_level']['rise_cm'] > 30:
            adaptation_requirements['required_measures'].append('coastal_protection')
            adaptation_requirements['cost_estimates']['coastal_protection'] = 50000000
        
        if 'temperature' in regional_impacts and regional_impacts['temperature']['increase_c'] > 2.0:
            adaptation_requirements['required_measures'].append('cooling_infrastructure')
            adaptation_requirements['cost_estimates']['cooling_infrastructure'] = 30000000
        
        return adaptation_requirements

    def _calculate_climate_migration(self, regional_impacts, population_profile):
        """Calculate climate-induced migration pressures"""
        population = population_profile.get('actual_population', 1000000)
        
        migration_factors = {
            'environmental_push_factors': {},
            'total_migration_pressure': 0
        }
        
        if 'sea_level' in regional_impacts:
            sea_level_rise = regional_impacts['sea_level']['rise_cm']
            if sea_level_rise > 50:
                migration_rate = min(0.4, sea_level_rise / 125)
                sea_level_migrants = int(population * 0.4 * migration_rate)
                migration_factors['environmental_push_factors']['sea_level_rise'] = sea_level_migrants
        
        migration_factors['total_migration_pressure'] = sum(migration_factors['environmental_push_factors'].values())
        return migration_factors

    def _calculate_climate_conflict_risk(self, regional_impacts, human_impacts):
        """Calculate climate-induced conflict risk"""
        conflict_risk_factors = {
            'resource_scarcity_conflicts': 0.0,
            'migration_related_tensions': 0.0,
            'overall_conflict_risk_score': 0
        }
        
        if 'precipitation' in regional_impacts:
            drought_risk = regional_impacts['precipitation'].get('drought_frequency_multiplier', 1.0)
            if drought_risk > 1.5:
                conflict_risk_factors['resource_scarcity_conflicts'] = min(0.8, (drought_risk - 1.0) / 2.0)
        
        total_displacement = human_impacts['displacement_projections']['permanent_displacement']
        if total_displacement > 10000:
            conflict_risk_factors['migration_related_tensions'] = min(1.0, total_displacement / 100000) * 0.6
        
        conflict_risk_factors['overall_conflict_risk_score'] = np.mean(list(conflict_risk_factors.values())[:-1])
        return conflict_risk_factors

    def _calculate_regional_climate_impacts(self, region, projection, population_profile):
        """Calculate region-specific climate impacts"""
        regional_factors = {
            'south_asia': {'heat_vulnerability': 1.8, 'flood_vulnerability': 2.2, 'sea_level_vulnerability': 2.0},
            'middle_east': {'heat_vulnerability': 2.5, 'drought_vulnerability': 2.8},
            'small_island_states': {'sea_level_vulnerability': 4.5}
        }
        
        factors = regional_factors.get(region, regional_factors['south_asia'])
        regional_impacts = {}
        
        # Temperature impacts
        temp_increase = projection['global_temp_increase_c']
        regional_impacts['temperature'] = {
            'increase_c': temp_increase * factors.get('heat_vulnerability', 1.0),
            'heat_days_increase': temp_increase * 15 * factors.get('heat_vulnerability', 1.0)
        }
        
        # Precipitation impacts
        precip_change = projection['precipitation_change_percent']['global_avg']
        regional_impacts['precipitation'] = {
            'annual_change_percent': precip_change,
            'drought_frequency_multiplier': factors.get('drought_vulnerability', 1.0)
        }
        
        # Sea level impacts
        if 'sea_level_vulnerability' in factors:
            sea_level_rise = projection['sea_level_rise_cm']
            regional_impacts['sea_level'] = {
                'rise_cm': sea_level_rise * factors['sea_level_vulnerability'],
                'population_at_risk': int(population_profile['actual_population'] * 0.1 * factors['sea_level_vulnerability'])
            }
        
        return regional_impacts

    def _calculate_infrastructure_climate_impacts(self, projection, population_profile):
        """Calculate climate impacts on infrastructure"""
        temp_increase = projection['global_temp_increase_c']
        extreme_weather_mult = projection['extreme_weather_frequency_multiplier']
        
        return {
            'transportation': {
                'road_damage_increase_percent': temp_increase * 15 + extreme_weather_mult * 10,
                'maintenance_cost_increase_percent': temp_increase * 20 + extreme_weather_mult * 15
            },
            'energy': {
                'power_grid_stress_events_per_year': extreme_weather_mult * 12,
                'cooling_demand_increase_percent': temp_increase * 25
            },
            'water_systems': {
                'treatment_capacity_stress': temp_increase * 0.8 + extreme_weather_mult * 0.4,
                'storage_evaporation_increase_percent': temp_increase * 12
            }
        }


class InfrastructureModel:
    """Infrastructure modeling and impact analysis system"""
    
    def __init__(self):
        self.infrastructure_types = self._load_infrastructure_types()
        self.interdependency_matrix = self._load_infrastructure_interdependencies()
        self.capacity_models = self._load_capacity_models()

    def _load_infrastructure_types(self):
        """Load comprehensive infrastructure type definitions"""
        return {
            'transportation': {
                'roads': {
                    'capacity_metric': 'vehicles_per_hour',
                    'vulnerability_factors': ['weather', 'seismic', 'conflict'],
                    'maintenance_cycle_months': 18,
                    'replacement_cost_per_km': 2500000,
                    'criticality_score': 8.5,
                    'redundancy_typical': 0.6
                },
                'railways': {
                    'capacity_metric': 'passengers_per_hour',
                    'vulnerability_factors': ['weather', 'seismic', 'cyber'],
                    'maintenance_cycle_months': 12,
                    'replacement_cost_per_km': 15000000,
                    'criticality_score': 7.8,
                    'redundancy_typical': 0.3
                },
                'airports': {
                    'capacity_metric': 'flights_per_day',
                    'vulnerability_factors': ['weather', 'conflict', 'cyber'],
                    'maintenance_cycle_months': 6,
                    'replacement_cost_per_facility': 2000000000,
                    'criticality_score': 9.2,
                    'redundancy_typical': 0.2
                },
                'ports': {
                    'capacity_metric': 'containers_per_day',
                    'vulnerability_factors': ['weather', 'sea_level', 'conflict'],
                    'maintenance_cycle_months': 24,
                    'replacement_cost_per_facility': 5000000000,
                    'criticality_score': 9.0,
                    'redundancy_typical': 0.4
                }
            },
            'energy': {
                'power_generation': {
                    'capacity_metric': 'megawatts',
                    'vulnerability_factors': ['weather', 'cyber', 'supply_chain'],
                    'maintenance_cycle_months': 8,
                    'replacement_cost_per_mw': 3000000,
                    'criticality_score': 9.8,
                    'redundancy_typical': 0.25
                },
                'transmission_grid': {
                    'capacity_metric': 'mw_transmission',
                    'vulnerability_factors': ['weather', 'cyber', 'physical'],
                    'maintenance_cycle_months': 12,
                    'replacement_cost_per_km': 800000,
                    'criticality_score': 9.5,
                    'redundancy_typical': 0.15
                },
                'distribution_grid': {
                    'capacity_metric': 'local_distribution',
                    'vulnerability_factors': ['weather', 'aging', 'overload'],
                    'maintenance_cycle_months': 18,
                    'replacement_cost_per_km': 150000,
                    'criticality_score': 8.8,
                    'redundancy_typical': 0.3
                }
            },
            'water_systems': {
                'treatment_plants': {
                    'capacity_metric': 'liters_per_day',
                    'vulnerability_factors': ['contamination', 'power', 'chemicals'],
                    'maintenance_cycle_months': 6,
                    'replacement_cost_per_facility': 50000000,
                    'criticality_score': 9.4,
                    'redundancy_typical': 0.2
                },
                'distribution_network': {
                    'capacity_metric': 'flow_rate',
                    'vulnerability_factors': ['aging', 'pressure', 'contamination'],
                    'maintenance_cycle_months': 36,
                    'replacement_cost_per_km': 400000,
                    'criticality_score': 8.9,
                    'redundancy_typical': 0.1
                },
                'storage_systems': {
                    'capacity_metric': 'storage_volume',
                    'vulnerability_factors': ['seismic', 'contamination', 'evaporation'],
                    'maintenance_cycle_months': 60,
                    'replacement_cost_per_facility': 25000000,
                    'criticality_score': 8.6,
                    'redundancy_typical': 0.4
                }
            },
            'telecommunications': {
                'cellular_networks': {
                    'capacity_metric': 'users_served',
                    'vulnerability_factors': ['power', 'cyber', 'physical'],
                    'maintenance_cycle_months': 12,
                    'replacement_cost_per_tower': 500000,
                    'criticality_score': 8.7,
                    'redundancy_typical': 0.8
                },
                'fiber_networks': {
                    'capacity_metric': 'bandwidth_gbps',
                    'vulnerability_factors': ['physical', 'cyber', 'power'],
                    'maintenance_cycle_months': 24,
                    'replacement_cost_per_km': 50000,
                    'criticality_score': 9.1,
                    'redundancy_typical': 0.6
                },
                'data_centers': {
                    'capacity_metric': 'processing_power',
                    'vulnerability_factors': ['power', 'cooling', 'cyber'],
                    'maintenance_cycle_months': 3,
                    'replacement_cost_per_facility': 100000000,
                    'criticality_score': 9.6,
                    'redundancy_typical': 0.9
                }
            }
        }

    def _load_infrastructure_interdependencies(self):
        """Load infrastructure interdependency data"""
        return {
            'energy': ['telecommunications', 'water_systems', 'transportation'],
            'telecommunications': ['energy'],
            'water_systems': ['energy', 'telecommunications'],
            'transportation': ['energy', 'telecommunications']
        }

    def _load_capacity_models(self):
        """Load infrastructure capacity modeling data"""
        return {
            'transportation': {'peak_usage_factor': 0.8, 'redundancy_threshold': 0.6},
            'energy': {'peak_usage_factor': 0.9, 'redundancy_threshold': 0.2},
            'water_systems': {'peak_usage_factor': 0.7, 'redundancy_threshold': 0.3},
            'telecommunications': {'peak_usage_factor': 0.6, 'redundancy_threshold': 0.7}
        }

    def analyze_infrastructure_impact(self, infrastructure_profile, impact_scenario, geographic_factors):
        """Analyze comprehensive infrastructure impact"""
        scenario_type = impact_scenario.get('type', 'conflict')
        intensity = impact_scenario.get('intensity', 'medium')
        duration = impact_scenario.get('duration_days', 30)
        
        direct_damage = self._calculate_direct_infrastructure_damage(infrastructure_profile, scenario_type, intensity)
        cascade_failures = self._calculate_infrastructure_cascades(direct_damage, self.interdependency_matrix)
        service_disruptions = self._calculate_service_disruptions(direct_damage, cascade_failures, duration)
        recovery_analysis = self._calculate_infrastructure_recovery(direct_damage, cascade_failures, geographic_factors)
        economic_impact = self._calculate_infrastructure_economic_impact(service_disruptions, recovery_analysis, infrastructure_profile)
        
        return {
            'infrastructure_profile': infrastructure_profile,
            'impact_scenario': impact_scenario,
            'direct_damage': direct_damage,
            'cascade_failures': cascade_failures,
            'service_disruptions': service_disruptions,
            'recovery_analysis': recovery_analysis,
            'economic_impact': economic_impact,
            'critical_path_analysis': self._identify_critical_infrastructure_paths(direct_damage, cascade_failures),
            'resilience_recommendations': self._generate_resilience_recommendations(direct_damage, cascade_failures)
        }

    def _calculate_infrastructure_recovery(self, direct_damage, cascade_failures, geographic_factors):
        """Calculate infrastructure recovery timeline and requirements"""
        recovery_analysis = {'recovery_phases': {}, 'timeline_projections': {}}
        
        for infra_type, damage_info in direct_damage.items():
            damage_rate = damage_info['damage_rate']
            base_recovery_months = 12 if damage_rate > 0.5 else 6
            
            recovery_analysis['timeline_projections'][infra_type] = {
                'base_recovery_months': base_recovery_months,
                'adjusted_recovery_months': int(base_recovery_months * 1.5),  # Geographic adjustment
                'financial_cost_usd': damage_info['total_replacement_cost'] * 1.5
            }
        
        return recovery_analysis

    def _calculate_infrastructure_economic_impact(self, service_disruptions, recovery_analysis, infrastructure_profile):
        """Calculate economic impact of infrastructure damage"""
        economic_impact = {'direct_costs': {}, 'indirect_costs': {}, 'total_economic_impact_usd': 0}
        
        total_direct_costs = sum([recovery['financial_cost_usd'] for recovery in recovery_analysis.get('timeline_projections', {}).values()])
        
        # Indirect costs from service disruptions
        total_indirect_costs = 0
        for infra_type, disruption_info in service_disruptions.items():
            disruption_rate = disruption_info['disruption_rate']
            duration_days = disruption_info['estimated_duration_days']
            daily_loss = {'transportation': 100000000, 'energy': 200000000, 'water_systems': 50000000, 'telecommunications': 150000000}
            indirect_cost = daily_loss.get(infra_type, 50000000) * disruption_rate * duration_days
            economic_impact['indirect_costs'][infra_type] = indirect_cost
            total_indirect_costs += indirect_cost
        
        economic_impact['total_economic_impact_usd'] = total_direct_costs + total_indirect_costs
        return economic_impact

    def _identify_critical_infrastructure_paths(self, direct_damage, cascade_failures):
        """Identify critical infrastructure failure paths"""
        return {
            'single_point_failures': ['Power generation systems', 'Main transportation hubs'],
            'cascade_amplifiers': [{'affected_system': system, 'risk_level': 'high'} for system in cascade_failures.keys()],
            'system_vulnerabilities': ['Energy grid dependency', 'Limited redundancy in telecommunications']
        }

    def _generate_resilience_recommendations(self, direct_damage, cascade_failures):
        """Generate infrastructure resilience recommendations"""
        return {
            'immediate_actions': ['Emergency response protocols', 'Deploy backup systems'],
            'short_term_improvements': ['Cross-sector coordination', 'Redundant systems'],
            'long_term_investments': ['Diversify dependencies', 'Strengthen critical nodes'],
            'policy_recommendations': ['Mandate redundancy levels', 'Regular stress testing']
        }

    def _calculate_direct_infrastructure_damage(self, infrastructure_profile, scenario_type, intensity):
        """Calculate direct damage to infrastructure systems"""
        damage_matrices = {
            'conflict': {
                'transportation': {'low': 0.15, 'medium': 0.35, 'high': 0.65, 'extreme': 0.85},
                'energy': {'low': 0.25, 'medium': 0.50, 'high': 0.75, 'extreme': 0.90},
                'telecommunications': {'low': 0.30, 'medium': 0.55, 'high': 0.80, 'extreme': 0.95},
                'water_systems': {'low': 0.10, 'medium': 0.25, 'high': 0.50, 'extreme': 0.75}
            },
            'natural_disaster': {
                'transportation': {'low': 0.20, 'medium': 0.45, 'high': 0.70, 'extreme': 0.90},
                'energy': {'low': 0.30, 'medium': 0.60, 'high': 0.80, 'extreme': 0.95},
                'telecommunications': {'low': 0.25, 'medium': 0.50, 'high': 0.75, 'extreme': 0.90},
                'water_systems': {'low': 0.35, 'medium': 0.65, 'high': 0.85, 'extreme': 0.95}
            }
        }
        
        scenario_damage = damage_matrices.get(scenario_type, damage_matrices['conflict'])
        direct_damage = {}
        
        for infrastructure_type, systems in self.infrastructure_types.items():
            if infrastructure_type in scenario_damage:
                damage_rate = scenario_damage[infrastructure_type][intensity]
                direct_damage[infrastructure_type] = {
                    'damage_rate': damage_rate,
                    'systems_affected': {},
                    'total_replacement_cost': 0,
                    'capacity_lost_percent': damage_rate * 100
                }
                
                for system_name, system_data in systems.items():
                    system_damage_rate = damage_rate * np.random.uniform(0.7, 1.3)
                    system_damage_rate = min(1.0, system_damage_rate)
                    replacement_cost = system_data.get('replacement_cost_per_facility', system_data.get('replacement_cost_per_km', 1000000))
                    
                    direct_damage[infrastructure_type]['systems_affected'][system_name] = {
                        'damage_rate': system_damage_rate,
                        'criticality_score': system_data['criticality_score'],
                        'redundancy_available': system_data['redundancy_typical'],
                        'replacement_cost': replacement_cost * system_damage_rate
                    }
                    
                    direct_damage[infrastructure_type]['total_replacement_cost'] += replacement_cost * system_damage_rate
        
        return direct_damage

    def _calculate_infrastructure_cascades(self, direct_damage, interdependency_matrix):
        """Calculate cascade failures through infrastructure interdependencies"""
        cascade_failures = {}
        
        for damaged_infrastructure, damage_info in direct_damage.items():
            damage_rate = damage_info['damage_rate']
            dependent_systems = interdependency_matrix.get(damaged_infrastructure, [])
            
            for dependent_system in dependent_systems:
                if dependent_system not in cascade_failures:
                    cascade_failures[dependent_system] = {
                        'cascade_sources': [],
                        'total_cascade_impact': 0,
                        'functionality_reduction': 0
                    }
                
                cascade_impact = damage_rate * 0.6  # 60% of damage cascades
                cascade_failures[dependent_system]['cascade_sources'].append({
                    'source': damaged_infrastructure,
                    'impact': cascade_impact
                })
                
                cascade_failures[dependent_system]['total_cascade_impact'] = max(
                    cascade_failures[dependent_system]['total_cascade_impact'], cascade_impact
                )
                cascade_failures[dependent_system]['functionality_reduction'] += cascade_impact * 0.5
        
        # Cap functionality reduction at 100%
        for system, cascade_info in cascade_failures.items():
            cascade_info['functionality_reduction'] = min(1.0, cascade_info['functionality_reduction'])
        
        return cascade_failures

    def _calculate_service_disruptions(self, direct_damage, cascade_failures, duration_days):
        """Calculate service disruptions to population"""
        service_disruptions = {}
        infrastructure_to_services = {
            'energy': ['electricity', 'heating', 'industrial_power'],
            'water_systems': ['potable_water', 'sanitation', 'industrial_water'],
            'telecommunications': ['internet', 'mobile_phone', 'emergency_communications'],
            'transportation': ['public_transit', 'freight', 'emergency_services']
        }
        
        for infrastructure_type, services in infrastructure_to_services.items():
            disruption_rate = 0
            if infrastructure_type in direct_damage:
                disruption_rate = direct_damage[infrastructure_type]['damage_rate']
            
            if infrastructure_type in cascade_failures:
                disruption_rate += cascade_failures[infrastructure_type]['functionality_reduction']
            
            disruption_rate = min(1.0, disruption_rate)
            
            if disruption_rate > 0.05:
                service_disruptions[infrastructure_type] = {
                    'disruption_rate': disruption_rate,
                    'services_affected': services,
                    'population_impact_percent': disruption_rate * 100,
                    'estimated_duration_days': duration_days * disruption_rate,
                    'service_degradation': {
                        service: {
                            'availability_percent': (1 - disruption_rate) * 100,
                            'quality_impact': disruption_rate
                        } for service in services
                    }
                }
        
        return service_disruptions