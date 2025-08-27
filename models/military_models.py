import numpy as np
import pandas as pd
import math
from datetime import datetime, timedelta

# Custom haversine function since scipy.spatial.distance.haversine is not available
def haversine(coord1, coord2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    Returns distance in kilometers.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import json
import sqlite3

class MilitaryAnalyzer:
    """Comprehensive military analysis system with advanced modeling capabilities"""
    
    def __init__(self):
        self.weapon_systems = self._load_weapon_systems()
        self.defense_systems = self._load_defense_systems()
        self.country_military_data = self._load_country_military_data()
        self.terrain_modifiers = self._load_terrain_modifiers()

    def _load_weapon_systems(self):
        """Load comprehensive weapon systems database"""
        return {
            'ballistic_missiles': {
                'ICBM': {
                    'range_km': [5500, 15000],
                    'payload_kg': [1000, 3500],
                    'velocity_mps': [6000, 8000],
                    'accuracy_cep_m': [100, 300],
                    'cost_million_usd': [30, 100],
                    'launch_prep_minutes': [30, 120]
                },
                'IRBM': {
                    'range_km': [1000, 5499],
                    'payload_kg': [500, 2000],
                    'velocity_mps': [3000, 5000],
                    'accuracy_cep_m': [50, 200],
                    'cost_million_usd': [10, 40],
                    'launch_prep_minutes': [15, 60]
                },
                'SRBM': {
                    'range_km': [150, 999],
                    'payload_kg': [200, 1000],
                    'velocity_mps': [1000, 3000],
                    'accuracy_cep_m': [10, 100],
                    'cost_million_usd': [1, 15],
                    'launch_prep_minutes': [5, 30]
                }
            },
            'cruise_missiles': {
                'subsonic': {
                    'range_km': [200, 2500],
                    'payload_kg': [200, 500],
                    'velocity_mps': [200, 300],
                    'accuracy_cep_m': [1, 10],
                    'cost_million_usd': [0.5, 3],
                    'stealth_rating': [0.7, 0.9]
                },
                'supersonic': {
                    'range_km': [300, 1000],
                    'payload_kg': [300, 800],
                    'velocity_mps': [800, 1200],
                    'accuracy_cep_m': [5, 30],
                    'cost_million_usd': [2, 10],
                    'stealth_rating': [0.3, 0.6]
                },
                'hypersonic': {
                    'range_km': [500, 3000],
                    'payload_kg': [400, 1200],
                    'velocity_mps': [1700, 3500],
                    'accuracy_cep_m': [10, 50],
                    'cost_million_usd': [15, 50],
                    'stealth_rating': [0.8, 0.95]
                }
            },
            'conventional_weapons': {
                'artillery': {
                    'range_km': [20, 70],
                    'payload_kg': [10, 200],
                    'accuracy_cep_m': [50, 200],
                    'cost_thousand_usd': [2, 50],
                    'rate_of_fire_per_minute': [2, 8]
                },
                'air_strikes': {
                    'range_km': [500, 3000],
                    'payload_kg': [500, 10000],
                    'accuracy_cep_m': [1, 20],
                    'cost_thousand_usd': [50, 500],
                    'survivability_rating': [0.6, 0.9]
                }
            }
        }

    def _load_defense_systems(self):
        """Load comprehensive defense systems database"""
        return {
            'point_defense': {
                'Iron Dome': {
                    'max_range_km': 70,
                    'min_range_km': 4,
                    'intercept_altitude_m': [150, 40000],
                    'success_rate': 0.90,
                    'reaction_time_s': 15,
                    'cost_per_interceptor': 40000,
                    'radar_range_km': 160,
                    'simultaneous_targets': 20
                },
                'Patriot PAC-3': {
                    'max_range_km': 160,
                    'min_range_km': 3,
                    'intercept_altitude_m': [600, 40000],
                    'success_rate': 0.85,
                    'reaction_time_s': 20,
                    'cost_per_interceptor': 3000000,
                    'radar_range_km': 180,
                    'simultaneous_targets': 8
                }
            },
            'area_defense': {
                'THAAD': {
                    'max_range_km': 200,
                    'min_range_km': 40,
                    'intercept_altitude_m': [40000, 150000],
                    'success_rate': 0.95,
                    'reaction_time_s': 25,
                    'cost_per_interceptor': 15000000,
                    'radar_range_km': 1000,
                    'simultaneous_targets': 24
                },
                'S-400': {
                    'max_range_km': 400,
                    'min_range_km': 2,
                    'intercept_altitude_m': [10, 185000],
                    'success_rate': 0.92,
                    'reaction_time_s': 18,
                    'cost_per_interceptor': 1200000,
                    'radar_range_km': 600,
                    'simultaneous_targets': 36
                }
            }
        }

    def _load_country_military_data(self):
        """Load comprehensive country-specific military capabilities"""
        return {
            'USA': {
                'defense_budget_billion_usd': 816,
                'active_personnel': 1340000,
                'nuclear_warheads': 5800,
                'icbm_count': 400,
                'aircraft_carriers': 11,
                'fighter_aircraft': 2085,
                'main_battle_tanks': 6612,
                'defense_systems': ['Patriot PAC-3', 'THAAD', 'Aegis'],
                'military_tech_level': 10,
                'logistics_capability': 10,
                'force_projection': 10
            },
            'China': {
                'defense_budget_billion_usd': 293,
                'active_personnel': 2000000,
                'nuclear_warheads': 350,
                'icbm_count': 100,
                'aircraft_carriers': 3,
                'fighter_aircraft': 1200,
                'main_battle_tanks': 5800,
                'defense_systems': ['HQ-9', 'HQ-19', 'S-400'],
                'military_tech_level': 8,
                'logistics_capability': 7,
                'force_projection': 6
            },
            'Russia': {
                'defense_budget_billion_usd': 154,
                'active_personnel': 830000,
                'nuclear_warheads': 6375,
                'icbm_count': 310,
                'aircraft_carriers': 1,
                'fighter_aircraft': 1200,
                'main_battle_tanks': 12950,
                'defense_systems': ['S-400', 'S-500', 'Pantsir'],
                'military_tech_level': 8,
                'logistics_capability': 6,
                'force_projection': 7
            },
            'India': {
                'defense_budget_billion_usd': 76.6,
                'active_personnel': 1455550,
                'nuclear_warheads': 164,
                'icbm_count': 12,
                'aircraft_carriers': 2,
                'fighter_aircraft': 538,
                'main_battle_tanks': 4614,
                'defense_systems': ['Akash', 'S-400', 'Iron Dome'],
                'military_tech_level': 6,
                'logistics_capability': 5,
                'force_projection': 4
            },
            'Pakistan': {
                'defense_budget_billion_usd': 13.4,
                'active_personnel': 654000,
                'nuclear_warheads': 170,
                'icbm_count': 0,
                'fighter_aircraft': 348,
                'main_battle_tanks': 2496,
                'defense_systems': ['HQ-16', 'FM-90'],
                'military_tech_level': 5,
                'logistics_capability': 4,
                'force_projection': 3
            },
            'Iran': {
                'defense_budget_billion_usd': 25.0,
                'active_personnel': 610000,
                'nuclear_warheads': 0,
                'icbm_count': 0,
                'fighter_aircraft': 140,
                'main_battle_tanks': 1996,
                'defense_systems': ['Bavar-373', 'Khordad-15'],
                'military_tech_level': 4,
                'logistics_capability': 3,
                'force_projection': 2
            },
            'Israel': {
                'defense_budget_billion_usd': 24.3,
                'active_personnel': 170000,
                'nuclear_warheads': 90,
                'icbm_count': 0,
                'fighter_aircraft': 241,
                'main_battle_tanks': 1370,
                'defense_systems': ['Iron Dome', 'David Sling', 'Arrow-3'],
                'military_tech_level': 9,
                'logistics_capability': 8,
                'force_projection': 5
            }
        }

    def _load_terrain_modifiers(self):
        """Load terrain-based combat modifiers"""
        return {
            'urban': {'defense_bonus': 1.4, 'attack_penalty': 0.7, 'casualty_multiplier': 2.1},
            'mountain': {'defense_bonus': 1.6, 'attack_penalty': 0.6, 'casualty_multiplier': 1.3},
            'desert': {'defense_bonus': 0.9, 'attack_penalty': 1.1, 'casualty_multiplier': 1.1},
            'forest': {'defense_bonus': 1.2, 'attack_penalty': 0.8, 'casualty_multiplier': 1.4},
            'plains': {'defense_bonus': 1.0, 'attack_penalty': 1.0, 'casualty_multiplier': 1.0},
            'coastal': {'defense_bonus': 1.1, 'attack_penalty': 0.9, 'casualty_multiplier': 1.2}
        }

    def calculate_missile_trajectory(self, launch_coords, target_coords, missile_type, missile_subtype):
        """Calculate comprehensive missile trajectory with physics-based modeling"""
        # Extract coordinates
        lat1, lon1 = launch_coords
        lat2, lon2 = target_coords
        
        # Calculate great circle distance
        distance_km = haversine((lat1, lon1), (lat2, lon2))
        
        # Get missile specifications
        specs = self.weapon_systems[missile_type][missile_subtype]
        
        # Randomize within specification ranges
        velocity = np.random.uniform(specs['velocity_mps'][0], specs['velocity_mps'][1])
        payload_kg = np.random.uniform(specs['payload_kg'][0], specs['payload_kg'][1])
        accuracy_cep = np.random.uniform(specs['accuracy_cep_m'][0], specs['accuracy_cep_m'][1])
        
        # Calculate ballistic trajectory
        if missile_type == 'ballistic_missiles':
            # Ballistic trajectory calculation
            if distance_km > 300:  # Long range
                apogee_altitude_km = distance_km * 0.15 + np.random.uniform(-50, 50)
                trajectory_distance = math.sqrt(distance_km**2 + (2 * apogee_altitude_km)**2)
                flight_time = trajectory_distance * 1000 / velocity
                # Terminal velocity accounting for atmospheric re-entry
                terminal_velocity = velocity * 0.85
            else:  # Short to medium range
                trajectory_distance = distance_km
                flight_time = distance_km * 1000 / velocity
                terminal_velocity = velocity * 0.9
        else:  # Cruise missiles
            trajectory_distance = distance_km * 1.1  # Account for terrain following
            flight_time = trajectory_distance * 1000 / velocity
            terminal_velocity = velocity
        
        # Calculate impact parameters
        kinetic_energy_joules = 0.5 * payload_kg * terminal_velocity**2
        
        # Explosive yield calculation (depends on warhead type)
        if payload_kg > 1000:  # Likely nuclear
            explosive_yield_kt = payload_kg * 0.02  # Rough nuclear yield estimation
        else:  # Conventional
            explosive_yield_kg_tnt = payload_kg * 0.6  # High explosive efficiency
            explosive_yield_kt = explosive_yield_kg_tnt / 1000
        
        # Account for accuracy - miss distance affects impact
        actual_accuracy = accuracy_cep * np.random.exponential(0.5)  # CEP distribution
        
        return {
            'distance_km': distance_km,
            'trajectory_distance_km': trajectory_distance,
            'flight_time_seconds': flight_time,
            'flight_time_minutes': flight_time / 60,
            'apogee_altitude_km': apogee_altitude_km if missile_type == 'ballistic_missiles' and distance_km > 300 else 0,
            'terminal_velocity_mps': terminal_velocity,
            'kinetic_energy_joules': kinetic_energy_joules,
            'kinetic_energy_megajoules': kinetic_energy_joules / 1000000,
            'explosive_yield_kt': explosive_yield_kt,
            'accuracy_miss_distance_m': actual_accuracy,
            'launch_detection_time_s': max(60, flight_time * 0.1),  # Early warning time
            'payload_kg': payload_kg,
            'cost_million_usd': np.random.uniform(specs['cost_million_usd'][0], specs['cost_million_usd'][1])
        }

    def calculate_defense_interception_probability(self, trajectory_data, defense_systems_active, target_location):
        """Calculate comprehensive interception probability with multiple systems"""
        total_interception_prob = 0.0
        interception_attempts = []
        
        for system_name in defense_systems_active:
            system_specs = None
            # Find system in defense database
            for category in self.defense_systems.values():
                if system_name in category:
                    system_specs = category[system_name]
                    break
            
            if not system_specs:
                continue
            
            # Calculate if target is within engagement envelope
            distance_to_target = trajectory_data['distance_km']
            flight_time = trajectory_data['flight_time_seconds']
            missile_velocity = trajectory_data['terminal_velocity_mps']
            
            # Check range constraints
            if distance_to_target > system_specs['max_range_km']:
                continue
            
            # Calculate engagement window
            detection_time = trajectory_data['launch_detection_time_s']
            reaction_time = system_specs['reaction_time_s']
            engagement_time_available = max(0, flight_time - detection_time - reaction_time)
            
            if engagement_time_available <= 0:
                continue
            
            # Calculate base success probability
            base_success_rate = system_specs['success_rate']
            
            # Apply velocity penalty for fast targets
            velocity_factor = min(1.0, 1500 / missile_velocity)  # Harder to hit fast targets
            
            # Apply altitude considerations
            target_altitude = trajectory_data.get('apogee_altitude_km', 10) * 1000  # Convert to meters
            altitude_factor = 1.0
            if target_altitude < system_specs['intercept_altitude_m'][0]:
                altitude_factor = 0.3  # Below minimum altitude
            elif target_altitude > system_specs['intercept_altitude_m'][1]:
                altitude_factor = 0.5  # Above maximum altitude
            
            # Calculate number of engagement opportunities
            max_engagements = min(3, int(engagement_time_available / 10))  # Assume 10 seconds between shots
            
            # Single shot probability
            single_shot_prob = base_success_rate * velocity_factor * altitude_factor
            
            # Multiple engagement probability
            system_total_prob = 1 - (1 - single_shot_prob) ** max_engagements
            
            interception_attempts.append({
                'system': system_name,
                'engagement_range_km': min(distance_to_target, system_specs['max_range_km']),
                'single_shot_probability': single_shot_prob,
                'number_of_engagements': max_engagements,
                'total_probability': system_total_prob,
                'engagement_cost_usd': max_engagements * system_specs['cost_per_interceptor']
            })
            
            # Use highest probability system (systems don't stack perfectly)
            total_interception_prob = max(total_interception_prob, system_total_prob)
        
        # Apply coordination bonus if multiple systems
        if len(interception_attempts) > 1:
            coordination_bonus = min(0.15, len(interception_attempts) * 0.05)
            total_interception_prob = min(0.98, total_interception_prob + coordination_bonus)
        
        return {
            'total_interception_probability': total_interception_prob,
            'interception_attempts': interception_attempts,
            'total_defense_cost_usd': sum(attempt['engagement_cost_usd'] for attempt in interception_attempts),
            'recommended_systems': sorted(interception_attempts, key=lambda x: x['total_probability'], reverse=True)[:3]
        }

    def estimate_casualties_comprehensive(self, trajectory_data, target_area_data, weapon_type='conventional'):
        """Comprehensive casualty estimation with detailed modeling"""
        population_density = target_area_data.get('population_density', 1000)
        area_type = target_area_data.get('area_type', 'urban')
        protection_level = target_area_data.get('protection_level', 0.1)
        building_density = target_area_data.get('building_density', 0.6)
        time_of_day = target_area_data.get('time_of_day', 'day')  # day/night affects casualties
        
        explosive_yield_kt = trajectory_data['explosive_yield_kt']
        miss_distance = trajectory_data['accuracy_miss_distance_m']
        
        if weapon_type == 'nuclear':
            return self._calculate_nuclear_casualties(explosive_yield_kt, population_density,
                                                      area_type, protection_level, miss_distance)
        else:
            return self._calculate_conventional_casualties(explosive_yield_kt, population_density,
                                                           area_type, protection_level, miss_distance,
                                                           building_density, time_of_day)

    def _calculate_nuclear_casualties(self, yield_kt, pop_density, area_type, protection, miss_distance):
        """Calculate nuclear weapon casualties"""
        # Nuclear blast effects
        fireball_radius_m = 150 * (yield_kt ** 0.4)  # Fireball radius
        lethal_radiation_radius_m = 1200 * (yield_kt ** 0.4)  # Lethal radiation radius
        thermal_radiation_radius_m = 2000 * (yield_kt ** 0.4)  # Severe burns radius
        
        # Adjust for miss distance
        if miss_distance > fireball_radius_m:
            effective_yield_reduction = max(0.1, 1 - (miss_distance - fireball_radius_m) / fireball_radius_m)
            fireball_radius_m *= effective_yield_reduction
            lethal_radiation_radius_m *= effective_yield_reduction
            thermal_radiation_radius_m *= effective_yield_reduction
        
        # Calculate affected areas
        fireball_area_km2 = math.pi * (fireball_radius_m / 1000) ** 2
        radiation_area_km2 = math.pi * (lethal_radiation_radius_m / 1000) ** 2
        thermal_area_km2 = math.pi * (thermal_radiation_radius_m / 1000) ** 2
        
        # Apply terrain modifiers
        terrain_mod = self.terrain_modifiers.get(area_type, self.terrain_modifiers['urban'])
        casualty_multiplier = terrain_mod['casualty_multiplier']
        
        # Calculate casualties by zone
        fireball_deaths = int(fireball_area_km2 * pop_density * 0.98 * casualty_multiplier)  # Near 100% fatality
        radiation_deaths = int((radiation_area_km2 - fireball_area_km2) * pop_density * 0.75 * casualty_multiplier)
        thermal_injuries = int((thermal_area_km2 - radiation_area_km2) * pop_density * 0.6 * casualty_multiplier)
        
        # Apply protection factor
        fireball_deaths = int(fireball_deaths * (1 - protection * 0.1))  # Minimal protection from fireball
        radiation_deaths = int(radiation_deaths * (1 - protection * 0.5))  # Some protection from radiation
        thermal_injuries = int(thermal_injuries * (1 - protection * 0.7))  # Good protection from thermal
        
        immediate_deaths = fireball_deaths + radiation_deaths
        total_affected = immediate_deaths + thermal_injuries
        
        return {
            'immediate_casualties': immediate_deaths,
            'injured': thermal_injuries,
            'total_affected': total_affected,
            'fireball_radius_m': fireball_radius_m,
            'radiation_radius_m': lethal_radiation_radius_m,
            'thermal_radius_m': thermal_radiation_radius_m,
            'affected_area_km2': thermal_area_km2,
            'casualty_density_per_km2': immediate_deaths / thermal_area_km2 if thermal_area_km2 > 0 else 0,
            'infrastructure_damage_percent': min(98, yield_kt * 0.8 + 60),
            'economic_damage_billion_usd': thermal_area_km2 * yield_kt * 0.1  # Rough estimate
        }

    def _calculate_conventional_casualties(self, yield_kt, pop_density, area_type, protection,
                                           miss_distance, building_density, time_of_day):
        """Calculate conventional weapon casualties"""
        # Convert to TNT equivalent
        tnt_kg = yield_kt * 1000
        
        # Calculate blast radius (empirical formula)
        lethal_radius_m = 65 * (tnt_kg ** 0.33)  # 50% casualty radius
        damage_radius_m = lethal_radius_m * 2.5  # Building damage radius
        
        # Adjust for miss distance
        if miss_distance > lethal_radius_m:
            effective_yield_reduction = max(0.1, 1 - (miss_distance - lethal_radius_m) / lethal_radius_m)
            lethal_radius_m *= effective_yield_reduction
            damage_radius_m *= effective_yield_reduction
        
        # Calculate affected areas
        lethal_area_km2 = math.pi * (lethal_radius_m / 1000) ** 2
        damage_area_km2 = math.pi * (damage_radius_m / 1000) ** 2
        
        # Apply terrain modifiers
        terrain_mod = self.terrain_modifiers.get(area_type, self.terrain_modifiers['urban'])
        casualty_multiplier = terrain_mod['casualty_multiplier']
        
        # Calculate base casualties
        people_in_lethal_zone = lethal_area_km2 * pop_density
        people_in_damage_zone = (damage_area_km2 - lethal_area_km2) * pop_density
        
        # Apply time of day modifier
        if time_of_day == 'night':
            people_in_lethal_zone *= 1.2  # More people in buildings
            people_in_damage_zone *= 1.2
        else:
            people_in_lethal_zone *= 0.8  # Some people in stronger buildings, outdoors
            people_in_damage_zone *= 0.9
        
        # Apply protection and building density factors
        lethal_casualties = int(people_in_lethal_zone * (1 - protection) * 0.6 * casualty_multiplier)
        injured_in_damage_zone = int(people_in_damage_zone * (1 - protection * 0.5) * 0.3 * casualty_multiplier)
        
        # Calculate confidence intervals (30% uncertainty)
        uncertainty = 0.3
        casualties_lower = int(lethal_casualties * (1 - uncertainty))
        casualties_upper = int(lethal_casualties * (1 + uncertainty))
        
        total_affected = lethal_casualties + injured_in_damage_zone
        
        return {
            'immediate_casualties': lethal_casualties,
            'injured': injured_in_damage_zone,
            'total_affected': total_affected,
            'casualties_lower_bound': casualties_lower,
            'casualties_upper_bound': casualties_upper,
            'lethal_radius_m': lethal_radius_m,
            'damage_radius_m': damage_radius_m,
            'affected_area_km2': damage_area_km2,
            'casualty_density_per_km2': lethal_casualties / lethal_area_km2 if lethal_area_km2 > 0 else 0,
            'infrastructure_damage_percent': min(95, building_density * 60 + 20),
            'economic_damage_million_usd': damage_area_km2 * 50 * building_density  # Rough estimate
        }


class NuclearWarfareModel:
    """Comprehensive nuclear warfare modeling system"""
    
    def __init__(self):
        self.nuclear_arsenals = self._load_nuclear_arsenals()
        self.nuclear_doctrine = self._load_nuclear_doctrines()
        self.escalation_thresholds = self._load_escalation_thresholds()

    def _load_nuclear_arsenals(self):
        """Load detailed nuclear arsenal data"""
        return {
            'USA': {
                'total_warheads': 5800,
                'deployed_strategic': 1357,
                'deployed_tactical': 230,
                'icbm_warheads': 400,
                'slbm_warheads': 1152,
                'bomber_warheads': 300,
                'average_yield_kt': 150,
                'max_yield_kt': 1200,
                'first_strike_capability': True,
                'triad_complete': True
            },
            'Russia': {
                'total_warheads': 6375,
                'deployed_strategic': 1458,
                'deployed_tactical': 1912,
                'icbm_warheads': 834,
                'slbm_warheads': 624,
                'bomber_warheads': 200,
                'average_yield_kt': 200,
                'max_yield_kt': 800,
                'first_strike_capability': True,
                'triad_complete': True
            },
            'China': {
                'total_warheads': 350,
                'deployed_strategic': 290,
                'deployed_tactical': 60,
                'icbm_warheads': 200,
                'slbm_warheads': 90,
                'bomber_warheads': 60,
                'average_yield_kt': 250,
                'max_yield_kt': 1000,
                'first_strike_capability': False,
                'triad_complete': True
            },
            'India': {
                'total_warheads': 164,
                'deployed_strategic': 100,
                'deployed_tactical': 64,
                'icbm_warheads': 12,
                'slbm_warheads': 32,
                'bomber_warheads': 56,
                'average_yield_kt': 45,
                'max_yield_kt': 200,
                'first_strike_capability': False,
                'triad_complete': True
            },
            'Pakistan': {
                'total_warheads': 170,
                'deployed_strategic': 120,
                'deployed_tactical': 50,
                'icbm_warheads': 0,
                'slbm_warheads': 0,
                'bomber_warheads': 170,
                'average_yield_kt': 25,
                'max_yield_kt': 40,
                'first_strike_capability': False,
                'triad_complete': False
            }
        }

    def _load_nuclear_doctrines(self):
        """Load nuclear doctrine data for different countries"""
        return {
            'USA': {
                'first_use_policy': 'conditional',
                'no_first_use': False,
                'escalation_threshold': 'high',
                'tactical_nuclear_use': True,
                'launch_on_warning': True,
                'dead_hand': False
            },
            'Russia': {
                'first_use_policy': 'conditional',
                'no_first_use': False,
                'escalation_threshold': 'medium',
                'tactical_nuclear_use': True,
                'launch_on_warning': True,
                'dead_hand': True
            },
            'China': {
                'first_use_policy': 'no_first_use',
                'no_first_use': True,
                'escalation_threshold': 'very_high',
                'tactical_nuclear_use': False,
                'launch_on_warning': False,
                'dead_hand': False
            },
            'India': {
                'first_use_policy': 'no_first_use',
                'no_first_use': True,
                'escalation_threshold': 'high',
                'tactical_nuclear_use': False,
                'launch_on_warning': False,
                'dead_hand': False
            },
            'Pakistan': {
                'first_use_policy': 'conditional',
                'no_first_use': False,
                'escalation_threshold': 'low',
                'tactical_nuclear_use': True,
                'launch_on_warning': False,
                'dead_hand': False
            }
        }

    def _load_escalation_thresholds(self):
        """Load escalation threshold data"""
        return {
            'conventional_to_tactical': {
                'territorial_loss_percent': 10,
                'force_loss_percent': 30,
                'strategic_asset_threat': True,
                'decision_time_hours': 12
            },
            'tactical_to_strategic': {
                'nuclear_exchange_count': 3,
                'civilian_casualties': 100000,
                'capital_threat': True,
                'decision_time_hours': 6
            },
            'strategic_to_all_out': {
                'strategic_exchange_count': 10,
                'counterforce_failure': True,
                'leadership_threat': True,
                'decision_time_hours': 2
            }
        }

    def calculate_nuclear_exchange_scenario(self, attacker, defender, escalation_level, first_strike=False):
        """Model comprehensive nuclear exchange scenario"""
        attacker_arsenal = self.nuclear_arsenals[attacker]
        defender_arsenal = self.nuclear_arsenals[defender]
        
        # Determine strike parameters based on escalation level
        escalation_params = {
            'limited': {'warheads_used_percent': 0.05, 'civilian_targets': False},
            'tactical': {'warheads_used_percent': 0.15, 'civilian_targets': True},
            'strategic': {'warheads_used_percent': 0.4, 'civilian_targets': True},
            'all_out': {'warheads_used_percent': 0.8, 'civilian_targets': True}
        }
        
        params = escalation_params[escalation_level]
        
        # Calculate first strike
        attacker_warheads_used = int(attacker_arsenal['total_warheads'] * params['warheads_used_percent'])
        
        # Calculate retaliation capability (reduced if first strike successful)
        if first_strike and attacker_arsenal['first_strike_capability']:
            defender_retaliation_percent = 0.3  # Most forces destroyed
        else:
            defender_retaliation_percent = 0.7  # Some survivability
        
        defender_warheads_used = int(defender_arsenal['total_warheads'] * params['warheads_used_percent'] * defender_retaliation_percent)
        
        # Calculate casualties for each side
        attacker_casualties = self._calculate_nuclear_casualties_country(
            defender, attacker, defender_warheads_used, params['civilian_targets']
        )
        
        defender_casualties = self._calculate_nuclear_casualties_country(
            attacker, defender, attacker_warheads_used, params['civilian_targets']
        )
        
        # Calculate global effects
        global_effects = self._calculate_global_nuclear_effects(
            attacker_warheads_used + defender_warheads_used,
            (attacker_arsenal['average_yield_kt'] + defender_arsenal['average_yield_kt']) / 2
        )
        
        return {
            'scenario_type': f'{escalation_level}_nuclear_exchange',
            'first_strike': first_strike,
            'attacker_warheads_used': attacker_warheads_used,
            'defender_warheads_used': defender_warheads_used,
            'total_warheads_detonated': attacker_warheads_used + defender_warheads_used,
            'attacker_casualties': attacker_casualties,
            'defender_casualties': defender_casualties,
            'global_effects': global_effects,
            'escalation_probability': self._calculate_escalation_probability(escalation_level),
            'war_duration_days': self._estimate_war_duration(escalation_level),
            'international_response': self._model_international_response(attacker, defender, escalation_level)
        }

    def _calculate_escalation_probability(self, current_level):
        """Calculate probability of escalation to next level"""
        escalation_probabilities = {
            'limited': 0.25,  # 25% chance of escalating from limited
            'tactical': 0.40,  # 40% chance of escalating from tactical
            'strategic': 0.65,  # 65% chance of escalating from strategic
            'all_out': 0.0    # No further escalation possible
        }
        return escalation_probabilities.get(current_level, 0.0)

    def _estimate_war_duration(self, escalation_level):
        """Estimate war duration based on escalation level"""
        duration_estimates = {
            'limited': 7,     # 1 week for limited exchange
            'tactical': 14,   # 2 weeks for tactical exchange
            'strategic': 3,   # 3 days for strategic exchange
            'all_out': 1      # 1 day for all-out exchange
        }
        return duration_estimates.get(escalation_level, 7)

    def _model_international_response(self, attacker, defender, escalation_level):
        """Model international community response"""
        major_powers = ['USA', 'Russia', 'China', 'EU', 'India']
        
        response_intensity = {
            'limited': 'diplomatic_sanctions',
            'tactical': 'economic_isolation',
            'strategic': 'military_intervention',
            'all_out': 'global_crisis_management'
        }
        
        # Remove the conflicting parties from major powers list
        neutral_powers = [power for power in major_powers if power not in [attacker, defender]]
        
        return {
            'response_type': response_intensity[escalation_level],
            'neutral_powers': neutral_powers,
            'diplomatic_isolation_level': min(10, escalation_level == 'all_out' and 10 or 6),
            'economic_sanctions_severity': min(10, escalation_level == 'strategic' and 8 or 5),
            'humanitarian_aid_mobilization': True if escalation_level in ['strategic', 'all_out'] else False,
            'un_security_council_action': True,
            'refugee_assistance_required': True if escalation_level in ['tactical', 'strategic', 'all_out'] else False
        }

    def _calculate_nuclear_casualties_country(self, striker, target, warheads_used, civilian_targets):
        """Calculate nuclear casualties for entire country"""
        # This would need real population and infrastructure data
        # For now, using simplified model
        country_populations = {
            'USA': 331000000,
            'Russia': 146000000,
            'China': 1440000000,
            'India': 1380000000,
            'Pakistan': 225000000,
            'Iran': 84000000,
            'Israel': 9500000
        }
        
        target_population = country_populations.get(target, 50000000)
        
        # Average warhead yield
        avg_yield = self.nuclear_arsenals[striker]['average_yield_kt']
        
        if civilian_targets:
            # Target major cities - higher casualties per warhead
            casualties_per_warhead = 150000 * (avg_yield / 100) ** 0.6
        else:
            # Target military - lower casualties per warhead
            casualties_per_warhead = 50000 * (avg_yield / 100) ** 0.6
        
        immediate_deaths = int(min(warheads_used * casualties_per_warhead, target_population * 0.4))
        
        # Radiation and long-term effects
        radiation_deaths = int(immediate_deaths * 0.5)
        injured = int(immediate_deaths * 1.8)
        
        # Infrastructure destruction
        infrastructure_destruction_percent = min(85, warheads_used * 8)
        
        return {
            'immediate_deaths': immediate_deaths,
            'radiation_deaths_30_days': radiation_deaths,
            'total_deaths': immediate_deaths + radiation_deaths,
            'injured': injured,
            'total_affected': immediate_deaths + radiation_deaths + injured,
            'population_killed_percent': ((immediate_deaths + radiation_deaths) / target_population) * 100,
            'infrastructure_destroyed_percent': infrastructure_destruction_percent,
            'economic_collapse_percent': min(90, infrastructure_destruction_percent * 1.1)
        }

    def _calculate_global_nuclear_effects(self, total_warheads, avg_yield):
        """Calculate global effects of nuclear exchange"""
        total_yield_mt = (total_warheads * avg_yield) / 1000  # Convert to megatons
        
        # Nuclear winter effects
        if total_yield_mt > 5:  # Threshold for significant climate effects
            nuclear_winter = {
                'temperature_drop_celsius': min(15, total_yield_mt * 0.8),
                'duration_years': min(10, total_yield_mt / 10),
                'agricultural_reduction_percent': min(80, total_yield_mt * 6),
                'global_famine_risk': 'Very High' if total_yield_mt > 50 else 'High' if total_yield_mt > 20 else 'Moderate'
            }
        else:
            nuclear_winter = {
                'temperature_drop_celsius': 0,
                'duration_years': 0,
                'agricultural_reduction_percent': 0,
                'global_famine_risk': 'Low'
            }
        
        # EMP effects
        emp_affected_countries = min(12, int(total_warheads / 5))
        
        # Radiation spread
        fallout_area_km2 = total_warheads * avg_yield * 150  # Rough estimate
        
        return {
            'nuclear_winter': nuclear_winter,
            'emp_affected_countries': emp_affected_countries,
            'radioactive_fallout_area_km2': fallout_area_km2,
            'global_economy_contraction_percent': min(40, total_yield_mt * 2),
            'refugee_population_millions': min(500, total_yield_mt * 15),
            'international_trade_disruption_percent': min(90, total_yield_mt * 4)
        }


class DefenseSystemModel:
    """Comprehensive defense system modeling"""
    
    def __init__(self):
        self.layered_defense_configs = self._load_layered_defense()

    def _load_layered_defense(self):
        """Load layered defense system configurations"""
        return {
            'israel_model': {
                'layers': [
                    {'name': 'Iron Dome', 'range_km': 70, 'altitude_m': [150, 40000], 'targets': 'short_range'},
                    {'name': 'David Sling', 'range_km': 300, 'altitude_m': [1000, 80000], 'targets': 'medium_range'},
                    {'name': 'Arrow-2', 'range_km': 90, 'altitude_m': [20000, 100000], 'targets': 'ballistic'},
                    {'name': 'Arrow-3', 'range_km': 2400, 'altitude_m': [100000, 800000], 'targets': 'exo_atmospheric'}
                ],
                'integration_bonus': 0.15,
                'total_cost_billion': 15
            },
            'usa_model': {
                'layers': [
                    {'name': 'Patriot PAC-3', 'range_km': 160, 'altitude_m': [600, 40000], 'targets': 'theater'},
                    {'name': 'THAAD', 'range_km': 200, 'altitude_m': [40000, 150000], 'targets': 'high_altitude'},
                    {'name': 'Aegis SM-3', 'range_km': 2500, 'altitude_m': [80000, 1500000], 'targets': 'exo_atmospheric'},
                    {'name': 'GMD', 'range_km': 5500, 'altitude_m': [200000, 2000000], 'targets': 'icbm'}
                ],
                'integration_bonus': 0.2,
                'total_cost_billion': 120
            }
        }

    def evaluate_defense_effectiveness(self, threat_scenario, defense_config):
        """Evaluate comprehensive defense system effectiveness"""
        threats = threat_scenario['incoming_threats']
        defense_layers = defense_config['layers']
        total_threats = len(threats)
        intercepted_threats = 0
        defense_cost = 0
        detailed_intercepts = []
        
        for threat in threats:
            threat_intercepted = False
            threat_intercept_attempts = []
            
            for layer in defense_layers:
                if threat_intercepted:
                    break
                
                # Check if layer can engage this threat
                if self._can_layer_engage_threat(layer, threat):
                    intercept_prob = self._calculate_layer_intercept_probability(layer, threat)
                    intercept_cost = self._calculate_intercept_cost(layer)
                    
                    # Simulate intercept attempt
                    if np.random.random() < intercept_prob:
                        threat_intercepted = True
                        intercepted_threats += 1
                        defense_cost += intercept_cost
                        
                        threat_intercept_attempts.append({
                            'layer': layer['name'],
                            'success': True,
                            'probability': intercept_prob,
                            'cost': intercept_cost
                        })
                    else:
                        defense_cost += intercept_cost
                        threat_intercept_attempts.append({
                            'layer': layer['name'],
                            'success': False,
                            'probability': intercept_prob,
                            'cost': intercept_cost
                        })
            
            detailed_intercepts.append({
                'threat_id': threat.get('id', len(detailed_intercepts)),
                'threat_type': threat['type'],
                'intercepted': threat_intercepted,
                'intercept_attempts': threat_intercept_attempts
            })
        
        # Apply integration bonus if multiple layers worked together
        if len([d for d in detailed_intercepts if len(d['intercept_attempts']) > 1]) > 0:
            integration_bonus_intercepts = int(total_threats * defense_config['integration_bonus'])
            intercepted_threats = min(total_threats, intercepted_threats + integration_bonus_intercepts)
        
        effectiveness_percent = (intercepted_threats / total_threats) * 100 if total_threats > 0 else 0
        
        return {
            'total_threats': total_threats,
            'intercepted_threats': intercepted_threats,
            'penetrating_threats': total_threats - intercepted_threats,
            'effectiveness_percent': effectiveness_percent,
            'total_defense_cost_million': defense_cost / 1000000,
            'cost_per_intercept_million': (defense_cost / 1000000) / max(1, intercepted_threats),
            'detailed_intercepts': detailed_intercepts,
            'layer_performance': self._analyze_layer_performance(detailed_intercepts)
        }

    def _analyze_layer_performance(self, detailed_intercepts):
        """Analyze performance of each defense layer"""
        layer_stats = {}
        
        for intercept in detailed_intercepts:
            for attempt in intercept['intercept_attempts']:
                layer_name = attempt['layer']
                if layer_name not in layer_stats:
                    layer_stats[layer_name] = {
                        'attempts': 0,
                        'successes': 0,
                        'total_cost': 0,
                        'success_rate': 0
                    }
                
                layer_stats[layer_name]['attempts'] += 1
                layer_stats[layer_name]['total_cost'] += attempt['cost']
                
                if attempt['success']:
                    layer_stats[layer_name]['successes'] += 1
        
        # Calculate success rates
        for layer_name in layer_stats:
            attempts = layer_stats[layer_name]['attempts']
            successes = layer_stats[layer_name]['successes']
            layer_stats[layer_name]['success_rate'] = (successes / attempts) if attempts > 0 else 0
        
        return layer_stats

    def _can_layer_engage_threat(self, layer, threat):
        """Check if defense layer can engage specific threat"""
        threat_range = threat.get('range_km', 0)
        threat_altitude = threat.get('altitude_m', 10000)
        threat_type = threat.get('type', 'ballistic')
        
        # Range check
        if threat_range > layer['range_km']:
            return False
        
        # Altitude check
        if not (layer['altitude_m'][0] <= threat_altitude <= layer['altitude_m'][1]):
            return False
        
        # Target type compatibility
        layer_targets = layer['targets']
        if layer_targets == 'short_range' and threat_type not in ['rocket', 'mortar']:
            return False
        
        return True

    def _calculate_layer_intercept_probability(self, layer, threat):
        """Calculate intercept probability for specific layer against threat"""
        base_probabilities = {
            'Iron Dome': 0.90,
            'David Sling': 0.85,
            'Arrow-2': 0.88,
            'Arrow-3': 0.85,
            'Patriot PAC-3': 0.80,
            'THAAD': 0.95,
            'Aegis SM-3': 0.83,
            'GMD': 0.65
        }
        
        base_prob = base_probabilities.get(layer['name'], 0.75)
        
        # Apply threat-specific modifiers
        if threat.get('stealth', False):
            base_prob *= 0.7
        
        if threat.get('velocity_mps', 1000) > 3000:
            base_prob *= 0.85  # Harder to hit fast targets
        
        if threat.get('maneuverable', False):
            base_prob *= 0.6  # Much harder to hit maneuverable targets
        
        return min(0.98, base_prob)

    def _calculate_intercept_cost(self, layer):
        """Calculate cost of intercept attempt"""
        intercept_costs = {
            'Iron Dome': 40000,
            'David Sling': 1000000,
            'Arrow-2': 3000000,
            'Arrow-3': 2200000,
            'Patriot PAC-3': 3000000,
            'THAAD': 15000000,
            'Aegis SM-3': 12000000,
            'GMD': 75000000
        }
        
        return intercept_costs.get(layer['name'], 1000000)