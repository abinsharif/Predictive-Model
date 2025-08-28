import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta
import json

class WaterFloodingModel:
    """Comprehensive water flooding model for island scenarios"""
    
    def __init__(self):
        self.default_parameters = self._load_default_parameters()
        self.terrain_factors = self._load_terrain_factors()
        self.island_profiles = self._load_island_profiles()
        
    def _load_default_parameters(self):
        """Load default parameters with scientific values"""
        return {
            # Physics constants
            'water_density_kg_m3': 1000,
            'gravity_m_s2': 9.81,
            
            # F-values (advanced settings)
            'f_seismic': 0.001,  # Fraction of energy converting to seismic
            'f_air': 0.005,      # Fraction of energy transferring to air motion
            'f_momentum': 0.8,    # Momentum transfer efficiency
            
            # Default island parameters
            'default_island_area_km2': 100,
            'default_avg_elevation_m': 10,
            'default_mountain_height_m': 50,
            'default_water_source_height_m': 100,
            
            # Default water parameters
            'default_water_volume_ratio': 1.0,  # Volume equal to island volume above sea level
            
            # Casualty estimation factors
            'building_protection_factor': 0.15,
            'population_density_per_km2': 3000,
            'vulnerability_factors': {
                'children_elderly': 1.5,
                'general_population': 1.0,
                'trained_emergency': 0.6
            }
        }
    
    def _load_terrain_factors(self):
        """Load terrain-specific factors"""
        return {
            'coastal': {
                'drainage_efficiency': 0.8,
                'flow_resistance': 0.7,
                'erosion_susceptibility': 1.2,
                'landslide_risk': 0.6
            },
            'mountainous': {
                'drainage_efficiency': 0.9,
                'flow_resistance': 1.3,
                'erosion_susceptibility': 1.8,
                'landslide_risk': 2.1
            },
            'flat': {
                'drainage_efficiency': 0.4,
                'flow_resistance': 0.5,
                'erosion_susceptibility': 0.8,
                'landslide_risk': 0.3
            },
            'urban': {
                'drainage_efficiency': 0.3,
                'flow_resistance': 1.5,
                'erosion_susceptibility': 0.9,
                'landslide_risk': 0.4
            },
            'forest': {
                'drainage_efficiency': 0.6,
                'flow_resistance': 1.8,
                'erosion_susceptibility': 0.6,
                'landslide_risk': 0.8
            }
        }
    
    def _load_island_profiles(self):
        """Load predefined island profiles"""
        return {
            'small_tropical': {
                'area_km2': 25,
                'avg_elevation_m': 15,
                'mountain_height_m': 80,
                'terrain_type': 'coastal',
                'population_density': 2000,
                'description': 'Small tropical island with coral formations'
            },
            'medium_volcanic': {
                'area_km2': 100,
                'avg_elevation_m': 25,
                'mountain_height_m': 150,
                'terrain_type': 'mountainous',
                'population_density': 1500,
                'description': 'Medium-sized volcanic island with steep slopes'
            },
            'large_continental': {
                'area_km2': 400,
                'avg_elevation_m': 8,
                'mountain_height_m': 35,
                'terrain_type': 'flat',
                'population_density': 5000,
                'description': 'Large continental shelf island, mostly flat'
            },
            'custom': {
                'area_km2': 100,
                'avg_elevation_m': 10,
                'mountain_height_m': 50,
                'terrain_type': 'coastal',
                'population_density': 3000,
                'description': 'Custom island configuration'
            }
        }
    
    def calculate_water_impact_scenario(self, scenario_config):
        """Calculate comprehensive water flooding impact scenario"""
        
        # Extract configuration
        island_profile = scenario_config.get('island_profile', 'custom')
        water_release_speed = scenario_config.get('water_release_speed', 'fast')  # fast, medium, slow
        water_volume_multiplier = scenario_config.get('water_volume_multiplier', 1.0)
        advanced_params = scenario_config.get('advanced_parameters', {})
        
        # Merge advanced parameters with defaults
        params = {**self.default_parameters, **advanced_params}
        
        # Get island specifications
        if island_profile in self.island_profiles:
            island_specs = self.island_profiles[island_profile].copy()
        else:
            island_specs = self.island_profiles['custom'].copy()
        
        # Override with any custom values from scenario_config
        for key in ['area_km2', 'avg_elevation_m', 'mountain_height_m', 'terrain_type', 'population_density']:
            if key in scenario_config:
                island_specs[key] = scenario_config[key]
        
        # Calculate basic geometry and mass
        geometry = self._calculate_basic_geometry(island_specs, water_volume_multiplier, params)
        
        # Calculate energy and velocity
        energy_data = self._calculate_energy_and_velocity(geometry, params, island_specs)
        
        # Calculate flow rates for different release speeds
        flow_data = self._calculate_flow_rates(geometry, water_release_speed)
        
        # Calculate local pressures and forces
        pressure_data = self._calculate_pressures_and_forces(energy_data, flow_data, geometry)
        
        # Calculate tsunami and ocean effects
        tsunami_data = self._calculate_tsunami_effects(geometry, island_specs)
        
        # Calculate seismic effects
        seismic_data = self._calculate_seismic_effects(energy_data, params)
        
        # Calculate slope failure and landslide risks
        landslide_data = self._calculate_landslide_risks(island_specs, pressure_data, params)
        
        # Calculate airflow and weather effects
        weather_data = self._calculate_weather_effects(energy_data, geometry, params)
        
        # Calculate casualties and human impact
        casualty_data = self._calculate_casualties(island_specs, pressure_data, flow_data, params)
        
        # Calculate environmental impact
        environmental_data = self._calculate_environmental_impact(island_specs, geometry, flow_data)
        
        # Calculate timeline projections
        timeline_data = self._calculate_timeline_projections(flow_data, casualty_data, environmental_data)
        
        return {
            'scenario_id': scenario_config.get('scenario_id', f'flood_{int(datetime.now().timestamp())}'),
            'scenario_config': scenario_config,
            'basic_geometry': geometry,
            'energy_analysis': energy_data,
            'flow_analysis': flow_data,
            'pressure_analysis': pressure_data,
            'tsunami_effects': tsunami_data,
            'seismic_effects': seismic_data,
            'landslide_analysis': landslide_data,
            'weather_effects': weather_data,
            'casualty_analysis': casualty_data,
            'environmental_impact': environmental_data,
            'timeline_projections': timeline_data,
            'confidence_analysis': self._calculate_confidence_levels(scenario_config),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _calculate_basic_geometry(self, island_specs, water_volume_multiplier, params):
        """Calculate basic geometry and mass of water"""
        
        # Island geometry
        area_m2 = island_specs['area_km2'] * 1_000_000  # Convert km² to m²
        avg_elevation_m = island_specs['avg_elevation_m']
        mountain_height_m = island_specs['mountain_height_m']
        
        # Water volume calculation
        island_volume_above_sea_m3 = area_m2 * avg_elevation_m
        water_volume_m3 = island_volume_above_sea_m3 * water_volume_multiplier
        water_mass_kg = water_volume_m3 * params['water_density_kg_m3']
        
        # Water source height
        water_source_height_m = params.get('water_source_height_m', params['default_water_source_height_m'])
        drop_height_m = water_source_height_m - avg_elevation_m
        
        return {
            'island_area_m2': area_m2,
            'island_area_km2': island_specs['area_km2'],
            'island_avg_elevation_m': avg_elevation_m,
            'island_mountain_height_m': mountain_height_m,
            'water_volume_m3': water_volume_m3,
            'water_volume_km3': water_volume_m3 / 1_000_000_000,
            'water_mass_kg': water_mass_kg,
            'water_source_height_m': water_source_height_m,
            'drop_height_m': drop_height_m,
            'volume_to_area_ratio_m': water_volume_m3 / area_m2
        }
    
    def _calculate_energy_and_velocity(self, geometry, params, island_specs):
        """Calculate energy and velocity of falling water"""
        
        water_mass_kg = geometry['water_mass_kg']
        drop_height_m = geometry['drop_height_m']
        g = params['gravity_m_s2']
        
        # Gravitational potential energy
        potential_energy_j = water_mass_kg * g * drop_height_m
        
        # Impact velocity (free fall)
        impact_velocity_ms = math.sqrt(2 * g * drop_height_m)
        impact_velocity_kmh = impact_velocity_ms * 3.6
        
        # TNT equivalent (energy comparison only)
        tnt_equivalent_tons = potential_energy_j / (4.184e9)  # 1 ton TNT ≈ 4.184e9 J
        
        # Kinetic energy at impact
        kinetic_energy_j = 0.5 * water_mass_kg * (impact_velocity_ms ** 2)
        
        return {
            'potential_energy_j': potential_energy_j,
            'potential_energy_gj': potential_energy_j / 1e9,
            'kinetic_energy_j': kinetic_energy_j,
            'kinetic_energy_gj': kinetic_energy_j / 1e9,
            'impact_velocity_ms': impact_velocity_ms,
            'impact_velocity_kmh': impact_velocity_kmh,
            'tnt_equivalent_tons': tnt_equivalent_tons,
            'tnt_equivalent_kilotons': tnt_equivalent_tons / 1000,
            'energy_per_m2_j': potential_energy_j / geometry['island_area_m2']
        }
    
    def _calculate_flow_rates(self, geometry, release_speed):
        """Calculate flow rates for different release speeds"""
        
        water_volume_m3 = geometry['water_volume_m3']
        
        # Define release time scenarios
        release_times = {
            'very_fast': 60,      # 1 minute
            'fast': 3600,         # 1 hour
            'medium': 21600,      # 6 hours
            'slow': 86400,        # 1 day
            'very_slow': 604800   # 1 week
        }
        
        release_time_s = release_times.get(release_speed, 3600)
        
        # Calculate flow rate
        flow_rate_m3_s = water_volume_m3 / release_time_s
        
        # Power calculation
        power_w = geometry['water_mass_kg'] * 9.81 * geometry['drop_height_m'] / release_time_s
        
        # Comparison with Amazon River (average ~200,000 m³/s)
        amazon_comparison = flow_rate_m3_s / 200000
        
        return {
            'release_time_s': release_time_s,
            'release_time_h': release_time_s / 3600,
            'release_time_days': release_time_s / 86400,
            'flow_rate_m3_s': flow_rate_m3_s,
            'power_w': power_w,
            'power_gw': power_w / 1e9,
            'power_tw': power_w / 1e12,
            'amazon_river_comparison': amazon_comparison,
            'release_speed_category': release_speed
        }
    
    def _calculate_pressures_and_forces(self, energy_data, flow_data, geometry):
        """Calculate local pressures on impact"""
        
        water_density = 1000  # kg/m³
        impact_velocity = energy_data['impact_velocity_ms']
        water_depth_m = geometry['volume_to_area_ratio_m']
        
        # Hydrostatic pressure (when water settles)
        hydrostatic_pressure_pa = water_density * 9.81 * water_depth_m
        hydrostatic_pressure_kpa = hydrostatic_pressure_pa / 1000
        hydrostatic_pressure_psi = hydrostatic_pressure_kpa * 0.145
        
        # Dynamic (stagnation) pressure for impact
        dynamic_pressure_pa = 0.5 * water_density * (impact_velocity ** 2)
        dynamic_pressure_kpa = dynamic_pressure_pa / 1000
        dynamic_pressure_psi = dynamic_pressure_kpa * 0.145
        
        # Force per unit area
        mass_flow_rate_kg_s = geometry['water_mass_kg'] / flow_data['release_time_s']
        average_force_per_m2 = (mass_flow_rate_kg_s * impact_velocity) / geometry['island_area_m2']
        
        return {
            'water_depth_equivalent_m': water_depth_m,
            'hydrostatic_pressure_pa': hydrostatic_pressure_pa,
            'hydrostatic_pressure_kpa': hydrostatic_pressure_kpa,
            'hydrostatic_pressure_psi': hydrostatic_pressure_psi,
            'dynamic_pressure_pa': dynamic_pressure_pa,
            'dynamic_pressure_kpa': dynamic_pressure_kpa,
            'dynamic_pressure_psi': dynamic_pressure_psi,
            'pressure_ratio_dynamic_to_static': dynamic_pressure_pa / max(1, hydrostatic_pressure_pa),
            'average_force_per_m2_n': average_force_per_m2,
            'building_damage_potential': 'Severe' if dynamic_pressure_kpa > 500 else 'Moderate' if dynamic_pressure_kpa > 100 else 'Light'
        }
    
    def _calculate_tsunami_effects(self, geometry, island_specs):
        """Calculate tsunami and ocean effects"""
        
        water_volume_m3 = geometry['water_volume_m3']
        
        # Local sea level rise calculations for different ocean areas
        ocean_areas_km2 = [100, 1000, 10000, 100000]  # Different spreading areas
        local_rises = []
        
        for area_km2 in ocean_areas_km2:
            area_m2 = area_km2 * 1_000_000
            rise_m = water_volume_m3 / area_m2
            local_rises.append({
                'area_km2': area_km2,
                'sea_level_rise_m': rise_m,
                'wave_height_estimate_m': rise_m * 1.5,  # Waves typically 1.5x the rise
                'tsunami_risk': 'Extreme' if rise_m > 5 else 'High' if rise_m > 1 else 'Moderate' if rise_m > 0.1 else 'Low'
            })
        
        # Global sea level effect (negligible)
        global_ocean_area_m2 = 3.61e14  # Approximate ocean area
        global_rise_m = water_volume_m3 / global_ocean_area_m2
        
        return {
            'local_tsunami_effects': local_rises,
            'global_sea_level_rise_m': global_rise_m,
            'global_rise_micrometers': global_rise_m * 1e6,
            'coastal_flooding_range_km': min(50, math.sqrt(water_volume_m3 / 1e6)),
            'wave_propagation_speed_ms': math.sqrt(9.81 * geometry['island_avg_elevation_m']),
            'max_wave_height_estimate_m': local_rises[0]['wave_height_estimate_m'] if local_rises else 0
        }
    
    def _calculate_seismic_effects(self, energy_data, params):
        """Calculate possible seismic effects"""
        
        total_energy_j = energy_data['potential_energy_j']
        f_seismic = params['f_seismic']
        
        # Seismic energy
        seismic_energy_j = total_energy_j * f_seismic
        
        # Rough magnitude estimation using empirical formula
        # log10(Es) ≈ 1.5 * M + 4.8
        if seismic_energy_j > 0:
            magnitude_estimate = (math.log10(seismic_energy_j) - 4.8) / 1.5
        else:
            magnitude_estimate = 0
        
        # Different f-values for sensitivity analysis
        magnitude_scenarios = []
        for f_val in [1e-5, 1e-4, 1e-3, 1e-2]:
            es = total_energy_j * f_val
            if es > 0:
                mag = (math.log10(es) - 4.8) / 1.5
                magnitude_scenarios.append({
                    'f_seismic': f_val,
                    'magnitude_estimate': mag,
                    'description': f'M{mag:.1f}' if mag > 0 else 'Negligible'
                })
        
        return {
            'seismic_energy_j': seismic_energy_j,
            'magnitude_estimate': magnitude_estimate,
            'magnitude_description': f'M{magnitude_estimate:.1f}' if magnitude_estimate > 0 else 'Negligible',
            'magnitude_scenarios': magnitude_scenarios,
            'tremor_risk': 'High' if magnitude_estimate > 4 else 'Moderate' if magnitude_estimate > 3 else 'Low',
            'landslide_trigger_potential': magnitude_estimate > 3.5
        }
    
    def _calculate_landslide_risks(self, island_specs, pressure_data, params):
        """Calculate slope failure and landslide risks"""
        
        terrain_type = island_specs['terrain_type']
        terrain_factors = self.terrain_factors.get(terrain_type, self.terrain_factors['coastal'])
        mountain_height = island_specs['mountain_height_m']
        
        # Base landslide risk from terrain
        base_landslide_risk = terrain_factors['landslide_risk']
        
        # Pressure-induced risk
        dynamic_pressure_kpa = pressure_data['dynamic_pressure_kpa']
        pressure_risk_multiplier = min(3.0, 1 + (dynamic_pressure_kpa / 100))
        
        # Elevation risk (steeper slopes = higher risk)
        elevation_risk_multiplier = min(2.0, 1 + (mountain_height / 100))
        
        # Combined risk
        total_landslide_risk = base_landslide_risk * pressure_risk_multiplier * elevation_risk_multiplier
        
        # Liquefaction risk (for sandy areas)
        liquefaction_risk = min(1.0, dynamic_pressure_kpa / 200) if terrain_type in ['coastal', 'flat'] else 0.1
        
        # Erosion calculation
        erosion_susceptibility = terrain_factors['erosion_susceptibility']
        flow_erosion_factor = min(5.0, pressure_data['dynamic_pressure_kpa'] / 50)
        total_erosion_risk = erosion_susceptibility * flow_erosion_factor
        
        return {
            'base_landslide_risk': base_landslide_risk,
            'pressure_risk_multiplier': pressure_risk_multiplier,
            'elevation_risk_multiplier': elevation_risk_multiplier,
            'total_landslide_risk': total_landslide_risk,
            'landslide_probability': min(0.95, total_landslide_risk / 5),
            'liquefaction_risk': liquefaction_risk,
            'liquefaction_probability': liquefaction_risk,
            'erosion_risk_score': total_erosion_risk,
            'soil_loss_estimate_m': min(5.0, total_erosion_risk * 0.5),
            'slope_failure_areas_percent': min(80, total_landslide_risk * 15),
            'risk_category': 'Extreme' if total_landslide_risk > 4 else 'High' if total_landslide_risk > 2 else 'Moderate' if total_landslide_risk > 1 else 'Low'
        }
    
    def _calculate_weather_effects(self, energy_data, geometry, params):
        """Calculate airflow, blast wind, and weather effects"""
        
        total_energy_j = energy_data['potential_energy_j']
        f_air = params['f_air']
        
        # Energy transferred to air
        air_energy_j = total_energy_j * f_air
        
        # Air mass in column (rough estimate)
        air_density = 1.225  # kg/m³
        column_height_m = 1000
        air_mass_kg = geometry['island_area_m2'] * column_height_m * air_density
        
        # Air velocity estimate
        if air_mass_kg > 0:
            air_velocity_ms = math.sqrt(2 * air_energy_j / air_mass_kg)
        else:
            air_velocity_ms = 0
        
        air_velocity_kmh = air_velocity_ms * 3.6
        
        # Wind effects classification
        if air_velocity_kmh < 20:
            wind_effect = 'Light breeze'
        elif air_velocity_kmh < 50:
            wind_effect = 'Strong wind'
        elif air_velocity_kmh < 100:
            wind_effect = 'Storm-force wind'
        else:
            wind_effect = 'Hurricane-force wind'
        
        # Evaporation and fog effects
        water_surface_area_m2 = geometry['island_area_m2']
        evaporation_rate_kg_s = min(1000, water_surface_area_m2 * 0.001)  # Rough estimate
        
        return {
            'air_energy_j': air_energy_j,
            'air_mass_affected_kg': air_mass_kg,
            'air_velocity_ms': air_velocity_ms,
            'air_velocity_kmh': air_velocity_kmh,
            'wind_effect_category': wind_effect,
            'debris_wind_risk': air_velocity_ms > 15,
            'evaporation_rate_kg_s': evaporation_rate_kg_s,
            'fog_formation_likelihood': 'High' if air_velocity_ms > 10 else 'Moderate' if air_velocity_ms > 5 else 'Low',
            'local_weather_disruption': air_velocity_ms > 20,
            'thunderstorm_potential': air_velocity_ms > 25
        }
    
    def _calculate_casualties(self, island_specs, pressure_data, flow_data, params):
        """Calculate human casualties and impacts"""
        
        population_density = island_specs['population_density']
        island_area_km2 = island_specs['area_km2']
        total_population = int(population_density * island_area_km2)
        
        # Vulnerability based on release speed and pressure
        dynamic_pressure_kpa = pressure_data['dynamic_pressure_kpa']
        release_speed = flow_data['release_speed_category']
        
        # Base vulnerability by release speed
        vulnerability_by_speed = {
            'very_fast': 0.8,   # 80% vulnerable
            'fast': 0.6,        # 60% vulnerable
            'medium': 0.4,      # 40% vulnerable
            'slow': 0.2,        # 20% vulnerable
            'very_slow': 0.1    # 10% vulnerable
        }
        
        base_vulnerability = vulnerability_by_speed.get(release_speed, 0.5)
        
        # Pressure modifier
        pressure_modifier = min(2.0, 1 + (dynamic_pressure_kpa / 200))
        
        # Terrain modifier
        terrain_type = island_specs['terrain_type']
        terrain_escape_difficulty = {
            'mountainous': 1.3,  # Harder to escape
            'urban': 1.4,        # Buildings can trap people
            'coastal': 0.9,      # Easier evacuation by sea
            'flat': 0.8,         # Easy evacuation
            'forest': 1.1        # Some obstacles
        }
        
        escape_difficulty = terrain_escape_difficulty.get(terrain_type, 1.0)
        
        # Protection factor (buildings, shelters, etc.)
        protection_factor = params.get('building_protection_factor', 0.15)
        
        # Calculate casualties
        vulnerable_population = total_population * base_vulnerability * pressure_modifier * escape_difficulty
        protected_population = vulnerable_population * protection_factor
        casualties_estimate = int(vulnerable_population - protected_population)
        
        # Uncertainty bounds (±30%)
        casualties_lower = int(casualties_estimate * 0.7)
        casualties_upper = int(casualties_estimate * 1.3)
        
        # Injured estimates
        injured_estimate = int(casualties_estimate * 1.5)  # More injured than killed
        
        # Long-term health impacts
        contamination_affected = int(total_population * 0.8)  # Most population affected by contaminated water
        displacement_estimate = int(total_population * 0.6)   # 60% displaced
        
        return {
            'total_population': total_population,
            'immediate_casualties': casualties_estimate,
            'casualties_lower_bound': casualties_lower,
            'casualties_upper_bound': casualties_upper,
            'injured_estimate': injured_estimate,
            'total_affected': casualties_estimate + injured_estimate,
            'displacement_estimate': displacement_estimate,
            'contamination_affected': contamination_affected,
            'casualty_rate_percent': (casualties_estimate / total_population) * 100 if total_population > 0 else 0,
            'vulnerability_factors': {
                'base_vulnerability': base_vulnerability,
                'pressure_modifier': pressure_modifier,
                'escape_difficulty': escape_difficulty,
                'protection_factor': protection_factor
            },
            'long_term_health_impact': {
                'disease_risk': 'High' if contamination_affected > total_population * 0.5 else 'Moderate',
                'sanitation_crisis': displacement_estimate > total_population * 0.4,
                'food_security_impact': 'Severe' if displacement_estimate > total_population * 0.5 else 'Moderate'
            }
        }
    
    def _calculate_environmental_impact(self, island_specs, geometry, flow_data):
        """Calculate environmental impact"""
        
        terrain_type = island_specs['terrain_type']
        island_area_km2 = island_specs['area_km2']
        water_depth_m = geometry['volume_to_area_ratio_m']
        
        # Farmland impact
        farmland_destroyed_percent = min(95, water_depth_m * 20)
        
        # Forest impact
        if terrain_type == 'forest':
            forest_destroyed_percent = min(90, water_depth_m * 15)
        else:
            forest_destroyed_percent = min(70, water_depth_m * 10)
        
        # Sediment transport
        erosion_volume_m3 = island_area_km2 * 1_000_000 * 0.5 * min(2.0, water_depth_m)  # Top 0.5m × water depth factor
        
        # Saltwater intrusion (if reaches sea)
        saltwater_intrusion_km2 = min(island_area_km2 * 0.3, water_depth_m * island_area_km2 * 0.1)
        
        # Recovery time estimates
        farmland_recovery_years = min(10, 2 + water_depth_m)
        forest_recovery_years = min(25, 5 + water_depth_m * 2)
        infrastructure_recovery_years = min(15, 3 + water_depth_m * 1.5)
        
        return {
            'farmland_destroyed_percent': farmland_destroyed_percent,
            'forest_destroyed_percent': forest_destroyed_percent,
            'total_ecosystem_damage_percent': (farmland_destroyed_percent + forest_destroyed_percent) / 2,
            'sediment_volume_m3': erosion_volume_m3,
            'sediment_volume_million_tons': erosion_volume_m3 * 1.5 / 1_000_000,  # Assuming soil density ~1500 kg/m³
            'saltwater_intrusion_area_km2': saltwater_intrusion_km2,
            'groundwater_contamination_percent': min(80, saltwater_intrusion_km2 / island_area_km2 * 100),
            'beach_and_coastal_change': 'Severe' if erosion_volume_m3 > 1_000_000 else 'Moderate',
            'recovery_timeline': {
                'farmland_recovery_years': farmland_recovery_years,
                'forest_recovery_years': forest_recovery_years,
                'infrastructure_recovery_years': infrastructure_recovery_years,
                'full_ecosystem_recovery_years': max(farmland_recovery_years, forest_recovery_years)
            },
            'permanent_landscape_changes': water_depth_m > 1.0,
            'new_water_bodies_likely': water_depth_m > 2.0
        }
    
    def _calculate_timeline_projections(self, flow_data, casualty_data, environmental_data):
        """Calculate timeline of events"""
        
        release_time_hours = flow_data['release_time_h']
        
        # Phase definitions
        phases = []
        
        # Immediate impact phase
        if release_time_hours < 1:
            phases.append({
                'phase': 'immediate_impact',
                'start_time_hours': 0,
                'end_time_hours': release_time_hours,
                'description': 'Catastrophic water release and immediate flooding',
                'key_events': [
                    'Water wall impacts low-lying areas',
                    'Building destruction begins',
                    'Immediate casualties occur',
                    'Communication systems fail'
                ]
            })
        else:
            phases.append({
                'phase': 'progressive_flooding',
                'start_time_hours': 0,
                'end_time_hours': release_time_hours,
                'description': 'Progressive water accumulation and flooding',
                'key_events': [
                    'Rising water levels',
                    'Gradual building damage',
                    'Evacuation opportunities',
                    'Infrastructure stress'
                ]
            })
        
        # Emergency response phase
        phases.append({
            'phase': 'emergency_response',
            'start_time_hours': release_time_hours,
            'end_time_hours': release_time_hours + 24,
            'description': 'Immediate emergency response and rescue operations',
            'key_events': [
                'Search and rescue operations',
                'Medical triage',
                'Emergency shelter establishment',
                'Assessment of damage'
            ]
        })
        
        # Stabilization phase
        phases.append({
            'phase': 'stabilization',
            'start_time_hours': release_time_hours + 24,
            'end_time_hours': release_time_hours + 168,  # 1 week
            'description': 'Situation stabilization and basic services restoration',
            'key_events': [
                'Water drainage efforts',
                'Temporary infrastructure',
                'Disease prevention measures',
                'Supply chain establishment'
            ]
        })
        
        # Recovery phase
        recovery_years = environmental_data['recovery_timeline']['infrastructure_recovery_years']
        phases.append({
            'phase': 'recovery_and_rebuilding',
            'start_time_hours': release_time_hours + 168,
            'end_time_hours': release_time_hours + (recovery_years * 8760),  # Convert years to hours
            'description': 'Long-term recovery and rebuilding efforts',
            'key_events': [
                'Infrastructure reconstruction',
                'Environmental restoration',
                'Economic recovery programs',
                'Community rebuilding'
            ]
        })
        
        return {
            'total_timeline_years': recovery_years + 1,
            'phases': phases,
            'critical_first_24_hours': {
                'casualties_occur_hours': min(release_time_hours, 6),
                'rescue_operations_start_hours': release_time_hours + 2,
                'medical_facilities_overwhelmed': casualty_data['immediate_casualties'] > 1000,
                'evacuation_completion_hours': release_time_hours + 12
            },
            'recovery_milestones': {
                'basic_services_restored_months': 3,
                'infrastructure_50_percent_restored_years': recovery_years * 0.3,
                'full_recovery_years': recovery_years,
                'new_normal_established_years': recovery_years + 2
            }
        }
    
    def _calculate_confidence_levels(self, scenario_config):
        """Calculate confidence levels for different aspects of the analysis"""
        
        # Base confidence levels for different model components
        confidence_factors = {
            'physical_calculations': 0.9,    # High confidence in physics
            'casualty_estimates': 0.6,       # Moderate confidence due to human factors
            'environmental_impact': 0.75,    # Good confidence for environmental processes
            'timeline_projections': 0.7,     # Good confidence for short-term, lower for long-term
            'seismic_effects': 0.5,         # Lower confidence due to uncertainty in energy conversion
            'weather_effects': 0.6          # Moderate confidence in atmospheric modeling
        }
        
        # Adjust confidence based on scenario complexity
        island_profile = scenario_config.get('island_profile', 'custom')
        if island_profile == 'custom':
            # Lower confidence for custom configurations
            for key in confidence_factors:
                confidence_factors[key] *= 0.9
        
        # Overall confidence
        overall_confidence = sum(confidence_factors.values()) / len(confidence_factors)
        
        return {
            'overall_confidence': overall_confidence,
            'component_confidence': confidence_factors,
            'uncertainty_sources': [
                'Water flow behavior complexity',
                'Human response variability', 
                'Terrain interaction effects',
                'Energy conversion efficiency factors',
                'Long-term environmental recovery rates'
            ],
            'confidence_interpretation': {
                'high': 'Results are based on well-established physics and data',
                'moderate': 'Results include estimates with reasonable uncertainty',
                'low': 'Results are preliminary estimates requiring validation'
            }
        }