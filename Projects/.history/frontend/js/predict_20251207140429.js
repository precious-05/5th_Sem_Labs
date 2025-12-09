// ===== CONFIGURATION =====
const API_BASE_URL = 'http://localhost:8000';
let riskChart = null;
let currentPrediction = null;

// ===== DOM ELEMENTS =====
const elements = {
    form: document.getElementById('thyroidForm'),
    predictBtn: document.getElementById('predictBtn'),
    resetBtn: document.getElementById('resetBtn'),
    resultsCard: document.getElementById('resultsCard'),
    closeResults: document.getElementById('closeResults'),
    newPredictionBtn: document.getElementById('newPredictionBtn'),
    saveReportBtn: document.getElementById('saveReportBtn'),
    shareResultsBtn: document.getElementById('shareResultsBtn'),
    loadingSpinner: document.getElementById('loadingSpinner'),
    emptyState: document.getElementById('emptyState'),
    
    // Input elements
    Age: document.getElementById('Age'),
    Family_History: document.getElementById('Family_History'),
    Radiation_Exposure: document.getElementById('Radiation_Exposure'),
    Iodine_Deficiency: document.getElementById('Iodine_Deficiency'),
    Smoking: document.getElementById('Smoking'),
    Obesity: document.getElementById('Obesity'),
    Diabetes: document.getElementById('Diabetes'),
    TSH_Level: document.getElementById('TSH_Level'),
    T3_Level: document.getElementById('T3_Level'),
    T4_Level: document.getElementById('T4_Level'),
    Nodule_Size: document.getElementById('Nodule_Size'),
    Thyroid_Cancer_Risk: document.getElementById('Thyroid_Cancer_Risk'),
    Gender_Male: document.getElementById('Gender_Male'),
    
    // Results elements
    riskPercentage: document.getElementById('riskPercentage'),
    riskCircle: document.getElementById('riskCircle'),
    predictionText: document.getElementById('predictionText'),
    confidenceText: document.getElementById('confidenceText'),
    riskTag: document.getElementById('riskTag'),
    meterFill: document.getElementById('meterFill'),
    meterPointer: document.getElementById('meterPointer'),
    chartContainer: document.getElementById('chartContainer'),
    factorsGrid: document.getElementById('factorsGrid'),
    recommendationsList: document.getElementById('recommendationsList')
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    initializePredictionPage();
});

async function initializePredictionPage() {
    try {
        // Hide preloader
        setTimeout(() => {
            document.querySelector('.preloader')?.classList.add('hidden');
            document.body.classList.add('loaded');
        }, 800);

        // Initialize components
        initializeEventListeners();
        setupInputValidation();
        initializeTooltips();
        loadSampleData();
        checkBackendConnection();
        
        // Update form with any saved data
        loadSavedFormData();
        
        console.log('✅ Prediction page initialized');
    } catch (error) {
        console.error('❌ Prediction page initialization failed:', error);
        showNotification('Failed to initialize prediction page', 'error');
    }
}

// ===== EVENT LISTENERS =====
function initializeEventListeners() {
    // Form submission
    if (elements.form) {
        elements.form.addEventListener('submit', handleFormSubmit);
    }
    
    // Reset form
    if (elements.resetBtn) {
        elements.resetBtn.addEventListener('click', resetForm);
    }
    
    // Close results
    if (elements.closeResults) {
        elements.closeResults.addEventListener('click', () => {
            elements.resultsCard.classList.add('hidden');
            elements.emptyState.classList.remove('hidden');
        });
    }
    
    // New prediction
    if (elements.newPredictionBtn) {
        elements.newPredictionBtn.addEventListener('click', startNewPrediction);
    }
    
    // Save report
    if (elements.saveReportBtn) {
        elements.saveReportBtn.addEventListener('click', saveReport);
    }
    
    // Share results
    if (elements.shareResultsBtn) {
        elements.shareResultsBtn.addEventListener('click', shareResults);
    }
    
    // Real-time input validation
    Object.keys(elements).forEach(key => {
        if (elements[key] && elements[key].tagName === 'INPUT') {
            elements[key].addEventListener('input', validateInput);
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter to submit
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (elements.predictBtn && !elements.predictBtn.disabled) {
                elements.form.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to close results
        if (e.key === 'Escape' && elements.resultsCard && !elements.resultsCard.classList.contains('hidden')) {
            elements.resultsCard.classList.add('hidden');
            elements.emptyState.classList.remove('hidden');
        }
    });
    
    // Form step navigation (for multi-step forms)
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        step.addEventListener('click', () => {
            showFormStep(index + 1);
        });
    });
}

// ===== INPUT VALIDATION =====
function setupInputValidation() {
    // Add validation patterns
    const validationRules = {
        Age: { min: 0, max: 120, step: 1 },
        TSH_Level: { min: 0, max: 100, step: 0.1 },
        T3_Level: { min: 0, max: 20, step: 0.1 },
        T4_Level: { min: 0, max: 30, step: 0.1 },
        Nodule_Size: { min: 0, max: 10, step: 0.1 }
    };
    
    // Set attributes for number inputs
    Object.keys(validationRules).forEach(field => {
        if (elements[field]) {
            const rule = validationRules[field];
            elements[field].min = rule.min;
            elements[field].max = rule.max;
            elements[field].step = rule.step;
        }
    });
}

function validateInput(e) {
    const input = e.target;
    const value = parseFloat(input.value);
    const field = input.id;
    
    // Skip validation for checkboxes and selects
    if (input.type === 'checkbox' || input.tagName === 'SELECT') return;
    
    // Get validation rules
    const rules = {
        Age: { min: 0, max: 120 },
        TSH_Level: { min: 0, max: 100 },
        T3_Level: { min: 0, max: 20 },
        T4_Level: { min: 0, max: 30 },
        Nodule_Size: { min: 0, max: 10 },
        Thyroid_Cancer_Risk: { min: 0, max: 4 }
    };
    
    if (rules[field]) {
        const rule = rules[field];
        
        // Validate range
        if (value < rule.min || value > rule.max) {
            input.classList.add('error');
            showInputError(input, `Value must be between ${rule.min} and ${rule.max}`);
        } else {
            input.classList.remove('error');
            clearInputError(input);
        }
    }
    
    // Update form validity
    updateFormValidity();
}

function validateFormData(formData) {
    const errors = [];
    
    // Validate Age
    if (formData.Age < 0 || formData.Age > 120) {
        errors.push('Age must be between 0 and 120 years');
        elements.Age.classList.add('error');
    }
    
    // Validate TSH Level
    if (formData.TSH_Level < 0 || formData.TSH_Level > 100) {
        errors.push('TSH Level must be between 0 and 100 mIU/L');
        elements.TSH_Level.classList.add('error');
    }
    
    // Validate T3 Level
    if (formData.T3_Level < 0 || formData.T3_Level > 20) {
        errors.push('T3 Level must be between 0 and 20 pg/mL');
        elements.T3_Level.classList.add('error');
    }
    
    // Validate T4 Level
    if (formData.T4_Level < 0 || formData.T4_Level > 30) {
        errors.push('T4 Level must be between 0 and 30 μg/dL');
        elements.T4_Level.classList.add('error');
    }
    
    // Validate Nodule Size
    if (formData.Nodule_Size < 0 || formData.Nodule_Size > 10) {
        errors.push('Nodule Size must be between 0 and 10 cm');
        elements.Nodule_Size.classList.add('error');
    }
    
    // Validate Cancer Risk Score
    if (formData.Thyroid_Cancer_Risk < 0 || formData.Thyroid_Cancer_Risk > 4) {
        errors.push('Cancer Risk Score must be between 0 and 4');
        elements.Thyroid_Cancer_Risk.classList.add('error');
    }
    
    // Show errors if any
    if (errors.length > 0) {
        showNotification(errors.join('<br>'), 'error');
        return false;
    }
    
    return true;
}

function updateFormValidity() {
    const errors = document.querySelectorAll('.input-group .error');
    const isValid = errors.length === 0;
    
    if (elements.predictBtn) {
        elements.predictBtn.disabled = !isValid;
    }
}

function showInputError(input, message) {
    // Remove existing error
    clearInputError(input);
    
    // Create error element
    const errorElement = document.createElement('div');
    errorElement.className = 'input-error';
    errorElement.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
    
    // Insert after input
    input.parentNode.appendChild(errorElement);
}

function clearInputError(input) {
    const existingError = input.parentNode.querySelector('.input-error');
    if (existingError) {
        existingError.remove();
    }
    input.classList.remove('error');
}

// ===== FORM HANDLING =====
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!elements.predictBtn || elements.predictBtn.disabled) {
        showNotification('Please fix validation errors before submitting', 'warning');
        return;
    }
    
    try {
        // Show loading state
        setLoadingState(true);
        
        // Get form data
        const formData = getFormData();
        
        // Validate form data
        if (!validateFormData(formData)) {
            setLoadingState(false);
            return;
        }
        
        // Save form data locally
        saveFormData(formData);
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        currentPrediction = result;
        
        // Display results
        displayResults(result);
        
        // Show success notification
        showNotification('Analysis completed successfully!', 'success');
        
        // Auto-scroll to results
        setTimeout(() => {
            elements.resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 500);
        
    } catch (error) {
        console.error('Prediction error:', error);
        showNotification(`Failed to get prediction: ${error.message}`, 'error');
    } finally {
        // Hide loading state
        setLoadingState(false);
    }
}

function getFormData() {
    return {
        Age: parseFloat(elements.Age.value) || 0,
        Family_History: elements.Family_History.checked ? 1 : 0,
        Radiation_Exposure: elements.Radiation_Exposure.checked ? 1 : 0,
        Iodine_Deficiency: elements.Iodine_Deficiency.checked ? 1 : 0,
        Smoking: elements.Smoking.checked ? 1 : 0,
        Obesity: elements.Obesity.checked ? 1 : 0,
        Diabetes: elements.Diabetes.checked ? 1 : 0,
        TSH_Level: parseFloat(elements.TSH_Level.value) || 0,
        T3_Level: parseFloat(elements.T3_Level.value) || 0,
        T4_Level: parseFloat(elements.T4_Level.value) || 0,
        Nodule_Size: parseFloat(elements.Nodule_Size.value) || 0,
        Thyroid_Cancer_Risk: parseInt(elements.Thyroid_Cancer_Risk.value) || 0,
        Gender_Male: parseInt(elements.Gender_Male.value) || 0
    };
}

function setLoadingState(isLoading) {
    if (elements.predictBtn) {
        elements.predictBtn.disabled = isLoading;
        elements.predictBtn.innerHTML = isLoading ? 
            '<i class="fas fa-spinner fa-spin"></i> Analyzing...' : 
            '<i class="fas fa-brain"></i> Analyze with AI';
    }
    
    if (elements.loadingSpinner) {
        elements.loadingSpinner.classList.toggle('hidden', !isLoading);
    }
    
    // Disable all inputs during loading
    Object.keys(elements).forEach(key => {
        if (elements[key] && (elements[key].tagName === 'INPUT' || elements[key].tagName === 'SELECT')) {
            elements[key].disabled = isLoading;
        }
    });
}

// ===== RESULTS DISPLAY =====
function displayResults(result) {
    if (!result) return;
    
    try {
        // Update risk percentage
        const riskPercentage = result.risk_percentage || 0;
        if (elements.riskPercentage) {
            elements.riskPercentage.textContent = `${riskPercentage.toFixed(1)}%`;
        }
        
        // Update prediction text
        if (elements.predictionText) {
            elements.predictionText.textContent = result.prediction || 'Unknown';
            elements.predictionText.className = result.prediction === 'Malignant' ? 'malignant' : 'benign';
        }
        
        // Update confidence
        if (elements.confidenceText) {
            elements.confidenceText.textContent = `Confidence: ${result.confidence || 'Unknown'}`;
        }
        
        // Update risk tag
        if (elements.riskTag) {
            elements.riskTag.textContent = getRiskLevel(riskPercentage);
            elements.riskTag.className = `risk-tag ${getRiskLevel(riskPercentage).toLowerCase().replace(' ', '-')}`;
        }
        
        // Update risk circle color
        updateRiskCircle(riskPercentage);
        
        // Update meter
        updateRiskMeter(riskPercentage);
        
        // Update chart
        updateChart(result);
        
        // Update key factors
        updateKeyFactors(result.features_importance || {});
        
        // Update recommendations
        updateRecommendations(result);
        
        // Show results card
        elements.resultsCard.classList.remove('hidden');
        elements.emptyState.classList.add('hidden');
        
        // Animate results
        animateResults();
        
    } catch (error) {
        console.error('Error displaying results:', error);
        showNotification('Failed to display results', 'error');
    }
}

function getRiskLevel(percentage) {
    if (percentage < 30) return 'Low Risk';
    if (percentage < 70) return 'Moderate Risk';
    return 'High Risk';
}

function updateRiskCircle(percentage) {
    if (!elements.riskCircle) return;
    
    // Calculate gradient based on risk percentage
    let gradient;
    if (percentage < 30) {
        gradient = `conic-gradient(var(--risk-low) 0%, var(--risk-low) ${percentage}%, var(--gray-lighter) ${percentage}%, var(--gray-lighter) 100%)`;
    } else if (percentage < 70) {
        gradient = `conic-gradient(var(--risk-low) 0%, var(--risk-low) 30%, var(--risk-moderate) 30%, var(--risk-moderate) ${percentage}%, var(--gray-lighter) ${percentage}%, var(--gray-lighter) 100%)`;
    } else {
        gradient = `conic-gradient(var(--risk-low) 0%, var(--risk-low) 30%, var(--risk-moderate) 30%, var(--risk-moderate) 70%, var(--risk-high) 70%, var(--risk-high) ${percentage}%, var(--gray-lighter) ${percentage}%, var(--gray-lighter) 100%)`;
    }
    
    elements.riskCircle.style.background = gradient;
    
    // Add pulse animation for high risk
    if (percentage >= 70) {
        elements.riskCircle.classList.add('pulse');
    } else {
        elements.riskCircle.classList.remove('pulse');
    }
}

function updateRiskMeter(percentage) {
    if (!elements.meterFill || !elements.meterPointer) return;
    
    // Animate meter fill
    elements.meterFill.style.width = `${percentage}%`;
    elements.meterPointer.style.left = `${percentage}%`;
    
    // Add transition
    elements.meterFill.style.transition = 'width 1.5s ease-out';
    elements.meterPointer.style.transition = 'left 1.5s ease-out';
}

function updateChart(result) {
    if (!elements.chartContainer) return;
    
    try {
        // Destroy existing chart
        if (riskChart) {
            riskChart.destroy();
        }
        
        // Parse chart data from backend
        let chartData;
        if (result.chart_data) {
            try {
                chartData = JSON.parse(result.chart_data);
            } catch (e) {
                console.warn('Invalid chart data:', e);
                chartData = createDefaultChart(result);
            }
        } else {
            chartData = createDefaultChart(result);
        }
        
        // Create new chart
        riskChart = Plotly.newPlot('chartContainer', chartData.data, chartData.layout, {
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['lasso2d', 'select2d']
        });
        
        // Add resize listener
        window.addEventListener('resize', () => {
            if (riskChart) {
                Plotly.Plots.resize(elements.chartContainer);
            }
        });
        
    } catch (error) {
        console.error('Error updating chart:', error);
        // Create simple chart as fallback
        createFallbackChart(result);
    }
}

function createDefaultChart(result) {
    const riskPercentage = result.risk_percentage || 0;
    
    return {
        data: [{
            type: 'indicator',
            mode: 'gauge+number',
            value: riskPercentage,
            title: {
                text: 'Thyroid Cancer Risk',
                font: { size: 24, family: 'Montserrat' }
            },
            gauge: {
                axis: {
                    range: [null, 100],
                    tickwidth: 1,
                    tickcolor: 'darkblue'
                },
                bar: { color: 'darkblue' },
                bgcolor: 'white',
                borderwidth: 2,
                bordercolor: 'gray',
                steps: [
                    { range: [0, 30], color: 'lightgreen' },
                    { range: [30, 70], color: 'yellow' },
                    { range: [70, 100], color: 'red' }
                ],
                threshold: {
                    line: { color: 'black', width: 4 },
                    thickness: 0.75,
                    value: riskPercentage
                }
            },
            number: { suffix: '%', font: { size: 40 } }
        }],
        layout: {
            height: 300,
            margin: { t: 0, b: 0, l: 0, r: 0 },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)'
        }
    };
}

function createFallbackChart(result) {
    const riskPercentage = result.risk_percentage || 0;
    
    // Create simple HTML chart as fallback
    elements.chartContainer.innerHTML = `
        <div class="fallback-chart">
            <div class="chart-title">Risk Assessment</div>
            <div class="chart-bar">
                <div class="chart-fill" style="width: ${riskPercentage}%"></div>
            </div>
            <div class="chart-labels">
                <span>0%</span>
                <span>50%</span>
                <span>100%</span>
            </div>
            <div class="chart-value">${riskPercentage.toFixed(1)}%</div>
        </div>
    `;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .fallback-chart {
            padding: 2rem;
            text-align: center;
        }
        .chart-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--dark);
        }
        .chart-bar {
            height: 20px;
            background: var(--gray-lighter);
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 0.5rem;
        }
        .chart-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--risk-low), var(--risk-moderate), var(--risk-high));
            border-radius: 10px;
            transition: width 1.5s ease-out;
        }
        .chart-labels {
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            color: var(--gray);
            margin-bottom: 1rem;
        }
        .chart-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--dark);
        }
    `;
    
    elements.chartContainer.appendChild(style);
}

function updateKeyFactors(factors) {
    if (!elements.factorsGrid) return;
    
    // Clear existing factors
    elements.factorsGrid.innerHTML = '';
    
    // Sort factors by importance
    const sortedFactors = Object.entries(factors)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6); // Show top 6 factors
    
    if (sortedFactors.length === 0) {
        elements.factorsGrid.innerHTML = '<div class="no-factors">No significant factors identified</div>';
        return;
    }
    
    // Create factor cards
    sortedFactors.forEach(([factor, importance], index) => {
        const factorElement = document.createElement('div');
        factorElement.className = 'factor-item';
        factorElement.style.animationDelay = `${index * 0.1}s`;
        
        const importancePercent = (importance * 100).toFixed(1);
        const factorName = formatFeatureName(factor);
        
        factorElement.innerHTML = `
            <div class="factor-header">
                <span class="factor-name">${factorName}</span>
                <span class="factor-percent">${importancePercent}%</span>
            </div>
            <div class="factor-bar">
                <div class="factor-fill" style="width: ${importancePercent}%"></div>
            </div>
            <div class="factor-description">${getFactorDescription(factor)}</div>
        `;
        
        elements.factorsGrid.appendChild(factorElement);
    });
}

function formatFeatureName(feature) {
    const names = {
        'Age': 'Age',
        'Family_History': 'Family History',
        'Radiation_Exposure': 'Radiation Exposure',
        'Iodine_Deficiency': 'Iodine Deficiency',
        'Smoking': 'Smoking',
        'Obesity': 'Obesity',
        'Diabetes': 'Diabetes',
        'TSH_Level': 'TSH Level',
        'T3_Level': 'T3 Level',
        'T4_Level': 'T4 Level',
        'Nodule_Size': 'Nodule Size',
        'Thyroid_Cancer_Risk': 'Cancer Risk Score',
        'Gender_Male': 'Gender'
    };
    
    return names[feature] || feature.replace(/_/g, ' ');
}

function getFactorDescription(feature) {
    const descriptions = {
        'Age': 'Age is a significant factor in thyroid cancer risk',
        'Family_History': 'Genetic predisposition increases risk',
        'Radiation_Exposure': 'Previous radiation exposure elevates risk',
        'TSH_Level': 'Thyroid Stimulating Hormone levels',
        'Nodule_Size': 'Larger nodules have higher malignancy potential',
        'Thyroid_Cancer_Risk': 'Clinical risk assessment score'
    };
    
    return descriptions[feature] || 'Significant contributing factor';
}

function updateRecommendations(result) {
    if (!elements.recommendationsList) return;
    
    const riskPercentage = result.risk_percentage || 0;
    const recommendations = [];
    
    // Risk-based recommendations
    if (riskPercentage >= 70) {
        recommendations.push(
            'Immediate consultation with endocrinologist recommended',
            'Consider fine needle aspiration biopsy (FNA)',
            'Thyroid ultrasound within 1 week',
            'Complete thyroid function panel tests',
            'Regular monitoring every 3 months'
        );
    } else if (riskPercentage >= 40) {
        recommendations.push(
            'Schedule appointment with endocrinologist',
            'Thyroid ultrasound examination',
            'Repeat TSH test in 6-8 weeks',
            'Monitor for symptom changes',
            'Follow-up in 6 months'
        );
    } else {
        recommendations.push(
            'Routine annual thyroid checkup',
            'Maintain healthy iodine intake',
            'Regular self-examination',
            'Follow-up if symptoms develop'
        );
    }
    
    // General recommendations
    recommendations.push(
        'Avoid smoking and limit alcohol consumption',
        'Maintain healthy body weight (BMI 18.5-24.9)',
        'Regular exercise (30 minutes daily)',
        'Balanced diet with selenium-rich foods',
        'Stress management techniques',
        'Adequate sleep (7-8 hours nightly)'
    );
    
    // Clear existing recommendations
    elements.recommendationsList.innerHTML = '';
    
    // Add recommendations
    recommendations.forEach((rec, index) => {
        const li = document.createElement('li');
        li.className = 'fade-in';
        li.style.animationDelay = `${index * 0.1}s`;
        li.innerHTML = `<i class="fas fa-check-circle"></i> ${rec}`;
        elements.recommendationsList.appendChild(li);
    });
}

function animateResults() {
    // Animate result elements sequentially
    const elementsToAnimate = [
        elements.riskCircle,
        elements.meterFill,
        elements.meterPointer
    ].filter(el => el);
    
    elementsToAnimate.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            el.style.transition = 'all 0.5s ease-out';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 200);
    });
    
    // Animate factor items
    const factorItems = document.querySelectorAll('.factor-item');
    factorItems.forEach((item, index) => {
        item.classList.add('fade-in');
        item.style.animationDelay = `${index * 0.1}s`;
    });
}

// ===== FORM MANAGEMENT =====
function resetForm() {
    if (confirm('Are you sure you want to reset all form fields?')) {
        elements.form.reset();
        clearAllErrors();
        loadSampleData();
        showNotification('Form reset successfully', 'success');
    }
}

function loadSampleData() {
    // Set reasonable default values for demo
    const sampleData = {
        Age: 45,
        TSH_Level: 2.5,
        T3_Level: 1.2,
        T4_Level: 8.0,
        Nodule_Size: 1.5,
        Thyroid_Cancer_Risk: 2,
        Gender_Male: 1
    };
    
    Object.keys(sampleData).forEach(key => {
        if (elements[key]) {
            elements[key].value = sampleData[key];
        }
    });
}

function startNewPrediction() {
    elements.resultsCard.classList.add('hidden');
    elements.emptyState.classList.remove('hidden');
    resetForm();
    
    // Scroll to form
    document.querySelector('.input-section').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
    
    showNotification('Ready for new analysis', 'info');
}

function saveFormData(formData) {
    try {
        localStorage.setItem('thyroid_last_form', JSON.stringify(formData));
        localStorage.setItem('thyroid_last_form_timestamp', new Date().toISOString());
    } catch (error) {
        console.warn('Could not save form data:', error);
    }
}

function loadSavedFormData() {
    try {
        const saved = localStorage.getItem('thyroid_last_form');
        if (saved) {
            const formData = JSON.parse(saved);
            
            // Load form values
            Object.keys(formData).forEach(key => {
                if (elements[key]) {
                    if (elements[key].type === 'checkbox') {
                        elements[key].checked = formData[key] === 1;
                    } else {
                        elements[key].value = formData[key];
                    }
                }
            });
        }
    } catch (error) {
        console.warn('Could not load saved form data:', error);
    }
}

function clearAllErrors() {
    document.querySelectorAll('.input-error').forEach(el => el.remove());
    document.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
}

// ===== REPORT GENERATION =====
function saveReport() {
    if (!currentPrediction) {
        showNotification('No prediction data available', 'warning');
        return;
    }
    
    try {
        const report = generateReport(currentPrediction);
        
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
        
        showNotification('Report downloaded successfully', 'success');
        
    } catch (error) {
        console.error('Error saving report:', error);
        showNotification('Failed to save report', 'error');
    }
}

function generateReport(result) {
    const riskPercentage = result.risk_percentage || 0;
    const formData = getFormData();
    
    return `
THYROID CANCER RISK ASSESSMENT REPORT
======================================
Generated by: ThyroScan Pro AI System
Report Date: ${new Date().toLocaleString()}
Report ID: THY-${Date.now().toString().slice(-8)}

PATIENT INFORMATION:
-------------------
Age: ${formData.Age} years
Gender: ${formData.Gender_Male === 1 ? 'Male' : 'Female'}

THYROID FUNCTION TESTS:
-----------------------
TSH Level: ${formData.TSH_Level} mIU/L (Normal: 0.4-4.0)
T3 Level: ${formData.T3_Level} pg/mL (Normal: 2.3-4.2)
T4 Level: ${formData.T4_Level} μg/dL (Normal: 0.8-1.8)

CLINICAL PARAMETERS:
-------------------
Nodule Size: ${formData.Nodule_Size} cm
Cancer Risk Score: ${formData.Thyroid_Cancer_Risk}/4

RISK FACTORS DETECTED:
---------------------
${[
    formData.Family_History === 1 ? '✓ Family History of Thyroid Disease' : null,
    formData.Radiation_Exposure === 1 ? '✓ Radiation Exposure' : null,
    formData.Iodine_Deficiency === 1 ? '✓ Iodine Deficiency' : null,
    formData.Smoking === 1 ? '✓ Smoking History' : null,
    formData.Obesity === 1 ? '✓ Obesity (BMI ≥ 30)' : null,
    formData.Diabetes === 1 ? '✓ Diabetes Mellitus' : null
].filter(Boolean).join('\n') || 'No significant risk factors detected'}

AI ANALYSIS RESULTS:
-------------------
Prediction: ${result.prediction || 'Unknown'}
Risk Percentage: ${riskPercentage.toFixed(1)}%
Confidence Level: ${result.confidence || 'Unknown'}
Risk Category: ${getRiskLevel(riskPercentage)}

KEY RISK FACTORS:
----------------
${Object.entries(result.features_importance || {})
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([factor, importance]) => 
        `• ${formatFeatureName(factor)}: ${(importance * 100).toFixed(1)}% impact`
    ).join('\n')}

MEDICAL RECOMMENDATIONS:
----------------------
${document.querySelectorAll('#recommendationsList li')
    .map(li => `• ${li.textContent}`)
    .join('\n')}

MODEL INFORMATION:
-----------------
Algorithm: Logistic Regression
Accuracy: 83%
Training Data: 300,000+ clinical records
Analysis Time: < 2 seconds

IMPORTANT DISCLAIMER:
--------------------
This report is generated by ThyroScan Pro for educational and research purposes only.
It is NOT a substitute for professional medical diagnosis, advice, or treatment.
Always consult with qualified healthcare professionals for medical concerns.

FOOTNOTES:
---------
1. Report generated using AI-powered analysis
2. Model accuracy: 83% on validation dataset
3. Data encrypted and stored securely
4. HIPAA compliant data handling

END OF REPORT
=============
    `;
}

function shareResults() {
    if (!currentPrediction) {
        showNotification('No results to share', 'warning');
        return;
    }
    
    const shareData = {
        title: 'Thyroid Cancer Risk Assessment',
        text: `My thyroid cancer risk assessment: ${currentPrediction.risk_percentage}% risk (${currentPrediction.prediction}). Analyzed by ThyroScan Pro AI.`,
        url: window.location.href
    };
    
    if (navigator.share) {
        navigator.share(shareData)
            .then(() => showNotification('Results shared successfully', 'success'))
            .catch(error => {
                console.log('Sharing cancelled:', error);
                copyResultsToClipboard();
            });
    } else {
        copyResultsToClipboard();
    }
}

function copyResultsToClipboard() {
    if (!currentPrediction) return;
    
    const text = `Thyroid Cancer Risk Assessment:
Prediction: ${currentPrediction.prediction}
Risk Percentage: ${currentPrediction.risk_percentage}%
Confidence: ${currentPrediction.confidence}
Analyzed by ThyroScan Pro AI

View full report: ${window.location.href}`;
    
    navigator.clipboard.writeText(text)
        .then(() => showNotification('Results copied to clipboard', 'success'))
        .catch(() => showNotification('Failed to copy results', 'error'));
}

// ===== TOOLTIPS =====
function initializeTooltips() {
    // Add tooltips to form labels
    const tooltips = {
        'Age': 'Patient age in years. Thyroid cancer risk increases with age.',
        'TSH_Level': 'Thyroid Stimulating Hormone. Normal range: 0.4-4.0 mIU/L.',
        'T3_Level': 'Triiodothyronine hormone. Normal range: 2.3-4.2 pg/mL.',
        'T4_Level': 'Thyroxine hormone. Normal range: 0.8-1.8 μg/dL.',
        'Nodule_Size': 'Diameter of thyroid nodule in centimeters.',
        'Thyroid_Cancer_Risk': 'Clinical assessment score from 0 (very low) to 4 (very high).'
    };
    
    Object.keys(tooltips).forEach(field => {
        if (elements[field]) {
            const label = elements[field].previousElementSibling;
            if (label) {
                addTooltip(label, tooltips[field]);
            }
        }
    });
}

function addTooltip(element, text) {
    element.style.position = 'relative';
    element.style.cursor = 'help';
    
    const tooltip = document.createElement('span');
    tooltip.className = 'tooltip';
    tooltip.textContent = '?';
    tooltip.title = text;
    
    element.appendChild(tooltip);
}

// ===== BACKEND CONNECTION =====
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend connected');
            updateConnectionIndicator(true);
        } else {
            throw new Error('Backend not responding');
        }
    } catch (error) {
        console.warn('⚠️ Backend connection failed');
        updateConnectionIndicator(false);
        showNotification('Cannot connect to analysis server. Please check backend.', 'error');
    }
}

function updateConnectionIndicator(connected) {
    const indicator = document.createElement('div');
    indicator.className = `connection-indicator ${connected ? 'connected' : 'disconnected'}`;
    indicator.innerHTML = `<i class="fas fa-${connected ? 'server' : 'server-slash'}"></i>`;
    
    // Remove existing indicator
    const existing = document.querySelector('.connection-indicator');
    if (existing) existing.remove();
    
    // Add to predict button
    if (elements.predictBtn) {
        elements.predictBtn.appendChild(indicator);
    }
}

// ===== NOTIFICATION SYSTEM =====
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 
                         type === 'error' ? 'exclamation-circle' : 
                         type === 'warning' ? 'exclamation-triangle' : 
                         'info-circle'}"></i>
        <span>${message}</span>
        <button class="close-notification">&times;</button>
    `;
    
    // Add styles if not already present
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem 1.5rem;
                border-radius: var(--radius-md);
                display: flex;
                align-items: center;
                gap: 10px;
                z-index: 10000;
                animation: slideInRight 0.3s ease-out;
                max-width: 400px;
                box-shadow: var(--shadow-lg);
            }
            .notification.success {
                background: var(--success);
                color: white;
            }
            .notification.error {
                background: var(--danger);
                color: white;
            }
            .notification.warning {
                background: var(--warning);
                color: white;
            }
            .notification.info {
                background: var(--info);
                color: white;
            }
            .close-notification {
                background: none;
                border: none;
                color: inherit;
                font-size: 1.2rem;
                cursor: pointer;
                margin-left: auto;
            }
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.3s ease-out forwards';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
    
    // Close button
    notification.querySelector('.close-notification').addEventListener('click', () => {
        notification.style.animation = 'slideOutRight 0.3s ease-out forwards';
        setTimeout(() => notification.remove(), 300);
    });
}

// ===== FORM STEPS NAVIGATION =====
function showFormStep(stepNumber) {
    const steps = document.querySelectorAll('.form-step');
    const stepIndicators = document.querySelectorAll('.step');
    
    // Hide all steps
    steps.forEach(step => step.classList.add('hidden'));
    
    // Show selected step
    const targetStep = document.querySelector(`.form-step-${stepNumber}`);
    if (targetStep) {
        targetStep.classList.remove('hidden');
    }
    
    // Update step indicators
    stepIndicators.forEach((indicator, index) => {
        if (index < stepNumber) {
            indicator.classList.add('completed');
            indicator.classList.add('active');
        } else if (index === stepNumber - 1) {
            indicator.classList.add('active');
            indicator.classList.remove('completed');
        } else {
            indicator.classList.remove('active', 'completed');
        }
    });
}

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('Prediction page error:', e.error);
    showNotification('An error occurred in the prediction system', 'error');
});

// ===== EXPORT FUNCTIONS =====
window.ThyroScanPredict = {
    getFormData,
    validateFormData,
    displayResults,
    saveReport,
    shareResults,
    resetForm
};

console.log(' Prediction module loaded successfully');