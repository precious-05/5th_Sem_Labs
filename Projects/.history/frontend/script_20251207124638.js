// ============================================
// THYROSCAN AI - ENHANCED FRONTEND JS
// Professional UI/UX with Preserved ML Logic
// ============================================

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
const historySearch = document.getElementById('historySearch');
const themeToggle = document.getElementById('themeToggle');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileNav = document.getElementById('mobileNav');
const closeMobileNav = document.querySelector('.close-mobile-nav');
const topNotification = document.querySelector('.top-notification');
const closeTopNotification = document.querySelector('.close-notification');
const quickGuide = document.getElementById('quickGuide');

// Chart Configuration
let riskChart = null;
let currentChartType = 'bar';

// State Management
let currentHistory = [];
let currentPage = 1;
let itemsPerPage = 10;
let sortField = 'timestamp';
let sortDirection = 'desc';

// Initialize Swiper Slider
let heroSlider = null;

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 ThyroScan AI - Initializing...');
    
    // Initialize components
    initHeroSlider();
    initTheme();
    loadHistory();
    testBackendConnection();
    setupEventListeners();
    setDefaultValues();
    initFormInteractions();
    
    // Add animation classes
    addPageAnimations();
    
    console.log('✅ ThyroScan AI - Initialized successfully!');
});

// ========== INITIALIZATION FUNCTIONS ==========

// Initialize Hero Slider
function initHeroSlider() {
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
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        on: {
            init: function () {
                console.log('🎬 Hero Slider initialized');
            }
        }
    });
}

// Initialize Theme
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

// Update Theme Icon
function updateThemeIcon(theme) {
    const icon = themeToggle.querySelector('i');
    icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

// Test Backend Connection
async function testBackendConnection() {
    try {
        showNotification('Connecting to backend server...', 'info');
        
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            showNotification('✅ Backend connected successfully', 'success', 3000);
            updateConnectionStatus(true);
        } else {
            throw new Error('Backend health check failed');
        }
    } catch (error) {
        console.error('Backend connection error:', error);
        showNotification('⚠️ Backend server not responding. Running in demo mode.', 'warning', 5000);
        updateConnectionStatus(false);
    }
}

// Update Connection Status
function updateConnectionStatus(connected) {
    const statusIndicator = document.createElement('div');
    statusIndicator.className = `connection-status ${connected ? 'connected' : 'disconnected'}`;
    statusIndicator.innerHTML = `
        <i class="fas fa-${connected ? 'plug' : 'unlink'}"></i>
        <span>${connected ? 'Connected' : 'Demo Mode'}</span>
    `;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .connection-status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 10000;
            backdrop-filter: blur(10px);
            animation: slideInRight 0.3s ease-out;
        }
        .connection-status.connected {
            background: rgba(16, 185, 129, 0.9);
            color: white;
        }
        .connection-status.disconnected {
            background: rgba(245, 158, 11, 0.9);
            color: white;
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(statusIndicator);
    
    // Remove after 5 seconds
    setTimeout(() => {
        statusIndicator.remove();
        document.head.removeChild(style);
    }, 5000);
}

// Setup Event Listeners
function setupEventListeners() {
    // Form submission
    thyroidForm.addEventListener('submit', handlePrediction);
    
    // Reset form
    resetBtn.addEventListener('click', resetForm);
    
    // Results management
    closeResults.addEventListener('click', closeResultsCard);
    newPredictionBtn.addEventListener('click', startNewPrediction);
    
    // Save report
    saveReportBtn.addEventListener('click', saveReport);
    
    // History management
    refreshHistory.addEventListener('click', () => {
        loadHistory();
        showNotification('History refreshed', 'success');
    });
    
    historyLimit.addEventListener('change', loadHistory);
    historySearch.addEventListener('input', debounce(searchHistory, 300));
    
    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);
    
    // Mobile navigation
    mobileMenuBtn.addEventListener('click', () => {
        mobileNav.classList.add('show');
        document.body.style.overflow = 'hidden';
    });
    
    closeMobileNav.addEventListener('click', () => {
        mobileNav.classList.remove('show');
        document.body.style.overflow = '';
    });
    
    // Mobile nav links
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', () => {
            mobileNav.classList.remove('show');
            document.body.style.overflow = '';
        });
    });
    
    // Close top notification
    closeTopNotification.addEventListener('click', () => {
        topNotification.style.transform = 'translateY(-100%)';
        setTimeout(() => {
            topNotification.remove();
        }, 300);
    });
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Update active nav link
                updateActiveNavLink(this);
                
                // Smooth scroll
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Chart type buttons
    document.querySelectorAll('.chart-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const type = this.getAttribute('data-chart');
            document.querySelectorAll('.chart-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentChartType = type;
            
            // Update chart if exists
            if (riskChart) {
                updateChartType(type);
            }
        });
    });
    
    // Sortable table headers
    document.querySelectorAll('.sortable').forEach(header => {
        header.addEventListener('click', () => {
            const field = header.getAttribute('data-sort');
            toggleSort(field);
            renderHistoryTable();
        });
    });
    
    // Pagination buttons
    document.querySelector('.pagination-btn.prev').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderHistoryTable();
        }
    });
    
    document.querySelector('.pagination-btn.next').addEventListener('click', () => {
        const totalPages = Math.ceil(currentHistory.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderHistoryTable();
        }
    });
    
    // Quick guide hover effects
    if (quickGuide) {
        quickGuide.addEventListener('mouseenter', () => {
            quickGuide.style.transform = 'translateY(-5px)';
            quickGuide.style.boxShadow = 'var(--shadow-xl)';
        });
        
        quickGuide.addEventListener('mouseleave', () => {
            quickGuide.style.transform = 'translateY(0)';
            quickGuide.style.boxShadow = 'var(--shadow-lg)';
        });
    }
    
    // Input range synchronization
    document.querySelectorAll('.range-slider').forEach(slider => {
        slider.addEventListener('input', function() {
            const inputId = this.closest('.input-group').querySelector('input[type="number"]').id;
            document.getElementById(inputId).value = this.value;
        });
    });
    
    // Input number synchronization
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('input', function() {
            const rangeSlider = this.closest('.input-group').querySelector('.range-slider');
            if (rangeSlider) {
                rangeSlider.value = this.value;
            }
        });
    });
}

// Initialize Form Interactions
function initFormInteractions() {
    // Gender selector
    document.querySelectorAll('.gender-option').forEach(option => {
        option.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            document.querySelectorAll('.gender-option').forEach(opt => opt.classList.remove('active'));
            this.classList.add('active');
            document.getElementById('Gender_Male').value = value;
        });
    });
    
    // Risk score selector
    const riskSelect = document.getElementById('Thyroid_Cancer_Risk');
    const riskDots = document.querySelectorAll('.risk-dot');
    
    riskSelect.addEventListener('change', function() {
        const value = parseInt(this.value);
        riskDots.forEach((dot, index) => {
            dot.classList.toggle('active', index === value);
        });
        
        // Update select options color
        this.querySelectorAll('option').forEach(opt => {
            opt.classList.remove('selected');
        });
        this.options[this.selectedIndex].classList.add('selected');
    });
    
    // Checkbox animations
    document.querySelectorAll('.risk-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (this.checked) {
                label.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    label.style.transform = 'scale(1)';
                }, 150);
            }
        });
    });
}

// Add Page Animations
function addPageAnimations() {
    // Animate sections on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all sections
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });
    
    // Animate cards
    document.querySelectorAll('.card, .form-card, .results-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100);
    });
}

// ========== FORM FUNCTIONS ==========

// Set Default Form Values
function setDefaultValues() {
    // Set default values
    document.getElementById('Age').value = 45;
    document.getElementById('TSH_Level').value = 2.5;
    document.getElementById('T3_Level').value = 1.2;
    document.getElementById('T4_Level').value = 8.0;
    document.getElementById('Nodule_Size').value = 1.5;
    document.getElementById('Thyroid_Cancer_Risk').value = 2;
    document.getElementById('Gender_Male').value = 1;
    
    // Update range sliders
    document.querySelectorAll('.range-slider').forEach(slider => {
        const inputId = slider.closest('.input-group').querySelector('input[type="number"]').id;
        slider.value = document.getElementById(inputId).value;
    });
    
    // Update gender selector
    document.querySelectorAll('.gender-option').forEach(opt => {
        opt.classList.remove('active');
        if (opt.getAttribute('data-value') === '1') {
            opt.classList.add('active');
        }
    });
    
    // Update risk dots
    document.querySelectorAll('.risk-dot').forEach((dot, index) => {
        dot.classList.toggle('active', index === 2);
    });
    
    // Uncheck all checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.checked = false;
    });
}

// Handle Prediction Form Submission
async function handlePrediction(e) {
    e.preventDefault();
    
    // Show loading state
    setLoadingState(true);
    
    try {
        // Get form data
        const formData = getFormData();
        
        // Validate form data
        if (!validateFormData(formData)) {
            setLoadingState(false);
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
        
        // Display results with animation
        await displayResults(result);
        
        // Reload history
        loadHistory();
        
        // Show success notification
        showNotification('✅ Analysis completed successfully!', 'success');
        
    } catch (error) {
        console.error('Prediction error:', error);
        
        // Show demo results if backend fails
        if (error.message.includes('Failed to fetch')) {
            showNotification('⚠️ Using demo data (backend unavailable)', 'warning');
            displayDemoResults();
        } else {
            showError('Failed to get prediction. Please try again.');
        }
    } finally {
        // Hide loading state
        setLoadingState(false);
    }
}

// Set Loading State
function setLoadingState(isLoading) {
    predictBtn.disabled = isLoading;
    
    if (isLoading) {
        predictBtn.classList.add('loading');
        predictBtn.querySelector('span').textContent = 'Analyzing...';
        
        // Add loading animation to form
        thyroidForm.style.opacity = '0.7';
        thyroidForm.style.pointerEvents = 'none';
        
        // Show progress animation
        showProgressAnimation();
    } else {
        predictBtn.classList.remove('loading');
        predictBtn.querySelector('span').textContent = 'Analyze with AI';
        
        // Restore form
        thyroidForm.style.opacity = '1';
        thyroidForm.style.pointerEvents = 'auto';
        
        // Hide progress animation
        hideProgressAnimation();
    }
}

// Show Progress Animation
function showProgressAnimation() {
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressBar.innerHTML = `
        <div class="progress-fill"></div>
        <div class="progress-text">Analyzing with AI...</div>
    `;
    
    const style = document.createElement('style');
    style.textContent = `
        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: var(--gray-4);
            z-index: 10000;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-blue), var(--medical-teal));
            width: 0%;
            animation: progress 2s ease-in-out infinite;
        }
        .progress-text {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.9rem;
            color: var(--primary-blue);
            font-weight: 600;
        }
        @keyframes progress {
            0% { width: 0%; transform: translateX(-100%); }
            50% { width: 50%; }
            100% { width: 100%; transform: translateX(100%); }
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(progressBar);
    
    window.progressAnimation = { element: progressBar, style };
}

// Hide Progress Animation
function hideProgressAnimation() {
    if (window.progressAnimation) {
        const { element, style } = window.progressAnimation;
        
        element.style.opacity = '0';
        element.style.transform = 'translateY(-10px)';
        element.style.transition = 'opacity 0.3s, transform 0.3s';
        
        setTimeout(() => {
            if (element.parentNode) element.remove();
            if (style.parentNode) style.remove();
            delete window.progressAnimation;
        }, 300);
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
    if (formData.Age < 0 || formData.Age > 120 || isNaN(formData.Age)) {
        highlightInvalidInput('Age');
        errors.push('Age must be between 0 and 120 years');
    }
    
    // Validate TSH Level
    if (formData.TSH_Level < 0 || formData.TSH_Level > 100 || isNaN(formData.TSH_Level)) {
        highlightInvalidInput('TSH_Level');
        errors.push('TSH Level must be between 0 and 100 mIU/L');
    }
    
    // Validate T3 Level
    if (formData.T3_Level < 0 || formData.T3_Level > 20 || isNaN(formData.T3_Level)) {
        highlightInvalidInput('T3_Level');
        errors.push('T3 Level must be between 0 and 20 pg/mL');
    }
    
    // Validate T4 Level
    if (formData.T4_Level < 0 || formData.T4_Level > 30 || isNaN(formData.T4_Level)) {
        highlightInvalidInput('T4_Level');
        errors.push('T4 Level must be between 0 and 30 μg/dL');
    }
    
    // Validate Nodule Size
    if (formData.Nodule_Size < 0 || formData.Nodule_Size > 10 || isNaN(formData.Nodule_Size)) {
        highlightInvalidInput('Nodule_Size');
        errors.push('Nodule Size must be between 0 and 10 cm');
    }
    
    if (errors.length > 0) {
        showError(errors.join('<br>'));
        return false;
    }
    
    return true;
}

// Highlight Invalid Input
function highlightInvalidInput(inputId) {
    const input = document.getElementById(inputId);
    input.style.borderColor = 'var(--danger-red)';
    input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
    
    // Add shake animation
    input.classList.add('shake');
    
    // Remove highlight after 2 seconds
    setTimeout(() => {
        input.style.borderColor = '';
        input.style.boxShadow = '';
        input.classList.remove('shake');
    }, 2000);
}

// Reset Form
function resetForm() {
    thyroidForm.reset();
    setDefaultValues();
    
    // Add animation
    thyroidForm.style.opacity = '0';
    thyroidForm.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        thyroidForm.style.opacity = '1';
        thyroidForm.style.transform = 'translateY(0)';
        thyroidForm.style.transition = 'opacity 0.3s, transform 0.3s';
    }, 50);
    
    showNotification('Form reset successfully', 'success');
}

// ========== RESULTS DISPLAY ==========

// Display Results
async function displayResults(result) {
    // Hide quick guide
    if (quickGuide) {
        quickGuide.style.opacity = '0';
        quickGuide.style.transform = 'translateY(20px)';
        setTimeout(() => {
            quickGuide.style.display = 'none';
        }, 300);
    }
    
    // Update risk percentage with animation
    await animateRiskPercentage(result.risk_percentage);
    
    // Update prediction text
    document.getElementById('predictionText').textContent = result.prediction;
    document.getElementById('confidenceText').textContent = `Confidence: ${result.confidence}`;
    
    // Update risk meter
    updateRiskMeter(result.risk_percentage);
    
    // Display chart if data exists
    if (result.chart_data) {
        try {
            const chartData = JSON.parse(result.chart_data);
            renderChart(chartData);
        } catch (error) {
            console.error('Chart data error:', error);
            renderDefaultChart(result);
        }
    } else {
        renderDefaultChart(result);
    }
    
    // Display key factors
    displayKeyFactors(result.features_importance || getDefaultFeatures());
    
    // Display recommendations
    displayRecommendations(result);
    
    // Show results card with animation
    showResultsCard();
    
    // Scroll to results
    setTimeout(() => {
        resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 500);
}

// Animate Risk Percentage
function animateRiskPercentage(finalPercentage) {
    return new Promise(resolve => {
        const riskPercentage = document.getElementById('riskPercentage');
        const riskCircle = document.querySelector('.circle');
        
        let current = 0;
        const increment = finalPercentage / 100;
        const duration = 1500;
        const stepTime = duration / 100;
        
        const animate = () => {
            current += increment;
            if (current >= finalPercentage) {
                current = finalPercentage;
                clearInterval(timer);
                resolve();
            }
            
            riskPercentage.textContent = `${Math.round(current)}%`;
            
            // Update circle stroke
            const circumference = 2 * Math.PI * 15.9155;
            const offset = circumference - (current / 100) * circumference;
            riskCircle.style.strokeDasharray = `${circumference} ${circumference}`;
            riskCircle.style.strokeDashoffset = offset;
        };
        
        const timer = setInterval(animate, stepTime);
    });
}

// Update Risk Meter
function updateRiskMeter(percentage) {
    const meterFill = document.getElementById('meterFill');
    const meterPointer = document.getElementById('meterPointer');
    
    // Animate meter fill
    meterFill.style.width = `${percentage}%`;
    
    // Animate pointer
    setTimeout(() => {
        meterPointer.style.left = `${percentage}%`;
        
        // Add bounce animation
        meterPointer.style.animation = 'none';
        setTimeout(() => {
            meterPointer.style.animation = 'bounce 0.5s ease';
        }, 10);
    }, 1000);
}

// Render Chart
function renderChart(chartData) {
    const container = document.getElementById('chartContainer');
    
    // Clear previous chart
    if (riskChart) {
        Plotly.purge(container);
    }
    
    // Update layout for better appearance
    chartData.layout = {
        ...chartData.layout,
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: {
            family: 'Poppins, sans-serif',
            color: 'var(--dark-1)'
        },
        margin: { t: 30, r: 30, b: 40, l: 60 },
        hoverlabel: {
            bgcolor: 'white',
            font: {
                family: 'Poppins, sans-serif'
            }
        }
    };
    
    // Create chart with animation
    Plotly.newPlot(container, chartData.data, chartData.layout, {
        displayModeBar: true,
        displaylogo: false,
        responsive: true,
        modeBarButtonsToRemove: ['sendDataToCloud', 'autoScale2d', 'resetScale2d'],
        modeBarButtonsToAdd: []
    }).then(graphDiv => {
        riskChart = graphDiv;
    });
}

// Render Default Chart
function renderDefaultChart(result) {
    const features = result.features_importance || getDefaultFeatures();
    const sortedFeatures = Object.entries(features)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 8);
    
    const chartData = {
        data: [{
            x: sortedFeatures.map(([key]) => formatFeatureName(key)),
            y: sortedFeatures.map(([,value]) => value * 100),
            type: 'bar',
            marker: {
                color: sortedFeatures.map((_, i) => 
                    `rgba(${59 + i * 20}, 130, ${246 - i * 20}, 0.8)`
                ),
                line: {
                    color: 'rgba(0,0,0,0.2)',
                    width: 1
                }
            },
            text: sortedFeatures.map(([,value]) => `${(value * 100).toFixed(1)}%`),
            textposition: 'auto',
            hoverinfo: 'x+text'
        }],
        layout: {
            title: 'Top Risk Factors',
            xaxis: {
                title: 'Factors',
                tickangle: -45
            },
            yaxis: {
                title: 'Importance (%)',
                range: [0, 100]
            }
        }
    };
    
    renderChart(chartData);
}

// Update Chart Type
function updateChartType(type) {
    if (!riskChart) return;
    
    const update = type === 'pie' ? {
        type: 'pie',
        labels: riskChart.data[0].x,
        values: riskChart.data[0].y,
        hole: 0.4,
        textinfo: 'percent+label',
        hoverinfo: 'label+percent+value'
    } : {
        type: 'bar'
    };
    
    Plotly.restyle('chartContainer', update);
}

// Display Key Factors
function displayKeyFactors(factors) {
    const factorsList = document.getElementById('factorsList');
    factorsList.innerHTML = '';
    
    const sortedFactors = Object.entries(factors)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 6);
    
    sortedFactors.forEach(([factor, importance], index) => {
        const factorDiv = document.createElement('div');
        factorDiv.className = 'factor-item';
        factorDiv.style.animationDelay = `${index * 0.1}s`;
        
        factorDiv.innerHTML = `
            <div class="factor-name">
                <span class="factor-rank">${index + 1}.</span>
                ${formatFeatureName(factor)}
            </div>
            <div class="factor-value">
                <div class="factor-bar">
                    <div class="factor-bar-fill" style="width: ${importance * 100}%"></div>
                </div>
                <span class="factor-percentage">${(importance * 100).toFixed(1)}%</span>
            </div>
        `;
        
        factorsList.appendChild(factorDiv);
    });
}

// Display Recommendations
function displayRecommendations(result) {
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';
    
    const recommendations = getRecommendations(result.risk_percentage);
    
    recommendations.forEach((rec, index) => {
        const li = document.createElement('div');
        li.className = 'recommendation-item';
        li.style.animationDelay = `${index * 0.1}s`;
        
        li.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <p>${rec}</p>
        `;
        
        recommendationsList.appendChild(li);
    });
}

// Get Recommendations
function getRecommendations(riskPercentage) {
    const recommendations = [];
    
    // Risk-based recommendations
    if (riskPercentage >= 70) {
        recommendations.push(
            'Immediate consultation with endocrinologist required',
            'Schedule fine needle aspiration biopsy (FNA)',
            'Complete thyroid function panel tests',
            'Ultrasound-guided biopsy if nodule > 1cm',
            'Consider genetic testing for RET mutations'
        );
    } else if (riskPercentage >= 40) {
        recommendations.push(
            'Schedule appointment with endocrinologist within 2 weeks',
            'Thyroid ultrasound examination recommended',
            'Monitor TSH levels every 3 months',
            'Maintain optimal iodine intake (150-200 mcg/day)',
            'Consider FNA if nodule grows >0.5cm in 6 months'
        );
    } else {
        recommendations.push(
            'Annual thyroid function test recommended',
            'Regular self-examination for neck lumps',
            'Maintain healthy lifestyle with balanced diet',
            'Monitor for symptoms: fatigue, weight changes',
            'Follow-up in 6-12 months'
        );
    }
    
    // General recommendations
    recommendations.push(
        'Avoid smoking and limit alcohol consumption',
        'Maintain BMI between 18.5-24.9',
        'Regular exercise (30 minutes daily)',
        'Stress management: meditation, yoga',
        'Adequate sleep (7-9 hours nightly)'
    );
    
    return recommendations.slice(0, 6); // Show top 6
}

// Show Results Card
function showResultsCard() {
    resultsCard.classList.remove('hidden');
    resultsCard.classList.add('show');
    
    // Add entrance animation
    resultsCard.style.opacity = '0';
    resultsCard.style.transform = 'translateY(30px) scale(0.95)';
    
    setTimeout(() => {
        resultsCard.style.opacity = '1';
        resultsCard.style.transform = 'translateY(0) scale(1)';
        resultsCard.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
    }, 50);
}

// Close Results Card
function closeResultsCard() {
    resultsCard.style.opacity = '0';
    resultsCard.style.transform = 'translateY(20px) scale(0.95)';
    
    setTimeout(() => {
        resultsCard.classList.add('hidden');
        resultsCard.classList.remove('show');
        
        // Show quick guide
        if (quickGuide) {
            quickGuide.style.display = 'block';
            setTimeout(() => {
                quickGuide.style.opacity = '1';
                quickGuide.style.transform = 'translateY(0)';
            }, 100);
        }
    }, 300);
}

// Start New Prediction
function startNewPrediction() {
    closeResultsCard();
    
    // Reset form
    setTimeout(() => {
        resetForm();
        
        // Scroll to form
        document.querySelector('#predict').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }, 400);
}

// ========== HISTORY FUNCTIONS ==========

// Load Prediction History
async function loadHistory() {
    try {
        const limit = historyLimit.value;
        showTableLoading(true);
        
        const response = await fetch(`${API_BASE_URL}/history?limit=${limit}`);
        
        if (!response.ok) {
            throw new Error('Failed to load history');
        }
        
        const data = await response.json();
        currentHistory = data.history || [];
        
        // Sort history
        sortHistory();
        
        // Render table
        renderHistoryTable();
        
    } catch (error) {
        console.error('Error loading history:', error);
        showError('Failed to load prediction history');
        showTableLoading(false);
    }
}

// Show Table Loading
function showTableLoading(show) {
    const loadingRow = document.getElementById('historyLoading');
    
    if (show) {
        loadingRow.classList.remove('hidden');
        if (historyEmpty) historyEmpty.classList.add('hidden');
    } else {
        loadingRow.classList.add('hidden');
    }
}

// Sort History
function sortHistory() {
    currentHistory.sort((a, b) => {
        let aValue, bValue;
        
        switch (sortField) {
            case 'timestamp':
                aValue = new Date(a.timestamp || 0);
                bValue = new Date(b.timestamp || 0);
                break;
            case 'age':
                aValue = a.user_data?.Age || 0;
                bValue = b.user_data?.Age || 0;
                break;
            case 'risk':
                aValue = a.risk_percentage || 0;
                bValue = b.risk_percentage || 0;
                break;
            case 'prediction':
                aValue = a.prediction || '';
                bValue = b.prediction || '';
                break;
            default:
                aValue = a.timestamp || 0;
                bValue = b.timestamp || 0;
        }
        
        if (sortDirection === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });
}

// Toggle Sort
function toggleSort(field) {
    if (sortField === field) {
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        sortField = field;
        sortDirection = 'desc';
    }
    
    // Update sort indicators
    document.querySelectorAll('.sortable i').forEach(icon => {
        icon.className = 'fas fa-sort';
    });
    
    const currentHeader = document.querySelector(`[data-sort="${sortField}"] i`);
    if (currentHeader) {
        currentHeader.className = sortDirection === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';
    }
}

// Render History Table
function renderHistoryTable() {
    showTableLoading(false);
    
    // Apply search filter
    let filteredHistory = currentHistory;
    const searchTerm = historySearch.value.toLowerCase().trim();
    
    if (searchTerm) {
        filteredHistory = currentHistory.filter(record => {
            return (
                (record.prediction || '').toLowerCase().includes(searchTerm) ||
                (record.user_data?.Age?.toString() || '').includes(searchTerm) ||
                (record.risk_percentage?.toString() || '').includes(searchTerm)
            );
        });
    }
    
    // Apply pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedHistory = filteredHistory.slice(startIndex, endIndex);
    
    // Update table body
    historyTableBody.innerHTML = '';
    
    if (paginatedHistory.length === 0) {
        if (historyEmpty) {
            historyEmpty.classList.remove('hidden');
        }
        updatePagination(0, 0);
        return;
    }
    
    if (historyEmpty) historyEmpty.classList.add('hidden');
    
    paginatedHistory.forEach((record, index) => {
        const row = document.createElement('tr');
        row.className = 'animate-fade-in';
        row.style.animationDelay = `${index * 0.05}s`;
        
        const riskClass = record.risk_percentage >= 70 ? 'high-risk' : 
                         record.risk_percentage >= 40 ? 'medium-risk' : 'low-risk';
        const predictionClass = record.prediction === 'Malignant' ? 'malignant' : 'benign';
        
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
                    ${record.risk_percentage || 0}%
                </span>
            </td>
            <td>
                <span class="prediction-badge ${predictionClass}">
                    <i class="fas fa-${predictionClass === 'malignant' ? 'exclamation-triangle' : 'check-circle'}"></i>
                    ${record.prediction || 'N/A'}
                </span>
            </td>
            <td>
                <button class="view-details-btn" onclick="viewHistoryDetails(${startIndex + index})">
                    <i class="fas fa-eye"></i>
                    <span>View</span>
                </button>
            </td>
        `;
        
        historyTableBody.appendChild(row);
    });
    
    // Update pagination
    updatePagination(filteredHistory.length, paginatedHistory.length);
    
    // Update count
    const countElement = document.getElementById('historyCount');
    if (countElement) {
        countElement.textContent = filteredHistory.length;
    }
}

// Update Pagination
function updatePagination(totalItems, currentItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const prevBtn = document.querySelector('.pagination-btn.prev');
    const nextBtn = document.querySelector('.pagination-btn.next');
    const pageInfo = document.querySelector('.page-info');
    
    // Update buttons
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages || totalPages === 0;
    
    // Update page info
    if (pageInfo) {
        pageInfo.textContent = totalPages > 0 
            ? `Page ${currentPage} of ${totalPages}`
            : 'No results';
    }
}

// Search History
function searchHistory() {
    currentPage = 1;
    renderHistoryTable();
}

// Format Timestamp
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

// View History Details
function viewHistoryDetails(index) {
    if (index < 0 || index >= currentHistory.length) return;
    
    const record = currentHistory[index];
    
    // Create modal
    const modal = createModal('Prediction Details', `
        <div class="modal-grid">
            <div class="modal-section">
                <h4><i class="fas fa-info-circle"></i> Summary</h4>
                <div class="detail-row">
                    <span class="detail-label">Date:</span>
                    <span class="detail-value">${formatTimestamp(record.timestamp)}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Prediction:</span>
                    <span class="prediction-badge ${record.prediction === 'Malignant' ? 'malignant' : 'benign'}">
                        ${record.prediction}
                    </span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Risk Score:</span>
                    <span class="detail-value">${record.risk_percentage}%</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Confidence:</span>
                    <span class="detail-value">${record.confidence || 'N/A'}</span>
                </div>
            </div>
            
            <div class="modal-section">
                <h4><i class="fas fa-clipboard-list"></i> Clinical Parameters</h4>
                <div class="parameters-grid">
                    ${Object.entries(record.user_data || {}).map(([key, value]) => `
                        <div class="parameter-item">
                            <span class="parameter-label">${formatFeatureName(key)}:</span>
                            <span class="parameter-value">${value}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="modal-section">
                <h4><i class="fas fa-chart-bar"></i> Risk Factors</h4>
                <div class="factors-list">
                    ${record.features_importance ? Object.entries(record.features_importance)
                        .sort(([,a], [,b]) => b - a)
                        .slice(0, 5)
                        .map(([key, value]) => `
                            <div class="factor-item">
                                <span class="factor-name">${formatFeatureName(key)}</span>
                                <span class="factor-value">${(value * 100).toFixed(1)}%</span>
                            </div>
                        `).join('') : 'No factor data available'}
                </div>
            </div>
        </div>
    `);
    
    // Add footer buttons
    const modalFooter = document.createElement('div');
    modalFooter.className = 'modal-footer';
    modalFooter.innerHTML = `
        <button class="btn-secondary" onclick="closeModal()">
            <i class="fas fa-times"></i> Close
        </button>
        <button class="btn-primary" onclick="recreateAnalysis(${index})">
            <i class="fas fa-redo"></i> Recreate Analysis
        </button>
    `;
    
    modal.querySelector('.modal-content').appendChild(modalFooter);
    
    // Add to body
    document.body.appendChild(modal);
    
    // Add modal styles
    addModalStyles();
}

// Create Modal
function createModal(title, content) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeModal()"></div>
        <div class="modal-content">
            <div class="modal-header">
                <h3>${title}</h3>
                <button class="modal-close" onclick="closeModal()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                ${content}
            </div>
        </div>
    `;
    
    return modal;
}

// Add Modal Styles
function addModalStyles() {
    const styleId = 'modal-styles';
    if (document.getElementById(styleId)) return;
    
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease;
        }
        .modal-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
        }
        .modal-content {
            position: relative;
            background: var(--white);
            border-radius: var(--radius-xl);
            width: 90%;
            max-width: 800px;
            max-height: 90vh;
            overflow-y: auto;
            animation: scaleIn 0.3s ease;
            box-shadow: var(--shadow-2xl);
        }
        .modal-header {
            padding: var(--space-xl);
            border-bottom: 1px solid var(--gray-4);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .modal-header h3 {
            margin: 0;
            display: flex;
            align-items: center;
            gap: var(--space-sm);
        }
        .modal-close {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: none;
            background: var(--gray-5);
            color: var(--dark-2);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: var(--transition-fast);
        }
        .modal-close:hover {
            background: var(--danger-red);
            color: white;
            transform: rotate(90deg);
        }
        .modal-body {
            padding: var(--space-xl);
        }
        .modal-footer {
            padding: var(--space-xl);
            border-top: 1px solid var(--gray-4);
            display: flex;
            gap: var(--space-md);
            justify-content: flex-end;
        }
        .modal-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: var(--space-xl);
        }
        @media (min-width: 768px) {
            .modal-grid {
                grid-template-columns: 1fr 1fr;
            }
        }
        .modal-section {
            background: var(--gray-5);
            padding: var(--space-lg);
            border-radius: var(--radius-lg);
        }
        .modal-section h4 {
            margin-top: 0;
            margin-bottom: var(--space-lg);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
        }
        .detail-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--space-sm) 0;
            border-bottom: 1px solid var(--gray-4);
        }
        .detail-row:last-child {
            border-bottom: none;
        }
        .parameters-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: var(--space-sm);
        }
        .parameter-item {
            display: flex;
            justify-content: space-between;
            padding: var(--space-sm);
            background: var(--white);
            border-radius: var(--radius-md);
        }
        .factors-list {
            display: flex;
            flex-direction: column;
            gap: var(--space-sm);
        }
        .factor-item {
            display: flex;
            justify-content: space-between;
            padding: var(--space-sm);
            background: var(--white);
            border-radius: var(--radius-md);
        }
    `;
    
    document.head.appendChild(style);
}

// Close Modal
function closeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.style.opacity = '0';
        modal.style.transform = 'scale(0.95)';
        
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

// Recreate Analysis
function recreateAnalysis(index) {
    const record = currentHistory[index];
    if (!record || !record.user_data) return;
    
    // Fill form with historical data
    Object.entries(record.user_data).forEach(([key, value]) => {
        const element = document.getElementById(key);
        if (element) {
            if (element.type === 'checkbox') {
                element.checked = value === 1;
            } else {
                element.value = value;
                
                // Update range slider if exists
                const rangeSlider = element.closest('.input-group')?.querySelector('.range-slider');
                if (rangeSlider) {
                    rangeSlider.value = value;
                }
            }
        }
    });
    
    // Update gender selector
    const genderValue = record.user_data.Gender_Male;
    document.querySelectorAll('.gender-option').forEach(opt => {
        opt.classList.toggle('active', opt.getAttribute('data-value') === genderValue.toString());
    });
    
    // Update risk dots
    const riskValue = record.user_data.Thyroid_Cancer_Risk || 2;
    document.querySelectorAll('.risk-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === riskValue);
    });
    
    closeModal();
    
    // Scroll to form
    setTimeout(() => {
        document.querySelector('#predict').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        
        showNotification('Form filled with historical data', 'success');
    }, 400);
}

// ========== UTILITY FUNCTIONS ==========

// Format Feature Name
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

// Get Default Features
function getDefaultFeatures() {
    return {
        'Age': 0.25,
        'TSH_Level': 0.18,
        'T4_Level': 0.15,
        'Nodule_Size': 0.12,
        'Thyroid_Cancer_Risk': 0.10,
        'Family_History': 0.08,
        'Radiation_Exposure': 0.06,
        'T3_Level': 0.04,
        'Gender_Male': 0.02
    };
}

// Save Report
function saveReport() {
    const riskPercentage = document.getElementById('riskPercentage').textContent;
    const prediction = document.getElementById('predictionText').textContent;
    const confidence = document.getElementById('confidenceText').textContent.replace('Confidence: ', '');
    
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
• Age: ${document.getElementById('Age').value} years
• Gender: ${document.getElementById('Gender_Male').value === '1' ? 'Male' : 'Female'}
• TSH Level: ${document.getElementById('TSH_Level').value} mIU/L
• T3 Level: ${document.getElementById('T3_Level').value} pg/mL
• T4 Level: ${document.getElementById('T4_Level').value} μg/dL
• Nodule Size: ${document.getElementById('Nodule_Size').value} cm
• Cancer Risk Score: ${document.getElementById('Thyroid_Cancer_Risk').value}

⚠️ RISK FACTORS IDENTIFIED
════════════════════════════════════════════════════
${Array.from(document.querySelectorAll('input[type="checkbox"]'))
    .filter(cb => cb.checked)
    .map(cb => `• ${cb.nextElementSibling.querySelector('h5').textContent}`)
    .join('\n') || '• No significant risk factors detected'}

🎯 KEY FINDINGS
════════════════════════════════════════════════════
${Array.from(document.querySelectorAll('.factor-item'))
    .map(item => `• ${item.querySelector('.factor-name').textContent.replace(/^\d+\.\s*/, '')}: ${item.querySelector('.factor-percentage').textContent}`)
    .join('\n')}

💡 RECOMMENDATIONS
════════════════════════════════════════════════════
${Array.from(document.querySelectorAll('.recommendation-item p'))
    .map(p => `• ${p.textContent}`)
    .join('\n')}

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
    
    showNotification('Report downloaded successfully!', 'success');
}

// Toggle Theme
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    // Update theme
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    
    // Show notification
    showNotification(`Switched to ${newTheme} theme`, 'info');
}

// Update Active Nav Link
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

// Debounce Function
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

// ========== DEMO FUNCTIONS ==========

// Display Demo Results (for testing)
function displayDemoResults() {
    const demoResult = {
        prediction: Math.random() > 0.5 ? 'Malignant' : 'Benign',
        risk_percentage: Math.floor(Math.random() * 100),
        confidence: (Math.random() * 20 + 80).toFixed(1) + '%',
        features_importance: getDefaultFeatures(),
        chart_data: JSON.stringify({
            data: [{
                x: ['Age', 'TSH Level', 'T4 Level', 'Nodule Size', 'Family History'],
                y: [25, 18, 15, 12, 8],
                type: 'bar',
                marker: {
                    color: ['#3b82f6', '#0ea5e9', '#06b6d4', '#10b981', '#8b5cf6']
                }
            }],
            layout: {
                title: 'Top Risk Factors (Demo)',
                xaxis: { title: 'Factors' },
                yaxis: { title: 'Importance (%)' }
            }
        })
    };
    
    displayResults(demoResult);
}

// ========== NOTIFICATION SYSTEM ==========

// Show Success Message
function showSuccess(message) {
    showNotification(message, 'success');
}

// Show Error Message
function showError(message) {
    showNotification(message, 'error');
}

// Show Notification
function showNotification(message, type = 'info', duration = 4000) {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type} animate-fade-in`;
    
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    
    notification.innerHTML = `
        <div class="notification-icon">
            <i class="fas fa-${icons[type] || 'info-circle'}"></i>
        </div>
        <div class="notification-content">
            <div class="notification-title">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add styles if not already added
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
                background: var(--white);
                border-radius: var(--radius-lg);
                box-shadow: var(--shadow-2xl);
                display: flex;
                align-items: center;
                gap: var(--space-md);
                padding: var(--space-lg);
                z-index: 10000;
                overflow: hidden;
                border-left: 4px solid;
                transform: translateX(100%);
                animation: slideInRight 0.3s ease-out forwards;
            }
            .notification.success {
                border-left-color: var(--success-green);
            }
            .notification.error {
                border-left-color: var(--danger-red);
            }
            .notification.warning {
                border-left-color: var(--warning-orange);
            }
            .notification.info {
                border-left-color: var(--primary-blue);
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
            .notification.success .notification-icon {
                background: rgba(16, 185, 129, 0.1);
                color: var(--success-green);
            }
            .notification.error .notification-icon {
                background: rgba(239, 68, 68, 0.1);
                color: var(--danger-red);
            }
            .notification.warning .notification-icon {
                background: rgba(245, 158, 11, 0.1);
                color: var(--warning-orange);
            }
            .notification.info .notification-icon {
                background: rgba(59, 130, 246, 0.1);
                color: var(--primary-blue);
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
            }
            .notification-message {
                font-size: 0.95rem;
                color: var(--dark-2);
                line-height: 1.4;
            }
            .notification-close {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                border: none;
                background: var(--gray-5);
                color: var(--gray-2);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                flex-shrink: 0;
                transition: var(--transition-fast);
            }
            .notification-close:hover {
                background: var(--gray-4);
                color: var(--dark-2);
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
    
    // Auto remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            notification.style.transition = 'transform 0.3s, opacity 0.3s';
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, duration);
}

// ========== SHAKE ANIMATION ==========
// Add shake animation to CSS
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    .shake {
        animation: shake 0.5s ease-in-out;
    }
`;
document.head.appendChild(shakeStyle);

// ========== EXPORT FUNCTIONS FOR GLOBAL USE ==========
window.viewHistoryDetails = viewHistoryDetails;
window.closeModal = closeModal;
window.recreateAnalysis = recreateAnalysis;

console.log('✨ ThyroScan AI JS - Enhanced version loaded!');