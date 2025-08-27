-- Comprehensive database schema for predictive modeling platform

-- Countries and regions
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    region TEXT,
    population INTEGER,
    gdp_trillion REAL,
    military_strength INTEGER,
    nuclear_weapons BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scenarios and configurations
CREATE TABLE IF NOT EXISTS scenarios (
    id TEXT PRIMARY KEY,
    name TEXT,
    description TEXT,
    config TEXT, -- JSON configuration
    status TEXT DEFAULT 'initialized',
    progress INTEGER DEFAULT 0,
    results TEXT, -- JSON results
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Military analysis results
CREATE TABLE IF NOT EXISTS military_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id TEXT,
    trajectory_data TEXT, -- JSON
    casualty_estimates TEXT, -- JSON
    defense_analysis TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- Economic analysis results
CREATE TABLE IF NOT EXISTS economic_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id TEXT,
    gdp_impact REAL,
    economic_damage_usd REAL,
    sectoral_impacts TEXT, -- JSON
    recovery_timeline TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- Population impact analysis
CREATE TABLE IF NOT EXISTS population_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id TEXT,
    population_affected INTEGER,
    displacement_data TEXT, -- JSON
    demographic_impacts TEXT, -- JSON
    social_dynamics TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- Infrastructure analysis
CREATE TABLE IF NOT EXISTS infrastructure_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id TEXT,
    infrastructure_damage TEXT, -- JSON
    service_disruptions TEXT, -- JSON
    recovery_requirements TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- Psychological impact analysis
CREATE TABLE IF NOT EXISTS psychological_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id TEXT,
    trauma_exposure TEXT, -- JSON
    mental_health_outcomes TEXT, -- JSON
    resilience_factors TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- Supply chain analysis
CREATE TABLE IF NOT EXISTS supply_chain_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id TEXT,
    disrupted_networks TEXT, -- JSON
    cascade_effects TEXT, -- JSON
    alternative_routes TEXT, -- JSON
    recovery_analysis TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- Climate impact analysis
CREATE TABLE IF NOT EXISTS climate_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id TEXT,
    climate_projections TEXT, -- JSON
    regional_impacts TEXT, -- JSON
    adaptation_needs TEXT, -- JSON
    migration_patterns TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- Global response modeling
CREATE TABLE IF NOT EXISTS global_response (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id TEXT,
    diplomatic_responses TEXT, -- JSON
    economic_measures TEXT, -- JSON
    military_responses TEXT, -- JSON
    humanitarian_aid TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- User sessions and chat history
CREATE TABLE IF NOT EXISTS chat_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    conversation_history TEXT, -- JSON
    scenario_configs TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Visualization cache
CREATE TABLE IF NOT EXISTS visualization_cache (
    id TEXT PRIMARY KEY,
    scenario_id TEXT,
    visualization_type TEXT,
    visualization_data TEXT, -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- Model performance metrics
CREATE TABLE IF NOT EXISTS model_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_type TEXT NOT NULL,
    scenario_id TEXT,
    execution_time_seconds REAL,
    accuracy_score REAL,
    confidence_level REAL,
    memory_usage_mb REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scenario_id) REFERENCES scenarios (id)
);

-- System logs
CREATE TABLE IF NOT EXISTS system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level TEXT NOT NULL,
    message TEXT NOT NULL,
    module TEXT,
    scenario_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_scenarios_status ON scenarios (status);
CREATE INDEX IF NOT EXISTS idx_scenarios_created_at ON scenarios (created_at);
CREATE INDEX IF NOT EXISTS idx_military_analysis_scenario ON military_analysis (scenario_id);
CREATE INDEX IF NOT EXISTS idx_economic_analysis_scenario ON economic_analysis (scenario_id);
CREATE INDEX IF NOT EXISTS idx_population_analysis_scenario ON population_analysis (scenario_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_user ON chat_sessions (user_id);
CREATE INDEX IF NOT EXISTS idx_visualization_cache_scenario ON visualization_cache (scenario_id);
CREATE INDEX IF NOT EXISTS idx_model_performance_type ON model_performance (model_type);
CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs (level);

-- Insert sample country data
INSERT OR REPLACE INTO countries (code, name, region, population, gdp_trillion, military_strength, nuclear_weapons) VALUES
('USA', 'United States of America', 'North America', 331900000, 26.9, 10, 1),
('CHN', 'People''s Republic of China', 'East Asia', 1425671352, 17.9, 9, 1),
('IND', 'Republic of India', 'South Asia', 1428627663, 3.74, 7, 1),
('PAK', 'Islamic Republic of Pakistan', 'South Asia', 231402117, 0.35, 5, 1),
('RUS', 'Russian Federation', 'Eurasia', 144713314, 1.83, 8, 1),
('IRN', 'Islamic Republic of Iran', 'Middle East', 85028759, 0.23, 4, 0),
('ISR', 'State of Israel', 'Middle East', 9500000, 0.48, 6, 1),
('DEU', 'Federal Republic of Germany', 'Europe', 83240525, 4.26, 6, 0),
('JPN', 'Japan', 'East Asia', 125584838, 4.94, 7, 0),
('KOR', 'Republic of Korea', 'East Asia', 51844834, 1.81, 6, 0),
('TWN', 'Taiwan', 'East Asia', 23500000, 0.79, 5, 0),
('SAU', 'Kingdom of Saudi Arabia', 'Middle East', 35844909, 0.83, 5, 0),
('UAE', 'United Arab Emirates', 'Middle East', 9441129, 0.51, 4, 0),
('TUR', 'Republic of Turkey', 'Eurasia', 85279553, 0.82, 6, 0),
('EGY', 'Arab Republic of Egypt', 'Africa', 105914499, 0.47, 5, 0);
