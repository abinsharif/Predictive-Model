
import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import base64
import io

class VisualizationEngine:
    """Advanced visualization engine for complex scenario data"""

    def __init__(self):
        self.chart_templates = self._load_chart_templates()
        self.color_schemes = self._load_color_schemes()
        self.map_projections = self._load_map_projections()

    def _load_chart_templates(self):
        """Load chart templates for different visualization types"""
        return {
            'timeline': {
                'type': 'line',
                'config': {
                    'responsive': True,
                    'interaction': {
                        'mode': 'index',
                        'intersect': False
                    }
                }
            },
            'impact_comparison': {
                'type': 'bar',
                'config': {
                    'responsive': True,
                    'scales': {
                        'y': {
                            'beginAtZero': True
                        }
                    }
                }
            },
            'geographic_heatmap': {
                'type': 'heatmap',
                'config': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'display': True
                        }
                    }
                }
            }
        }

    def _load_color_schemes(self):
        """Load color schemes for different types of data"""
        return {
            'severity': ['#2E8B57', '#FFD700', '#FF8C00', '#DC143C', '#8B0000'],
            'categories': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            'neutral': ['#34495e', '#7f8c8d', '#95a5a6', '#bdc3c7', '#ecf0f1'],
            'military': ['#2c3e50', '#34495e', '#7f8c8d', '#95a5a6', '#bdc3c7']
        }

    def _load_map_projections(self):
        """Load map projection configurations"""
        return {
            'world': {
                'center': [0, 20],
                'zoom': 1.5,
                'projection': 'mercator'
            },
            'asia': {
                'center': [100, 35], 
                'zoom': 3,
                'projection': 'mercator'
            },
            'europe': {
                'center': [15, 54],
                'zoom': 4,
                'projection': 'mercator'
            }
        }

    def generate_comprehensive_visualization(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive visualization data for scenario results"""

        scenario_results = scenario.get('results', {})
        scenario_config = scenario.get('config', {})

        visualization_data = {
            'overview_metrics': self._generate_overview_metrics(scenario_results),
            'timeline_chart': self._generate_timeline_chart(scenario_results),
            'impact_breakdown': self._generate_impact_breakdown(scenario_results),
            'geographic_visualization': self._generate_geographic_visualization(scenario_config, scenario_results),
            'risk_assessment_chart': self._generate_risk_assessment_chart(scenario_results),
            'comparison_charts': self._generate_comparison_charts(scenario_results),
            'three_d_scene_config': self._generate_3d_scene_config(scenario_config, scenario_results)
        }

        return visualization_data

    def _generate_overview_metrics(self, scenario_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overview metrics visualization"""

        metrics = {}

        # Extract key metrics from different models
        if 'model_results' in scenario_results:
            model_results = scenario_results['model_results']

            if 'military' in model_results:
                military_results = model_results['military']
                casualty_analysis = military_results.get('casualty_analysis', {})
                metrics['casualties'] = {
                    'value': casualty_analysis.get('immediate_casualties', 0),
                    'label': 'Estimated Casualties',
                    'format': 'number',
                    'severity': self._calculate_severity(casualty_analysis.get('immediate_casualties', 0), 'casualties')
                }

            if 'economic' in model_results:
                economic_results = model_results['economic']
                economic_damage = economic_results.get('economic_damage', {})
                metrics['economic_impact'] = {
                    'value': economic_damage.get('gdp_impact_percent', 0),
                    'label': 'GDP Impact (%)',
                    'format': 'percentage',
                    'severity': self._calculate_severity(economic_damage.get('gdp_impact_percent', 0), 'economic')
                }

            if 'population' in model_results:
                population_results = model_results['population']
                displacement = population_results.get('displacement_analysis', {})
                metrics['displacement'] = {
                    'value': displacement.get('total_displaced', 0),
                    'label': 'Displaced Population',
                    'format': 'number',
                    'severity': self._calculate_severity(displacement.get('total_displaced', 0), 'displacement')
                }

        return {
            'metrics': metrics,
            'chart_type': 'metrics_grid',
            'layout': {
                'columns': min(4, len(metrics)),
                'responsive': True
            }
        }

    def _generate_timeline_chart(self, scenario_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate timeline visualization"""

        timeline_data = scenario_results.get('timeline_projections', {})

        if not timeline_data:
            return {'error': 'No timeline data available'}

        # Extract timeline phases
        phases = timeline_data.get('phases', [])
        casualty_timeline = timeline_data.get('casualty_timeline', {})
        economic_timeline = timeline_data.get('economic_impact_timeline', {})

        # Prepare chart data
        labels = [phase.get('phase', f'Phase {i}') for i, phase in enumerate(phases)]

        datasets = []

        # Casualty progression
        if casualty_timeline:
            casualty_data = [casualty_timeline.get(phase.get('phase', ''), 0) for phase in phases]
            datasets.append({
                'label': 'Casualty Progression',
                'data': casualty_data,
                'borderColor': '#dc2626',
                'backgroundColor': 'rgba(220, 38, 38, 0.1)',
                'tension': 0.4
            })

        # Economic impact progression  
        if economic_timeline:
            economic_data = [economic_timeline.get(phase.get('phase', ''), 0) for phase in phases]
            datasets.append({
                'label': 'Economic Impact',
                'data': economic_data,
                'borderColor': '#2563eb',
                'backgroundColor': 'rgba(37, 99, 235, 0.1)',
                'tension': 0.4
            })

        return {
            'chart_type': 'line',
            'data': {
                'labels': labels,
                'datasets': datasets
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Scenario Timeline Progression'
                    },
                    'legend': {
                        'display': True
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'title': {
                            'display': True,
                            'text': 'Impact Magnitude'
                        }
                    },
                    'x': {
                        'title': {
                            'display': True,
                            'text': 'Timeline Phases'
                        }
                    }
                }
            }
        }

    def _generate_impact_breakdown(self, scenario_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate impact breakdown visualization"""

        integrated_analysis = scenario_results.get('integrated_analysis', {})
        compound_effects = integrated_analysis.get('compound_effects', {})

        # Extract impact categories
        impact_data = []

        if 'total_casualty_burden' in compound_effects:
            casualty_sources = compound_effects['total_casualty_burden'].get('casualty_sources', [])
            for source in casualty_sources:
                impact_data.append({
                    'category': source.get('source', 'Unknown'),
                    'value': source.get('casualties', 0),
                    'type': 'casualties'
                })

        if 'total_economic_impact' in compound_effects:
            economic_sources = compound_effects['total_economic_impact'].get('economic_sources', [])
            for source in economic_sources:
                impact_data.append({
                    'category': source.get('source', 'Unknown'),
                    'value': source.get('damage', 0) / 1000000000,  # Convert to billions
                    'type': 'economic'
                })

        # Create grouped bar chart
        categories = list(set([item['category'] for item in impact_data]))
        casualty_data = []
        economic_data = []

        for category in categories:
            casualty_value = sum([item['value'] for item in impact_data 
                                if item['category'] == category and item['type'] == 'casualties'])
            economic_value = sum([item['value'] for item in impact_data 
                                if item['category'] == category and item['type'] == 'economic'])

            casualty_data.append(casualty_value)
            economic_data.append(economic_value)

        return {
            'chart_type': 'bar',
            'data': {
                'labels': categories,
                'datasets': [
                    {
                        'label': 'Casualties',
                        'data': casualty_data,
                        'backgroundColor': 'rgba(220, 38, 38, 0.8)',
                        'borderColor': '#dc2626',
                        'borderWidth': 1,
                        'yAxisID': 'y'
                    },
                    {
                        'label': 'Economic Impact (Billions USD)',
                        'data': economic_data,
                        'backgroundColor': 'rgba(37, 99, 235, 0.8)',
                        'borderColor': '#2563eb',
                        'borderWidth': 1,
                        'yAxisID': 'y1'
                    }
                ]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Impact Breakdown by Source'
                    }
                },
                'scales': {
                    'y': {
                        'type': 'linear',
                        'display': True,
                        'position': 'left',
                        'title': {
                            'display': True,
                            'text': 'Casualties'
                        }
                    },
                    'y1': {
                        'type': 'linear',
                        'display': True,
                        'position': 'right',
                        'title': {
                            'display': True,
                            'text': 'Economic Impact (Billions USD)'
                        },
                        'grid': {
                            'drawOnChartArea': False
                        }
                    }
                }
            }
        }

    def _generate_geographic_visualization(self, scenario_config: Dict[str, Any], scenario_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate geographic visualization - no human imagery, geometric shapes only"""

        location = scenario_config.get('location', 'Unknown')
        countries_involved = scenario_config.get('countries_involved', [])

        # Country coordinates (simplified)
        country_coords = {
            'USA': [-95.7129, 37.0902],
            'China': [104.1954, 35.8617],
            'India': [78.9629, 20.5937],
            'Pakistan': [69.3451, 30.3753],
            'Russia': [105.3188, 61.5240],
            'Iran': [53.6880, 32.4279],
            'Taiwan': [120.9605, 23.6978]
        }

        # Generate map markers for affected regions
        markers = []

        for country in countries_involved:
            coords = country_coords.get(country)
            if coords:
                # Calculate impact intensity for this country
                impact_intensity = self._calculate_country_impact_intensity(country, scenario_results)

                markers.append({
                    'coordinates': coords,
                    'country': country,
                    'impact_intensity': impact_intensity,
                    'marker_size': max(10, min(50, impact_intensity * 100)),
                    'color': self._get_impact_color(impact_intensity)
                })

        # Generate impact zones (abstract geometric shapes)
        impact_zones = []

        if 'missile_threat' in scenario_config:
            missile_config = scenario_config['missile_threat']
            launch_coords = missile_config.get('launch_coords', [0, 0])
            target_coords = missile_config.get('target_coords', [0, 0])

            impact_zones.append({
                'type': 'trajectory_line',
                'coordinates': [launch_coords, target_coords],
                'color': '#ff0000',
                'width': 3
            })

            impact_zones.append({
                'type': 'impact_circle',
                'center': target_coords,
                'radius': 50000,  # 50km radius
                'color': 'rgba(255, 0, 0, 0.3)',
                'border_color': '#ff0000'
            })

        return {
            'map_type': 'geographic_impact',
            'projection': 'mercator',
            'center': self._calculate_map_center(markers),
            'zoom': self._calculate_map_zoom(markers),
            'markers': markers,
            'impact_zones': impact_zones,
            'legend': {
                'impact_levels': [
                    {'level': 'Low', 'color': '#22c55e'},
                    {'level': 'Medium', 'color': '#f59e0b'},
                    {'level': 'High', 'color': '#ef4444'},
                    {'level': 'Extreme', 'color': '#7c2d12'}
                ]
            }
        }

    def _generate_3d_scene_config(self, scenario_config: Dict[str, Any], scenario_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate 3D scene configuration - abstract geometric visualization only"""

        scene_config = {
            'scene_type': 'abstract_impact_visualization',
            'camera': {
                'position': [0, 5, 10],
                'target': [0, 0, 0],
                'fov': 75
            },
            'lighting': {
                'ambient': {'color': '#ffffff', 'intensity': 0.4},
                'directional': {'color': '#ffffff', 'intensity': 0.6, 'position': [1, 1, 1]}
            },
            'objects': []
        }

        # Add abstract geometric representations of impact
        if 'model_results' in scenario_results:
            model_results = scenario_results['model_results']

            # Represent casualties as red geometric shapes
            if 'military' in model_results:
                casualties = model_results['military'].get('casualty_analysis', {}).get('immediate_casualties', 0)
                casualty_intensity = min(1.0, casualties / 100000)  # Normalize

                scene_config['objects'].append({
                    'type': 'cylinder',
                    'position': [0, 0, 0],
                    'scale': [1, casualty_intensity * 5, 1],
                    'color': '#dc2626',
                    'opacity': 0.7,
                    'label': 'Casualty Impact'
                })

            # Represent economic impact as blue geometric shapes
            if 'economic' in model_results:
                economic_impact = model_results['economic'].get('economic_damage', {}).get('gdp_impact_percent', 0)
                economic_intensity = min(1.0, economic_impact / 20)  # Normalize to 20% max

                scene_config['objects'].append({
                    'type': 'box',
                    'position': [3, 0, 0],
                    'scale': [1, economic_intensity * 4, 1],
                    'color': '#2563eb',
                    'opacity': 0.7,
                    'label': 'Economic Impact'
                })

            # Represent infrastructure damage as gray geometric shapes
            if 'infrastructure' in model_results:
                infrastructure_impact = 0.5  # Placeholder

                scene_config['objects'].append({
                    'type': 'sphere',
                    'position': [-3, 0, 0],
                    'scale': [infrastructure_impact * 2, infrastructure_impact * 2, infrastructure_impact * 2],
                    'color': '#6b7280',
                    'opacity': 0.6,
                    'label': 'Infrastructure Impact'
                })

        # Add abstract terrain representation
        terrain_type = scenario_config.get('terrain_type', 'urban_medium')
        terrain_colors = {
            'urban_dense': '#374151',
            'urban_medium': '#4b5563',
            'suburban': '#6b7280',
            'rural_agricultural': '#16a34a',
            'mountainous': '#78716c',
            'coastal': '#0284c7',
            'desert': '#eab308',
            'forest': '#15803d'
        }

        terrain_color = terrain_colors.get(terrain_type, '#6b7280')

        scene_config['objects'].append({
            'type': 'plane',
            'position': [0, -1, 0],
            'scale': [10, 1, 10],
            'color': terrain_color,
            'opacity': 0.8,
            'label': f'Terrain: {terrain_type.replace("_", " ").title()}'
        })

        return scene_config

    def _calculate_severity(self, value: float, metric_type: str) -> str:
        """Calculate severity level for a metric"""

        thresholds = {
            'casualties': [1000, 10000, 50000, 200000],
            'economic': [1, 5, 15, 30],  # GDP percentage
            'displacement': [10000, 100000, 500000, 2000000]
        }

        metric_thresholds = thresholds.get(metric_type, [10, 100, 1000, 10000])

        if value < metric_thresholds[0]:
            return 'low'
        elif value < metric_thresholds[1]:
            return 'medium'
        elif value < metric_thresholds[2]:
            return 'high'
        elif value < metric_thresholds[3]:
            return 'severe'
        else:
            return 'extreme'

    def _calculate_country_impact_intensity(self, country: str, scenario_results: Dict[str, Any]) -> float:
        """Calculate impact intensity for a specific country"""
        # Simplified calculation - would be more sophisticated in real implementation
        base_intensity = 0.3

        if 'model_results' in scenario_results:
            model_results = scenario_results['model_results']

            # Add military impact
            if 'military' in model_results:
                base_intensity += 0.3

            # Add economic impact
            if 'economic' in model_results:
                base_intensity += 0.2

            # Add population impact
            if 'population' in model_results:
                base_intensity += 0.2

        return min(1.0, base_intensity)

    def _get_impact_color(self, intensity: float) -> str:
        """Get color based on impact intensity"""
        if intensity < 0.2:
            return '#22c55e'  # Green
        elif intensity < 0.4:
            return '#f59e0b'  # Yellow
        elif intensity < 0.6:
            return '#ef4444'  # Orange
        elif intensity < 0.8:
            return '#dc2626'  # Red
        else:
            return '#7c2d12'  # Dark red

    def _calculate_map_center(self, markers: List[Dict]) -> List[float]:
        """Calculate center point for map based on markers"""
        if not markers:
            return [0, 20]

        lats = [marker['coordinates'][1] for marker in markers]
        lons = [marker['coordinates'][0] for marker in markers]

        return [sum(lons) / len(lons), sum(lats) / len(lats)]

    def _calculate_map_zoom(self, markers: List[Dict]) -> int:
        """Calculate appropriate zoom level based on marker spread"""
        if len(markers) < 2:
            return 6

        lats = [marker['coordinates'][1] for marker in markers]
        lons = [marker['coordinates'][0] for marker in markers]

        lat_range = max(lats) - min(lats)
        lon_range = max(lons) - min(lons)

        max_range = max(lat_range, lon_range)

        if max_range > 90:
            return 2
        elif max_range > 45:
            return 3
        elif max_range > 20:
            return 4
        elif max_range > 10:
            return 5
        else:
            return 6

class Map3DRenderer:
    """3D map and visualization renderer"""

    def __init__(self):
        self.supported_formats = ['json', 'geojson', 'topojson']

    def render_3d_scene(self, scene_config: Dict[str, Any]) -> str:
        """Render 3D scene configuration as JSON for Three.js"""
        return json.dumps(scene_config, indent=2)

class ChartGenerator:
    """Chart generation utilities"""

    def __init__(self):
        self.chart_types = ['line', 'bar', 'scatter', 'heatmap', 'pie']

    def generate_chart_config(self, chart_type: str, data: Dict[str, Any], options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate chart configuration for Chart.js"""

        base_config = {
            'type': chart_type,
            'data': data,
            'options': options or {}
        }

        # Add responsive defaults
        if 'responsive' not in base_config['options']:
            base_config['options']['responsive'] = True

        return base_config
