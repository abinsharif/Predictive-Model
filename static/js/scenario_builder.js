// Scenario Builder Specific JavaScript

class ScenarioBuilder {
    constructor() {
        this.currentScenario = {};
        this.modelInfo = {};
        this.environmentPresets = {};
        this.init();
    }

    init() {
        this.loadModelInfo();
        this.loadEnvironmentPresets();
        this.setupFormHandlers();
        this.updateRuntimeEstimate();
    }

    setupFormHandlers() {
        // Scenario type change handler
        document.querySelectorAll('input[name="scenario_type"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.handleScenarioTypeChange(e.target.value);
            });
        });

        // Environment type change handler
        const environmentSelect = document.getElementById('environment_type');
        if (environmentSelect) {
            environmentSelect.addEventListener('change', (e) => {
                this.handleEnvironmentChange(e.target.value);
            });
        }

        // Model selection change handlers
        document.querySelectorAll('input[name="models"]').forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                this.updateRuntimeEstimate();
                this.updateModelInfo();
            });
        });

        // Parameter change handlers
        ['intensity', 'duration_days', 'population_size'].forEach(fieldName => {
            const field = document.getElementById(fieldName);
            if (field) {
                field.addEventListener('change', () => {
                    this.updateRuntimeEstimate();
                });
            }
        });
    }

    handleScenarioTypeChange(scenarioType) {
        // Update form fields based on scenario type
        this.updateFormForScenarioType(scenarioType);
        this.updateRuntimeEstimate();
    }

    updateFormForScenarioType(scenarioType) {
        const nuclearCheckbox = document.getElementById('nuclear_escalation');
        const supplyChainCheckbox = document.getElementById('supply_chain_impact');
        const climateCheckbox = document.getElementById('climate_effects');

        // Set default options based on scenario type
        switch (scenarioType) {
            case 'military':
                if (nuclearCheckbox) nuclearCheckbox.checked = false;
                if (supplyChainCheckbox) supplyChainCheckbox.checked = true;
                if (climateCheckbox) climateCheckbox.checked = false;
                break;
            case 'economic':
                if (nuclearCheckbox) nuclearCheckbox.checked = false;
                if (supplyChainCheckbox) supplyChainCheckbox.checked = true;
                if (climateCheckbox) climateCheckbox.checked = false;
                break;
            case 'climate':
                if (nuclearCheckbox) nuclearCheckbox.checked = false;
                if (supplyChainCheckbox) supplyChainCheckbox.checked = false;
                if (climateCheckbox) climateCheckbox.checked = true;
                break;
        }

        // Update model selections
        this.updateModelSelections(scenarioType);
    }

    updateModelSelections(scenarioType) {
        const modelRecommendations = {
            'military': ['military_analysis', 'population_impact', 'infrastructure_analysis', 'economic_impact'],
            'economic': ['economic_impact', 'supply_chain_analysis', 'population_impact'],
            'climate': ['climate_modeling', 'population_impact', 'economic_impact', 'infrastructure_analysis']
        };

        const recommended = modelRecommendations[scenarioType] || [];

        document.querySelectorAll('input[name="models"]').forEach(checkbox => {
            checkbox.checked = recommended.includes(checkbox.value);
        });
    }

    handleEnvironmentChange(environmentType) {
        // Load environment-specific presets
        this.loadEnvironmentSpecificData(environmentType);
        this.updatePopulationRange(environmentType);
    }

    updatePopulationRange(environmentType) {
        const populationField = document.getElementById('population_size');
        if (!populationField) return;

        const ranges = {
            'village': { min: 500, max: 5000, default: 2000 },
            'small_town': { min: 5000, max: 25000, default: 15000 },
            'medium_city': { min: 25000, max: 250000, default: 100000 },
            'large_city': { min: 250000, max: 1000000, default: 500000 },
            'megacity': { min: 1000000, max: 20000000, default: 5000000 },
            'country_region': { min: 1000000, max: 100000000, default: 25000000 },
            'large_country': { min: 100000000, max: 1500000000, default: 300000000 },
            'global': { min: 1000000000, max: 8000000000, default: 2000000000 }
        };

        const range = ranges[environmentType] || ranges['medium_city'];
        populationField.min = range.min;
        populationField.max = range.max;
        populationField.value = range.default;

        // Update placeholder
        populationField.placeholder = `${range.min.toLocaleString()} - ${range.max.toLocaleString()}`;
    }

    loadModelInfo() {
        window.pmp.makeAPIRequest('/api/model-info/military_analysis')
            .then(data => {
                this.modelInfo['military_analysis'] = data;
            })
            .catch(error => {
                console.error('Failed to load model info:', error);
            });
    }

    loadEnvironmentPresets() {
        window.pmp.makeAPIRequest('/api/environment-presets/medium_city')
            .then(data => {
                this.environmentPresets = data;
            })
            .catch(error => {
                console.error('Failed to load environment presets:', error);
            });
    }

    loadEnvironmentSpecificData(environmentType) {
        window.pmp.makeAPIRequest(`/api/environment-presets/${environmentType}`)
            .then(data => {
                this.applyEnvironmentPresets(data);
            })
            .catch(error => {
                console.error('Failed to load environment data:', error);
            });
    }

    applyEnvironmentPresets(presets) {
        // Apply infrastructure and other presets based on environment
        console.log('Applying environment presets:', presets);
    }

    updateModelInfo() {
        const selectedModels = Array.from(document.querySelectorAll('input[name="models"]:checked'))
            .map(cb => cb.value);

        const modelInfoContainer = document.getElementById('model-info');
        if (!modelInfoContainer) return;

        if (selectedModels.length === 0) {
            modelInfoContainer.innerHTML = '<p class="text-muted">Select models to see information.</p>';
            return;
        }

        let html = '';
        selectedModels.forEach(modelType => {
            const info = this.modelInfo[modelType] || {
                name: modelType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
                description: 'Advanced modeling system',
                complexity: 'Medium',
                runtime_seconds: [20, 40]
            };

            html += `
                <div class="model-info-panel">
                    <h6 class="fw-bold">${info.name}</h6>
                    <p class="small mb-2">${info.description}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="model-complexity complexity-${info.complexity.toLowerCase().replace(' ', '-')}">
                            ${info.complexity}
                        </span>
                        <small class="text-muted">
                            ${info.runtime_seconds[0]}-${info.runtime_seconds[1]}s
                        </small>
                    </div>
                </div>
            `;
        });

        modelInfoContainer.innerHTML = html;
    }

    updateRuntimeEstimate() {
        const selectedModels = document.querySelectorAll('input[name="models"]:checked').length;
        const intensity = document.getElementById('intensity')?.value || 'medium';
        const duration = parseInt(document.getElementById('duration_days')?.value || 30);

        // Base runtime calculation
        let baseRuntime = selectedModels * 15; // 15 seconds per model base

        // Intensity multiplier
        const intensityMultipliers = { 'low': 0.8, 'medium': 1.0, 'high': 1.3, 'extreme': 1.6 };
        baseRuntime *= intensityMultipliers[intensity] || 1.0;

        // Duration factor (longer scenarios take more time)
        if (duration > 365) baseRuntime *= 1.4;
        else if (duration > 90) baseRuntime *= 1.2;

        const minRuntime = Math.max(30, Math.floor(baseRuntime * 0.8));
        const maxRuntime = Math.ceil(baseRuntime * 1.5);

        const runtimeContainer = document.getElementById('runtime-estimate');
        if (runtimeContainer) {
            runtimeContainer.innerHTML = `
                <p class="text-center">
                    <span class="badge bg-primary fs-6">${minRuntime}-${maxRuntime} seconds</span>
                </p>
                <small class="text-muted">
                    Based on ${selectedModels} models at ${intensity} intensity.
                </small>
            `;
        }
    }

    loadPreset(presetName) {
        const presets = {
            'urban_conflict': {
                scenario_type: 'military',
                environment_type: 'medium_city',
                population_size: 500000,
                intensity: 'high',
                duration_days: 21,
                terrain_type: 'urban_medium'
            },
            'rural_disaster': {
                scenario_type: 'climate',
                environment_type: 'village',
                population_size: 25000,
                intensity: 'extreme',
                duration_days: 90,
                terrain_type: 'rural_agricultural'
            },
            'economic_crisis': {
                scenario_type: 'economic',
                environment_type: 'large_country',
                population_size: 100000000,
                intensity: 'high',
                duration_days: 365,
                terrain_type: 'urban_medium'
            },
            'global_pandemic': {
                scenario_type: 'climate',
                environment_type: 'global',
                population_size: 1000000000,
                intensity: 'extreme',
                duration_days: 730,
                terrain_type: 'urban_medium'
            }
        };

        const preset = presets[presetName];
        if (!preset) return;

        // Apply preset values to form
        Object.keys(preset).forEach(key => {
            const element = document.getElementById(key) || document.querySelector(`input[name="${key}"][value="${preset[key]}"]`);
            if (element) {
                if (element.type === 'radio') {
                    element.checked = true;
                    element.dispatchEvent(new Event('change'));
                } else {
                    element.value = preset[key];
                    element.dispatchEvent(new Event('change'));
                }
            }
        });

        window.pmp.showSuccess(`Applied ${presetName.replace('_', ' ')} preset`);
    }

    collectFormData() {
        const formData = new FormData(document.getElementById('scenarioForm'));
        const data = {};

        // Convert FormData to object
        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                // Handle multiple values (like checkboxes)
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        }

        // Convert string numbers to integers
        ['population_size', 'duration_days'].forEach(field => {
            if (data[field]) data[field] = parseInt(data[field]);
        });

        // Convert checkboxes to booleans
        ['nuclear_escalation', 'supply_chain_impact', 'climate_effects'].forEach(field => {
            data[field] = formData.has(field);
        });

        return data;
    }

    validateScenario(data) {
        const errors = [];

        if (!data.scenario_type) {
            errors.push('Please select a scenario type');
        }

        if (!data.population_size || data.population_size < 1000) {
            errors.push('Population size must be at least 1,000');
        }

        if (!data.duration_days || data.duration_days < 1) {
            errors.push('Duration must be at least 1 day');
        }

        if (!data.models || data.models.length === 0) {
            errors.push('Please select at least one analysis model');
        }

        return errors;
    }

    async runAnalysis() {
        const scenarioData = this.collectFormData();
        const validationErrors = this.validateScenario(scenarioData);

        if (validationErrors.length > 0) {
            window.pmp.showError('Validation errors:\n' + validationErrors.join('\n'));
            return;
        }

        try {
            // Show progress modal
            const modal = new bootstrap.Modal(document.getElementById('analysisModal'));
            modal.show();

            // Start analysis
            const response = await window.pmp.makeAPIRequest('/api/run-scenario', 'POST', scenarioData);

            if (response.status === 'success') {
                const scenarioId = response.scenario_id;

                // Poll for progress
                this.pollScenarioProgress(scenarioId, modal);

            } else {
                modal.hide();
                window.pmp.showError('Failed to start analysis: ' + (response.error || 'Unknown error'));
            }

        } catch (error) {
            modal.hide();
            window.pmp.showError('Failed to run analysis: ' + error.message);
        }
    }

    async pollScenarioProgress(scenarioId, modal) {
        const progressBar = document.getElementById('analysisProgress');
        const statusText = document.getElementById('analysisStatus');

        const pollInterval = setInterval(async () => {
            try {
                const status = await window.pmp.makeAPIRequest(`/api/scenario-status/${scenarioId}`);

                progressBar.style.width = `${status.progress || 0}%`;
                statusText.textContent = status.current_phase || 'Processing...';

                if (status.status === 'completed') {
                    clearInterval(pollInterval);
                    modal.hide();
                    window.pmp.showSuccess('Analysis completed successfully!');

                    // Redirect to results
                    setTimeout(() => {
                        window.location.href = `/results/${scenarioId}`;
                    }, 1500);

                } else if (status.status === 'error') {
                    clearInterval(pollInterval);
                    modal.hide();
                    window.pmp.showError('Analysis failed: ' + (status.error || 'Unknown error'));
                }

            } catch (error) {
                clearInterval(pollInterval);
                modal.hide();
                window.pmp.showError('Failed to get analysis status: ' + error.message);
            }
        }, 2000); // Poll every 2 seconds

        // Timeout after 10 minutes
        setTimeout(() => {
            clearInterval(pollInterval);
            modal.hide();
            window.pmp.showError('Analysis timed out. Please try again.');
        }, 600000);
    }

    saveScenario() {
        const scenarioData = this.collectFormData();
        const validationErrors = this.validateScenario(scenarioData);

        if (validationErrors.length > 0) {
            window.pmp.showError('Validation errors:\n' + validationErrors.join('\n'));
            return;
        }

        // Save to localStorage for now (in real app, would save to server)
        const scenarioId = 'scenario_' + Date.now();
        window.pmp.saveUserPreference(`saved_scenario_${scenarioId}`, scenarioData);

        window.pmp.showSuccess('Scenario saved successfully!');
    }

    resetForm() {
        document.getElementById('scenarioForm').reset();

        // Reset to defaults
        document.getElementById('military').checked = true;
        document.getElementById('intensity').value = 'medium';
        document.getElementById('duration_days').value = 30;
        document.getElementById('population_size').value = 1000000;

        // Reset model selections
        document.querySelectorAll('input[name="models"]').forEach(cb => cb.checked = true);

        this.updateRuntimeEstimate();
        this.updateModelInfo();

        window.pmp.showInfo('Form reset to defaults');
    }
}

// Global functions for template usage
window.runAnalysis = () => window.scenarioBuilder.runAnalysis();
window.saveScenario = () => window.scenarioBuilder.saveScenario();
window.resetForm = () => window.scenarioBuilder.resetForm();
window.loadPreset = (presetName) => window.scenarioBuilder.loadPreset(presetName);

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.scenarioBuilder = new ScenarioBuilder();
});