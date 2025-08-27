// Comprehensive Predictive Modeling Platform - Main JavaScript

class PredictiveModelingPlatform {
    constructor() {
        this.activeScenario = null;
        this.charts = {};
        this.threejsScene = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeCharts();
        this.setupWebSocket();
        this.loadUserPreferences();
    }

    setupEventListeners() {
        // Global event listeners
        document.addEventListener('DOMContentLoaded', () => {
            this.initializeTooltips();
            this.setupFormValidation();
        });

        // Window resize handler for responsive charts
        window.addEventListener('resize', () => {
            this.resizeCharts();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });
    }

    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    }

    validateForm(form) {
        return form.checkValidity();
    }

    initializeTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Chart Management
    initializeCharts() {
        Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        Chart.defaults.color = '#64748b';
        Chart.defaults.borderColor = '#e2e8f0';
    }

    createChart(containerId, config) {
        const ctx = document.getElementById(containerId);
        if (!ctx) return null;

        // Destroy existing chart if it exists
        if (this.charts[containerId]) {
            this.charts[containerId].destroy();
        }

        this.charts[containerId] = new Chart(ctx, config);
        return this.charts[containerId];
    }

    resizeCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.resize === 'function') {
                chart.resize();
            }
        });
    }

    // Three.js 3D Visualization
    initialize3DScene(containerId, sceneConfig) {
        const container = document.getElementById(containerId);
        if (!container) return;

        // Clear existing content
        container.innerHTML = '';

        // Create scene, camera, renderer
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(
            sceneConfig.camera.fov || 75,
            container.clientWidth / container.clientHeight,
            0.1,
            1000
        );

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        renderer.setClearColor(0x2a2a2a);
        container.appendChild(renderer.domElement);

        // Add lighting
        if (sceneConfig.lighting) {
            const ambientLight = new THREE.AmbientLight(
                sceneConfig.lighting.ambient.color,
                sceneConfig.lighting.ambient.intensity
            );
            scene.add(ambientLight);

            const directionalLight = new THREE.DirectionalLight(
                sceneConfig.lighting.directional.color,
                sceneConfig.lighting.directional.intensity
            );
            directionalLight.position.set(...sceneConfig.lighting.directional.position);
            scene.add(directionalLight);
        }

        // Add objects to scene
        if (sceneConfig.objects) {
            sceneConfig.objects.forEach(objConfig => {
                const object = this.create3DObject(objConfig);
                if (object) scene.add(object);
            });
        }

        // Set camera position
        camera.position.set(...sceneConfig.camera.position);
        if (sceneConfig.camera.target) {
            camera.lookAt(...sceneConfig.camera.target);
        }

        // Add controls
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        // Animation loop
        const animate = () => {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        };

        animate();

        // Handle window resize
        const handleResize = () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        };

        window.addEventListener('resize', handleResize);

        this.threejsScene = { scene, camera, renderer, controls };
        return this.threejsScene;
    }

    create3DObject(config) {
        let geometry, material, mesh;

        // Create geometry based on type
        switch (config.type) {
            case 'box':
                geometry = new THREE.BoxGeometry(
                    config.scale[0],
                    config.scale[1],
                    config.scale[2]
                );
                break;
            case 'sphere':
                geometry = new THREE.SphereGeometry(config.scale[0], 32, 32);
                break;
            case 'cylinder':
                geometry = new THREE.CylinderGeometry(
                    config.scale[0],
                    config.scale[0],
                    config.scale[1],
                    32
                );
                break;
            case 'plane':
                geometry = new THREE.PlaneGeometry(config.scale[0], config.scale[2]);
                break;
            default:
                return null;
        }

        // Create material
        material = new THREE.MeshLambertMaterial({
            color: config.color,
            transparent: config.opacity < 1,
            opacity: config.opacity || 1
        });

        mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(...config.position);

        // Add label if specified
        if (config.label) {
            mesh.userData = { label: config.label };
        }

        return mesh;
    }

    // API Communication
    async makeAPIRequest(endpoint, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(endpoint, options);
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'API request failed');
            }

            return result;
        } catch (error) {
            console.error('API Error:', error);
            this.showError('API Error: ' + error.message);
            throw error;
        }
    }

    // WebSocket for real-time updates
    setupWebSocket() {
        // Note: WebSocket would require server-side implementation
        // This is a placeholder for real-time scenario updates
        console.log('WebSocket setup placeholder');
    }

    // User Interface Helpers
    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'danger');
    }

    showInfo(message) {
        this.showAlert(message, 'info');
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';

        alertContainer.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertContainer);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertContainer.parentNode) {
                alertContainer.remove();
            }
        }, 5000);
    }

    showLoading(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'loading-overlay';
        loadingOverlay.innerHTML = '<div class="loading-spinner"></div>';

        container.style.position = 'relative';
        container.appendChild(loadingOverlay);
    }

    hideLoading(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const loadingOverlay = container.querySelector('.loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.remove();
        }
    }

    // Utility Functions
    formatNumber(num, decimals = 0) {
        return new Intl.NumberFormat('en-US', {
            maximumFractionDigits: decimals,
            minimumFractionDigits: decimals
        }).format(num);
    }

    formatCurrency(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency,
            notation: amount >= 1000000000 ? 'compact' : 'standard'
        }).format(amount);
    }

    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    }

    // Keyboard shortcuts
    handleKeyboardShortcuts(e) {
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 'n':
                    e.preventDefault();
                    // Navigate to new scenario
                    window.location.href = '/scenario-builder';
                    break;
                case 'h':
                    e.preventDefault();
                    // Navigate to dashboard
                    window.location.href = '/';
                    break;
            }
        }
    }

    // Local storage helpers
    saveUserPreference(key, value) {
        try {
            localStorage.setItem(`pmp_${key}`, JSON.stringify(value));
        } catch (e) {
            console.warn('Could not save user preference:', e);
        }
    }

    loadUserPreference(key, defaultValue = null) {
        try {
            const value = localStorage.getItem(`pmp_${key}`);
            return value ? JSON.parse(value) : defaultValue;
        } catch (e) {
            console.warn('Could not load user preference:', e);
            return defaultValue;
        }
    }

    loadUserPreferences() {
        // Load saved preferences like theme, chart preferences, etc.
        const theme = this.loadUserPreference('theme', 'light');
        this.applyTheme(theme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
    }

    // Export functionality
    exportResults(scenarioId, format = 'json') {
        this.makeAPIRequest(`/api/export/${scenarioId}?format=${format}`)
            .then(response => {
                // Handle export download
                const blob = new Blob([JSON.stringify(response, null, 2)], {
                    type: 'application/json'
                });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `scenario_${scenarioId}.${format}`;
                a.click();
                URL.revokeObjectURL(url);
            })
            .catch(error => {
                this.showError('Export failed: ' + error.message);
            });
    }
}

// Initialize the platform
window.PredictiveModelingPlatform = new PredictiveModelingPlatform();

// Expose globally for use in other scripts
window.pmp = window.PredictiveModelingPlatform;