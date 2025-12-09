// ============================================
// ENHANCED HISTORY.JS - History Page JavaScript for ThyroScan AI
// ============================================

// Global variables
let historyData = [];
let filteredHistory = [];
let currentPage = 1;
let itemsPerPage = 10;
let currentView = 'list';
let sortColumn = 'timestamp';
let sortDirection = 'desc';
let isInitialized = false;

// Initialize History Page with Enhanced UI
function initializeHistoryPage() {
    if (isInitialized) return;
    
    console.log('📊 Enhanced history page initializing...');
    
    // Show loading animation
    showPageLoader();
    
    // Initialize page elements with animations
    initializePageElements();
    
    // Load prediction history with progress
    loadHistory();
    
    // Initialize interactive elements
    initializeInteractiveElements();
    
    // Setup event listeners
    setupHistoryEventListeners();
    
    // Initialize filters with animations
    initializeFilters();
    
    // Initialize modals
    initializeModals();
    
    isInitialized = true;
    
    // Add scroll animations
    addScrollAnimations();
}

// Show Page Loader
function showPageLoader() {
    const loadingState = document.getElementById('historyLoading');
    if (loadingState) {
        loadingState.innerHTML = `
            <div class="loading-spinner enhanced">
                <div class="spinner-circle"></div>
                <div class="spinner-text">Loading History...</div>
            </div>
        `;
        loadingState.classList.remove('hidden');
    }
}

// Hide Page Loader
function hidePageLoader() {
    const loadingState = document.getElementById('historyLoading');
    if (loadingState) {
        loadingState.classList.add('hidden');
    }
}

// Initialize Page Elements with Animations
function initializePageElements() {
    // Update current year with animation
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
        yearElement.classList.add('fade-in');
    }
    
    // Initialize stats with counters
    initializeStatsCounters();
    
    // Initialize empty state with animation
    const emptyState = document.getElementById('historyEmpty');
    if (emptyState) {
        emptyState.classList.add('hidden');
        emptyState.innerHTML = `
            <div class="empty-state enhanced">
                <div class="empty-icon">
                    <i class="fas fa-history fa-pulse"></i>
                </div>
                <h3>No History Yet</h3>
                <p>Your prediction history will appear here after making predictions.</p>
                <button class="btn-primary" onclick="window.location.href='/predict'">
                    <i class="fas fa-plus"></i>
                    Make Your First Prediction
                </button>
            </div>
        `;
    }
    
    // Add particle effect background
    addBackgroundParticles();
}

// Initialize Stats Counters
function initializeStatsCounters() {
    // Animated counters for stats
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-count') || '0');
        animateCounter(counter, 0, target, 1500);
    });
}

// Animate Counter
function animateCounter(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Add Background Particles
function addBackgroundParticles() {
    const particlesContainer = document.createElement('div');
    particlesContainer.className = 'background-particles';
    document.body.appendChild(particlesContainer);
    
    // Create particles
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 20}s`;
        particle.style.width = particle.style.height = `${Math.random() * 4 + 1}px`;
        particle.style.opacity = Math.random() * 0.3 + 0.1;
        particlesContainer.appendChild(particle);
    }
}

// Add Scroll Animations
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe all elements with animation classes
    document.querySelectorAll('.fade-in-up, .slide-in-left, .slide-in-right').forEach(el => {
        observer.observe(el);
    });
}

// Load Prediction History with Enhanced UI
async function loadHistory() {
    try {
        // Show loading animation in table
        showTableLoading();
        
        const limit = 100;
        const response = await fetch(`${window.API_BASE_URL || 'http://localhost:8000'}/history?limit=${limit}`);
        
        if (response.ok) {
            const data = await response.json();
            historyData = data.history || [];
            
            if (historyData.length === 0) {
                historyData = generateDemoHistory();
                showNotification('Showing demo history data', 'info');
            }
            
            // Process with animations
            await processHistoryWithAnimations();
            
        } else {
            throw new Error('Failed to load history');
        }
        
    } catch (error) {
        console.error('Error loading history:', error);
        
        // Load demo data with fallback animation
        historyData = generateDemoHistory();
        await processHistoryWithAnimations();
        
        showNotification('Using demo data - API not available', 'warning');
    } finally {
        hideTableLoading();
        hidePageLoader();
    }
}

// Show Table Loading Animation
function showTableLoading() {
    const tableBody = document.getElementById('historyTableBody');
    if (tableBody) {
        tableBody.innerHTML = `
            <div class="table-loading">
                <div class="loading-rows">
                    ${Array(5).fill().map((_, i) => `
                        <div class="loading-row" style="animation-delay: ${i * 0.1}s">
                            <div class="loading-cell"></div>
                            <div class="loading-cell"></div>
                            <div class="loading-cell"></div>
                            <div class="loading-cell"></div>
                            <div class="loading-cell"></div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
}

// Hide Table Loading
function hideTableLoading() {
    const tableBody = document.getElementById('historyTableBody');
    if (tableBody && tableBody.querySelector('.table-loading')) {
        tableBody.innerHTML = '';
    }
}

// Process History with Animations
async function processHistoryWithAnimations() {
    return new Promise(resolve => {
        // Add slight delay for smooth transition
        setTimeout(() => {
            processHistoryData();
            updateHistoryDisplay();
            updateSummaryStats();
            initializeCharts();
            resolve();
        }, 300);
    });
}

// Generate Enhanced Demo History Data
function generateDemoHistory() {
    const demoData = [];
    const riskLevels = ['Low', 'Medium', 'High'];
    const predictions = ['Benign', 'Malignant'];
    
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);
    
    for (let i = 0; i < 25; i++) {
        const date = new Date(startDate);
        date.setDate(date.getDate() + Math.floor(Math.random() * 30));
        date.setHours(Math.floor(Math.random() * 24));
        date.setMinutes(Math.floor(Math.random() * 60));
        
        const riskPercentage = Math.floor(Math.random() * 100);
        const riskLevel = riskPercentage < 30 ? 'Low' : riskPercentage < 70 ? 'Medium' : 'High';
        const prediction = riskPercentage > 70 ? 'Malignant' : 'Benign';
        
        // Enhanced demo data with more realistic features
        demoData.push({
            id: `history_${Date.now()}_${i}`,
            timestamp: date.toISOString(),
            risk_percentage: riskPercentage,
            prediction: prediction,
            confidence: `${Math.floor(Math.random() * 15) + 80}%`,
            risk_level: riskLevel,
            user_data: {
                Age: Math.floor(Math.random() * 50) + 20,
                Gender_Male: Math.random() > 0.5 ? 1 : 0,
                TSH_Level: (Math.random() * 5).toFixed(2),
                T3_Level: (Math.random() * 2 + 1).toFixed(2),
                T4_Level: (Math.random() * 2 + 0.5).toFixed(2),
                Nodule_Size: (Math.random() * 4).toFixed(1),
                Thyroid_Cancer_Risk: Math.floor(Math.random() * 5),
                Family_History: Math.random() > 0.7 ? 1 : 0,
                Radiation_Exposure: Math.random() > 0.8 ? 1 : 0,
                Iodine_Deficiency: Math.random() > 0.6 ? 1 : 0,
                Smoking: Math.random() > 0.5 ? 1 : 0,
                Obesity: Math.random() > 0.4 ? 1 : 0,
                Diabetes: Math.random() > 0.3 ? 1 : 0
            },
            features_importance: {
                'Nodule Size': Math.random() * 0.3 + 0.4,
                'Age': Math.random() * 0.2 + 0.2,
                'TSH Level': Math.random() * 0.15 + 0.1,
                'Cancer Risk Score': Math.random() * 0.15 + 0.1
            },
            recommendations: [
                'Regular checkup recommended',
                'Maintain healthy lifestyle',
                'Monitor thyroid levels',
                'Consult specialist if symptoms appear'
            ]
        });
    }
    
    return demoData.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
}

// Process History Data with Sorting
function processHistoryData() {
    // Sort data with animation
    filteredHistory = [...historyData].sort((a, b) => {
        let aValue = a[sortColumn];
        let bValue = b[sortColumn];
        
        if (sortColumn === 'age') {
            aValue = a.user_data?.Age;
            bValue = b.user_data?.Age;
        } else if (sortColumn === 'gender') {
            aValue = a.user_data?.Gender_Male;
            bValue = b.user_data?.Gender_Male;
        }
        
        if (sortDirection === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });
    
    applyFilters();
}

// Apply Filters with Animation
function applyFilters() {
    const riskFilter = document.getElementById('filterRisk')?.value;
    const dateFilter = document.getElementById('filterDate')?.value;
    const predictionFilter = document.getElementById('filterPrediction')?.value;
    const searchTerm = document.getElementById('historySearch')?.value.toLowerCase();
    
    // Show filtering animation
    showFilteringAnimation();
    
    filteredHistory = historyData.filter(item => {
        // Risk filter
        if (riskFilter) {
            const riskPercentage = item.risk_percentage;
            if (riskFilter === 'low' && riskPercentage >= 30) return false;
            if (riskFilter === 'medium' && (riskPercentage < 30 || riskPercentage >= 70)) return false;
            if (riskFilter === 'high' && riskPercentage < 70) return false;
        }
        
        // Date filter
        if (dateFilter) {
            const itemDate = new Date(item.timestamp);
            const now = new Date();
            
            switch (dateFilter) {
                case 'today':
                    if (itemDate.toDateString() !== now.toDateString()) return false;
                    break;
                case 'week':
                    const weekAgo = new Date(now.setDate(now.getDate() - 7));
                    if (itemDate < weekAgo) return false;
                    break;
                case 'month':
                    const monthAgo = new Date(now.setMonth(now.getMonth() - 1));
                    if (itemDate < monthAgo) return false;
                    break;
                case 'year':
                    const yearAgo = new Date(now.setFullYear(now.getFullYear() - 1));
                    if (itemDate < yearAgo) return false;
                    break;
            }
        }
        
        // Prediction filter
        if (predictionFilter) {
            if (predictionFilter === 'benign' && item.prediction !== 'Benign') return false;
            if (predictionFilter === 'malignant' && item.prediction !== 'Malignant') return false;
        }
        
        // Search filter
        if (searchTerm) {
            const searchFields = [
                item.prediction,
                item.risk_level,
                item.user_data?.Age?.toString(),
                item.user_data?.Gender_Male === 1 ? 'male' : 'female'
            ].filter(Boolean);
            
            const matches = searchFields.some(field => 
                field.toLowerCase().includes(searchTerm)
            );
            
            if (!matches) return false;
        }
        
        return true;
    });
    
    // Hide filtering animation
    setTimeout(() => hideFilteringAnimation(), 300);
    
    updatePagination();
}

// Show Filtering Animation
function showFilteringAnimation() {
    const tableBody = document.getElementById('historyTableBody');
    if (tableBody) {
        tableBody.style.opacity = '0.5';
        tableBody.style.transition = 'opacity 0.3s ease';
    }
}

// Hide Filtering Animation
function hideFilteringAnimation() {
    const tableBody = document.getElementById('historyTableBody');
    if (tableBody) {
        tableBody.style.opacity = '1';
    }
}

// Update History Display with Animation
function updateHistoryDisplay() {
    if (currentView === 'list') {
        updateListView();
    } else {
        updateGridView();
    }
    
    updateEmptyState();
    animateContentAppearance();
}

// Update List View with Staggered Animations
function updateListView() {
    const tableBody = document.getElementById('historyTableBody');
    if (!tableBody) return;
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    tableBody.innerHTML = '';
    
    pageItems.forEach((item, index) => {
        const row = createEnhancedHistoryRow(item, startIndex + index);
        tableBody.appendChild(row);
    });
    
    updatePaginationControls();
    
    // Add hover effects
    addTableHoverEffects();
}

// Create Enhanced History Row
function createEnhancedHistoryRow(item, index) {
    const row = document.createElement('div');
    row.className = 'history-item enhanced fade-in-up';
    row.style.animationDelay = `${index * 0.05}s`;
    row.setAttribute('data-risk', item.risk_percentage);
    
    const date = new Date(item.timestamp);
    const age = item.user_data?.Age || 'N/A';
    const gender = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
    const riskPercentage = item.risk_percentage || 0;
    const prediction = item.prediction || 'N/A';
    
    // Get top 3 risk factors
    const riskFactors = Object.entries(item.features_importance || {})
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([name]) => name);
    
    row.innerHTML = `
        <div class="history-date enhanced">
            <div class="date-icon">
                <i class="fas fa-calendar-alt"></i>
            </div>
            <div class="date-content">
                <div class="date-day">${date.toLocaleDateString('en-US', { weekday: 'short' })}</div>
                <div class="date-full">${date.toLocaleDateString()}</div>
                <div class="date-time">${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
            </div>
        </div>
        
        <div class="history-patient enhanced">
            <div class="patient-avatar pulse-animation" style="--pulse-color: ${getRiskColor(riskPercentage)}">
                <i class="fas fa-user${gender === 'Male' ? '' : '-female'}"></i>
                <div class="avatar-pulse"></div>
            </div>
            <div class="patient-info">
                <h4>Patient ${index + 1}</h4>
                <p><i class="fas fa-birthday-cake"></i> ${age} yrs • <i class="fas fa-${gender === 'Male' ? 'mars' : 'venus'}"></i> ${gender}</p>
            </div>
        </div>
        
        <div class="history-risk enhanced">
            <div class="risk-gauge">
                <div class="gauge-circle">
                    <svg width="50" height="50">
                        <circle cx="25" cy="25" r="20" fill="none" stroke="rgba(0,0,0,0.1)" stroke-width="3"/>
                        <circle cx="25" cy="25" r="20" fill="none" stroke="${getRiskColor(riskPercentage)}" 
                                stroke-width="3" stroke-linecap="round" 
                                stroke-dasharray="126" stroke-dashoffset="${126 - (riskPercentage / 100) * 126}"/>
                    </svg>
                    <div class="gauge-value">${riskPercentage}%</div>
                </div>
            </div>
            <div class="risk-level ${getRiskLevelClass(riskPercentage)}">
                <i class="fas fa-${riskPercentage < 30 ? 'shield-alt' : riskPercentage < 70 ? 'exclamation-circle' : 'exclamation-triangle'}"></i>
                ${getRiskLevel(riskPercentage)}
            </div>
        </div>
        
        <div class="history-prediction enhanced">
            <span class="prediction-badge ${prediction === 'Malignant' ? 'malignant' : 'benign'}">
                <i class="fas fa-${prediction === 'Malignant' ? 'exclamation-triangle' : 'check-circle'}"></i>
                ${prediction}
            </span>
            <div class="prediction-confidence">
                <i class="fas fa-chart-line"></i>
                ${item.confidence || '85%'} confidence
            </div>
        </div>
        
        <div class="history-factors enhanced">
            <div class="factors-tags">
                ${riskFactors.map(factor => `
                    <span class="factor-tag">
                        <i class="fas fa-circle"></i>
                        ${factor}
                    </span>
                `).join('')}
            </div>
        </div>
        
        <div class="history-actions enhanced">
            <button class="btn-view enhanced" data-id="${item.id}" title="View Details">
                <i class="fas fa-eye"></i>
                <span class="tooltip">View Details</span>
            </button>
            <button class="btn-download" data-id="${item.id}" title="Download Report">
                <i class="fas fa-download"></i>
                <span class="tooltip">Download Report</span>
            </button>
            <button class="btn-delete enhanced" data-id="${item.id}" title="Delete Record">
                <i class="fas fa-trash-alt"></i>
                <span class="tooltip">Delete Record</span>
            </button>
        </div>
    `;
    
    // Add hover effects
    addRowHoverEffects(row, item);
    
    // Add event listeners
    addRowEventListeners(row, item, index);
    
    return row;
}

// Add Row Hover Effects
function addRowHoverEffects(row, item) {
    row.addEventListener('mouseenter', () => {
        row.style.transform = 'translateY(-2px)';
        row.style.boxShadow = '0 8px 32px rgba(114, 9, 183, 0.15)';
        row.style.borderColor = 'rgba(114, 9, 183, 0.3)';
        
        // Add ripple effect
        const ripple = document.createElement('div');
        ripple.className = 'ripple-effect';
        ripple.style.backgroundColor = getRiskColor(item.risk_percentage);
        row.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
    
    row.addEventListener('mouseleave', () => {
        row.style.transform = 'translateY(0)';
        row.style.boxShadow = 'var(--shadow-md)';
        row.style.borderColor = 'rgba(114, 9, 183, 0.1)';
    });
}

// Add Row Event Listeners
function addRowEventListeners(row, item, index) {
    const viewBtn = row.querySelector('.btn-view');
    const downloadBtn = row.querySelector('.btn-download');
    const deleteBtn = row.querySelector('.btn-delete');
    
    if (viewBtn) {
        viewBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            showEnhancedHistoryDetails(item);
        });
    }
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            downloadHistoryReport(item);
        });
    }
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            confirmDeleteHistory(item.id, index);
        });
    }
    
    // Click anywhere on row to view details
    row.addEventListener('click', (e) => {
        if (!e.target.closest('.history-actions')) {
            showEnhancedHistoryDetails(item);
        }
    });
}

// Add Table Hover Effects
function addTableHoverEffects() {
    const rows = document.querySelectorAll('.history-item');
    rows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            const risk = row.getAttribute('data-risk');
            if (risk) {
                row.style.setProperty('--highlight-color', getRiskColor(parseInt(risk)));
            }
        });
    });
}

// Update Grid View with Enhanced Cards
function updateGridView() {
    const gridView = document.getElementById('historyGrid');
    if (!gridView) return;
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    gridView.innerHTML = '';
    
    pageItems.forEach((item, index) => {
        const card = createEnhancedHistoryCard(item, startIndex + index);
        gridView.appendChild(card);
    });
    
    updatePaginationControls();
}

// Create Enhanced History Card
function createEnhancedHistoryCard(item, index) {
    const card = document.createElement('div');
    card.className = 'history-card enhanced fade-in-up';
    card.style.animationDelay = `${index * 0.05}s`;
    card.setAttribute('data-risk', item.risk_percentage);
    
    const date = new Date(item.timestamp);
    const riskPercentage = item.risk_percentage || 0;
    const prediction = item.prediction || 'N/A';
    
    card.innerHTML = `
        <div class="card-header enhanced">
            <div class="card-date">
                <i class="fas fa-calendar"></i>
                ${date.toLocaleDateString()} • ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
            <div class="card-actions">
                <button class="btn-view" data-id="${item.id}" title="View Details">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn-download" data-id="${item.id}" title="Download Report">
                    <i class="fas fa-download"></i>
                </button>
            </div>
        </div>
        
        <div class="card-risk enhanced">
            <div class="risk-circle-glow" style="--glow-color: ${getRiskColor(riskPercentage)}">
                <div class="circle-progress">
                    <svg width="100" height="100">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(0,0,0,0.1)" stroke-width="6"/>
                        <circle cx="50" cy="50" r="45" fill="none" stroke="${getRiskColor(riskPercentage)}" 
                                stroke-width="6" stroke-linecap="round" 
                                stroke-dasharray="283" stroke-dashoffset="${283 - (riskPercentage / 100) * 283}"/>
                    </svg>
                    <div class="score-content">
                        <span class="score-value">${riskPercentage}%</span>
                        <span class="score-label">Risk Score</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card-prediction enhanced">
            <span class="prediction-badge ${prediction === 'Malignant' ? 'malignant' : 'benign'}">
                <i class="fas fa-${prediction === 'Malignant' ? 'exclamation-triangle' : 'check-circle'} fa-beat"></i>
                ${prediction}
                <span class="confidence">${item.confidence || '85%'} confidence</span>
            </span>
        </div>
        
        <div class="card-details enhanced">
            <div class="detail-item">
                <span class="detail-label"><i class="fas fa-user"></i> Patient:</span>
                <span class="detail-value">${index + 1}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label"><i class="fas fa-birthday-cake"></i> Age:</span>
                <span class="detail-value">${item.user_data?.Age || 'N/A'} yrs</span>
            </div>
            <div class="detail-item">
                <span class="detail-label"><i class="fas fa-venus-mars"></i> Gender:</span>
                <span class="detail-value">${item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label"><i class="fas fa-tumor"></i> Nodule:</span>
                <span class="detail-value">${item.user_data?.Nodule_Size || 'N/A'} cm</span>
            </div>
        </div>
        
        <div class="card-factors enhanced">
            <h4><i class="fas fa-key"></i> Key Factors</h4>
            <div class="factors-list">
                ${Object.entries(item.features_importance || {})
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 2)
                    .map(([factor, importance]) => `
                        <div class="factor-item">
                            <span class="factor-name">${factor}</span>
                            <span class="factor-bar">
                                <span class="bar-fill" style="width: ${importance * 100}%"></span>
                            </span>
                        </div>
                    `).join('')}
            </div>
        </div>
        
        <div class="card-footer enhanced">
            <button class="btn-view-full ripple" data-id="${item.id}">
                <i class="fas fa-chart-bar"></i>
                View Full Report
            </button>
        </div>
    `;
    
    // Add hover effects to card
    addCardHoverEffects(card, item);
    
    // Add event listeners
    const viewBtn = card.querySelector('.btn-view-full');
    const actionBtns = card.querySelectorAll('.btn-view, .btn-download');
    
    if (viewBtn) {
        viewBtn.addEventListener('click', () => showEnhancedHistoryDetails(item));
    }
    
    actionBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (btn.classList.contains('btn-view')) {
                showEnhancedHistoryDetails(item);
            } else if (btn.classList.contains('btn-download')) {
                downloadHistoryReport(item);
            }
        });
    });
    
    // Click anywhere on card to view details
    card.addEventListener('click', (e) => {
        if (!e.target.closest('.card-actions') && !e.target.closest('.btn-view-full')) {
            showEnhancedHistoryDetails(item);
        }
    });
    
    return card;
}

// Add Card Hover Effects
function addCardHoverEffects(card, item) {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-8px) scale(1.02)';
        card.style.boxShadow = '0 20px 60px rgba(114, 9, 183, 0.2)';
        card.style.borderColor = getRiskColor(item.risk_percentage);
        
        // Add glow effect
        card.style.setProperty('--glow-opacity', '0.2');
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
        card.style.boxShadow = 'var(--shadow-lg)';
        card.style.borderColor = 'rgba(114, 9, 183, 0.1)';
        card.style.setProperty('--glow-opacity', '0');
    });
}

// Update Empty State
function updateEmptyState() {
    const emptyState = document.getElementById('historyEmpty');
    const tableBody = document.getElementById('historyTableBody');
    const gridView = document.getElementById('historyGrid');
    
    if (filteredHistory.length === 0) {
        if (emptyState) {
            emptyState.classList.remove('hidden');
            emptyState.classList.add('fade-in');
        }
        if (tableBody) tableBody.classList.add('hidden');
        if (gridView) gridView.classList.add('hidden');
    } else {
        if (emptyState) emptyState.classList.add('hidden');
        if (tableBody) tableBody.classList.remove('hidden');
        if (gridView) gridView.classList.remove('hidden');
    }
}

// Animate Content Appearance
function animateContentAppearance() {
    const items = document.querySelectorAll('.history-item, .history-card');
    items.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.05}s`;
    });
}

// Update Summary Stats with Animation
function updateSummaryStats() {
    // Total predictions
    const totalCount = document.getElementById('totalCount');
    if (totalCount) {
        animateCounter(totalCount, parseInt(totalCount.textContent) || 0, filteredHistory.length, 800);
    }
    
    // Benign cases
    const benignCount = document.getElementById('benignCount');
    if (benignCount) {
        const benignCases = filteredHistory.filter(item => item.prediction === 'Benign').length;
        animateCounter(benignCount, parseInt(benignCount.textContent) || 0, benignCases, 800);
    }
    
    // Malignant cases
    const malignantCount = document.getElementById('malignantCount');
    if (malignantCount) {
        const malignantCases = filteredHistory.filter(item => item.prediction === 'Malignant').length;
        animateCounter(malignantCount, parseInt(malignantCount.textContent) || 0, malignantCases, 800);
    }
    
    // Average risk
    const avgRisk = document.getElementById('avgRisk');
    if (avgRisk) {
        const totalRisk = filteredHistory.reduce((sum, item) => sum + (item.risk_percentage || 0), 0);
        const average = filteredHistory.length > 0 ? Math.round(totalRisk / filteredHistory.length) : 0;
        const currentAvg = parseInt(avgRisk.textContent) || 0;
        
        let start = currentAvg;
        let end = average;
        
        const duration = 1000;
        const startTime = Date.now();
        
        const updateCounter = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const value = Math.floor(start + (end - start) * easeOutQuart);
            
            avgRisk.textContent = `${value}%`;
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        };
        
        updateCounter();
    }
    
    // Update header stats
    updateHeaderStats();
}

// Update Header Stats with Animation
function updateHeaderStats() {
    const totalPredictions = document.getElementById('totalPredictions');
    const avgRiskScore = document.getElementById('avgRiskScore');
    const lastUpdated = document.getElementById('lastUpdated');
    
    if (totalPredictions) {
        totalPredictions.textContent = `${filteredHistory.length} Predictions`;
        totalPredictions.classList.add('pulse-text');
        setTimeout(() => totalPredictions.classList.remove('pulse-text'), 500);
    }
    
    if (avgRiskScore) {
        const totalRisk = filteredHistory.reduce((sum, item) => sum + (item.risk_percentage || 0), 0);
        const average = filteredHistory.length > 0 ? Math.round(totalRisk / filteredHistory.length) : 0;
        avgRiskScore.textContent = `Avg Risk: ${average}%`;
    }
    
    if (lastUpdated) {
        const now = new Date();
        lastUpdated.textContent = `Updated: ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
        lastUpdated.classList.add('fade-in');
    }
}

// Initialize Charts with Enhanced UI
function initializeCharts() {
    // Create chart containers if they don't exist
    createChartContainers();
    
    // Initialize distribution chart
    initializeDistributionChart();
    
    // Initialize trend chart
    initializeTrendChart();
    
    // Initialize risk heatmap
    initializeRiskHeatmap();
}

// Initialize Distribution Chart with Enhanced Options
function initializeDistributionChart() {
    const ctx = document.getElementById('riskDistributionChart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (window.riskDistributionChart) {
        window.riskDistributionChart.destroy();
    }
    
    // Enhanced chart options
    window.riskDistributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk (0-30%)', 'Medium Risk (31-69%)', 'High Risk (70-100%)'],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: [
                    'rgba(46, 213, 115, 0.8)',
                    'rgba(255, 165, 2, 0.8)',
                    'rgba(255, 71, 87, 0.8)'
                ],
                borderColor: [
                    'rgba(46, 213, 115, 1)',
                    'rgba(255, 165, 2, 1)',
                    'rgba(255, 71, 87, 1)'
                ],
                borderWidth: 3,
                hoverOffset: 20,
                hoverBackgroundColor: [
                    'rgba(46, 213, 115, 1)',
                    'rgba(255, 165, 2, 1)',
                    'rgba(255, 71, 87, 1)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                animateScale: true,
                animateRotate: true,
                duration: 2000,
                easing: 'easeOutQuart'
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 25,
                        font: {
                            family: 'Poppins',
                            size: 12,
                            weight: '500'
                        },
                        color: 'var(--dark)',
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 26, 46, 0.95)',
                    titleFont: {
                        family: 'Montserrat',
                        size: 12,
                        weight: '600'
                    },
                    bodyFont: {
                        family: 'Poppins',
                        size: 11
                    },
                    padding: 15,
                    cornerRadius: 10,
                    displayColors: true,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} cases (${percentage}%)`;
                        }
                    }
                }
            },
            cutout: '75%',
            radius: '90%'
        }
    });
}

// Initialize Trend Chart with Enhanced Options
function initializeTrendChart() {
    const ctx = document.getElementById('riskTrendChart');
    if (!ctx) return;
    
    if (window.riskTrendChart) {
        window.riskTrendChart.destroy();
    }
    
    // Enhanced trend chart
    window.riskTrendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Risk Score Trend',
                data: [],
                borderColor: 'rgba(114, 9, 183, 1)',
                backgroundColor: 'rgba(114, 9, 183, 0.1)',
                borderWidth: 4,
                fill: true,
                tension: 0.5,
                pointBackgroundColor: 'rgba(255, 255, 255, 1)',
                pointBorderColor: 'rgba(114, 9, 183, 1)',
                pointBorderWidth: 3,
                pointRadius: 6,
                pointHoverRadius: 10,
                pointHoverBackgroundColor: 'rgba(114, 9, 183, 1)',
                pointHoverBorderColor: 'rgba(255, 255, 255, 1)',
                pointHoverBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 2000,
                easing: 'easeOutQuart'
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(26, 26, 46, 0.95)',
                    titleFont: {
                        family: 'Montserrat',
                        size: 12,
                        weight: '600'
                    },
                    bodyFont: {
                        family: 'Poppins',
                        size: 11
                    },
                    padding: 15,
                    cornerRadius: 10,
                    callbacks: {
                        label: function(context) {
                            return `Risk: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: 'Poppins',
                            size: 11
                        },
                        color: 'var(--gray-dark)'
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            family: 'Poppins',
                            size: 11
                        },
                        color: 'var(--gray-dark)',
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'nearest'
            }
        }
    });
}

// Initialize Risk Heatmap
function initializeRiskHeatmap() {
    const heatmapContainer = document.getElementById('riskHeatmap');
    if (!heatmapContainer) return;
    
    // Create heatmap canvas if it doesn't exist
    if (!heatmapContainer.querySelector('canvas')) {
        heatmapContainer.innerHTML = '<canvas id="riskHeatmapChart"></canvas>';
    }
    
    const ctx = document.getElementById('riskHeatmapChart');
    if (!ctx) return;
    
    if (window.riskHeatmapChart) {
        window.riskHeatmapChart.destroy();
    }
    
    // Create heatmap data
    const heatmapData = generateHeatmapData();
    
    window.riskHeatmapChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Risk Distribution',
                data: heatmapData,
                backgroundColor: 'rgba(114, 9, 183, 0.6)',
                borderColor: 'rgba(114, 9, 183, 1)',
                borderWidth: 1,
                pointRadius: 8,
                pointHoverRadius: 12
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Age: ${context.parsed.x}, Risk: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Age'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Risk Score (%)'
                    },
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// Generate Heatmap Data
function generateHeatmapData() {
    return filteredHistory.map(item => ({
        x: item.user_data?.Age || 30,
        y: item.risk_percentage || 50
    }));
}

// Update Charts with Animation
function updateCharts() {
    updateDistributionChart();
    updateTrendChart();
    updateRiskHeatmap();
}

// Update Distribution Chart with Animation
function updateDistributionChart() {
    if (!window.riskDistributionChart) return;
    
    const lowRisk = filteredHistory.filter(item => (item.risk_percentage || 0) < 30).length;
    const mediumRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 30 && (item.risk_percentage || 0) < 70).length;
    const highRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 70).length;
    
    // Animate chart update
    window.riskDistributionChart.data.datasets[0].data = [lowRisk, mediumRisk, highRisk];
    window.riskDistributionChart.update('active');
}

// Update Trend Chart with Animation
function updateTrendChart() {
    if (!window.riskTrendChart) return;
    
    const period = document.getElementById('trendPeriod')?.value || 'month';
    const periodData = getTrendData(period);
    
    window.riskTrendChart.data.labels = periodData.labels;
    window.riskTrendChart.data.datasets[0].data = periodData.values;
    window.riskTrendChart.update('active');
}

// Get Trend Data
function getTrendData(period) {
    const now = new Date();
    let startDate = new Date();
    
    switch (period) {
        case 'week': startDate.setDate(now.getDate() - 7); break;
        case 'month': startDate.setMonth(now.getMonth() - 1); break;
        case 'quarter': startDate.setMonth(now.getMonth() - 3); break;
        case 'year': startDate.setFullYear(now.getFullYear() - 1); break;
    }
    
    const periodData = filteredHistory.filter(item => {
        const itemDate = new Date(item.timestamp);
        return itemDate >= startDate && itemDate <= now;
    });
    
    // Group by date
    const groupedData = {};
    periodData.forEach(item => {
        const date = new Date(item.timestamp).toLocaleDateString();
        if (!groupedData[date]) {
            groupedData[date] = { total: 0, count: 0 };
        }
        groupedData[date].total += item.risk_percentage || 0;
        groupedData[date].count += 1;
    });
    
    const labels = Object.keys(groupedData).sort();
    const values = labels.map(date => {
        const group = groupedData[date];
        return group.count > 0 ? Math.round(group.total / group.count) : 0;
    });
    
    return { labels, values };
}

// Update Risk Heatmap
function updateRiskHeatmap() {
    if (!window.riskHeatmapChart) return;
    
    const heatmapData = generateHeatmapData();
    window.riskHeatmapChart.data.datasets[0].data = heatmapData;
    window.riskHeatmapChart.update();
}

// Initialize Interactive Elements
function initializeInteractiveElements() {
    // Enhanced view toggle with animation
    const viewToggleBtns = document.querySelectorAll('.view-toggle-btn');
    viewToggleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const view = this.getAttribute('data-view');
            
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
            
            // Switch view with animation
            switchViewWithAnimation(view);
        });
    });
    
    // Enhanced search with animation
    const searchInput = document.getElementById('historySearch');
    if (searchInput) {
        searchInput.addEventListener('input', ThyroScan.debounce(() => {
            // Show search animation
            searchInput.classList.add('searching');
            
            applyFilters();
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
            
            setTimeout(() => searchInput.classList.remove('searching'), 500);
        }, 300));
    }
    
    // Enhanced filter selects
    const filterSelects = document.querySelectorAll('.filter-select, .small-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            // Add selection animation
            this.classList.add('selected');
            setTimeout(() => this.classList.remove('selected'), 300);
            
            applyFilters();
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
        });
    });
    
    // Add tooltips to all buttons
    addTooltips();
}

// Add Tooltips
function addTooltips() {
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(el => {
        el.addEventListener('mouseenter', showTooltip);
        el.addEventListener('mouseleave', hideTooltip);
    });
}

// Show Tooltip
function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'enhanced-tooltip';
    tooltip.textContent = this.getAttribute('title');
    document.body.appendChild(tooltip);
    
    const rect = this.getBoundingClientRect();
    tooltip.style.left = `${rect.left + rect.width / 2}px`;
    tooltip.style.top = `${rect.top - 10}px`;
    tooltip.style.transform = 'translateX(-50%) translateY(-100%)';
    
    this.tooltip = tooltip;
}

// Hide Tooltip
function hideTooltip() {
    if (this.tooltip) {
        this.tooltip.remove();
        this.tooltip = null;
    }
}

// Switch View with Animation
function switchViewWithAnimation(view) {
    if (currentView === view) return;
    
    // Add transition animation
    const oldView = document.getElementById(currentView === 'list' ? 'listView' : 'gridView');
    const newView = document.getElementById(view === 'list' ? 'listView' : 'gridView');
    
    if (oldView && newView) {
        oldView.style.opacity = '0';
        oldView.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            currentView = view;
            updateHistoryDisplay();
            
            newView.style.opacity = '1';
            newView.style.transform = 'translateY(0)';
        }, 300);
    } else {
        currentView = view;
        updateHistoryDisplay();
    }
    
    // Update active button
    document.querySelectorAll('.view-toggle-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-view') === view);
    });
}

// Initialize Filters with Enhanced UI
function initializeFilters() {
    // Set default values with animation
    const filterRisk = document.getElementById('filterRisk');
    const filterDate = document.getElementById('filterDate');
    const filterPrediction = document.getElementById('filterPrediction');
    
    [filterRisk, filterDate, filterPrediction].forEach(filter => {
        if (filter) {
            filter.value = '';
            filter.classList.add('filter-initialized');
            setTimeout(() => filter.classList.remove('filter-initialized'), 1000);
        }
    });
    
    // Add clear filters button
    addClearFiltersButton();
}

// Add Clear Filters Button
function addClearFiltersButton() {
    const filterGroup = document.querySelector('.filter-group');
    if (!filterGroup || document.getElementById('clearFiltersBtn')) return;
    
    const clearBtn = document.createElement('button');
    clearBtn.id = 'clearFiltersBtn';
    clearBtn.className = 'btn-icon clear-filters';
    clearBtn.innerHTML = '<i class="fas fa-times"></i>';
    clearBtn.title = 'Clear all filters';
    clearBtn.addEventListener('click', clearAllFilters);
    
    filterGroup.appendChild(clearBtn);
}

// Clear All Filters
function clearAllFilters() {
    // Reset filter values
    document.getElementById('filterRisk').value = '';
    document.getElementById('filterDate').value = '';
    document.getElementById('filterPrediction').value = '';
    document.getElementById('historySearch').value = '';
    
    // Add animation
    const filterGroup = document.querySelector('.filter-group');
    filterGroup.classList.add('filters-cleared');
    setTimeout(() => filterGroup.classList.remove('filters-cleared'), 500);
    
    // Apply filters
    applyFilters();
    updateHistoryDisplay();
    updateSummaryStats();
    updateCharts();
    
    showNotification('All filters cleared', 'success');
}

// Initialize Modals with Enhanced UI
function initializeModals() {
    // Detail modal with enhanced animations
    const detailModal = document.getElementById('detailModal');
    if (detailModal) {
        // Enhanced overlay click
        const overlay = detailModal.querySelector('.modal-overlay');
        if (overlay) {
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    closeDetailModalWithAnimation();
                }
            });
        }
        
        // Enhanced close button
        const closeButton = document.getElementById('closeDetailModal');
        if (closeButton) {
            closeButton.addEventListener('click', closeDetailModalWithAnimation);
        }
        
        // Escape key with animation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !detailModal.classList.contains('hidden')) {
                closeDetailModalWithAnimation();
            }
        });
    }
    
    // Confirmation modal with enhanced UI
    const confirmModal = document.getElementById('clearConfirmModal');
    if (confirmModal) {
        const overlay = confirmModal.querySelector('.modal-overlay');
        if (overlay) {
            overlay.addEventListener('click', closeConfirmModalWithAnimation);
        }
        
        const cancelBtn = document.getElementById('cancelClear');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', closeConfirmModalWithAnimation);
        }
    }
    
    // Add tab animations to detail modal
    setupModalTabs();
}

// Setup Modal Tabs
function setupModalTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Update active tab with animation
            tabBtns.forEach(b => {
                b.classList.remove('active');
                b.style.transform = 'scale(1)';
            });
            
            this.classList.add('active');
            this.style.transform = 'scale(1.05)';
            
            // Show corresponding content with animation
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `${tabId}Tab`) {
                    content.classList.add('active');
                    content.style.animation = 'fadeInUp 0.3s ease';
                }
            });
        });
    });
}

// Setup History Event Listeners with Enhanced UX
function setupHistoryEventListeners() {
    // Enhanced refresh button with animation
    const refreshBtn = document.getElementById('refreshHistory');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            // Add spin animation
            refreshBtn.classList.add('refreshing');
            refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            refreshBtn.disabled = true;
            
            // Refresh with progress animation
            loadHistory().finally(() => {
                setTimeout(() => {
                    refreshBtn.classList.remove('refreshing');
                    refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
                    refreshBtn.disabled = false;
                    
                    // Show success animation
                    refreshBtn.classList.add('refresh-success');
                    setTimeout(() => refreshBtn.classList.remove('refresh-success'), 1000);
                }, 500);
            });
        });
    }
    
    // Enhanced export button
    const exportBtn = document.getElementById('exportHistory');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            exportBtn.classList.add('exporting');
            setTimeout(() => exportBtn.classList.remove('exporting'), 1000);
            exportHistory();
        });
    }
    
    // Enhanced clear button
    const clearBtn = document.getElementById('clearHistory');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            // Add warning animation
            clearBtn.classList.add('warning-pulse');
            setTimeout(() => clearBtn.classList.remove('warning-pulse'), 1000);
            
            showConfirmModal();
        });
    }
    
    // Enhanced confirm clear button
    const confirmClearBtn = document.getElementById('confirmClear');
    if (confirmClearBtn) {
        confirmClearBtn.addEventListener('click', () => {
            confirmClearBtn.classList.add('processing');
            confirmClearBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Clearing...';
            
            setTimeout(() => {
                clearAllHistory();
                confirmClearBtn.classList.remove('processing');
                confirmClearBtn.innerHTML = 'Yes, Clear All';
            }, 500);
        });
    }
    
    // Enhanced pagination
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    
    if (prevPageBtn) {
        prevPageBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                updateHistoryDisplayWithPageAnimation('left');
            }
        });
    }
    
    if (nextPageBtn) {
        nextPageBtn.addEventListener('click', () => {
            const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                updateHistoryDisplayWithPageAnimation('right');
            }
        });
    }
    
    // Enhanced chart period changes
    const distributionPeriod = document.getElementById('distributionPeriod');
    const trendPeriod = document.getElementById('trendPeriod');
    
    if (distributionPeriod) {
        distributionPeriod.addEventListener('change', function() {
            this.classList.add('chart-updating');
            setTimeout(() => this.classList.remove('chart-updating'), 500);
            updateDistributionChart();
        });
    }
    
    if (trendPeriod) {
        trendPeriod.addEventListener('change', function() {
            this.classList.add('chart-updating');
            setTimeout(() => this.classList.remove('chart-updating'), 500);
            updateTrendChart();
        });
    }
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
}

// Update History Display with Page Animation
function updateHistoryDisplayWithPageAnimation(direction) {
    const content = document.getElementById(currentView === 'list' ? 'listView' : 'gridView');
    if (!content) return;
    
    // Add slide animation
    content.style.transform = `translateX(${direction === 'left' ? '20px' : '-20px'})`;
    content.style.opacity = '0.5';
    
    setTimeout(() => {
        updateHistoryDisplay();
        content.style.transform = 'translateX(0)';
        content.style.opacity = '1';
        content.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
        
        setTimeout(() => {
            content.style.transition = '';
        }, 300);
    }, 150);
}

// Add Keyboard Shortcuts
function addKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl + F to focus search
        if (e.ctrlKey && e.key === 'f') {
            e.preventDefault();
            const searchInput = document.getElementById('historySearch');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // Arrow keys for pagination
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            const prevPageBtn = document.getElementById('prevPage');
            if (prevPageBtn && !prevPageBtn.disabled) {
                prevPageBtn.click();
            }
        }
        
        if (e.key === 'ArrowRight') {
            e.preventDefault();
            const nextPageBtn = document.getElementById('nextPage');
            if (nextPageBtn && !nextPageBtn.disabled) {
                nextPageBtn.click();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const detailModal = document.getElementById('detailModal');
            const confirmModal = document.getElementById('clearConfirmModal');
            
            if (!detailModal.classList.contains('hidden')) {
                closeDetailModalWithAnimation();
            } else if (!confirmModal.classList.contains('hidden')) {
                closeConfirmModalWithAnimation();
            }
        }
    });
}

// Show Enhanced History Details
function showEnhancedHistoryDetails(item) {
    const modal = document.getElementById('detailModal');
    if (!modal) return;
    
    // Add opening animation
    modal.classList.add('modal-opening');
    
    // Populate modal with enhanced UI
    populateEnhancedDetailModal(item);
    
    // Show modal with animation
    setTimeout(() => {
        modal.classList.remove('hidden');
        modal.classList.add('active');
        modal.classList.remove('modal-opening');
        document.body.style.overflow = 'hidden';
    }, 100);
    
    // Add background blur
    document.body.classList.add('modal-open');
}

// Populate Enhanced Detail Modal
function populateEnhancedDetailModal(item) {
    // Basic info with animations
    const date = new Date(item.timestamp);
    const riskPercentage = item.risk_percentage || 0;
    
    // Animate risk score counter
    const riskPercentageElement = document.getElementById('detailRiskPercentage');
    if (riskPercentageElement) {
        animateCounter(riskPercentageElement, 0, riskPercentage, 1500);
    }
    
    // Update other elements
    document.getElementById('detailPrediction').textContent = item.prediction || 'N/A';
    document.getElementById('detailDate').textContent = `Date: ${date.toLocaleString()}`;
    document.getElementById('detailRiskLevel').textContent = getRiskLevel(riskPercentage);
    document.getElementById('detailConfidence').textContent = item.confidence || '85% confidence';
    
    // Animate risk circle
    const riskCircle = modal.querySelector('.circle-progress svg circle:last-child');
    if (riskCircle) {
        const circumference = 339;
        const offset = circumference - (riskPercentage / 100) * circumference;
        riskCircle.style.strokeDashoffset = offset;
        riskCircle.style.transition = 'stroke-dashoffset 1.5s ease';
    }
    
    // Populate parameters with animation
    populateParametersWithAnimation(item);
    
    // Populate recommendations
    const recommendationsList = document.getElementById('detailRecommendations');
    if (recommendationsList) {
        const recommendations = item.recommendations || generateRecommendations(riskPercentage);
        recommendationsList.innerHTML = recommendations.map((rec, index) => `
            <li style="animation-delay: ${index * 0.1}s">
                <i class="fas fa-check-circle"></i>
                <span>${rec}</span>
            </li>
        `).join('');
    }
    
    // Setup download and print buttons
    const downloadBtn = document.getElementById('downloadReport');
    const printBtn = document.getElementById('printReport');
    
    if (downloadBtn) {
        downloadBtn.onclick = () => {
            downloadBtn.classList.add('downloading');
            setTimeout(() => {
                downloadHistoryReport(item);
                downloadBtn.classList.remove('downloading');
            }, 300);
        };
    }
    
    if (printBtn) {
        printBtn.onclick = () => {
            printBtn.classList.add('printing');
            setTimeout(() => {
                printHistoryReport(item);
                printBtn.classList.remove('printing');
            }, 300);
        };
    }
}

// Populate Parameters with Animation
function populateParametersWithAnimation(item) {
    const parameters = {
        'detailAge': `${item.user_data?.Age || 'N/A'} years`,
        'detailGender': item.user_data?.Gender_Male === 1 ? 'Male' : 'Female',
        'detailTSH': `${item.user_data?.TSH_Level || 'N/A'} mIU/L`,
        'detailT3': `${item.user_data?.T3_Level || 'N/A'} pg/mL`,
        'detailT4': `${item.user_data?.T4_Level || 'N/A'} μg/dL`,
        'detailNodule': `${item.user_data?.Nodule_Size || 'N/A'} cm`,
        'detailCancerRisk': item.user_data?.Thyroid_Cancer_Risk || 'N/A'
    };
    
    Object.entries(parameters).forEach(([id, value], index) => {
        const element = document.getElementById(id);
        if (element) {
            element.style.animationDelay = `${index * 0.05}s`;
            element.classList.add('parameter-appear');
            setTimeout(() => {
                element.textContent = value;
                element.classList.remove('parameter-appear');
            }, 100);
        }
    });
    
    // Populate risk factors
    const factorsList = document.getElementById('detailFactorsList');
    if (factorsList) {
        const riskFactors = [
            { id: 'Family_History', label: 'Family History', checked: item.user_data?.Family_History },
            { id: 'Radiation_Exposure', label: 'Radiation Exposure', checked: item.user_data?.Radiation_Exposure },
            { id: 'Iodine_Deficiency', label: 'Iodine Deficiency', checked: item.user_data?.Iodine_Deficiency },
            { id: 'Smoking', label: 'Smoking', checked: item.user_data?.Smoking },
            { id: 'Obesity', label: 'Obesity', checked: item.user_data?.Obesity },
            { id: 'Diabetes', label: 'Diabetes', checked: item.user_data?.Diabetes }
        ];
        
        const activeFactors = riskFactors.filter(f => f.checked);
        
        if (activeFactors.length > 0) {
            factorsList.innerHTML = activeFactors.map((f, index) => `
                <div class="factor-item" style="animation-delay: ${index * 0.1}s">
                    <i class="fas fa-check-circle"></i>
                    <span>${f.label}</span>
                </div>
            `).join('');
        } else {
            factorsList.innerHTML = '<div class="no-factors">No risk factors recorded</div>';
        }
    }
}

// Close Detail Modal with Animation
function closeDetailModalWithAnimation() {
    const modal = document.getElementById('detailModal');
    if (!modal) return;
    
    modal.classList.add('modal-closing');
    
    setTimeout(() => {
        modal.classList.remove('active');
        modal.classList.add('hidden');
        modal.classList.remove('modal-closing');
        document.body.style.overflow = '';
        document.body.classList.remove('modal-open');
    }, 300);
}

// Show Confirm Modal with Animation
function showConfirmModal() {
    const modal = document.getElementById('clearConfirmModal');
    if (!modal) return;
    
    modal.classList.add('modal-opening');
    
    setTimeout(() => {
        modal.classList.remove('hidden');
        modal.classList.add('active');
        modal.classList.remove('modal-opening');
        document.body.style.overflow = 'hidden';
        document.body.classList.add('modal-open');
    }, 100);
}

// Close Confirm Modal with Animation
function closeConfirmModalWithAnimation() {
    const modal = document.getElementById('clearConfirmModal');
    if (!modal) return;
    
    modal.classList.add('modal-closing');
    
    setTimeout(() => {
        modal.classList.remove('active');
        modal.classList.add('hidden');
        modal.classList.remove('modal-closing');
        document.body.style.overflow = '';
        document.body.classList.remove('modal-open');
    }, 300);
}

// Enhanced Export History
function exportHistory() {
    if (filteredHistory.length === 0) {
        showNotification('No history data to export', 'warning');
        return;
    }
    
    // Create enhanced export data
    const exportData = filteredHistory.map(item => ({
        Date: new Date(item.timestamp).toLocaleString(),
        'Risk Score': `${item.risk_percentage}%`,
        Prediction: item.prediction,
        Confidence: item.confidence,
        'Risk Level': getRiskLevel(item.risk_percentage),
        Age: item.user_data?.Age,
        Gender: item.user_data?.Gender_Male === 1 ? 'Male' : 'Female',
        'Nodule Size': item.user_data?.Nodule_Size,
        'TSH Level': item.user_data?.TSH_Level,
        'T3 Level': item.user_data?.T3_Level,
        'T4 Level': item.user_data?.T4_Level
    }));
    
    // Convert to CSV
    const headers = Object.keys(exportData[0]);
    const csv = [
        headers.join(','),
        ...exportData.map(row => headers.map(header => `"${row[header]}"`).join(','))
    ].join('\n');
    
    // Add BOM for UTF-8
    const BOM = '\uFEFF';
    const blob = new Blob([BOM + csv], { type: 'text/csv;charset=utf-8' });
    
    // Create enhanced download link
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const filename = `thyroscan_history_${new Date().toISOString().split('T')[0]}_${filteredHistory.length}_records.csv`;
    a.download = filename;
    
    // Add click animation
    document.body.appendChild(a);
    a.click();
    
    // Clean up
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 100);
    
    showNotification(`Exported ${exportData.length} records to ${filename}`, 'success');
}

// Enhanced Clear All History
function clearAllHistory() {
    // Show confirmation animation
    showNotification('Clearing history...', 'info');
    
    // Clear local data with animation
    const clearAnimation = () => {
        historyData = [];
        filteredHistory = [];
        currentPage = 1;
        
        // Update display with fade out animation
        const items = document.querySelectorAll('.history-item, .history-card');
        items.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.05}s`;
            item.style.animation = 'fadeOut 0.3s ease forwards';
        });
        
        setTimeout(() => {
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
            
            // Show success animation
            showNotification('All history has been cleared', 'success');
            
            // Close modal
            closeConfirmModalWithAnimation();
        }, 500);
    };
    
    // Try to clear server data first
    clearServerHistory().finally(clearAnimation);
}

// Enhanced Show Notification
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icons = {
        'success': 'fa-check-circle',
        'error': 'fa-exclamation-circle',
        'warning': 'fa-exclamation-triangle',
        'info': 'fa-info-circle'
    };
    
    notification.innerHTML = `
        <i class="fas ${icons[type] || 'fa-info-circle'}"></i>
        <span class="notification-message">${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Add animation
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Auto remove
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Initialize enhanced CSS styles
function initializeEnhancedStyles() {
    const style = document.createElement('style');
    style.textContent = `
        /* Enhanced animations */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(20px); }
        }
        
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes ripple {
            0% { transform: scale(0); opacity: 1; }
            100% { transform: scale(4); opacity: 0; }
        }
        
        @keyframes glow {
            0%, 100% { box-shadow: 0 0 5px var(--glow-color); }
            50% { box-shadow: 0 0 20px var(--glow-color); }
        }
        
        /* Enhanced history item animations */
        .history-item.enhanced,
        .history-card.enhanced {
            animation: fadeInUp 0.5s ease forwards;
            opacity: 0;
        }
        
        .fade-in-up {
            animation: fadeInUp 0.5s ease forwards;
        }
        
        .slide-in-left {
            animation: slideInLeft 0.5s ease forwards;
        }
        
        .slide-in-right {
            animation: slideInRight 0.5s ease forwards;
        }
        
        /* Pulse animation for risk indicators */
        .pulse-animation {
            position: relative;
        }
        
        .avatar-pulse {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 2px solid var(--pulse-color);
            animation: pulse 2s infinite;
        }
        
        /* Ripple effect */
        .ripple-effect {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 5px;
            height: 5px;
            border-radius: 50%;
            animation: ripple 0.6s linear;
            z-index: 0;
        }
        
        /* Glowing effect for high risk */
        .risk-circle-glow {
            position: relative;
        }
        
        .risk-circle-glow::after {
            content: '';
            position: absolute;
            top: -10px;
            left: -10px;
            right: -10px;
            bottom: -10px;
            border-radius: 50%;
            background: var(--glow-color);
            opacity: var(--glow-opacity, 0);
            filter: blur(20px);
            transition: opacity 0.3s ease;
        }
        
        /* Enhanced tooltips */
        .enhanced-tooltip {
            position: fixed;
            background: rgba(26, 26, 46, 0.95);
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
            font-family: 'Poppins', sans-serif;
            z-index: 9999;
            white-space: nowrap;
            pointer-events: none;
            animation: fadeInUp 0.2s ease;
        }
        
        /* Loading animations */
        .loading-spinner.enhanced {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }
        
        .spinner-circle {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(114, 9, 183, 0.1);
            border-top-color: rgba(114, 9, 183, 1);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .table-loading .loading-row {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            animation: pulse 1.5s infinite;
        }
        
        .table-loading .loading-cell {
            flex: 1;
            height: 40px;
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
            border-radius: 8px;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* Notification styles */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 10px;
            background: white;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 9999;
            transform: translateX(100%);
            opacity: 0;
            transition: all 0.3s ease;
        }
        
        .notification.show {
            transform: translateX(0);
            opacity: 1;
        }
        
        .notification-success {
            border-left: 4px solid #2ED573;
        }
        
        .notification-error {
            border-left: 4px solid #FF4757;
        }
        
        .notification-warning {
            border-left: 4px solid #FFA502;
        }
        
        .notification-info {
            border-left: 4px solid #2D5BFF;
        }
        
        /* Background particles */
        .background-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            background: rgba(114, 9, 183, 0.1);
            border-radius: 50%;
            animation: float 20s infinite linear;
        }
        
        @keyframes float {
            0% { transform: translateY(0) rotate(0deg); }
            100% { transform: translateY(-1000px) rotate(720deg); }
        }
    `;
    document.head.appendChild(style);
}

// Initialize enhanced styles
initializeEnhancedStyles();

// Initialize history page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('historyTableBody')) {
        setTimeout(() => {
            initializeHistoryPage();
        }, 100);
    }
});

// Export enhanced functions
window.EnhancedHistory = {
    initializeHistoryPage,
    loadHistory,
    showEnhancedHistoryDetails,
    exportHistory,
    clearAllHistory,
    showNotification
};