import numpy as np
import pandas as pd
import networkx as nx
from datetime import datetime, timedelta
import json
import math
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from collections import defaultdict

class EconomicImpactModel:
    """Comprehensive economic impact modeling system"""
    
    def __init__(self):
        self.country_economic_data = self._load_country_economic_data()
        self.sector_interdependencies = self._load_sector_interdependencies()
        self.global_trade_matrix = self._load_global_trade_matrix()
        self.economic_indicators = self._load_economic_indicators()

    def _load_country_economic_data(self):
        """Load comprehensive economic data for all countries"""
        return {
            'USA': {
                'gdp_trillion_usd': 26.9,
                'gdp_per_capita': 80412,
                'population': 331900000,
                'unemployment_rate': 3.4,
                'inflation_rate': 3.2,
                'debt_to_gdp_ratio': 106.7,
                'credit_rating': 'AAA',
                'economic_complexity_index': 1.46,
                'major_industries': ['technology', 'finance', 'healthcare', 'energy', 'defense'],
                'trade_dependence': 0.27,
                'currency_stability': 0.95,
                'financial_system_strength': 0.98
            },
            'China': {
                'gdp_trillion_usd': 17.9,
                'gdp_per_capita': 12556,
                'population': 1425671352,
                'unemployment_rate': 5.2,
                'inflation_rate': 2.1,
                'debt_to_gdp_ratio': 77.1,
                'credit_rating': 'A+',
                'economic_complexity_index': 0.47,
                'major_industries': ['manufacturing', 'technology', 'construction', 'agriculture'],
                'trade_dependence': 0.36,
                'currency_stability': 0.82,
                'financial_system_strength': 0.75
            },
            'Germany': {
                'gdp_trillion_usd': 4.26,
                'gdp_per_capita': 51203,
                'population': 83240525,
                'unemployment_rate': 5.6,
                'inflation_rate': 8.7,
                'debt_to_gdp_ratio': 69.7,
                'credit_rating': 'AAA',
                'economic_complexity_index': 1.88,
                'major_industries': ['automotive', 'machinery', 'chemicals', 'technology'],
                'trade_dependence': 0.84,
                'currency_stability': 0.92,
                'financial_system_strength': 0.89
            },
            'Japan': {
                'gdp_trillion_usd': 4.94,
                'gdp_per_capita': 39340,
                'population': 125584838,
                'unemployment_rate': 2.6,
                'inflation_rate': 3.0,
                'debt_to_gdp_ratio': 261.3,
                'credit_rating': 'A',
                'economic_complexity_index': 1.59,
                'major_industries': ['automotive', 'electronics', 'machinery', 'steel'],
                'trade_dependence': 0.35,
                'currency_stability': 0.87,
                'financial_system_strength': 0.93
            },
            'India': {
                'gdp_trillion_usd': 3.74,
                'gdp_per_capita': 2601,
                'population': 1428627663,
                'unemployment_rate': 7.8,
                'inflation_rate': 5.7,
                'debt_to_gdp_ratio': 89.6,
                'credit_rating': 'BBB-',
                'economic_complexity_index': 0.21,
                'major_industries': ['services', 'agriculture', 'manufacturing', 'textiles'],
                'trade_dependence': 0.42,
                'currency_stability': 0.73,
                'financial_system_strength': 0.68
            },
            'Pakistan': {
                'gdp_trillion_usd': 0.35,
                'gdp_per_capita': 1596,
                'population': 231402117,
                'unemployment_rate': 6.3,
                'inflation_rate': 29.2,
                'debt_to_gdp_ratio': 87.2,
                'credit_rating': 'CCC+',
                'economic_complexity_index': -0.59,
                'major_industries': ['textiles', 'agriculture', 'chemicals', 'food_processing'],
                'trade_dependence': 0.32,
                'currency_stability': 0.45,
                'financial_system_strength': 0.38
            },
            'Russia': {
                'gdp_trillion_usd': 1.83,
                'gdp_per_capita': 12654,
                'population': 144713314,
                'unemployment_rate': 3.7,
                'inflation_rate': 13.8,
                'debt_to_gdp_ratio': 18.9,
                'credit_rating': 'B',
                'economic_complexity_index': 0.25,
                'major_industries': ['oil_gas', 'mining', 'defense', 'agriculture'],
                'trade_dependence': 0.46,
                'currency_stability': 0.52,
                'financial_system_strength': 0.48
            },
            'Iran': {
                'gdp_trillion_usd': 0.23,
                'gdp_per_capita': 2757,
                'population': 85028759,
                'unemployment_rate': 11.2,
                'inflation_rate': 40.2,
                'debt_to_gdp_ratio': 48.1,
                'credit_rating': 'CCC',
                'economic_complexity_index': -0.21,
                'major_industries': ['oil_gas', 'petrochemicals', 'textiles', 'agriculture'],
                'trade_dependence': 0.25,
                'currency_stability': 0.28,
                'financial_system_strength': 0.31
            }
        }

    def _load_sector_interdependencies(self):
        """Load sector interdependency matrix"""
        return {
            'agriculture': {
                'depends_on': ['energy', 'transportation', 'manufacturing', 'water'],
                'supports': ['food_processing', 'retail', 'export'],
                'vulnerability_score': 0.7,
                'resilience_days': 30
            },
            'energy': {
                'depends_on': ['mining', 'transportation', 'technology', 'finance'],
                'supports': ['manufacturing', 'transportation', 'residential', 'commercial'],
                'vulnerability_score': 0.9,
                'resilience_days': 7
            },
            'manufacturing': {
                'depends_on': ['energy', 'raw_materials', 'transportation', 'labor'],
                'supports': ['retail', 'export', 'construction', 'technology'],
                'vulnerability_score': 0.8,
                'resilience_days': 14
            },
            'finance': {
                'depends_on': ['technology', 'energy', 'legal_framework'],
                'supports': ['all_sectors'],
                'vulnerability_score': 0.95,
                'resilience_days': 1
            },
            'healthcare': {
                'depends_on': ['energy', 'pharmaceuticals', 'technology', 'transportation'],
                'supports': ['workforce', 'population_stability'],
                'vulnerability_score': 0.6,
                'resilience_days': 21
            },
            'technology': {
                'depends_on': ['energy', 'semiconductors', 'rare_earth_materials'],
                'supports': ['all_sectors'],
                'vulnerability_score': 0.85,
                'resilience_days': 5
            },
            'transportation': {
                'depends_on': ['energy', 'infrastructure', 'technology'],
                'supports': ['all_sectors'],
                'vulnerability_score': 0.8,
                'resilience_days': 3
            }
        }

    def _load_global_trade_matrix(self):
        """Load global trade dependency matrix"""
        return {
            'semiconductors': {
                'primary_suppliers': ['Taiwan', 'South Korea', 'China'],
                'market_concentration': 0.89,
                'annual_trade_billion': 574,
                'substitution_difficulty': 0.95,
                'strategic_importance': 0.98
            },
            'oil_gas': {
                'primary_suppliers': ['Saudi Arabia', 'Russia', 'USA', 'Iran'],
                'market_concentration': 0.67,
                'annual_trade_billion': 2100,
                'substitution_difficulty': 0.3,
                'strategic_importance': 0.92
            },
            'rare_earth_elements': {
                'primary_suppliers': ['China', 'Australia', 'USA'],
                'market_concentration': 0.92,
                'annual_trade_billion': 8.5,
                'substitution_difficulty': 0.88,
                'strategic_importance': 0.85
            },
            'pharmaceuticals': {
                'primary_suppliers': ['China', 'India', 'Germany', 'USA'],
                'market_concentration': 0.72,
                'annual_trade_billion': 425,
                'substitution_difficulty': 0.65,
                'strategic_importance': 0.9
            },
            'food_grains': {
                'primary_suppliers': ['Russia', 'Ukraine', 'USA', 'Brazil'],
                'market_concentration': 0.58,
                'annual_trade_billion': 180,
                'substitution_difficulty': 0.4,
                'strategic_importance': 0.88
            }
        }

    def _load_economic_indicators(self):
        """Load economic indicator definitions and thresholds"""
        return {
            'recession_thresholds': {
                'gdp_decline_percent': -2.0,
                'duration_quarters': 2,
                'unemployment_increase': 2.0
            },
            'crisis_indicators': {
                'currency_devaluation_threshold': 20.0,
                'inflation_spike_threshold': 15.0,
                'debt_crisis_threshold': 90.0,
                'market_crash_threshold': -30.0
            },
            'recovery_indicators': {
                'gdp_growth_minimum': 1.0,
                'unemployment_decline_rate': 0.5,
                'inflation_stability_range': [1.0, 4.0],
                'currency_stability_threshold': 0.8
            },
            'systemic_risk_factors': {
                'financial_system_weakness': 0.5,
                'trade_dependence_risk': 0.7,
                'debt_sustainability_risk': 100.0,
                'political_stability_risk': 0.3
            }
        }

    def calculate_economic_warfare_impact(self, attacker, target, warfare_type, intensity, duration_days):
        """Calculate comprehensive economic warfare impact"""
        target_economy = self.country_economic_data[target]
        attacker_economy = self.country_economic_data.get(attacker, {})
        
        # Base economic damage calculation
        base_damage = self._calculate_base_economic_damage(target_economy, warfare_type, intensity)
        
        # Apply duration effects
        duration_multiplier = self._calculate_duration_multiplier(duration_days, warfare_type)
        
        # Calculate sectoral impacts
        sectoral_impacts = self._calculate_sectoral_impacts(target, warfare_type, intensity)
        
        # Calculate cascade effects
        cascade_effects = self._calculate_cascade_effects(sectoral_impacts, target)
        
        # Calculate international spillovers
        international_spillovers = self._calculate_international_spillovers(target, base_damage)
        
        total_economic_damage = base_damage * duration_multiplier + cascade_effects
        
        # GDP impact calculation
        gdp_impact_percent = min(50, (total_economic_damage / (target_economy['gdp_trillion_usd'] * 1e12)) * 100)
        
        # Employment impact
        unemployment_increase = self._calculate_unemployment_impact(gdp_impact_percent, sectoral_impacts)
        
        # Inflation impact
        inflation_increase = self._calculate_inflation_impact(warfare_type, intensity, sectoral_impacts)
        
        # Recovery timeline
        recovery_timeline = self._calculate_recovery_timeline(gdp_impact_percent, target_economy, warfare_type)
        
        return {
            'target_country': target,
            'warfare_type': warfare_type,
            'intensity_level': intensity,
            'duration_days': duration_days,
            'economic_damage': {
                'total_damage_usd': total_economic_damage,
                'base_damage_usd': base_damage,
                'cascade_effects_usd': cascade_effects,
                'gdp_impact_percent': gdp_impact_percent,
                'per_capita_loss_usd': total_economic_damage / target_economy['population']
            },
            'sectoral_impacts': sectoral_impacts,
            'macroeconomic_effects': {
                'unemployment_increase_percent': unemployment_increase,
                'inflation_increase_percent': inflation_increase,
                'currency_devaluation_percent': self._calculate_currency_impact(gdp_impact_percent, target_economy),
                'credit_rating_impact': self._calculate_credit_rating_impact(gdp_impact_percent, target_economy)
            },
            'recovery_analysis': recovery_timeline,
            'international_spillovers': international_spillovers,
            'strategic_assessment': self._assess_economic_warfare_effectiveness(total_economic_damage, target_economy)
        }

    def _calculate_base_economic_damage(self, target_economy, warfare_type, intensity):
        """Calculate base economic damage based on warfare type and intensity"""
        gdp_usd = target_economy['gdp_trillion_usd'] * 1e12
        
        # Base damage factors by warfare type
        damage_factors = {
            'sanctions': {
                'low': 0.02,    # 2% of GDP
                'medium': 0.08, # 8% of GDP
                'high': 0.18,   # 18% of GDP
                'extreme': 0.35 # 35% of GDP
            },
            'supply_chain_disruption': {
                'low': 0.03,
                'medium': 0.12,
                'high': 0.25,
                'extreme': 0.45
            },
            'financial_system_attack': {
                'low': 0.05,
                'medium': 0.15,
                'high': 0.35,
                'extreme': 0.60
            },
            'infrastructure_targeting': {
                'low': 0.04,
                'medium': 0.14,
                'high': 0.28,
                'extreme': 0.50
            },
            'cyber_warfare': {
                'low': 0.01,
                'medium': 0.06,
                'high': 0.18,
                'extreme': 0.40
            }
        }
        
        damage_factor = damage_factors.get(warfare_type, damage_factors['sanctions'])[intensity]
        
        # Apply country-specific vulnerabilities
        vulnerability_modifier = 1.0
        if target_economy['trade_dependence'] > 0.5:
            vulnerability_modifier += 0.3
        if target_economy['financial_system_strength'] < 0.7:
            vulnerability_modifier += 0.2
        if target_economy['currency_stability'] < 0.6:
            vulnerability_modifier += 0.4
            
        return gdp_usd * damage_factor * vulnerability_modifier

    def _calculate_duration_multiplier(self, duration_days, warfare_type):
        """Calculate duration multiplier for sustained economic warfare"""
        # Base duration effects
        base_multipliers = {
            'sanctions': {
                30: 1.0,   # 1 month baseline
                90: 1.4,   # 3 months
                180: 1.8,  # 6 months
                365: 2.3,  # 1 year
                730: 2.8   # 2 years
            },
            'supply_chain_disruption': {
                30: 1.2,   # More immediate impact
                90: 1.6,
                180: 2.0,
                365: 2.5,
                730: 3.0
            },
            'financial_system_attack': {
                30: 1.3,   # Quick severe impact
                90: 1.7,
                180: 2.1,
                365: 2.6,
                730: 3.1
            },
            'infrastructure_targeting': {
                30: 1.1,
                90: 1.5,
                180: 1.9,
                365: 2.4,
                730: 2.9
            },
            'cyber_warfare': {
                30: 1.0,
                90: 1.3,
                180: 1.6,
                365: 2.0,
                730: 2.4
            }
        }
        
        multipliers = base_multipliers.get(warfare_type, base_multipliers['sanctions'])
        
        # Find closest duration key
        duration_keys = sorted(multipliers.keys())
        for key in duration_keys:
            if duration_days <= key:
                return multipliers[key]
        
        # If duration exceeds maximum, extrapolate
        return multipliers[max(duration_keys)] * (duration_days / max(duration_keys)) ** 0.3

    def _calculate_recovery_timeline(self, gdp_impact_percent, target_economy, warfare_type):
        """Calculate comprehensive economic recovery timeline"""
        # Base recovery periods by damage level
        base_recovery_months = {
            (0, 5): 6,      # Minor damage: 6 months
            (5, 15): 18,    # Moderate damage: 1.5 years
            (15, 30): 36,   # Severe damage: 3 years
            (30, 50): 60,   # Extreme damage: 5 years
            (50, 100): 120  # Catastrophic: 10 years
        }
        
        # Find appropriate recovery period
        recovery_months = 120  # Default maximum
        for (min_damage, max_damage), months in base_recovery_months.items():
            if min_damage <= gdp_impact_percent < max_damage:
                recovery_months = months
                break
        
        # Apply country-specific modifiers
        country_resilience = (
            target_economy['financial_system_strength'] * 0.4 +
            target_economy['currency_stability'] * 0.3 +
            (1 - target_economy['debt_to_gdp_ratio'] / 150) * 0.3
        )
        
        # Warfare type affects recovery speed
        warfare_recovery_factors = {
            'sanctions': 0.8,                    # Easier to recover from
            'supply_chain_disruption': 0.9,     # Medium recovery difficulty
            'financial_system_attack': 1.2,     # Harder to recover from
            'infrastructure_targeting': 1.1,    # Physical rebuilding needed
            'cyber_warfare': 0.7                # Faster digital recovery
        }
        
        warfare_factor = warfare_recovery_factors.get(warfare_type, 1.0)
        adjusted_recovery_months = recovery_months * warfare_factor / max(0.3, country_resilience)
        
        # Recovery phases
        phases = {
            'crisis_phase': int(adjusted_recovery_months * 0.2),
            'stabilization_phase': int(adjusted_recovery_months * 0.3),
            'recovery_phase': int(adjusted_recovery_months * 0.5)
        }
        
        return {
            'total_recovery_months': int(adjusted_recovery_months),
            'phases': phases,
            'country_resilience_score': country_resilience,
            'warfare_impact_factor': warfare_factor,
            'recovery_certainty': max(0.4, 1.0 - gdp_impact_percent / 100)
        }

    def _calculate_currency_impact(self, gdp_impact_percent, target_economy):
        """Calculate currency devaluation from economic damage"""
        base_devaluation = gdp_impact_percent * 1.5  # GDP impact amplified for currency
        
        # Country-specific vulnerability factors
        currency_vulnerability = 1.0 - target_economy['currency_stability']
        debt_factor = max(0, target_economy['debt_to_gdp_ratio'] - 60) / 100  # Debt above 60% adds risk
        trade_factor = target_economy['trade_dependence'] * 0.5  # Trade dependence adds vulnerability
        
        total_devaluation = base_devaluation * (1 + currency_vulnerability + debt_factor + trade_factor)
        
        return min(80, total_devaluation)  # Cap at 80% devaluation

    def _calculate_credit_rating_impact(self, gdp_impact_percent, target_economy):
        """Calculate credit rating impact from economic damage"""
        current_rating = target_economy['credit_rating']
        
        # Rating scale mapping
        rating_scale = {
            'AAA': 10, 'AA+': 9, 'AA': 8, 'AA-': 7,
            'A+': 6, 'A': 5, 'A-': 4,
            'BBB+': 3, 'BBB': 2, 'BBB-': 1,
            'BB+': 0, 'BB': -1, 'BB-': -2,
            'B+': -3, 'B': -4, 'B-': -5,
            'CCC+': -6, 'CCC': -7, 'CCC-': -8,
            'CC': -9, 'C': -10, 'D': -11
        }
        
        reverse_scale = {v: k for k, v in rating_scale.items()}
        current_score = rating_scale.get(current_rating, 0)
        
        # Calculate rating impact
        rating_decline = int(gdp_impact_percent / 8)  # 1 notch per 8% GDP impact
        new_score = max(-11, current_score - rating_decline)
        new_rating = reverse_scale.get(new_score, 'D')
        
        return {
            'current_rating': current_rating,
            'new_rating': new_rating,
            'notches_downgrade': rating_decline,
            'investment_grade_loss': new_score < 1 and current_score >= 1
        }

    def _assess_economic_warfare_effectiveness(self, total_damage, target_economy):
        """Assess the strategic effectiveness of economic warfare"""
        gdp_usd = target_economy['gdp_trillion_usd'] * 1e12
        damage_ratio = total_damage / gdp_usd
        
        # Effectiveness categories
        if damage_ratio < 0.05:
            effectiveness = 'minimal'
            strategic_impact = 'Limited disruption, unlikely to change behavior'
        elif damage_ratio < 0.15:
            effectiveness = 'moderate'
            strategic_impact = 'Noticeable impact, may influence policy decisions'
        elif damage_ratio < 0.30:
            effectiveness = 'significant'
            strategic_impact = 'Substantial damage, likely to force strategic changes'
        elif damage_ratio < 0.50:
            effectiveness = 'severe'
            strategic_impact = 'Major economic crisis, government stability at risk'
        else:
            effectiveness = 'catastrophic'
            strategic_impact = 'Economic collapse, regime change possible'
        
        # Calculate collateral damage to attacker
        self_damage_factor = 0.1 * target_economy['trade_dependence']  # Trade partners suffer
        
        return {
            'effectiveness_level': effectiveness,
            'damage_ratio': damage_ratio,
            'strategic_impact': strategic_impact,
            'estimated_self_damage_percent': self_damage_factor * 100,
            'success_probability': min(0.9, damage_ratio * 2),  # Higher damage = higher success
            'unintended_consequences_risk': max(0.1, damage_ratio - 0.2)
        }

    def _calculate_sectoral_impacts(self, target_country, warfare_type, intensity):
        """Calculate impact on specific economic sectors"""
        target_economy = self.country_economic_data[target_country]
        sectoral_impacts = {}
        
        # Define sector vulnerability to different warfare types
        sector_vulnerabilities = {
            'sanctions': {
                'export_industries': 0.8,
                'finance': 0.6,
                'technology': 0.7,
                'energy': 0.5,
                'agriculture': 0.3
            },
            'supply_chain_disruption': {
                'manufacturing': 0.9,
                'technology': 0.85,
                'automotive': 0.8,
                'pharmaceuticals': 0.7,
                'agriculture': 0.4
            },
            'financial_system_attack': {
                'finance': 0.95,
                'real_estate': 0.7,
                'retail': 0.6,
                'manufacturing': 0.5,
                'services': 0.4
            },
            'infrastructure_targeting': {
                'energy': 0.9,
                'transportation': 0.85,
                'telecommunications': 0.8,
                'water_utilities': 0.75,
                'manufacturing': 0.6
            }
        }
        
        intensity_multipliers = {'low': 0.3, 'medium': 0.6, 'high': 0.8, 'extreme': 1.0}
        vulnerabilities = sector_vulnerabilities.get(warfare_type, sector_vulnerabilities['sanctions'])
        intensity_mult = intensity_multipliers[intensity]
        
        for sector, vulnerability in vulnerabilities.items():
            # Estimate sector size as percentage of GDP
            sector_gdp_share = self._estimate_sector_gdp_share(target_country, sector)
            sector_gdp_usd = target_economy['gdp_trillion_usd'] * 1e12 * sector_gdp_share
            
            # Calculate sector damage
            sector_damage = sector_gdp_usd * vulnerability * intensity_mult
            
            # Calculate employment impact
            sector_employment_share = self._estimate_sector_employment_share(target_country, sector)
            jobs_at_risk = int(target_economy['population'] * 0.6 * sector_employment_share * vulnerability * intensity_mult)
            
            sectoral_impacts[sector] = {
                'gdp_share_percent': sector_gdp_share * 100,
                'damage_usd': sector_damage,
                'damage_percent': vulnerability * intensity_mult * 100,
                'jobs_at_risk': jobs_at_risk,
                'recovery_months': self._estimate_sector_recovery_time(sector, vulnerability * intensity_mult)
            }
        
        return sectoral_impacts

    def _estimate_sector_recovery_time(self, sector, damage_factor):
        """Estimate sector-specific recovery time"""
        base_recovery_times = {
            'finance': 6,           # Financial markets recover relatively quickly
            'technology': 12,       # Tech sector medium recovery
            'manufacturing': 18,    # Physical infrastructure takes longer
            'energy': 24,          # Energy infrastructure complex to rebuild
            'agriculture': 12,     # Seasonal but can recover
            'transportation': 15,   # Infrastructure dependent
            'healthcare': 9,       # Critical sector gets priority
            'retail': 8,           # Consumer sectors bounce back faster
            'construction': 20,    # Physical rebuilding sector
            'automotive': 15,      # Manufacturing with supply chains
            'telecommunications': 10, # Tech infrastructure
            'water_utilities': 18,   # Essential infrastructure
            'pharmaceuticals': 14,   # Regulated but essential
            'real_estate': 30,      # Long-term asset recovery
            'services': 10,         # Service sectors flexible
            'export_industries': 16  # Trade dependent recovery
        }
        
        base_months = base_recovery_times.get(sector, 12)
        return int(base_months * (1 + damage_factor))

    def _calculate_cascade_effects(self, sectoral_impacts, target_country):
        """Calculate economic cascade effects through supply chains"""
        total_cascade_damage = 0
        
        for affected_sector, impact in sectoral_impacts.items():
            sector_interdeps = self.sector_interdependencies.get(affected_sector, {})
            
            # Calculate upstream effects (suppliers affected)
            upstream_sectors = sector_interdeps.get('depends_on', [])
            for upstream_sector in upstream_sectors:
                if upstream_sector in sectoral_impacts:
                    continue  # Already directly impacted
                
                # Calculate indirect impact
                cascade_factor = 0.3  # 30% of direct impact cascades upstream
                indirect_damage = impact['damage_usd'] * cascade_factor
                total_cascade_damage += indirect_damage
            
            # Calculate downstream effects (customers affected)
            downstream_sectors = sector_interdeps.get('supports', [])
            for downstream_sector in downstream_sectors:
                if downstream_sector in sectoral_impacts:
                    continue  # Already directly impacted
                
                # Calculate indirect impact
                cascade_factor = 0.25  # 25% of direct impact cascades downstream
                indirect_damage = impact['damage_usd'] * cascade_factor
                total_cascade_damage += indirect_damage
        
        return total_cascade_damage

    def _calculate_international_spillovers(self, target_country, base_damage):
        """Calculate international economic spillovers"""
        target_economy = self.country_economic_data[target_country]
        
        # Calculate spillover based on country's global economic importance
        global_gdp_share = target_economy['gdp_trillion_usd'] / 104  # Global GDP ~104 trillion
        trade_intensity = target_economy['trade_dependence']
        
        spillovers = {}
        
        # Major trading partners affected
        major_economies = ['USA', 'China', 'Germany', 'Japan']
        for economy in major_economies:
            if economy == target_country:
                continue
            
            # Estimate trade relationship intensity
            trade_relationship = self._estimate_trade_relationship(target_country, economy)
            spillover_damage = base_damage * global_gdp_share * trade_relationship * 0.1
            
            spillovers[economy] = {
                'spillover_damage_usd': spillover_damage,
                'gdp_impact_percent': (spillover_damage / (self.country_economic_data[economy]['gdp_trillion_usd'] * 1e12)) * 100,
                'trade_relationship_strength': trade_relationship
            }
        
        # Global market effects
        spillovers['global_effects'] = {
            'stock_market_decline_percent': min(25, base_damage / 1e12 * 0.8),
            'commodity_price_volatility_increase': min(40, base_damage / 1e12 * 1.2),
            'international_trade_decline_percent': min(15, base_damage / 1e12 * 0.6)
        }
        
        return spillovers

    def _estimate_trade_relationship(self, country1, country2):
        """Estimate trade relationship strength between countries"""
        # Simplified trade relationship matrix
        trade_relationships = {
            ('USA', 'China'): 0.8,
            ('USA', 'Germany'): 0.6,
            ('USA', 'Japan'): 0.7,
            ('China', 'Germany'): 0.5,
            ('China', 'Japan'): 0.6,
            ('Germany', 'Japan'): 0.4,
            ('India', 'USA'): 0.5,
            ('India', 'China'): 0.4,
            ('Pakistan', 'China'): 0.7,
            ('Pakistan', 'USA'): 0.3,
            ('Russia', 'Germany'): 0.6,
            ('Russia', 'China'): 0.5,
            ('Iran', 'China'): 0.4,
            ('Iran', 'Russia'): 0.5
        }
        
        # Check both directions
        key = (country1, country2) if (country1, country2) in trade_relationships else (country2, country1)
        return trade_relationships.get(key, 0.2)  # Default low relationship

    def _estimate_sector_gdp_share(self, country, sector):
        """Estimate sector's share of country GDP"""
        # Simplified sector GDP shares (would need real data)
        sector_shares = {
            'USA': {
                'finance': 0.21, 'technology': 0.18, 'healthcare': 0.12,
                'manufacturing': 0.12, 'energy': 0.08, 'agriculture': 0.01
            },
            'China': {
                'manufacturing': 0.28, 'construction': 0.14, 'finance': 0.08,
                'technology': 0.06, 'agriculture': 0.07, 'energy': 0.06
            },
            'Germany': {
                'manufacturing': 0.23, 'finance': 0.15, 'automotive': 0.12,
                'technology': 0.08, 'energy': 0.06, 'agriculture': 0.01
            }
        }
        
        country_sectors = sector_shares.get(country, {})
        return country_sectors.get(sector, 0.05)  # Default 5% if not found

    def _estimate_sector_employment_share(self, country, sector):
        """Estimate sector's share of total employment"""
        # Simplified employment shares
        employment_shares = {
            'manufacturing': 0.15,
            'services': 0.45,
            'agriculture': 0.08,
            'finance': 0.06,
            'technology': 0.04,
            'energy': 0.02,
            'healthcare': 0.12
        }
        
        return employment_shares.get(sector, 0.03)

    def _calculate_unemployment_impact(self, gdp_impact_percent, sectoral_impacts):
        """Calculate unemployment increase from economic damage"""
        # Okun's law: 1% GDP decline = ~2% unemployment increase
        base_unemployment_increase = gdp_impact_percent * 2
        
        # Add sector-specific effects
        sector_unemployment = sum(
            impact['jobs_at_risk'] for impact in sectoral_impacts.values()
        )
        
        # Convert to percentage increase
        # This is simplified - would need actual labor force data
        total_unemployment_increase = base_unemployment_increase + (sector_unemployment / 10000000)
        
        return min(25, total_unemployment_increase)  # Cap at 25% increase

    def _calculate_inflation_impact(self, warfare_type, intensity, sectoral_impacts):
        """Calculate inflation impact from economic warfare"""
        intensity_multipliers = {'low': 0.5, 'medium': 1.0, 'high': 1.8, 'extreme': 3.0}
        
        base_inflation_increase = {
            'sanctions': 2.0,
            'supply_chain_disruption': 4.0,
            'financial_system_attack': 3.0,
            'infrastructure_targeting': 3.5,
            'cyber_warfare': 1.5
        }
        
        base_increase = base_inflation_increase.get(warfare_type, 2.0)
        intensity_mult = intensity_multipliers[intensity]
        
        # Add sector-specific inflation effects
        sector_inflation = 0
        if 'energy' in sectoral_impacts:
            sector_inflation += sectoral_impacts['energy']['damage_percent'] * 0.3
        if 'agriculture' in sectoral_impacts:
            sector_inflation += sectoral_impacts['agriculture']['damage_percent'] * 0.2
        
        total_inflation_increase = (base_increase * intensity_mult) + (sector_inflation / 100 * 10)
        
        return min(50, total_inflation_increase)  # Cap at 50% increase


class SupplyChainModel:
    """Advanced global supply chain modeling system"""
    
    def __init__(self):
        self.supply_chain_network = self._build_supply_chain_network()
        self.critical_materials = self._load_critical_materials()
        self.transportation_routes = self._load_transportation_routes()

    def _build_supply_chain_network(self):
        """Build global supply chain network graph"""
        G = nx.DiGraph()
        
        # Add nodes (countries/regions)
        countries = ['USA', 'China', 'Germany', 'Japan', 'South Korea', 'Taiwan',
                    'India', 'Russia', 'Saudi Arabia', 'Brazil', 'Australia', 'Canada']
        
        for country in countries:
            G.add_node(country)
        
        # Add critical supply chain edges with weights
        supply_relationships = [
            ('China', 'USA', {'material': 'rare_earths', 'dependency': 0.8, 'volume_billion': 15}),
            ('Taiwan', 'USA', {'material': 'semiconductors', 'dependency': 0.9, 'volume_billion': 120}),
            ('Saudi Arabia', 'USA', {'material': 'oil', 'dependency': 0.3, 'volume_billion': 45}),
            ('China', 'Germany', {'material': 'manufactured_goods', 'dependency': 0.6, 'volume_billion': 180}),
            ('Russia', 'Germany', {'material': 'natural_gas', 'dependency': 0.7, 'volume_billion': 85}),
            ('Australia', 'China', {'material': 'iron_ore', 'dependency': 0.8, 'volume_billion': 65}),
            ('Ukraine', 'global', {'material': 'wheat', 'dependency': 0.3, 'volume_billion': 8}),
            ('India', 'global', {'material': 'pharmaceuticals', 'dependency': 0.4, 'volume_billion': 25})
        ]
        
        for source, target, attrs in supply_relationships:
            G.add_edge(source, target, **attrs)
        
        return G

    def _load_critical_materials(self):
        """Load critical materials database"""
        return {
            'semiconductors': {
                'strategic_importance': 0.98,
                'substitution_difficulty': 0.95,
                'global_production_concentration': 0.89,
                'primary_producers': ['Taiwan', 'South Korea', 'China'],
                'annual_market_billion': 574,
                'supply_chain_complexity': 0.92
            },
            'rare_earth_elements': {
                'strategic_importance': 0.85,
                'substitution_difficulty': 0.88,
                'global_production_concentration': 0.92,
                'primary_producers': ['China', 'Australia', 'USA'],
                'annual_market_billion': 8.5,
                'supply_chain_complexity': 0.78
            },
            'lithium': {
                'strategic_importance': 0.82,
                'substitution_difficulty': 0.65,
                'global_production_concentration': 0.76,
                'primary_producers': ['Australia', 'Chile', 'China'],
                'annual_market_billion': 12.3,
                'supply_chain_complexity': 0.68
            },
            'cobalt': {
                'strategic_importance': 0.75,
                'substitution_difficulty': 0.70,
                'global_production_concentration': 0.84,
                'primary_producers': ['DRC', 'Australia', 'Cuba'],
                'annual_market_billion': 6.8,
                'supply_chain_complexity': 0.72
            },
            'natural_gas': {
                'strategic_importance': 0.92,
                'substitution_difficulty': 0.40,
                'global_production_concentration': 0.67,
                'primary_producers': ['Russia', 'USA', 'Qatar'],
                'annual_market_billion': 890,
                'supply_chain_complexity': 0.85
            }
        }

    def _load_transportation_routes(self):
        """Load critical transportation route data"""
        return {
            'strait_of_hormuz': {
                'daily_oil_flow_million_barrels': 21,
                'global_oil_percentage': 20,
                'alternative_route_cost_multiplier': 2.5,
                'closure_impact_billion_daily': 85
            },
            'suez_canal': {
                'annual_trade_billion': 1000,
                'global_trade_percentage': 12,
                'alternative_route_cost_multiplier': 1.8,
                'closure_impact_billion_daily': 9.6
            },
            'strait_of_malacca': {
                'annual_trade_billion': 3400,
                'global_trade_percentage': 25,
                'alternative_route_cost_multiplier': 2.2,
                'closure_impact_billion_daily': 28
            },
            'panama_canal': {
                'annual_trade_billion': 270,
                'global_trade_percentage': 6,
                'alternative_route_cost_multiplier': 1.6,
                'closure_impact_billion_daily': 2.1
            },
            'south_china_sea': {
                'annual_trade_billion': 5200,
                'global_trade_percentage': 33,
                'alternative_route_cost_multiplier': 3.0,
                'closure_impact_billion_daily': 42
            }
        }

    def analyze_supply_chain_disruption(self, disrupted_nodes, disrupted_materials, disruption_intensity):
        """Analyze comprehensive supply chain disruption effects"""
        disruption_effects = {}
        
        for node in disrupted_nodes:
            node_effects = self._analyze_node_disruption(node, disrupted_materials, disruption_intensity)
            disruption_effects[node] = node_effects
        
        # Calculate global cascade effects
        cascade_effects = self._calculate_supply_chain_cascades(disrupted_nodes, disruption_intensity)
        
        # Calculate alternative routing costs
        alternative_routes = self._calculate_alternative_routes(disrupted_nodes, disrupted_materials)
        
        # Calculate recovery timeline
        recovery_analysis = self._analyze_supply_chain_recovery(disrupted_nodes, disruption_intensity)
        
        return {
            'disrupted_nodes': disrupted_nodes,
            'disrupted_materials': disrupted_materials,
            'disruption_intensity': disruption_intensity,
            'node_effects': disruption_effects,
            'cascade_effects': cascade_effects,
            'alternative_routes': alternative_routes,
            'recovery_analysis': recovery_analysis,
            'global_impact_summary': self._summarize_global_impact(disruption_effects, cascade_effects)
        }

    def _calculate_alternative_routes(self, disrupted_nodes, disrupted_materials):
        """Calculate alternative routing options and costs"""
        alternative_routes = {}
        
        for node in disrupted_nodes:
            node_alternatives = {}
            
            # Get all outgoing edges from this node
            outgoing_edges = list(self.supply_chain_network.out_edges(node, data=True))
            
            for source, target, attrs in outgoing_edges:
                material = attrs['material']
                if disrupted_materials == 'all' or material in disrupted_materials:
                    # Find alternative suppliers
                    alternatives = self._find_alternative_suppliers(material, node)
                    
                    node_alternatives[f"{material}_to_{target}"] = {
                        'original_supplier': source,
                        'alternative_suppliers': alternatives,
                        'cost_increase_percent': self._calculate_alternative_cost_increase(material, alternatives),
                        'capacity_available_percent': self._estimate_alternative_capacity(material, alternatives),
                        'setup_time_months': self._estimate_setup_time(material, alternatives)
                    }
            
            alternative_routes[node] = node_alternatives
        
        return alternative_routes

    def _find_alternative_suppliers(self, material, disrupted_node):
        """Find alternative suppliers for a material"""
        material_data = self.critical_materials.get(material, {})
        primary_producers = material_data.get('primary_producers', [])
        
        # Remove disrupted node from alternatives
        alternatives = [producer for producer in primary_producers if producer != disrupted_node]
        
        # Add capacity estimates
        alternative_suppliers = []
        for supplier in alternatives:
            # Simplified capacity estimation
            if supplier in ['USA', 'China', 'Germany']:
                capacity_share = 0.3
            elif supplier in ['Japan', 'South Korea', 'Australia']:
                capacity_share = 0.2
            else:
                capacity_share = 0.1
                
            alternative_suppliers.append({
                'country': supplier,
                'estimated_capacity_share': capacity_share,
                'political_stability': 0.8,  # Simplified
                'supply_reliability': 0.7    # Simplified
            })
        
        return alternative_suppliers

    def _calculate_alternative_cost_increase(self, material, alternatives):
        """Calculate cost increase for alternative suppliers"""
        if not alternatives:
            return 200  # No alternatives = very expensive
        
        material_data = self.critical_materials.get(material, {})
        base_cost_increase = material_data.get('substitution_difficulty', 0.5) * 50
        
        # Lower cost if more alternatives available
        alternative_factor = max(0.5, 1.0 - len(alternatives) * 0.1)
        
        return min(150, base_cost_increase * alternative_factor)

    def _estimate_alternative_capacity(self, material, alternatives):
        """Estimate available capacity from alternative suppliers"""
        if not alternatives:
            return 0
        
        total_capacity = sum(alt['estimated_capacity_share'] for alt in alternatives)
        return min(100, total_capacity * 100)

    def _estimate_setup_time(self, material, alternatives):
        """Estimate time to set up alternative supply chains"""
        if not alternatives:
            return 24  # No alternatives = very long setup
        
        material_data = self.critical_materials.get(material, {})
        complexity = material_data.get('supply_chain_complexity', 0.5)
        
        base_setup_months = complexity * 12
        alternative_factor = max(0.5, 1.0 - len(alternatives) * 0.05)
        
        return int(base_setup_months * alternative_factor)

    def _analyze_supply_chain_recovery(self, disrupted_nodes, disruption_intensity):
        """Analyze supply chain recovery timeline and requirements"""
        recovery_analysis = {}
        
        for node in disrupted_nodes:
            # Base recovery time depends on disruption type and intensity
            base_recovery_months = {
                0.2: 3,   # Low disruption
                0.5: 8,   # Medium disruption
                0.8: 18,  # High disruption
                1.0: 30   # Complete disruption
            }
            
            # Find closest intensity
            recovery_months = 30  # Default maximum
            for intensity_level, months in base_recovery_months.items():
                if disruption_intensity <= intensity_level:
                    recovery_months = months
                    break
            
            # Factor in country-specific recovery capabilities
            recovery_capability = self._estimate_recovery_capability(node)
            adjusted_recovery = recovery_months / max(0.3, recovery_capability)
            
            recovery_analysis[node] = {
                'estimated_recovery_months': int(adjusted_recovery),
                'recovery_phases': {
                    'emergency_response': int(adjusted_recovery * 0.1),
                    'basic_restoration': int(adjusted_recovery * 0.4),
                    'full_capacity_restoration': int(adjusted_recovery * 0.5)
                },
                'recovery_capability_score': recovery_capability,
                'key_bottlenecks': self._identify_recovery_bottlenecks(node, disruption_intensity),
                'international_assistance_required': disruption_intensity > 0.7
            }
        
        return recovery_analysis

    def _estimate_recovery_capability(self, country):
        """Estimate country's supply chain recovery capability"""
        # Simplified recovery capability based on economic factors
        capability_scores = {
            'USA': 0.9, 'China': 0.8, 'Germany': 0.85, 'Japan': 0.83,
            'South Korea': 0.78, 'Taiwan': 0.75, 'Australia': 0.72,
            'Canada': 0.70, 'Brazil': 0.55, 'India': 0.58,
            'Russia': 0.52, 'Saudi Arabia': 0.48
        }
        
        return capability_scores.get(country, 0.4)

    def _identify_recovery_bottlenecks(self, country, intensity):
        """Identify key bottlenecks for supply chain recovery"""
        bottlenecks = []
        
        if intensity > 0.8:
            bottlenecks.extend(['infrastructure_damage', 'skilled_workforce_loss'])
        if intensity > 0.6:
            bottlenecks.extend(['equipment_replacement', 'supply_chain_reconfiguration'])
        if intensity > 0.4:
            bottlenecks.extend(['logistics_coordination', 'quality_control_restoration'])
        
        # Country-specific bottlenecks
        if country in ['Taiwan', 'South Korea']:
            bottlenecks.append('geopolitical_stability')
        if country in ['Russia', 'Iran']:
            bottlenecks.append('international_sanctions')
        
        return list(set(bottlenecks))  # Remove duplicates

    def _summarize_global_impact(self, disruption_effects, cascade_effects):
        """Summarize global impact of supply chain disruption"""
        total_trade_loss = sum(
            node_effect['direct_trade_loss_billion'] 
            for node_effect in disruption_effects.values()
        )
        
        total_cascade_loss = sum(
            cascade_effect.get('estimated_economic_loss_billion', 0)
            for cascade_effect in cascade_effects.values()
        )
        
        affected_countries = len(disruption_effects) + len(cascade_effects)
        
        # Calculate severity
        if total_trade_loss + total_cascade_loss < 100:
            severity = 'low'
        elif total_trade_loss + total_cascade_loss < 500:
            severity = 'moderate'
        elif total_trade_loss + total_cascade_loss < 1500:
            severity = 'high'
        else:
            severity = 'extreme'
        
        return {
            'total_economic_impact_billion': total_trade_loss + total_cascade_loss,
            'direct_trade_loss_billion': total_trade_loss,
            'cascade_effects_billion': total_cascade_loss,
            'countries_affected': affected_countries,
            'severity_level': severity,
            'global_gdp_impact_percent': (total_trade_loss + total_cascade_loss) / 104000 * 100,  # Global GDP ~104T
            'estimated_recovery_months': self._estimate_global_recovery_time(severity),
            'long_term_structural_changes': severity in ['high', 'extreme']
        }

    def _estimate_global_recovery_time(self, severity):
        """Estimate global supply chain recovery time"""
        recovery_times = {
            'low': 6,
            'moderate': 18,
            'high': 36,
            'extreme': 60
        }
        return recovery_times.get(severity, 24)

    def _analyze_node_disruption(self, node, materials, intensity):
        """Analyze disruption effects for a specific node"""
        # Get all supply relationships from this node
        outgoing_edges = list(self.supply_chain_network.out_edges(node, data=True))
        
        node_disruption_effects = {
            'direct_trade_loss_billion': 0,
            'dependent_countries': [],
            'material_shortages': {},
            'price_increases': {}
        }
        
        for source, target, attrs in outgoing_edges:
            material = attrs['material']
            if materials == 'all' or material in materials:
                dependency = attrs['dependency']
                volume = attrs['volume_billion']
                
                # Calculate disruption based on intensity and dependency
                disruption_factor = intensity * dependency
                trade_loss = volume * disruption_factor
                
                node_disruption_effects['direct_trade_loss_billion'] += trade_loss
                node_disruption_effects['dependent_countries'].append({
                    'country': target,
                    'material': material,
                    'dependency_loss': disruption_factor,
                    'trade_loss_billion': trade_loss
                })
                
                # Calculate material shortages
                shortage_percent = disruption_factor * 100
                node_disruption_effects['material_shortages'][material] = shortage_percent
                
                # Calculate price increases (shortage drives prices up)
                price_increase_percent = shortage_percent * 1.5  # Price elasticity factor
                node_disruption_effects['price_increases'][material] = min(300, price_increase_percent)
        
        return node_disruption_effects

    def _calculate_supply_chain_cascades(self, disrupted_nodes, intensity):
        """Calculate cascade effects through supply chain network"""
        cascade_effects = {}
        
        # Use network analysis to find cascade paths
        for node in self.supply_chain_network.nodes():
            if node in disrupted_nodes:
                continue
            
            # Calculate indirect effects on this node
            indirect_impact = 0
            affected_materials = set()
            
            for disrupted_node in disrupted_nodes:
                # Find all paths from disrupted node to current node
                try:
                    paths = list(nx.all_simple_paths(
                        self.supply_chain_network,
                        disrupted_node,
                        node,
                        cutoff=3  # Max 3 hops
                    ))
                    
                    for path in paths:
                        # Calculate impact along this path
                        path_impact = intensity
                        for i in range(len(path) - 1):
                            edge_data = self.supply_chain_network[path[i]][path[i+1]]
                            path_impact *= edge_data['dependency'] * 0.7  # Cascade dampening
                            affected_materials.add(edge_data['material'])
                        
                        indirect_impact = max(indirect_impact, path_impact)
                        
                except nx.NetworkXNoPath:
                    continue
            
            if indirect_impact > 0.1:  # Only record significant cascades
                cascade_effects[node] = {
                    'indirect_impact_factor': indirect_impact,
                    'affected_materials': list(affected_materials),
                    'estimated_economic_loss_billion': indirect_impact * 5  # Rough scaling
                }
        
        return cascade_effects


class MarketDisruptionModel:
    """Financial market disruption modeling system"""
    
    def __init__(self):
        self.market_correlations = self._load_market_correlations()
        self.volatility_models = self._load_volatility_models()
        self.sector_sensitivities = self._load_sector_sensitivities()

    def _load_market_correlations(self):
        """Load market correlation data"""
        return {
            'equity_bond': -0.3,
            'equity_commodity': 0.4,
            'equity_currency': 0.6,
            'equity_crypto': 0.5,
            'bond_commodity': -0.2,
            'bond_currency': -0.4,
            'bond_crypto': -0.1,
            'commodity_currency': 0.3,
            'commodity_crypto': 0.2,
            'currency_crypto': 0.3
        }

    def _load_volatility_models(self):
        """Load volatility modeling parameters"""
        return {
            'base_volatility': {
                'equity': 0.16,      # 16% annual volatility
                'bond': 0.05,        # 5% annual volatility
                'commodity': 0.25,   # 25% annual volatility
                'currency': 0.08,    # 8% annual volatility
                'crypto': 0.80       # 80% annual volatility
            },
            'crisis_multipliers': {
                'geopolitical_conflict': 2.5,
                'economic_warfare': 3.0,
                'supply_chain_crisis': 2.2,
                'nuclear_threat': 4.0,
                'financial_system_attack': 3.5
            },
            'mean_reversion_speed': {
                'equity': 0.1,       # 10% daily mean reversion
                'bond': 0.05,        # 5% daily mean reversion
                'commodity': 0.08,   # 8% daily mean reversion
                'currency': 0.12,    # 12% daily mean reversion
                'crypto': 0.15       # 15% daily mean reversion
            }
        }

    def _load_sector_sensitivities(self):
        """Load sector-specific market sensitivities"""
        return {
            'defense': {
                'geopolitical_conflict': 0.2,    # Defense stocks rise during conflict
                'economic_warfare': 0.1,
                'nuclear_threat': 0.3
            },
            'energy': {
                'geopolitical_conflict': 0.3,
                'supply_chain_crisis': 0.4,
                'infrastructure_targeting': 0.5
            },
            'technology': {
                'cyber_warfare': -0.4,           # Tech stocks fall during cyber attacks
                'supply_chain_crisis': -0.3,
                'economic_warfare': -0.2
            },
            'finance': {
                'financial_system_attack': -0.6,
                'economic_warfare': -0.4,
                'currency_crisis': -0.5
            },
            'healthcare': {
                'geopolitical_conflict': 0.1,   # Healthcare less affected
                'pandemic': 0.2,
                'nuclear_threat': 0.15
            },
            'consumer_goods': {
                'economic_warfare': -0.3,
                'supply_chain_crisis': -0.4,
                'inflation_spike': -0.2
            }
        }

    def model_market_disruption(self, trigger_event, trigger_magnitude, affected_markets):
        """Model comprehensive market disruption effects"""
        market_effects = {}
        
        for market in affected_markets:
            market_impact = self._calculate_market_impact(market, trigger_event, trigger_magnitude)
            market_effects[market] = market_impact
        
        # Calculate cross-market contagion
        contagion_effects = self._calculate_market_contagion(market_effects)
        
        # Model volatility spillovers
        volatility_effects = self._model_volatility_spillovers(trigger_event, trigger_magnitude)
        
        return {
            'trigger_event': trigger_event,
            'trigger_magnitude': trigger_magnitude,
            'direct_market_effects': market_effects,
            'contagion_effects': contagion_effects,
            'volatility_spillovers': volatility_effects,
            'recovery_timeline': self._estimate_market_recovery(market_effects, trigger_magnitude)
        }

    def _calculate_market_impact(self, market, trigger_event, magnitude):
        """Calculate direct impact on specific market"""
        # Market sensitivity to different events
        event_sensitivities = {
            'geopolitical_conflict': {
                'equity': -0.15, 'bond': 0.08, 'commodity': 0.25, 'currency': -0.12, 'crypto': -0.30
            },
            'economic_warfare': {
                'equity': -0.20, 'bond': 0.05, 'commodity': 0.30, 'currency': -0.18, 'crypto': -0.25
            },
            'supply_chain_crisis': {
                'equity': -0.12, 'bond': 0.03, 'commodity': 0.40, 'currency': -0.08, 'crypto': -0.15
            },
            'nuclear_threat': {
                'equity': -0.35, 'bond': 0.20, 'commodity': 0.50, 'currency': -0.25, 'crypto': -0.40
            }
        }
        
        base_impact = event_sensitivities.get(trigger_event, {}).get(market, -0.10)
        scaled_impact = base_impact * magnitude
        
        # Add volatility increase
        volatility_increase = abs(scaled_impact) * 2.5
        
        return {
            'market_type': market,
            'price_impact_percent': scaled_impact * 100,
            'volatility_increase_percent': volatility_increase * 100,
            'volume_change_percent': abs(scaled_impact) * 150,  # Higher activity during crisis
            'liquidity_impact_percent': abs(scaled_impact) * 80  # Reduced liquidity
        }

    def _model_volatility_spillovers(self, trigger_event, magnitude):
        """Model volatility spillovers across markets and regions"""
        base_volatility = self.volatility_models['base_volatility']
        crisis_multipliers = self.volatility_models['crisis_multipliers']
        
        crisis_multiplier = crisis_multipliers.get(trigger_event, 2.0)
        
        spillover_effects = {}
        
        for market, base_vol in base_volatility.items():
            # Calculate crisis-adjusted volatility
            crisis_volatility = base_vol * crisis_multiplier * magnitude
            
            # Calculate volatility persistence (how long elevated volatility lasts)
            persistence_days = int(30 * magnitude * crisis_multiplier / 2)
            
            spillover_effects[market] = {
                'base_volatility': base_vol * 100,
                'crisis_volatility': crisis_volatility * 100,
                'volatility_increase_factor': crisis_multiplier * magnitude,
                'persistence_days': persistence_days,
                'mean_reversion_speed': self.volatility_models['mean_reversion_speed'][market]
            }
        
        return spillover_effects

    def _calculate_market_contagion(self, market_effects):
        """Calculate contagion effects between markets"""
        contagion_effects = {}
        
        for market1, effect1 in market_effects.items():
            for market2, effect2 in market_effects.items():
                if market1 >= market2:  # Avoid duplicates
                    continue
                
                # Get correlation between markets
                correlation_key = f"{market1}_{market2}" if f"{market1}_{market2}" in self.market_correlations else f"{market2}_{market1}"
                correlation = self.market_correlations.get(correlation_key, 0)
                
                if abs(correlation) > 0.2:  # Significant correlation
                    contagion_factor = correlation * 0.6  # Contagion dampening
                    contagion_effects[f"{market1}_to_{market2}"] = {
                        'correlation': correlation,
                        'contagion_impact_percent': effect1['price_impact_percent'] * contagion_factor,
                        'amplification_factor': abs(contagion_factor)
                    }
        
        return contagion_effects

    def _estimate_market_recovery(self, market_effects, trigger_magnitude):
        """Estimate market recovery timeline"""
        recovery_estimates = {}
        
        for market, effects in market_effects.items():
            impact_magnitude = abs(effects['price_impact_percent'])
            
            # Base recovery time based on impact severity
            if impact_magnitude < 5:
                base_recovery_days = 7
            elif impact_magnitude < 15:
                base_recovery_days = 21
            elif impact_magnitude < 30:
                base_recovery_days = 60
            else:
                base_recovery_days = 120
            
            # Apply market-specific recovery factors
            market_recovery_factors = {
                'equity': 1.0,      # Baseline recovery
                'bond': 0.8,        # Bonds recover faster
                'commodity': 1.2,   # Commodities slower due to physical constraints
                'currency': 0.9,    # Currency markets quite efficient
                'crypto': 1.5       # Crypto markets more volatile, slower recovery
            }
            
            recovery_factor = market_recovery_factors.get(market, 1.0)
            adjusted_recovery_days = int(base_recovery_days * recovery_factor * trigger_magnitude)
            
            # Recovery phases
            recovery_estimates[market] = {
                'total_recovery_days': adjusted_recovery_days,
                'phases': {
                    'initial_shock': int(adjusted_recovery_days * 0.1),
                    'stabilization': int(adjusted_recovery_days * 0.4),
                    'gradual_recovery': int(adjusted_recovery_days * 0.5)
                },
                'confidence_level': max(0.3, 0.9 - trigger_magnitude * 0.5),
                'volatility_normalization_days': int(adjusted_recovery_days * 1.5)
            }
        
        return recovery_estimates