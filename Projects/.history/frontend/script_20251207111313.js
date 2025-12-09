// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const thyroidForm = document.getElementById('thyroidForm');
const predictBtn = document.getElementById('predictBtn');
const resetBtn = document.getElementById('resetBtn');
const resultsCard = document.getElementById('resultsCard');
const closeResults = document.getElementById('closeResults');
const newPredictionBtn = document.getElementById('newPredictionBtn');
const saveReportBtn = document.getElementById('saveReportBtn');
const refreshHistory = document.getElementById('refreshHistory');
const historyLimit = document.getElementById('historyLimit');
const historyTableBody = document.getElementById('historyTableBody');
const historyEmpty = document.getElementById('historyEmpty');

// Chart Configuration
let riskChart = null;

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    // Load prediction history
    loadHistory();
    
    // Test backend connection
    testBackendConnection();
    
    // Set up event listeners
    setupEventListeners();
    
    // Set default values
    setDefaultValues();
});

// Test Backend Connection
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend connected successfully');
        } else {
            showError('Backend connection failed. Please ensure server is running.');
        }
    } catch (error) {
        console.error('Backend connection error:', error);
        showError('Cannot connect to backend server. Please start the server.');
    }
}

// Setup Event Listeners
function setupEventListeners() {
    // Form submission
    thyroidForm.addEventListener('submit', handlePrediction);
    
    // Reset form
    resetBtn.addEventListener('click', resetForm);
    
    // Close results
    closeResults.addEventListener('click', () => {
        resultsCard.classList.add('hidden');
    });
    
    // New prediction
    newPredictionBtn.addEventListener('click', () => {
        resultsCard.classList.add('hidden');
        thyroidForm.reset();
        setDefaultValues();
    });
    
    // Save report
    saveReportBtn.addEventListener('click', saveReport);
    
    // Refresh history
    refreshHistory.addEventListener('click', loadHistory);
    historyLimit.addEventListener('change', loadHistory);
    
    // Mobile menu
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        });
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update active nav link
                document.querySelectorAll('.nav-links a').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
            }
        });
    });
}

// Set Default Form Values
function setDefaultValues() {
    document.getElementById('Age').value = 45;
    document.getElementById('TSH_Level').value = 2.5;
    document.getElementById('T3_Level').value = 1.2;
    document.getElementById('T4_Level').value = 8.0;
    document.getElementById('Nodule_Size').value = 1.5;
    document.getElementById('Thyroid_Cancer_Risk').value = 2;
    document.getElementById('Gender_Male').value = 1;
    
    // Uncheck all checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.checked = false;
    });
}

// Handle Prediction Form Submission
async function handlePrediction(e) {
    e.preventDefault();
    
    // Show loading
    predictBtn.disabled = true;
    document.getElementById('loadingSpinner').classList.remove('hidden');
    
    try {
        // Get form data
        const formData = getFormData();
        
        // Validate form data
        if (!validateFormData(formData)) {
            return;
        }
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Display results
        displayResults(result);
        
        // Reload history
        loadHistory();
        
    } catch (error) {
        console.error('Prediction error:', error);
        showError('Failed to get prediction. Please check backend connection.');
    } finally {
        // Hide loading
        predictBtn.disabled = false;
        document.getElementById('loadingSpinner').classList.add('hidden');
    }
}

// Get Form Data
function getFormData() {
    const formData = {
        Age: parseFloat(document.getElementById('Age').value),
        Family_History: document.getElementById('Family_History').checked ? 1 : 0,
        Radiation_Exposure: document.getElementById('Radiation_Exposure').checked ? 1 : 0,
        Iodine_Deficiency: document.getElementById('Iodine_Deficiency').checked ? 1 : 0,
        Smoking: document.getElementById('Smoking').checked ? 1 : 0,
        Obesity: document.getElementById('Obesity').checked ? 1 : 0,
        Diabetes: document.getElementById('Diabetes').checked ? 1 : 0,
        TSH_Level: parseFloat(document.getElementById('TSH_Level').value),
        T3_Level: parseFloat(document.getElementById('T3_Level').value),
        T4_Level: parseFloat(document.getElementById('T4_Level').value),
        Nodule_Size: parseFloat(document.getElementById('Nodule_Size').value),
        Thyroid_Cancer_Risk: parseInt(document.getElementById('Thyroid_Cancer_Risk').value),
        Gender_Male: parseInt(document.getElementById('Gender_Male').value)
    };
    
    return formData;
}

// Validate Form Data
function validateFormData(formData) {
    const errors = [];
    
    // Validate Age
    if (formData.Age < 0 || formData.Age > 120) {
        errors.push('Age must be between 0 and 120 years');
    }
    
    // Validate TSH Level
    if (formData.TSH_Level < 0 || formData.TSH_Level > 100) {
        errors.push('TSH Level must be between 0 and 100 mIU/L');
    }
    
    // Validate T3 Level
    if (formData.T3_Level < 0 || formData.T3_Level > 20) {
        errors.push('T3 Level must be between 0 and 20 pg/mL');
    }
    
    // Validate T4 Level
    if (formData.T4_Level < 0 || formData.T4_Level > 30) {
        errors.push('T4 Level must be between 0 and 30 μg/dL');
    }
    
    // Validate Nodule Size
    if (formData.Nodule_Size < 0 || formData.Nodule_Size > 10) {
        errors.push('Nodule Size must be between 0 and 10 cm');
    }
    
    // Validate Cancer Risk Score
    if (formData.Thyroid_Cancer_Risk < 0 || formData.Thyroid_Cancer_Risk > 4) {
        errors.push('Cancer Risk Score must be between 0 and 4');
    }
    
    if (errors.length > 0) {
        showError(errors.join('<br>'));
        return false;
    }
    
    return true;
}

// Display Results
function displayResults(result) {
    // Update risk percentage
    const riskPercentage = result.risk_percentage;
    document.getElementById('riskPercentage').textContent = `${riskPercentage}%`;
    document.getElementById('predictionText').textContent = result.prediction;
    document.getElementById('confidenceText').textContent = `Confidence: ${result.confidence}`;
    
    // Update risk circle color
    const riskCircle = document.getElementById('riskCircle');
    riskCircle.style.background = getRiskGradient(riskPercentage);
    
    // Update meter fill
    const meterFill = document.getElementById('meterFill');
    meterFill.style.width = `${riskPercentage}%`;
    
    // Display chart
    if (result.chart_data) {
        const chartData = JSON.parse(result.chart_data);
        Plotly.newPlot('chartContainer', chartData.data, chartData.layout);
    }
    
    // Display key factors
    displayKeyFactors(result.features_importance);
    
    // Display recommendations
    displayRecommendations(result);
    
    // Show results card
    resultsCard.classList.remove('hidden');
    resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Get Risk Gradient Color
function getRiskGradient(percentage) {
    if (percentage < 30) {
        return 'conic-gradient(#10b981 0%, #10b981 100%)';
    } else if (percentage < 70) {
        return `conic-gradient(#10b981 0%, #10b981 30%, #f59e0b 30%, #f59e0b 100%)`;
    } else {
        return `conic-gradient(#10b981 0%, #10b981 30%, #f59e0b 30%, #f59e0b 70%, #ef4444 70%)`;
    }
}

// Display Key Factors
function displayKeyFactors(factors) {
    const factorsList = document.getElementById('factorsList');
    factorsList.innerHTML = '';
    
    Object.entries(factors).forEach(([factor, importance]) => {
        const factorDiv = document.createElement('div');
        factorDiv.className = 'factor-item';
        factorDiv.innerHTML = `
            <div class="factor-name">${formatFeatureName(factor)}</div>
            <div class="factor-value">Impact: ${(importance * 100).toFixed(1)}%</div>
        `;
        factorsList.appendChild(factorDiv);
    });
}

// Format Feature Name
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
    
    return names[feature] || feature;
}

// Display Recommendations
function displayRecommendations(result) {
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';
    
    const recommendations = [];
    
    // Risk-based recommendations
    if (result.risk_percentage >= 70) {
        recommendations.push(
            'Consult an endocrinologist immediately',
            'Consider fine needle aspiration biopsy',
            'Regular monitoring every 3 months',
            'Complete thyroid function tests'
        );
    } else if (result.risk_percentage >= 40) {
        recommendations.push(
            'Schedule appointment with endocrinologist',
            'Ultrasound examination recommended',
            'Monitor thyroid levels every 6 months',
            'Maintain healthy iodine intake'
        );
    } else {
        recommendations.push(
            'Regular annual checkup recommended',
            'Maintain healthy lifestyle',
            'Monitor for any symptom changes',
            'Balanced diet with proper iodine'
        );
    }
    
    // Add general recommendations
    recommendations.push(
        'Avoid smoking and alcohol consumption',
        'Maintain healthy BMI',
        'Regular exercise (30 mins daily)',
        'Stress management techniques'
    );
    
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsList.appendChild(li);
    });
}

// Load Prediction History
async function loadHistory() {
    try {
        const limit = historyLimit.value;
        const response = await fetch(`${API_BASE_URL}/history?limit=${limit}`);
        
        if (!response.ok) {
            throw new Error('Failed to load history');
        }
        
        const data = await response.json();
        updateHistoryTable(data.history);
        
    } catch (error) {
        console.error('Error loading history:', error);
        showError('Failed to load prediction history');
    }
}

// Update History Table
function updateHistoryTable(history) {
    historyTableBody.innerHTML = '';
    
    if (!history || history.length === 0) {
        historyEmpty.classList.remove('hidden');
        return;
    }
    
    historyEmpty.classList.add('hidden');
    
    history.forEach((record, index) => {
        const row = document.createElement('tr');
        row.className = 'fade-in';
        row.style.animationDelay = `${index * 0.1}s`;
        
        const riskClass = record.risk_percentage >= 70 ? 'high-risk' : 
                         record.risk_percentage >= 40 ? 'medium-risk' : 'low-risk';
        
        row.innerHTML = `
            <td>${record.timestamp || 'N/A'}</td>
            <td>${record.user_data?.Age || 'N/A'}</td>
            <td>${record.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</td>
            <td>
                <span class="risk-badge ${riskClass}">
                    ${record.risk_percentage}%
                </span>
            </td>
            <td>
                <span class="prediction-badge ${record.prediction === 'Malignant' ? 'malignant' : 'benign'}">
                    ${record.prediction}
                </span>
            </td>
            <td>
                <button class="view-details-btn" data-index="${index}">
                    <i class="fas fa-eye"></i> View
                </button>
            </td>
        `;
        
        historyTableBody.appendChild(row);
    });
    
    // Add event listeners to view buttons
    document.querySelectorAll('.view-details-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const index = this.getAttribute('data-index');
            viewHistoryDetails(history[index]);
        });
    });
}

// View History Details
function viewHistoryDetails(record) {
    // Create modal with details
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-info-circle"></i> Prediction Details</h3>
                <button class="close-modal">&times;</button>
            </div>
            <div class="modal-body">
                <div class="detail-item">
                    <strong>Date:</strong> ${record.timestamp}
                </div>
                <div class="detail-item">
                    <strong>Prediction:</strong> 
                    <span class="prediction-badge ${record.prediction === 'Malignant' ? 'malignant' : 'benign'}">
                        ${record.prediction}
                    </span>
                </div>
                <div class="detail-item">
                    <strong>Risk Percentage:</strong> ${record.risk_percentage}%
                </div>
                <div class="detail-item">
                    <strong>Clinical Parameters:</strong>
                    <div class="parameters-grid">
                        ${Object.entries(record.user_data || {}).map(([key, value]) => `
                            <div class="parameter">
                                <span class="param-key">${formatFeatureName(key)}:</span>
                                <span class="param-value">${value}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-secondary close-modal">Close</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add modal styles
    const style = document.createElement('style');
    style.textContent = `
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        }
        .modal-content {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #e5e7eb;
        }
        .close-modal {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #6b7280;
        }
        .detail-item {
            margin-bottom: 1rem;
        }
        .parameters-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 0.5rem;
        }
        .parameter {
            background: #f9fafb;
            padding: 0.5rem 1rem;
            border-radius: 6px;
        }
        .param-key {
            font-weight: 600;
            color: #374151;
        }
        .param-value {
            color: #6b7280;
            float: right;
        }
        .modal-footer {
            margin-top: 2rem;
            text-align: right;
        }
    `;
    document.head.appendChild(style);
    
    // Close modal event listeners
    modal.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', () => {
            document.body.removeChild(modal);
            document.head.removeChild(style);
        });
    });
}

// Save Report
function saveReport() {
    const riskPercentage = document.getElementById('riskPercentage').textContent;
    const prediction = document.getElementById('predictionText').textContent;
    
    const report = `
THYROID CANCER RISK ASSESSMENT REPORT
======================================
Date: ${new Date().toLocaleString()}
Prediction: ${prediction}
Risk Percentage: ${riskPercentage}
Confidence Level: ${document.getElementById('confidenceText').textContent}

CLINICAL PARAMETERS:
-------------------
Age: ${document.getElementById('Age').value} years
TSH Level: ${document.getElementById('TSH_Level').value} mIU/L
T3 Level: ${document.getElementById('T3_Level').value} pg/mL
T4 Level: ${document.getElementById('T4_Level').value} μg/dL
Nodule Size: ${document.getElementById('Nodule_Size').value} cm
Cancer Risk Score: ${document.getElementById('Thyroid_Cancer_Risk').value}
Gender: ${document.getElementById('Gender_Male').value === '1' ? 'Male' : 'Female'}

RISK FACTORS:
-------------
${Array.from(document.querySelectorAll('input[type="checkbox"]'))
    .filter(cb => cb.checked)
    .map(cb => `✓ ${cb.nextElementSibling.textContent}`)
    .join('\n') || 'No significant risk factors detected'}

RECOMMENDATIONS:
---------------
${Array.from(document.querySelectorAll('#recommendationsList li'))
    .map(li => `• ${li.textContent}`)
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
    
    showSuccess('Report downloaded successfully!');
}

// Reset Form
function resetForm() {
    thyroidForm.reset();
    setDefaultValues();
    showSuccess('Form reset successfully');
}

// Show Success Message
function showSuccess(message) {
    showNotification(message, 'success');
}

// Show Error Message
function showError(message) {
    showNotification(message, 'error');
}

// Show Notification
function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
        <button class="close-notification">&times;</button>
    `;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
            max-width: 400px;
        }
        .notification.success {
            background: #10b981;
            color: white;
        }
        .notification.error {
            background: #ef4444;
            color: white;
        }
        .notification.info {
            background: #3b82f6;
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
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
            document.head.removeChild(style);
        }
    }, 5000);
    
    // Close button
    notification.querySelector('.close-notification').addEventListener('click', () => {
        notification.remove();
        document.head.removeChild(style);
    });
}

// Add CSS classes for history badges
const badgeStyles = document.createElement('style');
badgeStyles.textContent = `
    .risk-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .risk-badge.high-risk {
        background: #fee2e2;
        color: #dc2626;
    }
    .risk-badge.medium-risk {
        background: #fef3c7;
        color: #d97706;
    }
    .risk-badge.low-risk {
        background: #d1fae5;
        color: #059669;
    }
    .prediction-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .prediction-badge.malignant {
        background: #fee2e2;
        color: #dc2626;
    }
    .prediction-badge.benign {
        background: #d1fae5;
        color: #059669;
    }
    .view-details-btn {
        background: var(--primary);
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 6px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 0.9rem;
        transition: var(--transition);
    }
    .view-details-btn:hover {
        background: var(--primary-dark);
    }
`;
document.head.appendChild(badgeStyles);