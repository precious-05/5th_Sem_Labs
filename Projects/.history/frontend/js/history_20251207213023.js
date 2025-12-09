// ============================================
// ENHANCED HISTORY.JS - Modern History Page
// ============================================

// Global variables
let historyData = [];
let filteredHistory = [];
let currentPage = 1;
let itemsPerPage = 8;
let currentView = 'list';
let sortColumn = 'timestamp';
let sortDirection = 'desc';
let distributionChart = null;
let trendChart = null;

// Modern configuration
const HISTORY_CONFIG = {
    ANIMATION_DELAY: 50,
    ITEMS_PER_PAGE: 8,
    CHART_UPDATE_DELAY: 500,
    SEARCH_DEBOUNCE: 300
};

// Initialize History Page
function initializeHistoryPage() {
    console.log('📊 Modern history page initialized');
    
    // Apply modern styles
    applyModernHistoryStyles();
    
    // Initialize with animations
    initializeWithAnimations();
    
    // Initialize page elements
    initializePageElements();
    
    // Load prediction history
    loadHistory();
    
    // Setup event listeners
    setupHistoryEventListeners();
    
    // Initialize modals
    initializeModals();
}

// Apply Modern Styles
function applyModernHistoryStyles() {
    const modernCSS = `
        /* Enhanced History Styles */
        .history-item {
            background: var(--white);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            border: 1px solid var(--gray-light);
            transition: var(--transition-normal);
            position: relative;
            overflow: hidden;
        }
        
        .history-item:hover {
            transform: translateY(-4px);
            border-color: var(--primary);
            box-shadow: var(--shadow-lg);
        }
        
        .history-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--gradient-primary);
            transform: scaleY(0);
            transform-origin: top;
            transition: transform var(--transition-normal);
        }
        
        .history-item:hover::before {
            transform: scaleY(1);
        }
        
        .history-card {
            background: var(--white);
            border-radius: var(--radius-lg);
            padding: var(--space-xl);
            box-shadow: var(--shadow-md);
            border: 1px solid var(--gray-light);
            transition: var(--transition-normal);
            height: 100%;
        }
        
        .history-card:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-xl);
            border-color: var(--primary);
        }
        
        /* Modern animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .fade-in {
            animation: fadeInUp 0.6s ease-out forwards;
            opacity: 0;
        }
        
        /* Enhanced risk circles */
        .risk-circle-small {
            position: relative;
            width: 80px;
            height: 80px;
            margin: 0 auto;
        }
        
        .risk-circle-small .circle-progress {
            transform: rotate(-90deg);
        }
        
        .risk-circle-small svg circle {
            transition: stroke-dashoffset 1.5s ease;
        }
        
        /* Modern badges */
        .prediction-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: var(--radius-full);
            font-size: 0.85rem;
            font-weight: 600;
            transition: var(--transition-normal);
        }
        
        .prediction-badge.benign {
            background: rgba(6, 214, 160, 0.1);
            color: var(--success);
            border: 1px solid rgba(6, 214, 160, 0.2);
        }
        
        .prediction-badge.malignant {
            background: rgba(239, 71, 111, 0.1);
            color: var(--danger);
            border: 1px solid rgba(239, 71, 111, 0.2);
        }
        
        .prediction-badge:hover {
            transform: scale(1.05);
            box-shadow: var(--shadow-sm);
        }
        
        /* Enhanced tooltips */
        [title] {
            position: relative;
        }
        
        [title]:hover::after {
            content: attr(title);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: var(--dark);
            color: var(--white);
            padding: 8px 12px;
            border-radius: var(--radius-sm);
            font-size: 0.85rem;
            white-space: nowrap;
            z-index: 1000;
            margin-bottom: 8px;
            opacity: 0;
            animation: fadeIn 0.2s ease-out forwards;
        }
        
        /* Loading animation */
        .loading-spinner {
            animation: spin 1.5s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    
    const style = document.createElement('style');
    style.id = 'modern-history-styles';
    style.textContent = modernCSS;
    document.head.appendChild(style);
}

// Initialize with Animations
function initializeWithAnimations() {
    // Add loading animation
    const mainContent = document.querySelector('.history-main');
    if (mainContent) {
        mainContent.style.opacity = '0';
        mainContent.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            mainContent.style.transition = 'all 0.6s ease-out';
            mainContent.style.opacity = '1';
            mainContent.style.transform = 'translateY(0)';
        }, 100);
    }
}

// Initialize Page Elements
function initializePageElements() {
    // Update current year
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
    
    // Initialize empty state
    const emptyState = document.getElementById('historyEmpty');
    if (emptyState) {
        emptyState.classList.add('hidden');
    }
    
    // Initialize loading state
    const loadingState = document.getElementById('historyLoading');
    if (loadingState) {
        loadingState.classList.remove('hidden');
    }
    
    // Initialize charts containers
    createChartContainers();
}

// Load Prediction History
async function loadHistory() {
    try {
        showLoadingState();
        
        const limit = 100;
        const response = await fetch(`${window.API_BASE_URL || 'http://localhost:8000'}/history?limit=${limit}`);
        
        if (response.ok) {
            const data = await response.json();
            historyData = data.history || [];
            
            if (historyData.length === 0) {
                historyData = generateDemoHistory();
                showNotification('Showing demo history data', 'info', 'Demo Mode');
            }
            
            processHistoryData();
            updateHistoryDisplay();
            updateSummaryStats();
            initializeCharts();
            updateCharts();
            
        } else {
            throw new Error('Failed to load history');
        }
        
    } catch (error) {
        console.error('Error loading history:', error);
        
        // Load demo data if API fails
        historyData = generateDemoHistory();
        processHistoryData();
        updateHistoryDisplay();
        updateSummaryStats();
        initializeCharts();
        updateCharts();
        
        showNotification('Using demo data - API not available', 'warning', 'Offline Mode');
    } finally {
        hideLoadingState();
    }
}

// Show Loading State
function showLoadingState() {
    const loadingState = document.getElementById('historyLoading');
    const mainContent = document.querySelector('.history-main > .container');
    
    if (loadingState) {
        loadingState.classList.remove('hidden');
    }
    
    if (mainContent) {
        mainContent.style.opacity = '0.5';
        mainContent.style.pointerEvents = 'none';
    }
}

// Hide Loading State
function hideLoadingState() {
    const loadingState = document.getElementById('historyLoading');
    const mainContent = document.querySelector('.history-main > .container');
    
    if (loadingState) {
        loadingState.classList.add('hidden');
    }
    
    if (mainContent) {
        mainContent.style.opacity = '1';
        mainContent.style.pointerEvents = 'all';
    }
}

// Generate Demo History Data
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
        
        demoData.push({
            id: `demo_${i + 1}`,
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

// Process History Data
function processHistoryData() {
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

// Apply Filters
function applyFilters() {
    const riskFilter = document.getElementById('filterRisk')?.value;
    const dateFilter = document.getElementById('filterDate')?.value;
    const predictionFilter = document.getElementById('filterPrediction')?.value;
    const searchTerm = document.getElementById('historySearch')?.value.toLowerCase();
    
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
    
    updatePagination();
}

// Update History Display
function updateHistoryDisplay() {
    if (currentView === 'list') {
        updateListView();
    } else {
        updateGridView();
    }
    
    updateEmptyState();
    updatePaginationControls();
}

// Update List View
function updateListView() {
    const tableBody = document.getElementById('historyTableBody');
    if (!tableBody) return;
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    tableBody.innerHTML = '';
    
    pageItems.forEach((item, index) => {
        const row = createHistoryRow(item, startIndex + index);
        tableBody.appendChild(row);
    });
}

// Create History Row
function createHistoryRow(item, index) {
    const row = document.createElement('div');
    row.className = 'history-item fade-in';
    row.style.animationDelay = `${index * HISTORY_CONFIG.ANIMATION_DELAY}ms`;
    
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
        <div class="history-date">
            <div class="date-day">${date.toLocaleDateString('en-US', { weekday: 'short' })}</div>
            <div class="date-full">${date.toLocaleDateString()}</div>
            <div class="date-time">${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
        </div>
        
        <div class="history-patient">
            <div class="patient-avatar">
                <i class="fas fa-user${gender === 'Male' ? '' : '-female'}"></i>
            </div>
            <div class="patient-info">
                <h4>Patient ${index + 1}</h4>
                <p>${age} yrs • ${gender}</p>
            </div>
        </div>
        
        <div class="history-risk">
            <div class="risk-score">${riskPercentage}%</div>
            <div class="risk-level ${getRiskLevelClass(riskPercentage)}">
                ${getRiskLevel(riskPercentage)}
            </div>
        </div>
        
        <div class="history-prediction">
            <span class="prediction-badge ${prediction === 'Malignant' ? 'malignant' : 'benign'}">
                <i class="fas fa-${prediction === 'Malignant' ? 'exclamation-triangle' : 'check-circle'}"></i>
                ${prediction}
            </span>
            <div class="prediction-confidence">
                ${item.confidence || '85%'} confidence
            </div>
        </div>
        
        <div class="history-factors">
            <div class="factors-tags">
                ${riskFactors.map(factor => `
                    <span class="factor-tag">${factor}</span>
                `).join('')}
            </div>
        </div>
        
        <div class="history-actions">
            <button class="btn-view" data-id="${item.id}" title="View Details">
                <i class="fas fa-eye"></i>
            </button>
            <button class="btn-delete" data-id="${item.id}" title="Delete Record">
                <i class="fas fa-trash-alt"></i>
            </button>
        </div>
    `;
    
    // Add event listeners with animations
    const viewBtn = row.querySelector('.btn-view');
    const deleteBtn = row.querySelector('.btn-delete');
    
    if (viewBtn) {
        viewBtn.addEventListener('click', (e) => {
            e.currentTarget.style.transform = 'scale(0.9)';
            setTimeout(() => {
                e.currentTarget.style.transform = '';
                showHistoryDetails(item);
            }, 150);
        });
    }
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
            e.currentTarget.style.transform = 'scale(0.9)';
            setTimeout(() => {
                e.currentTarget.style.transform = '';
                confirmDeleteHistory(item.id, index);
            }, 150);
        });
    }
    
    // Add hover effect to entire row
    row.addEventListener('mouseenter', () => {
        row.style.transform = 'translateY(-4px)';
    });
    
    row.addEventListener('mouseleave', () => {
        row.style.transform = 'translateY(0)';
    });
    
    return row;
}

// Update Grid View
function updateGridView() {
    const gridView = document.getElementById('historyGrid');
    if (!gridView) return;
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    gridView.innerHTML = '';
    
    pageItems.forEach((item, index) => {
        const card = createHistoryCard(item, startIndex + index);
        gridView.appendChild(card);
    });
}

// Create History Card
function createHistoryCard(item, index) {
    const card = document.createElement('div');
    card.className = 'history-card fade-in';
    card.style.animationDelay = `${index * HISTORY_CONFIG.ANIMATION_DELAY}ms`;
    
    const date = new Date(item.timestamp);
    const riskPercentage = item.risk_percentage || 0;
    const prediction = item.prediction || 'N/A';
    
    card.innerHTML = `
        <div class="card-header">
            <div class="card-date">
                ${date.toLocaleDateString()} • ${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </div>
            <div class="card-actions">
                <button class="btn-view" data-id="${item.id}" title="View Details">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn-delete" data-id="${item.id}" title="Delete Record">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </div>
        </div>
        
        <div class="card-risk">
            <div class="risk-circle-small">
                <div class="circle-progress">
                    <svg width="80" height="80">
                        <circle cx="40" cy="40" r="35" fill="none" stroke="#e0e0e0" stroke-width="4"/>
                        <circle cx="40" cy="40" r="35" fill="none" stroke="${getRiskColor(riskPercentage)}" 
                                stroke-width="4" stroke-linecap="round" 
                                stroke-dasharray="220" stroke-dashoffset="${220 - (riskPercentage / 100) * 220}"/>
                    </svg>
                    <div class="score-content">
                        <span class="score-value">${riskPercentage}%</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card-prediction">
            <span class="prediction-badge ${prediction === 'Malignant' ? 'malignant' : 'benign'}">
                <i class="fas fa-${prediction === 'Malignant' ? 'exclamation-triangle' : 'check-circle'}"></i>
                ${prediction}
            </span>
        </div>
        
        <div class="card-details">
            <div class="detail-item">
                <span class="detail-label">Age:</span>
                <span class="detail-value">${item.user_data?.Age || 'N/A'} yrs</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Gender:</span>
                <span class="detail-value">${item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Nodule:</span>
                <span class="detail-value">${item.user_data?.Nodule_Size || 'N/A'} cm</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Confidence:</span>
                <span class="detail-value">${item.confidence || '85%'}</span>
            </div>
        </div>
        
        <div class="card-footer">
            <button class="btn-view-full" data-id="${item.id}">
                <i class="fas fa-chart-bar"></i>
                View Full Report
            </button>
        </div>
    `;
    
    // Add event listeners with animations
    const viewBtn = card.querySelector('.btn-view-full');
    const deleteBtn = card.querySelector('.btn-delete');
    const smallViewBtn = card.querySelector('.btn-view');
    
    if (viewBtn) {
        viewBtn.addEventListener('click', (e) => {
            animateButton(e.currentTarget);
            showHistoryDetails(item);
        });
    }
    
    if (smallViewBtn) {
        smallViewBtn.addEventListener('click', (e) => {
            animateButton(e.currentTarget);
            showHistoryDetails(item);
        });
    }
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
            animateButton(e.currentTarget);
            confirmDeleteHistory(item.id, index);
        });
    }
    
    // Card hover effects
    card.addEventListener('mouseenter', () => {
        const circle = card.querySelector('circle:last-child');
        if (circle) {
            circle.style.transition = 'stroke-dashoffset 0.8s ease';
        }
    });
    
    return card;
}

// Update Empty State
function updateEmptyState() {
    const emptyState = document.getElementById('historyEmpty');
    const tableBody = document.getElementById('historyTableBody');
    const gridView = document.getElementById('historyGrid');
    const listView = document.getElementById('listView');
    
    if (filteredHistory.length === 0) {
        if (emptyState) emptyState.classList.remove('hidden');
        if (tableBody) tableBody.innerHTML = '';
        if (gridView) gridView.innerHTML = '';
        if (listView) listView.classList.add('hidden');
    } else {
        if (emptyState) emptyState.classList.add('hidden');
        if (listView) listView.classList.remove('hidden');
    }
}

// Update Summary Stats
function updateSummaryStats() {
    // Total predictions
    const totalCount = document.getElementById('totalCount');
    if (totalCount) {
        totalCount.textContent = filteredHistory.length;
        animateNumber(totalCount, parseInt(totalCount.textContent) || 0);
    }
    
    // Benign cases
    const benignCount = document.getElementById('benignCount');
    if (benignCount) {
        const benignCases = filteredHistory.filter(item => item.prediction === 'Benign').length;
        benignCount.textContent = benignCases;
        animateNumber(benignCount, benignCases);
    }
    
    // Malignant cases
    const malignantCount = document.getElementById('malignantCount');
    if (malignantCount) {
        const malignantCases = filteredHistory.filter(item => item.prediction === 'Malignant').length;
        malignantCount.textContent = malignantCases;
        animateNumber(malignantCount, malignantCases);
    }
    
    // Average risk
    const avgRisk = document.getElementById('avgRisk');
    if (avgRisk) {
        const totalRisk = filteredHistory.reduce((sum, item) => sum + (item.risk_percentage || 0), 0);
        const average = filteredHistory.length > 0 ? totalRisk / filteredHistory.length : 0;
        avgRisk.textContent = `${Math.round(average)}%`;
        animateNumber(avgRisk, Math.round(average));
    }
    
    updateHeaderStats();
}

// Animate Number
function animateNumber(element, target) {
    const current = parseInt(element.textContent) || 0;
    const diff = target - current;
    const steps = 20;
    const step = diff / steps;
    let currentValue = current;
    
    const timer = setInterval(() => {
        currentValue += step;
        if ((step > 0 && currentValue >= target) || (step < 0 && currentValue <= target)) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.round(currentValue);
        }
    }, 30);
}

// Update Header Stats
function updateHeaderStats() {
    const totalPredictions = document.getElementById('totalPredictions');
    const avgRiskScore = document.getElementById('avgRiskScore');
    const lastUpdated = document.getElementById('lastUpdated');
    
    if (totalPredictions) {
        totalPredictions.textContent = `${filteredHistory.length} Predictions`;
    }
    
    if (avgRiskScore) {
        const totalRisk = filteredHistory.reduce((sum, item) => sum + (item.risk_percentage || 0), 0);
        const average = filteredHistory.length > 0 ? totalRisk / filteredHistory.length : 0;
        avgRiskScore.textContent = `Avg Risk: ${Math.round(average)}%`;
    }
    
    if (lastUpdated) {
        const now = new Date();
        lastUpdated.textContent = `Updated: ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }
}

// Initialize Charts
function initializeCharts() {
    createChartContainers();
    initializeDistributionChart();
    initializeTrendChart();
}

// Create Chart Containers
function createChartContainers() {
    const distributionChart = document.getElementById('distributionChart');
    const trendChart = document.getElementById('trendChart');
    
    if (distributionChart && !distributionChart.querySelector('canvas')) {
        distributionChart.innerHTML = '<canvas id="riskDistributionChart"></canvas>';
    }
    
    if (trendChart && !trendChart.querySelector('canvas')) {
        trendChart.innerHTML = '<canvas id="riskTrendChart"></canvas>';
    }
}

// Initialize Distribution Chart
function initializeDistributionChart() {
    const ctx = document.getElementById('riskDistributionChart');
    if (!ctx) return;
    
    if (distributionChart) {
        distributionChart.destroy();
    }
    
    distributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk (0-30%)', 'Medium Risk (31-69%)', 'High Risk (70-100%)'],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: [
                    'rgba(6, 214, 160, 0.8)',
                    'rgba(255, 209, 102, 0.8)',
                    'rgba(239, 71, 111, 0.8)'
                ],
                borderColor: [
                    'rgba(6, 214, 160, 1)',
                    'rgba(255, 209, 102, 1)',
                    'rgba(239, 71, 111, 1)'
                ],
                borderWidth: 2,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            family: 'Poppins',
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(29, 53, 87, 0.9)',
                    titleFont: {
                        family: 'Poppins',
                        size: 12
                    },
                    bodyFont: {
                        family: 'Poppins',
                        size: 11
                    },
                    padding: 12,
                    cornerRadius: 8
                }
            },
            cutout: '70%',
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}

// Initialize Trend Chart
function initializeTrendChart() {
    const ctx = document.getElementById('riskTrendChart');
    if (!ctx) return;
    
    if (trendChart) {
        trendChart.destroy();
    }
    
    trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Risk Score Trend',
                data: [],
                borderColor: 'rgba(67, 97, 238, 1)',
                backgroundColor: 'rgba(67, 97, 238, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(67, 97, 238, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(29, 53, 87, 0.9)',
                    titleFont: {
                        family: 'Poppins',
                        size: 12
                    },
                    bodyFont: {
                        family: 'Poppins',
                        size: 11
                    },
                    padding: 12,
                    cornerRadius: 8
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            family: 'Poppins',
                            size: 11
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        font: {
                            family: 'Poppins',
                            size: 11
                        }
                    }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            }
        }
    });
}

// Update Charts
function updateCharts() {
    updateDistributionChart();
    updateTrendChart();
}

// Update Distribution Chart
function updateDistributionChart() {
    if (!distributionChart) return;
    
    const lowRisk = filteredHistory.filter(item => (item.risk_percentage || 0) < 30).length;
    const mediumRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 30 && (item.risk_percentage || 0) < 70).length;
    const highRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 70).length;
    
    distributionChart.data.datasets[0].data = [lowRisk, mediumRisk, highRisk];
    distributionChart.update();
}

// Update Trend Chart
function updateTrendChart() {
    if (!trendChart) return;
    
    const period = document.getElementById('trendPeriod')?.value || 'month';
    const now = new Date();
    let startDate = new Date();
    
    switch (period) {
        case 'week':
            startDate.setDate(now.getDate() - 7);
            break;
        case 'month':
            startDate.setMonth(now.getMonth() - 1);
            break;
        case 'quarter':
            startDate.setMonth(now.getMonth() - 3);
            break;
        case 'year':
            startDate.setFullYear(now.getFullYear() - 1);
            break;
    }
    
    const periodData = filteredHistory.filter(item => {
        const itemDate = new Date(item.timestamp);
        return itemDate >= startDate && itemDate <= now;
    });
    
    const groupedData = {};
    periodData.forEach(item => {
        const date = new Date(item.timestamp).toLocaleDateString();
        if (!groupedData[date]) {
            groupedData[date] = {
                total: 0,
                count: 0
            };
        }
        groupedData[date].total += item.risk_percentage || 0;
        groupedData[date].count += 1;
    });
    
    const labels = Object.keys(groupedData).sort();
    const data = labels.map(date => {
        const group = groupedData[date];
        return group.count > 0 ? Math.round(group.total / group.count) : 0;
    });
    
    trendChart.data.labels = labels;
    trendChart.data.datasets[0].data = data;
    trendChart.update();
}

// Setup History Event Listeners
function setupHistoryEventListeners() {
    // View toggle buttons
    const viewToggleBtns = document.querySelectorAll('.view-toggle-btn');
    viewToggleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const view = this.getAttribute('data-view');
            switchView(view);
        });
    });
    
    // Search input with debounce
    const searchInput = document.getElementById('historySearch');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(() => {
            applyFilters();
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
        }, HISTORY_CONFIG.SEARCH_DEBOUNCE));
    }
    
    // Filter selects
    const filterSelects = document.querySelectorAll('.filter-select, .small-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', () => {
            applyFilters();
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
        });
    });
    
    // Refresh button
    const refreshBtn = document.getElementById('refreshHistory');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            refreshBtn.disabled = true;
            
            loadHistory().finally(() => {
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i>';
                refreshBtn.disabled = false;
            });
        });
    }
    
    // Export button
    const exportBtn = document.getElementById('exportHistory');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportHistory);
    }
    
    // Clear button
    const clearBtn = document.getElementById('clearHistory');
    if (clearBtn) {
        clearBtn.addEventListener('click', showConfirmModal);
    }
    
    // Confirm clear button
    const confirmClearBtn = document.getElementById('confirmClear');
    if (confirmClearBtn) {
        confirmClearBtn.addEventListener('click', clearAllHistory);
    }
    
    // Pagination buttons
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    
    if (prevPageBtn) {
        prevPageBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                updateHistoryDisplay();
            }
        });
    }
    
    if (nextPageBtn) {
        nextPageBtn.addEventListener('click', () => {
            const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                updateHistoryDisplay();
            }
        });
    }
    
    // Chart period changes
    const distributionPeriod = document.getElementById('distributionPeriod');
    const trendPeriod = document.getElementById('trendPeriod');
    
    if (distributionPeriod) {
        distributionPeriod.addEventListener('change', updateDistributionChart);
    }
    
    if (trendPeriod) {
        trendPeriod.addEventListener('change', updateTrendChart);
    }
}

// Switch View
function switchView(view) {
    currentView = view;
    
    document.querySelectorAll('.view-toggle-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-view') === view) {
            btn.classList.add('active');
        }
    });
    
    const listView = document.getElementById('listView');
    const gridView = document.getElementById('gridView');
    
    if (listView) listView.classList.toggle('active', view === 'list');
    if (gridView) gridView.classList.toggle('hidden', view !== 'grid');
    
    updateHistoryDisplay();
}

// Update Pagination
function updatePagination() {
    const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
    
    if (currentPage > totalPages && totalPages > 0) {
        currentPage = 1;
    }
}

// Update Pagination Controls
function updatePaginationControls() {
    const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    const pageNumbers = document.getElementById('pageNumbers');
    const pagination = document.getElementById('historyPagination');
    
    if (prevPageBtn) {
        prevPageBtn.disabled = currentPage === 1;
        prevPageBtn.style.opacity = currentPage === 1 ? '0.5' : '1';
    }
    
    if (nextPageBtn) {
        nextPageBtn.disabled = currentPage === totalPages || totalPages === 0;
        nextPageBtn.style.opacity = (currentPage === totalPages || totalPages === 0) ? '0.5' : '1';
    }
    
    if (pageNumbers && totalPages > 0) {
        pageNumbers.innerHTML = '';
        
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, startPage + 4);
        
        if (endPage - startPage < 4) {
            startPage = Math.max(1, endPage - 4);
        }
        
        for (let i = startPage; i <= endPage; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.className = `page-number ${i === currentPage ? 'active' : ''}`;
            pageBtn.textContent = i;
            pageBtn.addEventListener('click', () => {
                currentPage = i;
                updateHistoryDisplay();
            });
            pageNumbers.appendChild(pageBtn);
        }
    }
    
    if (pagination) {
        pagination.classList.toggle('hidden', filteredHistory.length <= itemsPerPage);
    }
}

// Show History Details
function showHistoryDetails(item) {
    const modal = document.getElementById('detailModal');
    if (!modal) return;
    
    populateDetailModal(item);
    
    modal.classList.remove('hidden');
    modal.style.opacity = '0';
    modal.style.transform = 'scale(0.9)';
    
    setTimeout(() => {
        modal.style.transition = 'all 0.3s ease-out';
        modal.style.opacity = '1';
        modal.style.transform = 'scale(1)';
    }, 10);
    
    document.body.style.overflow = 'hidden';
}

// Populate Detail Modal
function populateDetailModal(item) {
    const modalContent = document.querySelector('.modal-content');
    if (!modalContent) return;
    
    const date = new Date(item.timestamp);
    
    modalContent.innerHTML = `
        <div class="detail-header">
            <div class="detail-risk-score">
                <div class="detail-risk-circle">
                    <div class="score-circle" style="width: 120px; height: 120px;">
                        <svg width="120" height="120">
                            <circle cx="60" cy="60" r="55" fill="none" stroke="#e0e0e0" stroke-width="6"/>
                            <circle cx="60" cy="60" r="55" fill="none" stroke="${getRiskColor(item.risk_percentage || 0)}" 
                                    stroke-width="6" stroke-linecap="round" 
                                    stroke-dasharray="345" stroke-dashoffset="${345 - ((item.risk_percentage || 0) / 100) * 345}"/>
                        </svg>
                        <div class="score-content">
                            <span class="score-value">${item.risk_percentage || 0}%</span>
                            <span class="score-label">Risk Score</span>
                        </div>
                    </div>
                </div>
                <div class="detail-risk-info">
                    <h3>${item.prediction || 'N/A'} Prediction</h3>
                    <p class="detail-date">${date.toLocaleString()}</p>
                    <div class="detail-badges">
                        <span class="detail-badge ${getRiskLevelClass(item.risk_percentage || 0)}">
                            ${getRiskLevel(item.risk_percentage || 0)}
                        </span>
                        <span class="detail-badge">
                            <i class="fas fa-shield-alt"></i>
                            ${item.confidence || '85%'} Confidence
                        </span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="detail-tabs">
            <button class="tab-btn active" data-tab="parameters">
                <i class="fas fa-sliders-h"></i> Parameters
            </button>
            <button class="tab-btn" data-tab="factors">
                <i class="fas fa-chart-bar"></i> Risk Factors
            </button>
            <button class="tab-btn" data-tab="recommendations">
                <i class="fas fa-stethoscope"></i> Recommendations
            </button>
            <button class="tab-btn" data-tab="report">
                <i class="fas fa-file-alt"></i> Report
            </button>
        </div>
        
        <div id="parametersTab" class="tab-content active">
            <div class="parameters-grid">
                <div class="parameter-section">
                    <h4>Patient Information</h4>
                    <div class="parameter-list">
                        <div class="parameter-item">
                            <span class="param-label">Age</span>
                            <span class="param-value">${item.user_data?.Age || 'N/A'} years</span>
                        </div>
                        <div class="parameter-item">
                            <span class="param-label">Gender</span>
                            <span class="param-value">${item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</span>
                        </div>
                    </div>
                </div>
                <div class="parameter-section">
                    <h4>Thyroid Levels</h4>
                    <div class="parameter-list">
                        <div class="parameter-item">
                            <span class="param-label">TSH Level</span>
                            <span class="param-value">${item.user_data?.TSH_Level || 'N/A'} mIU/L</span>
                        </div>
                        <div class="parameter-item">
                            <span class="param-label">T3 Level</span>
                            <span class="param-value">${item.user_data?.T3_Level || 'N/A'} pg/mL</span>
                        </div>
                        <div class="parameter-item">
                            <span class="param-label">T4 Level</span>
                            <span class="param-value">${item.user_data?.T4_Level || 'N/A'} μg/dL</span>
                        </div>
                    </div>
                </div>
                <div class="parameter-section">
                    <h4>Clinical Findings</h4>
                    <div class="parameter-list">
                        <div class="parameter-item">
                            <span class="param-label">Nodule Size</span>
                            <span class="param-value">${item.user_data?.Nodule_Size || 'N/A'} cm</span>
                        </div>
                        <div class="parameter-item">
                            <span class="param-label">Cancer Risk Score</span>
                            <span class="param-value">${item.user_data?.Thyroid_Cancer_Risk || 'N/A'}/5</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div id="factorsTab" class="tab-content">
            <div class="factors-analysis">
                <h4>Key Contributing Factors</h4>
                <div class="factors-chart">
                    <canvas id="factorImportanceChart"></canvas>
                </div>
                <div id="detailFactorsList" class="factors-list"></div>
            </div>
        </div>
        
        <div id="recommendationsTab" class="tab-content">
            <div class="recommendations-list">
                <h4>Medical Recommendations</h4>
                <ul id="detailRecommendations"></ul>
            </div>
        </div>
        
        <div id="reportTab" class="tab-content">
            <div class="report-preview">
                <h4>Complete Report</h4>
                <div id="reportContent" class="report-content"></div>
                <div class="report-actions">
                    <button id="downloadReport" class="btn-primary">
                        <i class="fas fa-download"></i> Download PDF
                    </button>
                    <button id="printReport" class="btn-secondary">
                        <i class="fas fa-print"></i> Print Report
                    </button>
                </div>
            </div>
        </div>
        
        <div class="modal-actions">
            <button class="btn-secondary" onclick="closeDetailModal()">
                <i class="fas fa-times"></i> Close
            </button>
            <button class="btn-primary" onclick="downloadHistoryReport(${JSON.stringify(item).replace(/"/g, '&quot;')})">
                <i class="fas fa-file-export"></i> Export Data
            </button>
        </div>
    `;
    
    // Populate dynamic content
    const riskFactors = getRiskFactorsText(item.user_data);
    const recommendations = item.recommendations || generateRecommendations(item.risk_percentage || 0);
    
    document.getElementById('detailFactorsList').innerHTML = riskFactors;
    document.getElementById('detailRecommendations').innerHTML = recommendations.map(rec => 
        `<li><i class="fas fa-check"></i> ${rec}</li>`
    ).join('');
    
    // Report content
    const reportContent = document.getElementById('reportContent');
    if (reportContent) {
        reportContent.innerHTML = `
            <h5>Thyroid Risk Assessment Report</h5>
            <p><strong>Report ID:</strong> ${item.id || 'N/A'}</p>
            <p><strong>Date:</strong> ${date.toLocaleString()}</p>
            <p><strong>Risk Score:</strong> ${item.risk_percentage || 0}%</p>
            <p><strong>Prediction:</strong> ${item.prediction || 'N/A'}</p>
            <p><strong>Confidence Level:</strong> ${item.confidence || '85%'}</p>
            <hr>
            <p>This is a preview of the full report. Download the PDF for complete details including all clinical parameters, risk factors, and medical recommendations.</p>
        `;
    }
    
    // Tab functionality
    const tabBtns = modalContent.querySelectorAll('.tab-btn');
    const tabContents = modalContent.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            tabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `${tabId}Tab`) {
                    content.classList.add('active');
                }
            });
        });
    });
    
    // Initialize factor importance chart
    setTimeout(() => {
        initializeFactorImportanceChart(item.features_importance || {});
    }, 100);
}

// Initialize Factor Importance Chart
function initializeFactorImportanceChart(features) {
    const ctx = document.getElementById('factorImportanceChart');
    if (!ctx) return;
    
    const sortedFeatures = Object.entries(features)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedFeatures.map(([name]) => name),
            datasets: [{
                label: 'Importance',
                data: sortedFeatures.map(([, importance]) => importance * 100),
                backgroundColor: 'rgba(67, 97, 238, 0.7)',
                borderColor: 'rgba(67, 97, 238, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Importance (%)'
                    }
                }
            }
        }
    });
}

// Close Detail Modal
function closeDetailModal() {
    const modal = document.getElementById('detailModal');
    if (!modal) return;
    
    modal.style.opacity = '0';
    modal.style.transform = 'scale(0.9)';
    
    setTimeout(() => {
        modal.classList.add('hidden');
        modal.style.opacity = '';
        modal.style.transform = '';
        document.body.style.overflow = '';
    }, 300);
}

// Initialize Modals
function initializeModals() {
    // Detail modal
    const detailModal = document.getElementById('detailModal');
    if (detailModal) {
        const overlay = detailModal.querySelector('.modal-overlay');
        if (overlay) {
            overlay.addEventListener('click', closeDetailModal);
        }
        
        const closeButton = document.getElementById('closeDetailModal');
        if (closeButton) {
            closeButton.addEventListener('click', closeDetailModal);
        }
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !detailModal.classList.contains('hidden')) {
                closeDetailModal();
            }
        });
    }
    
    // Confirmation modal
    const confirmModal = document.getElementById('clearConfirmModal');
    if (confirmModal) {
        const overlay = confirmModal.querySelector('.modal-overlay');
        if (overlay) {
            overlay.addEventListener('click', closeConfirmModal);
        }
        
        const cancelBtn = document.getElementById('cancelClear');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', closeConfirmModal);
        }
    }
}

// Show Confirm Modal
function showConfirmModal() {
    const modal = document.getElementById('clearConfirmModal');
    if (!modal) return;
    
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Close Confirm Modal
function closeConfirmModal() {
    const modal = document.getElementById('clearConfirmModal');
    if (!modal) return;
    
    modal.classList.add('hidden');
    document.body.style.overflow = '';
}

// Export History
function exportHistory() {
    if (filteredHistory.length === 0) {
        showNotification('No history data to export', 'warning', 'Export Failed');
        return;
    }
    
    const exportBtn = document.getElementById('exportHistory');
    if (exportBtn) {
        exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        exportBtn.disabled = true;
    }
    
    setTimeout(() => {
        const exportData = filteredHistory.map(item => ({
            Date: new Date(item.timestamp).toLocaleString(),
            'Risk Score': `${item.risk_percentage}%`,
            Prediction: item.prediction,
            Confidence: item.confidence,
            Age: item.user_data?.Age,
            Gender: item.user_data?.Gender_Male === 1 ? 'Male' : 'Female',
            'Nodule Size': item.user_data?.Nodule_Size,
            'TSH Level': item.user_data?.TSH_Level
        }));
        
        const headers = Object.keys(exportData[0]);
        const csv = [
            headers.join(','),
            ...exportData.map(row => headers.map(header => `"${row[header]}"`).join(','))
        ].join('\n');
        
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `thyroscan_history_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification(`Exported ${exportData.length} records`, 'success', 'Export Complete');
        
        if (exportBtn) {
            exportBtn.innerHTML = '<i class="fas fa-download"></i>';
            exportBtn.disabled = false;
        }
    }, 500);
}

// Clear All History
function clearAllHistory() {
    closeConfirmModal();
    
    // Animate clearing
    const historyItems = document.querySelectorAll('.history-item, .history-card');
    historyItems.forEach((item, index) => {
        item.style.transition = 'all 0.3s ease-out';
        item.style.opacity = '0';
        item.style.transform = 'translateX(100px)';
        
        setTimeout(() => {
            item.style.display = 'none';
        }, 300);
    });
    
    setTimeout(() => {
        // Clear local data
        historyData = [];
        filteredHistory = [];
        currentPage = 1;
        
        // Update display
        updateHistoryDisplay();
        updateSummaryStats();
        updateCharts();
        
        showNotification('All history has been cleared', 'success', 'History Cleared');
        
        // Try to clear server data
        clearServerHistory();
    }, 500);
}

// Clear Server History
async function clearServerHistory() {
    try {
        const response = await fetch(`${window.API_BASE_URL || 'http://localhost:8000'}/clear-history`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            console.log('✅ Server history cleared');
        }
    } catch (error) {
        console.log('⚠️ Could not clear server history');
    }
}

// Confirm Delete History
function confirmDeleteHistory(id, index) {
    showNotification(
        'Are you sure you want to delete this record?<br><small>Click here to confirm.</small>',
        'warning',
        'Confirm Delete',
        5000
    ).then(() => {
        deleteHistoryRecord(id, index);
    }).catch(() => {
        // User cancelled
    });
}

// Delete History Record
function deleteHistoryRecord(id, index) {
    const itemToDelete = document.querySelector(`[data-id="${id}"]`)?.closest('.history-item, .history-card');
    
    if (itemToDelete) {
        // Animate deletion
        itemToDelete.style.transition = 'all 0.3s ease-out';
        itemToDelete.style.opacity = '0';
        itemToDelete.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            // Remove from DOM
            itemToDelete.style.display = 'none';
            
            // Remove from data
            historyData = historyData.filter(item => item.id !== id);
            filteredHistory = filteredHistory.filter(item => item.id !== id);
            
            // Update display
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
            
            showNotification('Record deleted successfully', 'success', 'Deleted');
            
            // Try to delete from server
            deleteServerRecord(id);
        }, 300);
    }
}

// Delete Server Record
async function deleteServerRecord(id) {
    try {
        const response = await fetch(`${window.API_BASE_URL || 'http://localhost:8000'}/delete/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            console.log(`✅ Record ${id} deleted from server`);
        }
    } catch (error) {
        console.log(`⚠️ Could not delete record ${id} from server`);
    }
}

// Download History Report
function downloadHistoryReport(item) {
    const report = generateHistoryReport(item);
    
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ThyroScan_Report_${item.id || new Date().getTime()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Report downloaded', 'success', 'Download Complete');
}

// Print History Report
function printHistoryReport(item) {
    const report = generateHistoryReport(item);
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>ThyroScan AI Report</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    h1 { color: #4361ee; }
                    .section { margin: 20px 0; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                <pre>${report}</pre>
                <script>
                    window.onload = function() {
                        window.print();
                        window.onafterprint = function() {
                            window.close();
                        };
                    };
                </script>
            </body>
        </html>
    `);
    printWindow.document.close();
}

// Generate History Report
function generateHistoryReport(item) {
    const date = new Date(item.timestamp);
    
    return `
THYROSCAN AI - THYROID RISK ASSESSMENT REPORT
=============================================
Report ID: ${item.id || 'N/A'}
Generated: ${date.toLocaleString()}

SUMMARY
-------
Risk Score: ${item.risk_percentage || 0}%
Prediction: ${item.prediction || 'N/A'}
Confidence Level: ${item.confidence || '85%'}
Risk Level: ${getRiskLevel(item.risk_percentage || 0)}

CLINICAL PARAMETERS
-------------------
Age: ${item.user_data?.Age || 'N/A'} years
Gender: ${item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}
TSH Level: ${item.user_data?.TSH_Level || 'N/A'} mIU/L
T3 Level: ${item.user_data?.T3_Level || 'N/A'} pg/mL
T4 Level: ${item.user_data?.T4_Level || 'N/A'} μg/dL
Nodule Size: ${item.user_data?.Nodule_Size || 'N/A'} cm
Cancer Risk Score: ${item.user_data?.Thyroid_Cancer_Risk || 'N/A'}

RISK FACTORS
------------
${getRiskFactorsText(item.user_data)}

KEY CONTRIBUTING FACTORS
-----------------------
${Object.entries(item.features_importance || {})
    .sort((a, b) => b[1] - a[1])
    .map(([factor, importance]) => `• ${factor}: ${(importance * 100).toFixed(1)}%`)
    .join('\n')}

MEDICAL RECOMMENDATIONS
-----------------------
${(item.recommendations || []).map(rec => `• ${rec}`).join('\n')}

DISCLAIMER
----------
This report is generated by ThyroScan AI for educational and research purposes only.
It is not a substitute for professional medical diagnosis, advice, or treatment.
Always consult qualified healthcare providers for medical concerns.

Generated by ThyroScan AI | Model Accuracy: 83%
=============================================
    `;
}

// Get Risk Factors Text
function getRiskFactorsText(userData) {
    if (!userData) return 'No risk factor data available';
    
    const riskFactors = [
        { id: 'Family_History', label: 'Family History of Thyroid Disease' },
        { id: 'Radiation_Exposure', label: 'Radiation Exposure' },
        { id: 'Iodine_Deficiency', label: 'Iodine Deficiency' },
        { id: 'Smoking', label: 'Smoking History' },
        { id: 'Obesity', label: 'Obesity (BMI ≥ 30)' },
        { id: 'Diabetes', label: 'Diabetes Mellitus' }
    ];
    
    const activeFactors = riskFactors
        .filter(factor => userData[factor.id] === 1)
        .map(factor => `• ${factor.label}`);
    
    return activeFactors.length > 0 
        ? activeFactors.join('\n') 
        : 'No significant risk factors identified';
}

// Get Risk Level
function getRiskLevel(percentage) {
    if (percentage < 30) return 'Low Risk';
    if (percentage < 70) return 'Medium Risk';
    return 'High Risk';
}

// Get Risk Level Class
function getRiskLevelClass(percentage) {
    if (percentage < 30) return 'low';
    if (percentage < 70) return 'medium';
    return 'high';
}

// Get Risk Color
function getRiskColor(percentage) {
    if (percentage < 30) return '#06d6a0'; // Success green
    if (percentage < 70) return '#ffd166'; // Warning yellow
    return '#ef476f'; // Danger red
}

// Generate Recommendations
function generateRecommendations(riskPercentage) {
    const recommendations = [];
    
    if (riskPercentage >= 70) {
        recommendations.push(
            'Consult an endocrinologist immediately',
            'Consider fine needle aspiration biopsy',
            'Regular monitoring every 3 months',
            'Complete thyroid function tests'
        );
    } else if (riskPercentage >= 40) {
        recommendations.push(
            'Schedule appointment with endocrinologist',
            'Monitor thyroid levels every 6 months',
            'Maintain healthy iodine intake',
            'Regular ultrasound follow-up'
        );
    } else {
        recommendations.push(
            'Regular annual checkup recommended',
            'Maintain healthy lifestyle',
            'Monitor for any symptom changes',
            'Balanced diet with proper iodine'
        );
    }
    
    return recommendations;
}

// Show Notification
function showNotification(message, type = 'info', title = '', duration = 3000) {
    return new Promise((resolve, reject) => {
        // Remove existing notification
        const existing = document.querySelector('.thyroscan-notification');
        if (existing) existing.remove();
        
        // Create notification
        const notification = document.createElement('div');
        notification.className = `thyroscan-notification ${type}`;
        
        const icon = {
            info: 'fas fa-info-circle',
            success: 'fas fa-check-circle',
            warning: 'fas fa-exclamation-triangle',
            error: 'fas fa-times-circle'
        }[type] || 'fas fa-info-circle';
        
        notification.innerHTML = `
            <div class="notification-content">
                <i class="${icon}"></i>
                <div class="notification-text">
                    ${title ? `<strong>${title}</strong><br>` : ''}
                    ${message}
                </div>
                <button class="notification-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        // Add to DOM
        document.body.appendChild(notification);
        
        // Show with animation
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Close button
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
                reject();
            }, 300);
        });
        
        // Auto close
        const timeout = setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
                resolve();
            }, 300);
        }, duration);
        
        // Hover to keep
        notification.addEventListener('mouseenter', () => {
            clearTimeout(timeout);
        });
        
        notification.addEventListener('mouseleave', () => {
            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => {
                    notification.remove();
                    resolve();
                }, 300);
            }, 1000);
        });
        
        // Click to confirm
        notification.addEventListener('click', (e) => {
            if (!e.target.closest('.notification-close')) {
                notification.classList.remove('show');
                setTimeout(() => {
                    notification.remove();
                    resolve();
                }, 300);
            }
        });
    });
}

// Add notification styles
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .thyroscan-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--white);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-xl);
        border-left: 4px solid var(--primary);
        max-width: 400px;
        z-index: 9999;
        transform: translateX(100%);
        transition: transform 0.3s ease-out;
    }
    
    .thyroscan-notification.show {
        transform: translateX(0);
    }
    
    .thyroscan-notification.success {
        border-left-color: var(--success);
    }
    
    .thyroscan-notification.warning {
        border-left-color: var(--warning);
    }
    
    .thyroscan-notification.error {
        border-left-color: var(--danger);
    }
    
    .notification-content {
        display: flex;
        align-items: flex-start;
        gap: var(--space-md);
        padding: var(--space-lg);
    }
    
    .notification-content i:first-child {
        font-size: 1.2rem;
        margin-top: 2px;
    }
    
    .notification-text {
        flex: 1;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .notification-text strong {
        color: var(--dark);
    }
    
    .notification-close {
        background: none;
        border: none;
        color: var(--gray);
        cursor: pointer;
        padding: 4px;
        transition: var(--transition-fast);
    }
    
    .notification-close:hover {
        color: var(--dark);
    }
`;
document.head.appendChild(notificationStyles);

// Animate Button
function animateButton(button) {
    button.style.transform = 'scale(0.95)';
    button.style.transition = 'transform 0.1s ease';
    
    setTimeout(() => {
        button.style.transform = '';
    }, 100);
}

// Debounce function
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

// Initialize history page
document.addEventListener('DOMContentLoaded', () => {
    if (typeof initializeHistoryPage === 'function') {
        setTimeout(() => {
            initializeHistoryPage();
        }, 100);
    }
});

// Export for debugging
window.HistoryPage = {
    initializeHistoryPage,
    loadHistory,
    updateHistoryDisplay,
    showHistoryDetails,
    exportHistory,
    clearAllHistory,
    getRiskLevel,
    getRiskColor
};