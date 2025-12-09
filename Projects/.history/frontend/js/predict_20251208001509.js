// ============================================
// PREDICT.JS - Prediction Page JavaScript for ThyroScan AI
// ADJUSTED FOR MONGODB BACKEND
// ============================================

// Global variables
let predictionChart = null;
let currentFormData = null;
let isSubmitting = false;

// API Configuration - MATCHING HISTORY.JS
const API_CONFIG = {
    BASE_URL: window.API_BASE_URL || 'http://localhost:8000',
    ENDPOINTS: {
        HISTORY: '/history',
        PREDICT: '/predict',
        HEALTH: '/health'
    }
};

// Initialize Predict Page
function initializePredictPage() {
    console.log('🔮 Predict page initialized');
    
    // Initialize form elements
    initializeForm();
    
    // Initialize real-time validation
    initializeRealTimeValidation();
    
    // Initialize range indicators
    initializeRangeIndicators();
    
    // Initialize interactive elements
    initializeInteractiveElements();
    
    // Initialize results modal
    initializeResultsModal();
    
    // Setup event listeners
    setupPredictEventListeners();
    
    // Set default values
    setDefaultValues();
    
    // Initialize form steps
    initializeFormSteps();
}

// Initialize Form
function initializeForm() {
    const form = document.getElementById('thyroidForm');
    if (!form) return;
    
    // Initialize floating labels
    const floatingInputs = form.querySelectorAll('.floating-input input, .floating-select select');
    floatingInputs.forEach(input => {
        // Check if input has value on load
        if (input.value.trim() !== '') {
            input.parentElement.classList.add('has-value');
        }
        
        // Add input event
        input.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                this.parentElement.classList.add('has-value');
            } else {
                this.parentElement.classList.remove('has-value');
            }
        });
    });
    
    // Initialize checkbox cards
    const checkboxes = form.querySelectorAll('.risk-factor-card input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const card = this.closest('.risk-factor-card');
            if (this.checked) {
                card.classList.add('checked');
                // Add animation
                card.style.transform = 'translateY(-2px)';
                setTimeout(() => {
                    card.style.transform = '';
                }, 300);
            } else {
                card.classList.remove('checked');
            }
        });
    });
}

// Initialize Real-Time Validation
function initializeRealTimeValidation() {
    const validateInputs = document.querySelectorAll('.floating-input input[type="number"]');
    
    validateInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateNumberInput(this);
        });
        
        input.addEventListener('blur', function() {
            validateNumberInput(this, true);
        });
    });
}

// Validate Number Input
function validateNumberInput(input, showError = false) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min) || 0;
    const max = parseFloat(input.max) || Infinity;
    const parent = input.closest('.input-group');
    
    // Remove previous validation classes
    parent.classList.remove('valid', 'invalid');
    
    if (input.value.trim() === '') {
        return true;
    }
    
    if (isNaN(value)) {
        if (showError) {
            parent.classList.add('invalid');
            showInputError(input, 'Please enter a valid number');
        }
        return false;
    }
    
    if (value < min || value > max) {
        if (showError) {
            parent.classList.add('invalid');
            showInputError(input, `Value must be between ${min} and ${max}`);
        }
        return false;
    }
    
    parent.classList.add('valid');
    return true;
}

// Show Input Error
function showInputError(input, message) {
    const parent = input.closest('.input-group');
    let errorElement = parent.querySelector('.input-error');
    
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'input-error';
        parent.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (errorElement.parentNode) {
            errorElement.remove();
        }
    }, 5000);
}

// Initialize Range Indicators
function initializeRangeIndicators() {
    const rangeInputs = document.querySelectorAll('input[type="number"][min][max]');
    
    rangeInputs.forEach(input => {
        const parent = input.closest('.input-group');
        const rangeBar = parent?.querySelector('.range-fill');
        
        if (rangeBar) {
            updateRangeIndicator(input, rangeBar);
            
            input.addEventListener('input', function() {
                updateRangeIndicator(this, rangeBar);
            });
        }
    });
}

// Update Range Indicator
function updateRangeIndicator(input, rangeBar) {
    const value = parseFloat(input.value) || 0;
    const min = parseFloat(input.min) || 0;
    const max = parseFloat(input.max) || 100;
    
    const percentage = ((value - min) / (max - min)) * 100;
    rangeBar.style.width = `${Math.min(100, Math.max(0, percentage))}%`;
    
    // Update color based on value
    if (percentage < 30) {
        rangeBar.style.background = 'var(--gradient-secondary)';
    } else if (percentage < 70) {
        rangeBar.style.background = 'var(--gradient-primary)';
    } else {
        rangeBar.style.background = 'var(--gradient-accent)';
    }
}

// Initialize Interactive Elements
function initializeInteractiveElements() {
    // Input action buttons
    const actionButtons = document.querySelectorAll('.btn-input-action');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const tooltip = this.getAttribute('data-tooltip');
            if (tooltip) {
                ThyroScan.showInfo(tooltip, 'Information');
            }
        });
    });
    
    // Help button
    const helpButton = document.querySelector('.btn-help');
    if (helpButton) {
        helpButton.addEventListener('click', function(e) {
            e.preventDefault();
            showFormHelp();
        });
    }
    
    // Form section cards hover effect
    const formCards = document.querySelectorAll('.form-section-card');
    formCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

// Show Form Help
function showFormHelp() {
    const helpContent = `
        <h4>Form Help Guide</h4>
        <p><strong>Age:</strong> Enter patient's age in years (0-120)</p>
        <p><strong>TSH Level:</strong> Normal range: 0.4-4.0 mIU/L</p>
        <p><strong>T3 Level:</strong> Normal range: 2.3-4.2 pg/mL</p>
        <p><strong>T4 Level:</strong> Normal range: 0.8-1.8 μg/dL</p>
        <p><strong>Nodule Size:</strong> Thyroid nodule diameter in cm</p>
        <p><strong>Risk Factors:</strong> Check all that apply to the patient</p>
    `;
    
    ThyroScan.showInfo(helpContent, 'Form Instructions');
}

// Initialize Results Modal
function initializeResultsModal() {
    const modal = document.getElementById('resultsModal');
    if (!modal) return;
    
    // Close modal when clicking overlay
    const overlay = modal.querySelector('.modal-overlay');
    if (overlay) {
        overlay.addEventListener('click', closeResultsModal);
    }
    
    // Close modal when clicking close button
    const closeButton = document.getElementById('closeResults');
    if (closeButton) {
        closeButton.addEventListener('click', closeResultsModal);
    }
    
    // Escape key to close modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            closeResultsModal();
        }
    });
}

// Initialize Form Steps
function initializeFormSteps() {
    const steps = document.querySelectorAll('.step');
    const progressFill = document.querySelector('.progress-fill');
    
    if (!steps.length || !progressFill) return;
    
    // Update step based on form completion
    const form = document.getElementById('thyroidForm');
    form.addEventListener('input', ThyroScan.debounce(() => {
        updateFormProgress();
    }, 500));
}

// Update Form Progress
function updateFormProgress() {
    const form = document.getElementById('thyroidForm');
    if (!form) return;
    
    const requiredInputs = form.querySelectorAll('input[required], select[required]');
    const filledInputs = Array.from(requiredInputs).filter(input => {
        if (input.type === 'checkbox') {
            return input.checked;
        }
        return input.value.trim() !== '';
    });
    
    const progress = (filledInputs.length / requiredInputs.length) * 100;
    const progressFill = document.querySelector('.progress-fill');
    
    if (progressFill) {
        progressFill.style.width = `${progress}%`;
    }
    
    // Update steps
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        step.classList.remove('active');
        if (progress >= (index + 1) * 33) {
            step.classList.add('active');
        }
    });
    
    // Update preview if available
    updateResultsPreview();
}

// Update Results Preview
function updateResultsPreview() {
    const preview = document.getElementById('resultsPreview');
    if (!preview || preview.classList.contains('hidden')) return;
    
    const formData = getFormData();
    if (!formData) return;
    
    // Calculate simple risk score for preview
    let riskScore = 0;
    
    // Age factor
    if (formData.Age > 50) riskScore += 20;
    else if (formData.Age > 30) riskScore += 10;
    
    // TSH factor
    if (formData.TSH_Level > 4 || formData.TSH_Level < 0.4) riskScore += 15;
    
    // Nodule size factor
    if (formData.Nodule_Size > 3) riskScore += 25;
    else if (formData.Nodule_Size > 1) riskScore += 10;
    
    // Risk factors count
    const riskFactors = [
        formData.Family_History,
        formData.Radiation_Exposure,
        formData.Iodine_Deficiency,
        formData.Smoking,
        formData.Obesity,
        formData.Diabetes
    ].filter(Boolean).length;
    
    riskScore += riskFactors * 5;
    
    // Cap at 100
    riskScore = Math.min(100, riskScore);
    
    // Update preview display
    const percentageElement = preview.querySelector('.risk-percentage');
    const circleElement = preview.querySelector('.circle-progress circle:last-child');
    
    if (percentageElement) {
        percentageElement.textContent = `${Math.round(riskScore)}%`;
    }
    
    if (circleElement) {
        const circumference = 2 * Math.PI * 54;
        const offset = circumference - (riskScore / 100) * circumference;
        circleElement.style.strokeDashoffset = offset;
    }
}

// Setup Predict Event Listeners
function setupPredictEventListeners() {
    // Form submission
    const form = document.getElementById('thyroidForm');
    if (form) {
        form.addEventListener('submit', handlePredictionSubmit);
    }
    
    // Reset button
    const resetBtn = document.getElementById('resetBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', resetForm);
    }
    
    // Save report button
    const saveReportBtn = document.getElementById('saveReportBtn');
    if (saveReportBtn) {
        saveReportBtn.addEventListener('click', saveReport);
    }
    
    // New prediction button
    const newPredictionBtn = document.getElementById('newPredictionBtn');
    if (newPredictionBtn) {
        newPredictionBtn.addEventListener('click', startNewPrediction);
    }
}

// Set Default Values
function setDefaultValues() {
    // Set default values for form
    const defaults = {
        'Age': 45,
        'TSH_Level': 2.5,
        'T3_Level': 1.2,
        'T4_Level': 8.0,
        'Nodule_Size': 1.5,
        'Thyroid_Cancer_Risk': '2',
        'Gender_Male': '1'
    };
    
    Object.entries(defaults).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            element.value = value;
            
            // Trigger input event for floating labels
            if (element.tagName === 'INPUT' || element.tagName === 'SELECT') {
                element.dispatchEvent(new Event('input'));
            }
        }
    });
    
    // Update progress after setting defaults
    setTimeout(updateFormProgress, 100);
}

// Get Form Data
function getFormData() {
    const form = document.getElementById('thyroidForm');
    if (!form) return null;
    
    try {
        const data = {
            Age: parseFloat(document.getElementById('Age').value) || 0,
            TSH_Level: parseFloat(document.getElementById('TSH_Level').value) || 0,
            T3_Level: parseFloat(document.getElementById('T3_Level').value) || 0,
            T4_Level: parseFloat(document.float(document.getElementById('T4_Level').value)) || 0,
            Nodule_Size: parseFloat(document.getElementById('Nodule_Size').value) || 0,
            Thyroid_Cancer_Risk: parseInt(document.getElementById('Thyroid_Cancer_Risk').value) || 0,
            Gender_Male: parseInt(document.getElementById('Gender_Male').value) || 0,
            Family_History: document.getElementById('Family_History').checked ? 1 : 0,
            Radiation_Exposure: document.getElementById('Radiation_Exposure').checked ? 1 : 0,
            Iodine_Deficiency: document.getElementById('Iodine_Deficiency').checked ? 1 : 0,
            Smoking: document.getElementById('Smoking').checked ? 1 : 0,
            Obesity: document.getElementById('Obesity').checked ? 1 : 0,
            Diabetes: document.getElementById('Diabetes').checked ? 1 : 0
        };
        
        return data;
    } catch (error) {
        console.error('Error getting form data:', error);
        return null;
    }
}

// Validate Form
function validateForm() {
    const form = document.getElementById('thyroidForm');
    if (!form) return false;
    
    let isValid = true;
    const errors = [];
    
    // Validate required fields
    const requiredInputs = form.querySelectorAll('[required]');
    requiredInputs.forEach(input => {
        if (input.type === 'checkbox') {
            // Checkboxes don't need validation for required
            return;
        }
        
        if (!input.value.trim()) {
            isValid = false;
            input.closest('.input-group')?.classList.add('invalid');
            errors.push(`${input.previousElementSibling?.textContent || 'Field'} is required`);
        }
    });
    
    // Validate number ranges
    const numberInputs = form.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        if (!validateNumberInput(input, false)) {
            isValid = false;
            input.closest('.input-group')?.classList.add('invalid');
        }
    });
    
    if (!isValid && errors.length > 0) {
        ThyroScan.showError(errors.join('<br>'), 'Validation Error');
    }
    
    return isValid;
}

// Handle Prediction Submit - ADJUSTED FOR YOUR BACKEND
async function handlePredictionSubmit(e) {
    e.preventDefault();
    
    if (isSubmitting) return;
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    isSubmitting = true;
    currentFormData = getFormData();
    
    if (!currentFormData) {
        ThyroScan.showError('Unable to get form data', 'Error');
        isSubmitting = false;
        return;
    }
    
    // Show loading state
    const predictBtn = document.getElementById('predictBtn');
    const originalHTML = predictBtn.innerHTML;
    predictBtn.innerHTML = `
        <i class="fas fa-spinner fa-spin"></i>
        Analyzing with AI...
    `;
    predictBtn.disabled = true;
    
    try {
        // YOUR BACKEND API: POST /predict
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.PREDICT}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentFormData)
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        const result = await response.json();
        
        console.log('✅ Prediction result:', result);
        
        // YOUR BACKEND RESPONSE FORMAT:
        // {
        //   "prediction": "Malignant" or "Benign",
        //   "risk_percentage": 65.5,
        //   "confidence": "High/Medium/Low",
        //   "features_importance": {...},
        //   "chart_data": "JSON string of Plotly chart"
        // }
        
        // Display the actual results (not just notification)
        displayResults(result);
        
        // Save to localStorage for history page to detect
        saveToLocalStorage(result);
        
        // Show success message with actual prediction
        ThyroScan.showSuccess(
            `Prediction: ${result.prediction} | Risk: ${result.risk_percentage}% | Confidence: ${result.confidence}`, 
            'Analysis Complete'
        );
        
    } catch (error) {
        console.error('❌ Prediction error:', error);
        
        // Show error message
        ThyroScan.showError(
            `Failed to get prediction: ${error.message}`, 
            'Analysis Failed'
        );
        
        // Show mock results for demo/fallback
        showMockResults();
        
    } finally {
        // Reset loading state
        predictBtn.innerHTML = originalHTML;
        predictBtn.disabled = false;
        isSubmitting = false;
    }
}

// Save to LocalStorage (for history page detection)
function saveToLocalStorage(result) {
    try {
        // Save prediction data to localStorage (temporarily)
        const predictionData = {
            user_data: currentFormData,
            prediction: result.prediction,
            risk_percentage: result.risk_percentage,
            timestamp: new Date().toISOString()
        };
        
        // Save to localStorage for history page to detect
        localStorage.setItem('thyroscan_new_prediction', JSON.stringify(predictionData));
        
        // Also save to local history backup
        const existingHistory = JSON.parse(localStorage.getItem('thyroscan_local_history') || '[]');
        existingHistory.unshift(predictionData);
        
        // Keep only last 50 records
        if (existingHistory.length > 50) {
            existingHistory.length = 50;
        }
        
        localStorage.setItem('thyroscan_local_history', JSON.stringify(existingHistory));
        
        console.log('✅ Prediction saved to localStorage');
        
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

// Display Results - ADJUSTED FOR YOUR BACKEND RESPONSE
function displayResults(result) {
    // Update risk percentage
    const riskPercentage = result.risk_percentage || 0;
    document.getElementById('riskPercentage').textContent = `${riskPercentage.toFixed(1)}%`;
    document.getElementById('predictionText').textContent = result.prediction || 'Analysis Complete';
    document.getElementById('confidenceText').textContent = `Confidence: ${result.confidence || 'Medium'}`;
    
    // Update risk circle
    updateRiskCircle(riskPercentage);
    
    // Update meter fill
    const meterFill = document.getElementById('meterFill');
    if (meterFill) {
        meterFill.style.width = `${riskPercentage}%`;
        
        // Update meter color based on risk
        if (riskPercentage < 30) {
            meterFill.style.background = 'var(--gradient-secondary)';
        } else if (riskPercentage < 70) {
            meterFill.style.background = 'var(--gradient-primary)';
        } else {
            meterFill.style.background = 'var(--gradient-accent)';
        }
    }
    
    // Display chart if available from backend
    if (result.chart_data) {
        try {
            const chartData = typeof result.chart_data === 'string' 
                ? JSON.parse(result.chart_data) 
                : result.chart_data;
            displayChart(chartData);
        } catch (error) {
            console.error('Error parsing chart data:', error);
            createDefaultChart();
        }
    } else {
        createDefaultChart();
    }
    
    // Display key factors from backend
    displayKeyFactors(result.features_importance || {});
    
    // Generate and display recommendations based on risk percentage
    displayRecommendations([], riskPercentage);
    
    // Show results modal
    showResultsModal();
}

// Update Risk Circle
function updateRiskCircle(percentage) {
    const circle = document.querySelector('.score-circle circle:last-child');
    if (!circle) return;
    
    const radius = 70; // Should match SVG radius
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (percentage / 100) * circumference;
    
    circle.style.strokeDashoffset = offset;
    
    // Update color based on risk
    if (percentage < 30) {
        circle.style.stroke = 'url(#gradient-secondary)';
    } else if (percentage < 70) {
        circle.style.stroke = 'url(#gradient-primary)';
    } else {
        circle.style.stroke = 'url(#gradient-accent)';
    }
}

// Display Chart - HANDLES PLOTLY FROM BACKEND
function displayChart(chartData) {
    const container = document.getElementById('chartContainer');
    if (!container) return;
    
    // Destroy existing chart
    if (predictionChart) {
        predictionChart.destroy();
    }
    
    // Check if it's Plotly data from backend
    if (window.Plotly && chartData.data && chartData.layout) {
        try {
            Plotly.newPlot('chartContainer', chartData.data, chartData.layout, {
                responsive: true
            });
            return;
        } catch (error) {
            console.error('Plotly chart error:', error);
        }
    }
    
    // Fallback to default chart
    createDefaultChart();
}

// Create Default Chart
function createDefaultChart() {
    const container = document.getElementById('chartContainer');
    if (!container) return;
    
    // Create Chart.js chart as fallback
    if (window.Chart) {
        const ctx = container.getContext?.('2d');
        if (!ctx) {
            container.innerHTML = `
                <div class="chart-placeholder">
                    <i class="fas fa-chart-bar"></i>
                    <p>Feature importance visualization</p>
                </div>
            `;
            return;
        }
        
        if (predictionChart) {
            predictionChart.destroy();
        }
        
        // Sample data based on form data
        const labels = ['Age', 'TSH', 'T3', 'T4', 'Nodule Size'];
        const values = [
            (currentFormData?.Age || 0) / 100 * 10,
            (currentFormData?.TSH_Level || 0) / 10 * 8,
            (currentFormData?.T3_Level || 0) / 5 * 6,
            (currentFormData?.T4_Level || 0) / 20 * 7,
            (currentFormData?.Nodule_Size || 0) * 2
        ];
        
        predictionChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Impact Score',
                    data: values,
                    backgroundColor: ['#2D5BFF', '#00D4AA', '#FF6B9D', '#FFA502', '#3498DB'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10
                    }
                }
            }
        });
    } else {
        container.innerHTML = `
            <div class="chart-placeholder">
                <i class="fas fa-chart-bar"></i>
                <p>Feature importance chart will appear here</p>
            </div>
        `;
    }
}

// Display Key Factors - ADJUSTED FOR BACKEND FORMAT
function displayKeyFactors(factors) {
    const container = document.getElementById('factorsList');
    if (!container) return;
    
    container.innerHTML = '';
    
    let factorsArray = [];
    
    // Convert factors object to array
    if (factors && typeof factors === 'object') {
        factorsArray = Object.entries(factors)
            .map(([name, value]) => ({ name, value: parseFloat(value) || 0 }))
            .sort((a, b) => b.value - a.value)
            .slice(0, 6); // Show top 6 factors
    }
    
    // If no factors from backend, create from form data
    if (factorsArray.length === 0 && currentFormData) {
        factorsArray = [
            { name: 'Nodule Size', value: currentFormData?.Nodule_Size || 0 },
            { name: 'Age', value: (currentFormData?.Age || 0) / 5 },
            { name: 'TSH Level', value: Math.abs((currentFormData?.TSH_Level || 0) - 2.5) },
            { name: 'Cancer Risk Score', value: currentFormData?.Thyroid_Cancer_Risk || 0 },
            { name: 'T4 Level', value: Math.abs((currentFormData?.T4_Level || 0) - 10) },
            { name: 'T3 Level', value: Math.abs((currentFormData?.T3_Level || 0) - 1.2) }
        ].filter(f => f.value > 0);
    }
    
    if (factorsArray.length === 0) {
        container.innerHTML = '<div class="no-factors">No significant factors detected</div>';
        return;
    }
    
    // Normalize values for display
    const maxValue = Math.max(...factorsArray.map(f => f.value));
    
    factorsArray.forEach((factor, index) => {
        const percentage = maxValue > 0 ? (factor.value / maxValue) * 100 : 0;
        
        const factorElement = document.createElement('div');
        factorElement.className = 'factor-item fade-in-up';
        factorElement.style.animationDelay = `${index * 0.1}s`;
        factorElement.innerHTML = `
            <div class="factor-header">
                <h4>${factor.name}</h4>
                <span class="factor-value">${factor.value.toFixed(2)}</span>
            </div>
            <div class="factor-bar">
                <div class="factor-bar-fill" style="width: ${percentage}%"></div>
            </div>
            <div class="factor-impact">
                Impact: ${percentage.toFixed(1)}%
            </div>
        `;
        
        container.appendChild(factorElement);
    });
}

// Display Recommendations
function displayRecommendations(recommendations, riskPercentage) {
    const container = document.getElementById('recommendationsList');
    if (!container) return;
    
    container.innerHTML = '';
    
    // Generate recommendations based on risk if not provided
    if (!recommendations || recommendations.length === 0) {
        recommendations = generateRecommendations(riskPercentage);
    }
    
    recommendations.forEach((rec, index) => {
        const recElement = document.createElement('div');
        recElement.className = 'recommendation-item fade-in-up';
        recElement.style.animationDelay = `${index * 0.1}s`;
        recElement.innerHTML = `
            <div class="recommendation-icon">
                <i class="fas fa-check-circle"></i>
            </div>
            <div class="recommendation-content">
                <p>${rec}</p>
            </div>
        `;
        
        container.appendChild(recElement);
    });
}

// Generate Recommendations
function generateRecommendations(riskPercentage) {
    const recommendations = [];
    
    if (riskPercentage >= 70) {
        recommendations.push(
            'Consult an endocrinologist immediately',
            'Consider fine needle aspiration biopsy',
            'Regular monitoring every 3 months recommended',
            'Complete thyroid function tests required',
            'Ultrasound examination strongly advised'
        );
    } else if (riskPercentage >= 40) {
        recommendations.push(
            'Schedule appointment with endocrinologist',
            'Monitor thyroid levels every 6 months',
            'Maintain healthy iodine intake',
            'Regular ultrasound follow-up recommended',
            'Lifestyle modification advised'
        );
    } else {
        recommendations.push(
            'Regular annual checkup recommended',
            'Maintain healthy lifestyle',
            'Monitor for any symptom changes',
            'Balanced diet with proper iodine',
            'Regular exercise routine beneficial'
        );
    }
    
    // Add general recommendations
    recommendations.push(
        'Avoid smoking and alcohol consumption',
        'Maintain healthy BMI range',
        'Stress management techniques',
        'Regular sleep pattern maintenance'
    );
    
    return recommendations.slice(0, 6); // Limit to 6 recommendations
}

// Show Results Modal
function showResultsModal() {
    const modal = document.getElementById('resultsModal');
    if (!modal) return;
    
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    
    // Add animation
    modal.style.animation = 'modalSlideIn 0.3s ease';
    
    // Scroll to top of modal
    setTimeout(() => {
        modal.scrollTop = 0;
    }, 100);
}

// Close Results Modal
function closeResultsModal() {
    const modal = document.getElementById('resultsModal');
    if (!modal) return;
    
    modal.style.animation = 'modalSlideOut 0.3s ease';
    
    setTimeout(() => {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
    }, 300);
}

// Save Report
function saveReport() {
    const riskPercentage = document.getElementById('riskPercentage').textContent;
    const prediction = document.getElementById('predictionText').textContent;
    const confidence = document.getElementById('confidenceText').textContent;
    
    const report = `
THYROID CANCER RISK ASSESSMENT REPORT
======================================
Date: ${new Date().toLocaleString()}
Prediction: ${prediction}
Risk Percentage: ${riskPercentage}
${confidence}

CLINICAL PARAMETERS:
-------------------
Age: ${currentFormData?.Age || 'N/A'} years
TSH Level: ${currentFormData?.TSH_Level || 'N/A'} mIU/L
T3 Level: ${currentFormData?.T3_Level || 'N/A'} pg/mL
T4 Level: ${currentFormData?.T4_Level || 'N/A'} μg/dL
Nodule Size: ${currentFormData?.Nodule_Size || 'N/A'} cm
Cancer Risk Score: ${currentFormData?.Thyroid_Cancer_Risk || 'N/A'}
Gender: ${currentFormData?.Gender_Male === 1 ? 'Male' : 'Female'}

RISK FACTORS:
-------------
${getRiskFactorsText()}

RECOMMENDATIONS:
---------------
${Array.from(document.querySelectorAll('.recommendation-content p'))
    .map(p => `• ${p.textContent}`)
    .join('\n')}

DISCLAIMER:
----------
This report is generated by ThyroScan AI for educational purposes only.
It is not a substitute for professional medical diagnosis.
Always consult with healthcare professionals for medical advice.

Generated by ThyroScan AI | Model Accuracy: 83%
    `;
    
    // Create download link
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Thyroid_Report_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    ThyroScan.showSuccess('Report downloaded successfully!', 'Report Saved');
}

// Get Risk Factors Text
function getRiskFactorsText() {
    const riskFactors = [
        { id: 'Family_History', label: 'Family History of Thyroid Disease' },
        { id: 'Radiation_Exposure', label: 'Radiation Exposure' },
        { id: 'Iodine_Deficiency', label: 'Iodine Deficiency' },
        { id: 'Smoking', label: 'Smoking History' },
        { id: 'Obesity', label: 'Obesity (BMI ≥ 30)' },
        { id: 'Diabetes', label: 'Diabetes Mellitus' }
    ];
    
    const activeFactors = riskFactors
        .filter(factor => currentFormData?.[factor.id] === 1)
        .map(factor => `✓ ${factor.label}`);
    
    return activeFactors.length > 0 
        ? activeFactors.join('\n') 
        : 'No significant risk factors detected';
}

// Reset Form
function resetForm() {
    const form = document.getElementById('thyroidForm');
    if (!form) return;
    
    form.reset();
    setDefaultValues();
    
    // Reset validation classes
    const inputGroups = form.querySelectorAll('.input-group');
    inputGroups.forEach(group => {
        group.classList.remove('valid', 'invalid', 'has-value');
    });
    
    // Reset checkbox cards
    const checkboxCards = form.querySelectorAll('.risk-factor-card');
    checkboxCards.forEach(card => {
        card.classList.remove('checked');
    });
    
    // Reset progress
    updateFormProgress();
    
    ThyroScan.showSuccess('Form has been reset', 'Form Reset');
}

// Start New Prediction
function startNewPrediction() {
    closeResultsModal();
    resetForm();
    
    // Scroll to form
    const formSection = document.querySelector('.form-section');
    if (formSection) {
        formSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// Show Mock Results (for demo/fallback)
function showMockResults() {
    const mockResult = {
        prediction: Math.random() > 0.5 ? 'Malignant' : 'Benign',
        risk_percentage: Math.floor(Math.random() * 30) + 60,
        confidence: Math.random() > 0.5 ? 'High' : Math.random() > 0.3 ? 'Medium' : 'Low',
        features_importance: {
            'Nodule Size': Math.random() * 0.3 + 0.4,
            'Age': Math.random() * 0.2 + 0.2,
            'TSH Level': Math.random() * 0.15 + 0.1,
            'Cancer Risk Score': Math.random() * 0.15 + 0.1,
            'Family History': Math.random() * 0.1,
            'Radiation Exposure': Math.random() * 0.05
        }
    };
    
    displayResults(mockResult);
    ThyroScan.showInfo('Showing demonstration results', 'Demo Mode');
}

// Initialize predict page
document.addEventListener('DOMContentLoaded', () => {
    if (typeof initializePredictPage === 'function') {
        initializePredictPage();
    }
});

// Export functions for debugging
window.PredictPage = {
    initializePredictPage,
    getFormData,
    validateForm,
    displayResults,
    showMockResults
};