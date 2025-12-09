// ============================================
// THYROSCAN AI - PROFESSIONAL MEDICAL JS
// Enhanced UI/UX with Beautiful Animations
// ============================================

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Global State
let heroSlider = null;
let riskChart = null;
let currentHistory = [];
let currentPage = 1;
let itemsPerPage = 10;
let isAnalyzing = false;

// DOM Elements
const elements = {
    // Loading
    loadingScreen: document.getElementById('loadingScreen'),
    
    // Navigation
    mobileToggle: document.getElementById('mobileToggle'),
    mobileNav: document.getElementById('mobileNav'),
    mobileClose: document.getElementById('mobileClose'),
    alertClose: document.querySelector('.alert-close'),
    
    // Form
    thyroidForm: document.getElementById('thyroidForm'),
    predictBtn: document.getElementById('predictBtn'),
    resetBtn: document.getElementById('resetBtn'),
    
    // Results
    resultsCard: document.getElementById('resultsCard'),
    quickGuide: document.getElementById('quickGuide'),
    closeResults: document.getElementById('closeResults'),
    newPredictionBtn: document.getElementById('newPredictionBtn'),
    saveReportBtn: document.getElementById('saveReportBtn'),
    
    // History
    refreshHistory: document.getElementById('refreshHistory'),
    historyLimit: document.getElementById('historyLimit'),
    historySearch: document.getElementById('historySearch'),
    historyTableBody: document.getElementById('historyTableBody'),
    historyEmpty: document.getElementById('historyEmpty'),
    historyCount: document.getElementById('historyCount'),
    
    // Chart
    chartContainer: document.getElementById('chartContainer'),
    
    // Risk Elements
    riskPercentage: document.getElementById('riskPercentage'),
    riskCircle: document.querySelector('.circle'),
    predictionText: document.getElementById('predictionText'),
    confidenceText: document.getElementById('confidenceText'),
    meterFill: document.getElementById('meterFill'),
    meterPointer: document.getElementById('meterPointer'),
    
    // Factors & Recommendations
    factorsList: document.getElementById('factorsList'),
    recommendationsList: document.getElementById('recommendationsList')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 ThyroScan AI - Initializing Professional Medical System...');
    
    initializeApp();
    initializeSwiper();
    initializeAOS();
    setupEventListeners();
    setupFormInteractions();
    setDefaultValues();
    
    // Simulate loading for better UX
    setTimeout(() => {
        hideLoadingScreen();
        showWelcomeNotification();
        testBackendConnection();
        loadHistory();
    }, 1500);
});

// ========== INITIALIZATION FUNCTIONS ==========

function initializeApp() {
    // Add CSS animations dynamically
    addCustomAnimations();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Setup smooth scrolling
    setupSmoothScrolling();
    
    // Setup intersection observers
    setupObservers();
}

function initializeSwiper() {
    heroSlider = new Swiper('.hero-slider', {
        direction: 'horizontal',
        loop: true,
        speed: 800,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        effect: 'fade',
        fadeEffect: {
            crossFade: true
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
            dynamicBullets: true,
            renderBullet: function (index, className) {
                return `<span class="${className}"><div class="bullet-inner"></div></span>`;
            }
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        on: {
            init: function () {
                console.log('🎬 Professional Image Slider Initialized');
                animateSliderElements();
            }
        }
    });
}

function initializeAOS() {
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true,
        mirror: false,
        offset: 100
    });
}

function hideLoadingScreen() {
    if (elements.loadingScreen) {
        elements.loadingScreen.classList.add('fade-out');
        setTimeout(() => {
            elements.loadingScreen.style.display = 'none';
        }, 500);
    }
}

function showWelcomeNotification() {
    createNotification({
        title: 'Welcome to ThyroScan AI',
        message: 'Professional Thyroid Risk Assessment System',
        type: 'info',
        duration: 4000,
        icon: 'heartbeat'
    });
}

// ========== ANIMATION FUNCTIONS ==========

function addCustomAnimations() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes pulseSoft {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        @keyframes slideInFromBottom {
            from { transform: translateY(100px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .float-animation {
            animation: float 3s ease-in-out infinite;
        }
        
        .pulse-soft {
            animation: pulseSoft 2s ease-in-out infinite;
        }
        
        .gradient-shift {
            background-size: 200% 200%;
            animation: gradientShift 3s ease infinite;
        }
        
        .slide-in-bottom {
            animation: slideInFromBottom 0.6s ease-out;
        }
    `;
    document.head.appendChild(style);
}

function animateSliderElements() {
    // Animate slider elements
    const slides = document.querySelectorAll('.swiper-slide');
    slides.forEach((slide, index) => {
        slide.style.opacity = '0';
        slide.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            slide.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            slide.style.opacity = '1';
            slide.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// ========== EVENT LISTENERS SETUP ==========

function setupEventListeners() {
    // Navigation
    elements.mobileToggle?.addEventListener('click', toggleMobileNav);
    elements.mobileClose?.addEventListener('click', closeMobileNav);
    elements.alertClose?.addEventListener('click', closeAlertBar);
    
    // Form
    elements.thyroidForm?.addEventListener('submit', handlePrediction);
    elements.resetBtn?.addEventListener('click', resetForm);
    
    // Results
    elements.closeResults?.addEventListener('click', closeResultsCard);
    elements.newPredictionBtn?.addEventListener('click', startNewPrediction);
    elements.saveReportBtn?.addEventListener('click', saveReport);
    
    // History
    elements.refreshHistory?.addEventListener('click', () => {
        loadHistory();
        createNotification({
            title: 'History Refreshed',
            message: 'Latest predictions loaded',
            type: 'success'
        });
    });
    
    elements.historyLimit?.addEventListener('change', loadHistory);
    elements.historySearch?.addEventListener('input', debounce(searchHistory, 300));
    
    // Navigation links
    setupNavigationLinks();
    
    // Window events
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', handleResize);
}

function setupFormInteractions() {
    // Age slider sync
    const ageSlider = document.querySelector('.form-slider');
    const ageInput = document.getElementById('Age');
    
    if (ageSlider && ageInput) {
        ageSlider.addEventListener('input', function() {
            ageInput.value = this.value;
            animateInputChange(ageInput);
        });
        
        ageInput.addEventListener('input', function() {
            ageSlider.value = this.value;
        });
    }
    
    // Gender selector
    document.querySelectorAll('.gender-option').forEach(option => {
        option.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            
            // Update UI
            document.querySelectorAll('.gender-option').forEach(opt => {
                opt.classList.remove('active');
                opt.style.transform = 'scale(1)';
            });
            
            this.classList.add('active');
            this.style.transform = 'scale(1.05)';
            
            // Update hidden select
            const genderSelect = document.getElementById('Gender_Male');
            if (genderSelect) {
                genderSelect.value = value;
                genderSelect.dispatchEvent(new Event('change'));
            }
            
            // Animation
            animateElement(this, 'bounce');
        });
    });
    
    // Risk score visual
    const riskSelect = document.getElementById('Thyroid_Cancer_Risk');
    const riskSegments = document.querySelectorAll('.risk-segment');
    
    if (riskSelect) {
        riskSelect.addEventListener('change', function() {
            const value = parseInt(this.value);
            
            // Update segments
            riskSegments.forEach((segment, index) => {
                segment.classList.remove('active');
                if (index <= value) {
                    segment.classList.add('active');
                }
            });
            
            // Animate change
            animateElement(this, 'pulse');
        });
    }
    
    // Checkbox animations
    document.querySelectorAll('.risk-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (this.checked) {
                animateElement(label, 'bounce');
                label.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    label.style.transform = 'scale(1)';
                }, 150);
            }
        });
    });
}

function setupNavigationLinks() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Close mobile nav if open
                closeMobileNav();
                
                // Update active state
                updateActiveNavLink(this);
                
                // Smooth scroll
                smoothScrollTo(targetElement);
            }
        });
    });
}

function setupSmoothScrolling() {
    // Add smooth scroll behavior to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function setupObservers() {
    // Intersection Observer for animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-visible');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observe elements for animation
    document.querySelectorAll('.feature-item, .about-card, .tech-item').forEach(el => {
        observer.observe(el);
    });
}

function initializeTooltips() {
    // Add tooltips to form inputs
    document.querySelectorAll('.input-hint').forEach(hint => {
        const input = hint.previousElementSibling?.querySelector('input');
        if (input) {
            input.addEventListener('focus', () => {
                hint.style.opacity = '1';
                hint.style.transform = 'translateY(0)';
            });
            
            input.addEventListener('blur', () => {
                hint.style.opacity = '0';
                hint.style.transform = 'translateY(-5px)';
            });
        }
    });
}

// ========== FORM HANDLING ==========

function setDefaultValues() {
    // Set default values
    const defaults = {
        'Age': 45,
        'TSH_Level': 2.5,
        'T3_Level': 1.2,
        'T4_Level': 8.0,
        'Nodule_Size': 1.5,
        'Thyroid_Cancer_Risk': 2,
        'Gender_Male': 1
    };
    
    Object.entries(defaults).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            element.value = value;
            
            // Trigger change event for visual updates
            if (element.tagName === 'SELECT') {
                element.dispatchEvent(new Event('change'));
            }
        }
    });
    
    // Update age slider
    const ageSlider = document.querySelector('.form-slider');
    if (ageSlider) {
        ageSlider.value = defaults.Age;
    }
    
    // Uncheck all checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.checked = false;
    });
    
    console.log('✅ Default values set');
}

async function handlePrediction(e) {
    e.preventDefault();
    
    if (isAnalyzing) return;
    
    // Get form data
    const formData = getFormData();
    
    // Validate
    if (!validateFormData(formData)) {
        return;
    }
    
    // Start analysis
    startAnalysis();
    
    try {
        // Simulate API delay for better UX
        await new Promise(resolve => setTimeout(resolve, 800));
        
        // Make API call
        const result = await makePredictionAPI(formData);
        
        // Display results
        await displayResults(result);
        
        // Load updated history
        loadHistory();
        
        // Show success notification
        createNotification({
            title: 'Analysis Complete',
            message: 'Thyroid risk assessment generated successfully',
            type: 'success',
            duration: 3000
        });
        
    } catch (error) {
        console.error('Prediction error:', error);
        
        // Show error or demo data
        if (error.message.includes('Failed to fetch')) {
            createNotification({
                title: 'Demo Mode',
                message: 'Using demo data (backend unavailable)',
                type: 'warning',
                duration: 4000
            });
            
            // Display demo results
            const demoResult = generateDemoResult(formData);
            await displayResults(demoResult);
        } else {
            createNotification({
                title: 'Analysis Failed',
                message: 'Please try again or check your connection',
                type: 'error',
                duration: 4000
            });
        }
    } finally {
        endAnalysis();
    }
}

function getFormData() {
    const formData = {
        Age: parseFloat(document.getElementById('Age').value),
        Family_History: document.getElementById('Family_History')?.checked ? 1 : 0,
        Radiation_Exposure: document.getElementById('Radiation_Exposure')?.checked ? 1 : 0,
        Iodine_Deficiency: document.getElementById('Iodine_Deficiency')?.checked ? 1 : 0,
        Smoking: document.getElementById('Smoking')?.checked ? 1 : 0,
        Obesity: document.getElementById('Obesity')?.checked ? 1 : 0,
        Diabetes: document.getElementById('Diabetes')?.checked ? 1 : 0,
        TSH_Level: parseFloat(document.getElementById('TSH_Level').value),
        T3_Level: parseFloat(document.getElementById('T3_Level').value),
        T4_Level: parseFloat(document.getElementById('T4_Level').value),
        Nodule_Size: parseFloat(document.getElementById('Nodule_Size').value),
        Thyroid_Cancer_Risk: parseInt(document.getElementById('Thyroid_Cancer_Risk').value),
        Gender_Male: parseInt(document.getElementById('Gender_Male').value)
    };
    
    return formData;
}

function validateFormData(formData) {
    const errors = [];
    
    // Age validation
    if (isNaN(formData.Age) || formData.Age < 0 || formData.Age > 120) {
        highlightInvalidInput('Age', 'Age must be between 0-120 years');
        errors.push('Invalid age');
    }
    
    // TSH validation
    if (isNaN(formData.TSH_Level) || formData.TSH_Level < 0 || formData.TSH_Level > 100) {
        highlightInvalidInput('TSH_Level', 'TSH must be between 0-100 mIU/L');
        errors.push('Invalid TSH level');
    }
    
    // T3 validation
    if (isNaN(formData.T3_Level) || formData.T3_Level < 0 || formData.T3_Level > 20) {
        highlightInvalidInput('T3_Level', 'T3 must be between 0-20 pg/mL');
        errors.push('Invalid T3 level');
    }
    
    // T4 validation
    if (isNaN(formData.T4_Level) || formData.T4_Level < 0 || formData.T4_Level > 30) {
        highlightInvalidInput('T4_Level', 'T4 must be between 0-30 μg/dL');
        errors.push('Invalid T4 level');
    }
    
    // Nodule size validation
    if (isNaN(formData.Nodule_Size) || formData.Nodule_Size < 0 || formData.Nodule_Size > 10) {
        highlightInvalidInput('Nodule_Size', 'Nodule size must be between 0-10 cm');
        errors.push('Invalid nodule size');
    }
    
    if (errors.length > 0) {
        createNotification({
            title: 'Validation Error',
            message: errors.join(', '),
            type: 'error',
            duration: 4000
        });
        return false;
    }
    
    return true;
}

function highlightInvalidInput(inputId, message) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    // Add error class
    input.classList.add('input-error');
    
    // Create error message
    let errorElement = input.parentNode.querySelector('.error-message');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        input.parentNode.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    errorElement.style.opacity = '0';
    errorElement.style.transform = 'translateY(-10px)';
    
    // Animate in
    setTimeout(() => {
        errorElement.style.transition = 'opacity 0.3s, transform 0.3s';
        errorElement.style.opacity = '1';
        errorElement.style.transform = 'translateY(0)';
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        input.classList.remove('input-error');
        errorElement.style.opacity = '0';
        errorElement.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            if (errorElement.parentNode) {
                errorElement.parentNode.removeChild(errorElement);
            }
        }, 300);
    }, 3000);
}

async function makePredictionAPI(formData) {
    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.warn('API call failed, using demo data:', error);
        throw error;
    }
}

function generateDemoResult(formData) {
    // Calculate demo risk based on form data
    let baseRisk = 30;
    
    // Age factor
    if (formData.Age > 50) baseRisk += 15;
    if (formData.Age > 65) baseRisk += 10;
    
    // TSH factor
    if (formData.TSH_Level > 4) baseRisk += 10;
    if (formData.TSH_Level > 10) baseRisk += 15;
    
    // Nodule size factor
    if (formData.Nodule_Size > 2) baseRisk += 10;
    if (formData.Nodule_Size > 4) baseRisk += 15;
    
    // Risk score factor
    baseRisk += formData.Thyroid_Cancer_Risk * 10;
    
    // Checkbox factors
    if (formData.Family_History) baseRisk += 5;
    if (formData.Radiation_Exposure) baseRisk += 15;
    if (formData.Smoking) baseRisk += 5;
    
    // Cap at 95%
    const riskPercentage = Math.min(baseRisk, 95);
    
    // Generate prediction
    const prediction = riskPercentage >= 70 ? 'Malignant' : 
                      riskPercentage >= 40 ? 'Suspicious' : 'Benign';
    
    // Generate confidence
    const confidence = Math.min(riskPercentage + 5, 98).toFixed(1) + '%';
    
    // Generate feature importance
    const features = {
        'Age': Math.random() * 0.3 + 0.2,
        'TSH_Level': Math.random() * 0.25 + 0.15,
        'Nodule_Size': Math.random() * 0.2 + 0.1,
        'Thyroid_Cancer_Risk': Math.random() * 0.15 + 0.1,
        'Radiation_Exposure': formData.Radiation_Exposure ? 0.15 : 0,
        'Family_History': formData.Family_History ? 0.1 : 0,
        'T4_Level': Math.random() * 0.1 + 0.05,
        'T3_Level': Math.random() * 0.08 + 0.04,
        'Gender_Male': Math.random() * 0.05 + 0.02
    };
    
    // Normalize to sum to 1
    const total = Object.values(features).reduce((a, b) => a + b, 0);
    Object.keys(features).forEach(key => {
        features[key] = features[key] / total;
    });
    
    return {
        prediction,
        risk_percentage: riskPercentage,
        confidence,
        features_importance: features,
        chart_data: JSON.stringify(generateDemoChartData(features))
    };
}

function generateDemoChartData(features) {
    const sortedFeatures = Object.entries(features)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 8);
    
    return {
        data: [{
            x: sortedFeatures.map(([key]) => formatFeatureName(key)),
            y: sortedFeatures.map(([,value]) => (value * 100).toFixed(1)),
            type: 'bar',
            marker: {
                color: sortedFeatures.map((_, i) => 
                    `rgba(59, 130, 246, ${0.7 + i * 0.05})`
                ),
                line: {
                    color: 'rgba(0,0,0,0.1)',
                    width: 1
                }
            },
            text: sortedFeatures.map(([,value]) => `${(value * 100).toFixed(1)}%`),
            textposition: 'auto',
            hoverinfo: 'x+text'
        }],
        layout: {
            title: 'Feature Importance Analysis',
            xaxis: {
                title: 'Clinical Parameters',
                tickangle: -45,
                gridcolor: 'rgba(0,0,0,0.05)'
            },
            yaxis: {
                title: 'Importance (%)',
                gridcolor: 'rgba(0,0,0,0.05)'
            },
            paper_bgcolor: 'transparent',
            plot_bgcolor: 'transparent',
            font: {
                family: 'Poppins, sans-serif'
            },
            margin: { t: 40, r: 20, b: 80, l: 60 }
        }
    };
}

// ========== RESULTS DISPLAY ==========

async function displayResults(result) {
    // Hide quick guide
    if (elements.quickGuide) {
        animateElement(elements.quickGuide, 'fadeOut', () => {
            elements.quickGuide.style.display = 'none';
        });
    }
    
    // Update risk percentage with animation
    await animateRiskPercentage(result.risk_percentage);
    
    // Update other elements
    updatePredictionText(result);
    updateRiskMeter(result.risk_percentage);
    
    // Display chart
    renderChart(result);
    
    // Display key factors
    displayKeyFactors(result.features_importance);
    
    // Display recommendations
    displayRecommendations(result);
    
    // Show results card
    showResultsCard();
    
    // Scroll to results
    setTimeout(() => {
        elements.resultsCard.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }, 500);
}

async function animateRiskPercentage(targetPercentage) {
    return new Promise(resolve => {
        let current = 0;
        const increment = targetPercentage / 50; // 50 steps
        const duration = 1000; // 1 second
        const stepTime = duration / 50;
        
        const animate = () => {
            current += increment;
            if (current >= targetPercentage) {
                current = targetPercentage;
                clearInterval(timer);
                resolve();
            }
            
            // Update percentage text
            if (elements.riskPercentage) {
                elements.riskPercentage.textContent = `${Math.round(current)}%`;
            }
            
            // Update circle stroke
            if (elements.riskCircle) {
                const circumference = 2 * Math.PI * 15.9155;
                const offset = circumference - (current / 100) * circumference;
                elements.riskCircle.style.strokeDasharray = `${circumference} ${circumference}`;
                elements.riskCircle.style.strokeDashoffset = offset;
                
                // Update color based on percentage
                if (current < 30) {
                    elements.riskCircle.style.stroke = '#10b981';
                } else if (current < 70) {
                    elements.riskCircle.style.stroke = '#f59e0b';
                } else {
                    elements.riskCircle.style.stroke = '#ef4444';
                }
            }
        };
        
        const timer = setInterval(animate, stepTime);
    });
}

function updatePredictionText(result) {
    if (elements.predictionText) {
        elements.predictionText.textContent = result.prediction;
        
        // Add color based on prediction
        if (result.prediction === 'Malignant') {
            elements.predictionText.style.color = '#ef4444';
        } else if (result.prediction === 'Suspicious') {
            elements.predictionText.style.color = '#f59e0b';
        } else {
            elements.predictionText.style.color = '#10b981';
        }
    }
    
    if (elements.confidenceText) {
        elements.confidenceText.textContent = `Confidence: ${result.confidence}`;
    }
}

function updateRiskMeter(percentage) {
    if (!elements.meterFill || !elements.meterPointer) return;
    
    // Animate meter fill
    elements.meterFill.style.width = `${percentage}%`;
    
    // Animate pointer after a delay
    setTimeout(() => {
        elements.meterPointer.style.left = `${percentage}%`;
        
        // Add bounce animation
        elements.meterPointer.style.animation = 'none';
        setTimeout(() => {
            elements.meterPointer.style.animation = 'bounce 0.5s ease';
        }, 10);
    }, 800);
}

function renderChart(result) {
    // Clear previous chart
    if (riskChart) {
        Plotly.purge(elements.chartContainer);
    }
    
    try {
        let chartData;
        if (result.chart_data) {
            chartData = JSON.parse(result.chart_data);
        } else {
            chartData = generateDemoChartData(result.features_importance || {});
        }
        
        // Enhance chart appearance
        chartData.layout = {
            ...chartData.layout,
            hovermode: 'closest',
            showlegend: false,
            xaxis: {
                ...chartData.layout.xaxis,
                automargin: true
            },
            yaxis: {
                ...chartData.layout.yaxis,
                automargin: true
            }
        };
        
        // Create chart with animation
        Plotly.newPlot(elements.chartContainer, chartData.data, chartData.layout, {
            displayModeBar: true,
            displaylogo: false,
            responsive: true,
            modeBarButtonsToRemove: ['sendDataToCloud', 'autoScale2d', 'resetScale2d'],
            modeBarButtonsToAdd: [{
                name: 'Download',
                icon: Plotly.Icons.camera,
                click: function(gd) {
                    Plotly.downloadImage(gd, {
                        format: 'png',
                        filename: 'thyroid-risk-analysis'
                    });
                }
            }]
        }).then(graphDiv => {
            riskChart = graphDiv;
            
            // Add animation to chart bars
            setTimeout(() => {
                const bars = document.querySelectorAll('.barlayer .trace');
                bars.forEach((bar, index) => {
                    bar.style.opacity = '0';
                    bar.style.transform = 'translateY(20px)';
                    
                    setTimeout(() => {
                        bar.style.transition = 'opacity 0.5s, transform 0.5s';
                        bar.style.opacity = '1';
                        bar.style.transform = 'translateY(0)';
                    }, index * 100);
                });
            }, 500);
        });
    } catch (error) {
        console.error('Chart rendering error:', error);
        elements.chartContainer.innerHTML = `
            <div class="chart-error">
                <i class="fas fa-chart-line"></i>
                <p>Chart data unavailable</p>
            </div>
        `;
    }
}

function displayKeyFactors(factors) {
    if (!elements.factorsList) return;
    
    elements.factorsList.innerHTML = '';
    
    if (!factors || Object.keys(factors).length === 0) {
        elements.factorsList.innerHTML = `
            <div class="no-factors">
                <i class="fas fa-info-circle"></i>
                <p>No factor data available</p>
            </div>
        `;
        return;
    }
    
    const sortedFactors = Object.entries(factors)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 6);
    
    sortedFactors.forEach(([factor, importance], index) => {
        const factorDiv = document.createElement('div');
        factorDiv.className = 'factor-item slide-in-bottom';
        factorDiv.style.animationDelay = `${index * 0.1}s`;
        
        const percentage = (importance * 100).toFixed(1);
        const width = Math.min(percentage * 2, 100); // Scale for visual
        
        factorDiv.innerHTML = `
            <div class="factor-header">
                <span class="factor-name">${formatFeatureName(factor)}</span>
                <span class="factor-percentage">${percentage}%</span>
            </div>
            <div class="factor-bar">
                <div class="factor-bar-fill" style="width: ${width}%"></div>
            </div>
        `;
        
        elements.factorsList.appendChild(factorDiv);
        
        // Animate bar fill
        setTimeout(() => {
            const fill = factorDiv.querySelector('.factor-bar-fill');
            if (fill) {
                fill.style.transition = 'width 1s ease-out';
                fill.style.width = `${width}%`;
            }
        }, 100 + index * 100);
    });
}

function displayRecommendations(result) {
    if (!elements.recommendationsList) return;
    
    elements.recommendationsList.innerHTML = '';
    
    const recommendations = getRecommendations(result.risk_percentage);
    
    recommendations.forEach((rec, index) => {
        const recDiv = document.createElement('div');
        recDiv.className = 'recommendation-item slide-in-bottom';
        recDiv.style.animationDelay = `${index * 0.1}s`;
        
        recDiv.innerHTML = `
            <div class="recommendation-icon">
                <i class="fas fa-check-circle"></i>
            </div>
            <div class="recommendation-text">
                <p>${rec}</p>
            </div>
        `;
        
        elements.recommendationsList.appendChild(recDiv);
    });
}

function getRecommendations(riskPercentage) {
    const recommendations = [];
    
    if (riskPercentage >= 70) {
        recommendations.push(
            'Immediate consultation with endocrinologist recommended',
            'Schedule fine needle aspiration biopsy (FNA) within 2 weeks',
            'Complete thyroid function panel including TSH, T3, T4',
            'Ultrasound-guided biopsy if nodule size > 1cm',
            'Consider genetic testing for RET proto-oncogene mutations',
            'Regular monitoring every 3 months essential'
        );
    } else if (riskPercentage >= 40) {
        recommendations.push(
            'Schedule appointment with endocrinologist within 4 weeks',
            'Thyroid ultrasound examination recommended',
            'Monitor TSH levels every 3-6 months',
            'Maintain optimal iodine intake (150-200 mcg/day)',
            'Consider FNA if nodule grows >0.5cm in 6 months',
            'Regular self-examination for neck changes'
        );
    } else {
        recommendations.push(
            'Annual thyroid function test recommended',
            'Regular self-examination for neck lumps monthly',
            'Maintain healthy lifestyle with balanced diet',
            'Monitor for symptoms: fatigue, weight changes, mood swings',
            'Follow-up examination in 6-12 months',
            'Maintain healthy BMI (18.5-24.9)'
        );
    }
    
    // Add general recommendations
    recommendations.push(
        'Avoid smoking and limit alcohol consumption',
        'Regular exercise (30 minutes daily, 5 days/week)',
        'Stress management techniques: meditation, yoga',
        'Adequate sleep (7-9 hours nightly)',
        'Regular hydration (2-3 liters daily)'
    );
    
    return recommendations.slice(0, 6);
}

function showResultsCard() {
    if (!elements.resultsCard) return;
    
    elements.resultsCard.style.display = 'block';
    elements.resultsCard.style.opacity = '0';
    elements.resultsCard.style.transform = 'translateY(20px) scale(0.95)';
    
    setTimeout(() => {
        elements.resultsCard.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        elements.resultsCard.style.opacity = '1';
        elements.resultsCard.style.transform = 'translateY(0) scale(1)';
        elements.resultsCard.classList.add('show');
    }, 50);
}

function closeResultsCard() {
    if (!elements.resultsCard) return;
    
    elements.resultsCard.style.opacity = '0';
    elements.resultsCard.style.transform = 'translateY(20px) scale(0.95)';
    
    setTimeout(() => {
        elements.resultsCard.classList.remove('show');
        elements.resultsCard.style.display = 'none';
        
        // Show quick guide
        if (elements.quickGuide) {
            elements.quickGuide.style.display = 'block';
            elements.quickGuide.style.opacity = '0';
            elements.quickGuide.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                elements.quickGuide.style.transition = 'opacity 0.3s, transform 0.3s';
                elements.quickGuide.style.opacity = '1';
                elements.quickGuide.style.transform = 'translateY(0)';
            }, 100);
        }
    }, 300);
}

function startNewPrediction() {
    closeResultsCard();
    
    setTimeout(() => {
        resetForm();
        
        // Scroll to form
        document.querySelector('#predict').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        
        createNotification({
            title: 'New Analysis',
            message: 'Ready for new prediction',
            type: 'info'
        });
    }, 400);
}

// ========== HISTORY FUNCTIONS ==========

async function loadHistory() {
    try {
        showTableLoading(true);
        
        const limit = elements.historyLimit?.value || 10;
        
        // Try to fetch from API
        const response = await fetch(`${API_BASE_URL}/history?limit=${limit}`);
        
        if (response.ok) {
            const data = await response.json();
            currentHistory = data.history || [];
        } else {
            // Use demo history if API fails
            currentHistory = generateDemoHistory(limit);
        }
        
        renderHistoryTable();
        
    } catch (error) {
        console.error('Error loading history:', error);
        // Use demo data
        currentHistory = generateDemoHistory(10);
        renderHistoryTable();
        
        createNotification({
            title: 'Demo History',
            message: 'Using demo prediction history',
            type: 'warning',
            duration: 3000
        });
    } finally {
        showTableLoading(false);
    }
}

function generateDemoHistory(limit) {
    const history = [];
    const now = new Date();
    
    for (let i = 0; i < limit; i++) {
        const date = new Date(now);
        date.setDate(date.getDate() - i);
        
        const riskPercentage = Math.floor(Math.random() * 100);
        const prediction = riskPercentage >= 70 ? 'Malignant' : 
                          riskPercentage >= 40 ? 'Suspicious' : 'Benign';
        
        history.push({
            timestamp: date.toISOString(),
            user_data: {
                Age: Math.floor(Math.random() * 50) + 20,
                Gender_Male: Math.random() > 0.5 ? 1 : 0,
                TSH_Level: (Math.random() * 10).toFixed(1),
                T3_Level: (Math.random() * 3 + 0.5).toFixed(1),
                T4_Level: (Math.random() * 20 + 5).toFixed(1),
                Nodule_Size: (Math.random() * 5).toFixed(1),
                Thyroid_Cancer_Risk: Math.floor(Math.random() * 5)
            },
            risk_percentage: riskPercentage,
            prediction: prediction,
            confidence: (Math.min(riskPercentage + Math.random() * 10, 98)).toFixed(1) + '%'
        });
    }
    
    return history;
}

function renderHistoryTable() {
    if (!elements.historyTableBody) return;
    
    showTableLoading(false);
    
    // Apply search filter
    let filteredHistory = currentHistory;
    const searchTerm = elements.historySearch?.value.toLowerCase().trim();
    
    if (searchTerm) {
        filteredHistory = currentHistory.filter(record => {
            return (
                (record.prediction || '').toLowerCase().includes(searchTerm) ||
                (record.user_data?.Age?.toString() || '').includes(searchTerm) ||
                (record.risk_percentage?.toString() || '').includes(searchTerm) ||
                (record.timestamp || '').toLowerCase().includes(searchTerm)
            );
        });
    }
    
    // Update count
    if (elements.historyCount) {
        elements.historyCount.textContent = filteredHistory.length;
    }
    
    // Show/hide empty state
    if (elements.historyEmpty) {
        if (filteredHistory.length === 0) {
            elements.historyEmpty.classList.remove('hidden');
            elements.historyTableBody.innerHTML = '';
            return;
        } else {
            elements.historyEmpty.classList.add('hidden');
        }
    }
    
    // Apply pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedHistory = filteredHistory.slice(startIndex, endIndex);
    
    // Clear table
    elements.historyTableBody.innerHTML = '';
    
    // Populate table
    paginatedHistory.forEach((record, index) => {
        const row = createHistoryRow(record, startIndex + index);
        row.style.animationDelay = `${index * 0.05}s`;
        elements.historyTableBody.appendChild(row);
    });
    
    // Update pagination
    updatePagination(filteredHistory.length);
}

function createHistoryRow(record, index) {
    const row = document.createElement('tr');
    row.className = 'history-row slide-in-bottom';
    
    const riskClass = record.risk_percentage >= 70 ? 'high-risk' : 
                     record.risk_percentage >= 40 ? 'medium-risk' : 'low-risk';
    
    const predictionClass = record.prediction === 'Malignant' ? 'malignant' : 
                          record.prediction === 'Suspicious' ? 'suspicious' : 'benign';
    
    row.innerHTML = `
        <td>
            <div class="timestamp-cell">
                <i class="fas fa-calendar"></i>
                <span>${formatTimestamp(record.timestamp)}</span>
            </div>
        </td>
        <td>
            <div class="age-cell">
                <i class="fas fa-user"></i>
                <span>${record.user_data?.Age || 'N/A'}</span>
            </div>
        </td>
        <td>
            <div class="gender-cell">
                <i class="fas fa-${record.user_data?.Gender_Male === 1 ? 'male' : 'female'}"></i>
                <span>${record.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</span>
            </div>
        </td>
        <td>
            <span class="risk-badge ${riskClass}">
                <i class="fas fa-chart-line"></i>
                ${record.risk_percentage || 0}%
            </span>
        </td>
        <td>
            <span class="prediction-badge ${predictionClass}">
                <i class="fas fa-${predictionClass === 'malignant' ? 'exclamation-triangle' : 
                                  predictionClass === 'suspicious' ? 'question-circle' : 'check-circle'}"></i>
                ${record.prediction || 'N/A'}
            </span>
        </td>
        <td>
            <button class="btn-view-details" onclick="viewHistoryDetails(${index})">
                <i class="fas fa-eye"></i>
                <span>View</span>
            </button>
        </td>
    `;
    
    return row;
}

function showTableLoading(show) {
    const loadingRow = document.getElementById('historyLoading');
    if (loadingRow) {
        if (show) {
            loadingRow.classList.remove('hidden');
        } else {
            loadingRow.classList.add('hidden');
        }
    }
}

function updatePagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const prevBtn = document.querySelector('.pagination-btn.prev');
    const nextBtn = document.querySelector('.pagination-btn.next');
    const pageInfo = document.querySelector('.page-info');
    
    if (prevBtn) prevBtn.disabled = currentPage === 1;
    if (nextBtn) nextBtn.disabled = currentPage === totalPages || totalPages === 0;
    
    if (pageInfo) {
        pageInfo.textContent = totalPages > 0 
            ? `Page ${currentPage} of ${totalPages}`
            : 'No results';
    }
}

function searchHistory() {
    currentPage = 1;
    renderHistoryTable();
}

function formatTimestamp(timestamp) {
    if (!timestamp) return 'N/A';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ========== ANALYSIS STATE MANAGEMENT ==========

function startAnalysis() {
    isAnalyzing = true;
    
    // Update button state
    if (elements.predictBtn) {
        elements.predictBtn.disabled = true;
        elements.predictBtn.innerHTML = `
            <i class="fas fa-spinner fa-spin"></i>
            <span>Analyzing...</span>
        `;
        
        // Add loading animation
        elements.predictBtn.classList.add('loading');
    }
    
    // Show progress bar
    showProgressBar();
    
    // Disable form
    if (elements.thyroidForm) {
        elements.thyroidForm.style.opacity = '0.7';
        elements.thyroidForm.style.pointerEvents = 'none';
    }
    
    createNotification({
        title: 'Analysis Started',
        message: 'Processing clinical parameters with AI...',
        type: 'info'
    });
}

function endAnalysis() {
    isAnalyzing = false;
    
    // Reset button state
    if (elements.predictBtn) {
        elements.predictBtn.disabled = false;
        elements.predictBtn.innerHTML = `
            <i class="fas fa-brain"></i>
            <span>Analyze with AI</span>
        `;
        elements.predictBtn.classList.remove('loading');
    }
    
    // Hide progress bar
    hideProgressBar();
    
    // Enable form
    if (elements.thyroidForm) {
        elements.thyroidForm.style.opacity = '1';
        elements.thyroidForm.style.pointerEvents = 'auto';
    }
}

function showProgressBar() {
    const progressBar = document.createElement('div');
    progressBar.id = 'analysisProgressBar';
    progressBar.className = 'progress-bar';
    progressBar.innerHTML = `
        <div class="progress-fill"></div>
        <div class="progress-text">
            <i class="fas fa-cogs"></i>
            <span>AI Analysis in Progress</span>
        </div>
    `;
    
    document.body.appendChild(progressBar);
    
    // Animate
    setTimeout(() => {
        progressBar.style.opacity = '1';
        progressBar.style.transform = 'translateY(0)';
    }, 10);
}

function hideProgressBar() {
    const progressBar = document.getElementById('analysisProgressBar');
    if (progressBar) {
        progressBar.style.opacity = '0';
        progressBar.style.transform = 'translateY(-10px)';
        
        setTimeout(() => {
            if (progressBar.parentNode) {
                progressBar.parentNode.removeChild(progressBar);
            }
        }, 300);
    }
}

// ========== UTILITY FUNCTIONS ==========

function toggleMobileNav() {
    if (elements.mobileNav) {
        elements.mobileNav.classList.toggle('show');
        elements.mobileToggle.classList.toggle('active');
        
        if (elements.mobileNav.classList.contains('show')) {
            document.body.style.overflow = 'hidden';
            animateMobileNavIn();
        } else {
            document.body.style.overflow = '';
            animateMobileNavOut();
        }
    }
}

function closeMobileNav() {
    if (elements.mobileNav) {
        elements.mobileNav.classList.remove('show');
        elements.mobileToggle.classList.remove('active');
        document.body.style.overflow = '';
        animateMobileNavOut();
    }
}

function animateMobileNavIn() {
    const links = document.querySelectorAll('.mobile-nav-link');
    links.forEach((link, index) => {
        link.style.opacity = '0';
        link.style.transform = 'translateX(20px)';
        
        setTimeout(() => {
            link.style.transition = 'opacity 0.3s, transform 0.3s';
            link.style.opacity = '1';
            link.style.transform = 'translateX(0)';
        }, 100 + index * 50);
    });
}

function animateMobileNavOut() {
    const links = document.querySelectorAll('.mobile-nav-link');
    links.forEach((link, index) => {
        link.style.opacity = '0';
        link.style.transform = 'translateX(20px)';
    });
}

function closeAlertBar() {
    const alertBar = document.querySelector('.alert-bar');
    if (alertBar) {
        alertBar.style.transform = 'translateY(-100%)';
        setTimeout(() => {
            alertBar.remove();
        }, 300);
    }
}

function resetForm() {
    if (elements.thyroidForm) {
        elements.thyroidForm.reset();
        setDefaultValues();
        
        // Animate reset
        animateElement(elements.thyroidForm, 'fadeOutIn');
        
        createNotification({
            title: 'Form Reset',
            message: 'All fields have been cleared',
            type: 'success',
            duration: 2000
        });
    }
}

function updateActiveNavLink(clickedLink) {
    // Update desktop nav
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    clickedLink.classList.add('active');
    
    // Update mobile nav
    const mobileLink = document.querySelector(`.mobile-nav-link[href="${clickedLink.getAttribute('href')}"]`);
    if (mobileLink) {
        document.querySelectorAll('.mobile-nav-link').forEach(link => {
            link.classList.remove('active');
        });
        mobileLink.classList.add('active');
    }
}

function smoothScrollTo(element) {
    const headerOffset = 80;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

function handleScroll() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar?.classList.add('scrolled');
    } else {
        navbar?.classList.remove('scrolled');
    }
    
    // Update active nav based on scroll
    updateActiveNavOnScroll();
}

function handleResize() {
    // Handle responsive adjustments
    if (window.innerWidth > 992) {
        closeMobileNav();
    }
}

function updateActiveNavOnScroll() {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.scrollY + 100;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}

function formatFeatureName(feature) {
    const names = {
        'Age': 'Age',
        'Family_History': 'Family History',
        'Radiation_Exposure': 'Radiation Exposure',
        'Iodine_Deficiency': 'Iodine Deficiency',
        'Smoking': 'Smoking History',
        'Obesity': 'Obesity (BMI ≥ 30)',
        'Diabetes': 'Diabetes Mellitus',
        'TSH_Level': 'TSH Level',
        'T3_Level': 'T3 Level',
        'T4_Level': 'T4 Level',
        'Nodule_Size': 'Nodule Size',
        'Thyroid_Cancer_Risk': 'Cancer Risk Score',
        'Gender_Male': 'Gender'
    };
    
    return names[feature] || feature.replace(/_/g, ' ');
}

function animateElement(element, animation, callback = null) {
    if (!element) return;
    
    element.classList.add(`animate-${animation}`);
    
    if (callback) {
        const duration = animation === 'fadeOut' ? 300 : 600;
        setTimeout(callback, duration);
    }
    
    setTimeout(() => {
        element.classList.remove(`animate-${animation}`);
    }, 600);
}

function animateInputChange(input) {
    input.style.transform = 'scale(1.05)';
    setTimeout(() => {
        input.style.transform = 'scale(1)';
    }, 150);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ========== NOTIFICATION SYSTEM ==========

function createNotification(config) {
    const {
        title,
        message,
        type = 'info',
        duration = 3000,
        icon = null
    } = config;
    
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type} slide-in-bottom`;
    
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    
    notification.innerHTML = `
        <div class="notification-icon">
            <i class="fas fa-${icon || icons[type] || 'info-circle'}"></i>
        </div>
        <div class="notification-content">
            <div class="notification-title">${title}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles if not present
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                min-width: 300px;
                max-width: 400px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                display: flex;
                align-items: center;
                gap: 16px;
                padding: 20px;
                z-index: 10000;
                overflow: hidden;
                border-left: 4px solid;
                transform: translateX(100%);
                animation: slideInRight 0.3s ease-out forwards;
            }
            .notification-success {
                border-left-color: #10b981;
            }
            .notification-error {
                border-left-color: #ef4444;
            }
            .notification-warning {
                border-left-color: #f59e0b;
            }
            .notification-info {
                border-left-color: #3b82f6;
            }
            .notification-icon {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
                flex-shrink: 0;
            }
            .notification-success .notification-icon {
                background: rgba(16, 185, 129, 0.1);
                color: #10b981;
            }
            .notification-error .notification-icon {
                background: rgba(239, 68, 68, 0.1);
                color: #ef4444;
            }
            .notification-warning .notification-icon {
                background: rgba(245, 158, 11, 0.1);
                color: #f59e0b;
            }
            .notification-info .notification-icon {
                background: rgba(59, 130, 246, 0.1);
                color: #3b82f6;
            }
            .notification-content {
                flex: 1;
                min-width: 0;
            }
            .notification-title {
                font-weight: 700;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 2px;
                color: #1f2937;
            }
            .notification-message {
                font-size: 0.95rem;
                color: #4b5563;
                line-height: 1.4;
            }
            .notification-close {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                border: none;
                background: #f3f4f6;
                color: #6b7280;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                flex-shrink: 0;
                transition: all 0.2s;
            }
            .notification-close:hover {
                background: #e5e7eb;
                color: #374151;
            }
            @keyframes slideInRight {
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
    }
    
    document.body.appendChild(notification);
    
    // Close button
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        notification.style.transition = 'transform 0.3s, opacity 0.3s';
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    });
    
    // Auto remove
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            notification.style.transition = 'transform 0.3s, opacity 0.3s';
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }, duration);
}

// ========== SAVE REPORT ==========

function saveReport() {
    const riskPercentage = elements.riskPercentage?.textContent || '0';
    const prediction = elements.predictionText?.textContent || 'Unknown';
    const confidence = elements.confidenceText?.textContent.replace('Confidence: ', '') || '--%';
    
    const report = `
╔═══════════════════════════════════════════════════╗
║        THYROID CANCER RISK ASSESSMENT REPORT      ║
╚═══════════════════════════════════════════════════╝

📋 REPORT SUMMARY
════════════════════════════════════════════════════
• Report Date: ${new Date().toLocaleString()}
• Prediction: ${prediction}
• Risk Percentage: ${riskPercentage}
• ${confidence}

📊 CLINICAL PARAMETERS
════════════════════════════════════════════════════
${getFormDataForReport()}

🎯 KEY FINDINGS
════════════════════════════════════════════════════
${getKeyFindingsForReport()}

💡 RECOMMENDATIONS
════════════════════════════════════════════════════
${getRecommendationsForReport()}

────────────────────────────────────────────────────
📋 DISCLAIMER
════════════════════════════════════════════════════
This report is generated by ThyroScan AI for educational
and research purposes only. It is not a substitute for
professional medical diagnosis, advice, or treatment.
Always consult with qualified healthcare professionals
for medical advice and treatment decisions.

For medical emergencies, contact healthcare
professionals immediately.

────────────────────────────────────────────────────
Generated by ThyroScan AI v1.0.0
Model Accuracy: 83%
Report ID: ${Date.now().toString(36).toUpperCase()}
════════════════════════════════════════════════════
    `;
    
    // Create download
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ThyroScan_Report_${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    createNotification({
        title: 'Report Downloaded',
        message: 'Thyroid risk assessment report saved',
        type: 'success',
        duration: 3000
    });
}

function getFormDataForReport() {
    const data = [];
    const inputs = document.querySelectorAll('#thyroidForm input, #thyroidForm select');
    
    inputs.forEach(input => {
        if (input.type === 'checkbox') {
            if (input.checked) {
                const label = input.nextElementSibling?.querySelector('h5')?.textContent;
                if (label) {
                    data.push(`• ${label}: Present`);
                }
            }
        } else if (input.type !== 'hidden' && input.id) {
            const label = document.querySelector(`label[for="${input.id}"]`);
            if (label) {
                const labelText = label.textContent.replace(/[\n\r]+|[\s]{2,}/g, ' ').trim();
                data.push(`• ${labelText}: ${input.value}`);
            }
        }
    });
    
    return data.join('\n');
}

function getKeyFindingsForReport() {
    const findings = [];
    const factorItems = document.querySelectorAll('.factor-item');
    
    factorItems.forEach(item => {
        const name = item.querySelector('.factor-name')?.textContent;
        const value = item.querySelector('.factor-percentage')?.textContent;
        if (name && value) {
            findings.push(`• ${name}: ${value} influence`);
        }
    });
    
    return findings.join('\n') || '• No significant factors identified';
}

function getRecommendationsForReport() {
    const recommendations = [];
    const recItems = document.querySelectorAll('.recommendation-item p');
    
    recItems.forEach(item => {
        recommendations.push(`• ${item.textContent}`);
    });
    
    return recommendations.join('\n') || '• No specific recommendations available';
}

// ========== BACKEND CONNECTION TEST ==========

async function testBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend connected successfully');
            createNotification({
                title: 'System Ready',
                message: 'Connected to AI backend',
                type: 'success',
                duration: 3000
            });
        }
    } catch (error) {
        console.warn('⚠️ Backend not available, running in demo mode');
    }
}

// ========== GLOBAL FUNCTION EXPORTS ==========

window.viewHistoryDetails = function(index) {
    if (index < 0 || index >= currentHistory.length) return;
    
    const record = currentHistory[index];
    
    createNotification({
        title: 'Viewing History',
        message: `Details for prediction #${index + 1}`,
        type: 'info',
        duration: 2000
    });
    
    // In a real app, you would show a modal with details
    console.log('History details:', record);
};

// Initialize when page loads
console.log('✨ ThyroScan AI - Professional Medical System Initialized');