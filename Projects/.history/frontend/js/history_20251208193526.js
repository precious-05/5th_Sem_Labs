// ============================================
// HISTORY.JS - CORRECTED VERSION
// 100% Compatible with your HTML
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
let chartInstances = {};

// ✅ FIX 1: API Configuration with default
const API_CONFIG = {
    BASE_URL: window.API_BASE_URL || 'http://localhost:8000',
    ENDPOINTS: {
        HISTORY: '/history',
        STATS: '/stats',     // ✅ ADDED for statistics
        PREDICT: '/predict',
        HEALTH: '/health'
    }
};

// Initialize History Page
function initializeHistoryPage() {
    if (isInitialized) {
        console.log('⚠️ Already initialized');
        return;
    }
    
    console.log('📊 Initializing History Page...');
    
    // Show loading animation
    showPageLoader();
    
    // Initialize page elements
    initializePageElements();
    
    // Setup event listeners FIRST
    setupHistoryEventListeners();
    
    // Initialize filters
    initializeFilters();
    
    // Initialize modals
    initializeModals();
    
    // Load prediction history and statistics
    loadHistory();
    loadStatistics();  // ✅ NEW: Load header statistics
    
    isInitialized = true;
}

// Show Page Loader
function showPageLoader() {
    const loadingState = document.getElementById('historyLoading');
    if (loadingState) {
        loadingState.innerHTML = `
            <div class="loading-spinner enhanced">
                <div class="spinner-circle"></div>
                <div class="spinner-text">Loading History from Database...</div>
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

// Initialize Page Elements
function initializePageElements() {
    // Initialize empty state
    const emptyState = document.getElementById('historyEmpty');
    if (emptyState) {
        emptyState.classList.add('hidden');
    }
}

// ✅ FIX 2: Load Statistics for Header
async function loadStatistics() {
    try {
        console.log('📊 Loading statistics...');
        
        const response = await fetch(
            `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.STATS}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }
        );
        
        if (!response.ok) {
            throw new Error(`Stats API Error: ${response.status}`);
        }
        
        const stats = await response.json();
        
        // Update header statistics
        updateHeaderStats(stats);
        
    } catch (error) {
        console.error('❌ Error loading statistics:', error);
        // Calculate stats from loaded history data
        calculateHeaderStats();
    }
}

// ✅ FIX 3: Update Header Statistics
function updateHeaderStats(stats) {
    // Total predictions
    const totalElement = document.getElementById('totalPredictions');
    if (totalElement) {
        totalElement.textContent = stats.total_predictions || 0;
    }
    
    // Average risk score
    const avgRiskElement = document.getElementById('avgRiskScore');
    if (avgRiskElement) {
        avgRiskElement.textContent = `${stats.risk_stats?.average || 0}%`;
    }
    
    // Last updated
    const lastUpdatedElement = document.getElementById('lastUpdated');
    if (lastUpdatedElement) {
        lastUpdatedElement.textContent = stats.last_updated || '--';
    }
}

// Calculate Header Stats from history data
function calculateHeaderStats() {
    if (historyData.length === 0) return;
    
    // Total predictions
    const totalElement = document.getElementById('totalPredictions');
    if (totalElement) {
        totalElement.textContent = historyData.length;
    }
    
    // Average risk
    const avgRiskElement = document.getElementById('avgRiskScore');
    if (avgRiskElement) {
        const totalRisk = historyData.reduce((sum, item) => sum + (item.risk_percentage || 0), 0);
        const average = historyData.length > 0 ? Math.round(totalRisk / historyData.length) : 0;
        avgRiskElement.textContent = `${average}%`;
    }
    
    // Last updated
    const lastUpdatedElement = document.getElementById('lastUpdated');
    if (lastUpdatedElement && historyData.length > 0) {
        const latest = historyData[0];
        if (latest.timestamp) {
            lastUpdatedElement.textContent = latest.timestamp.split(' ')[0]; // Just date
        }
    }
}

// Load Prediction History
async function loadHistory() {
    try {
        // Show loading animation
        showTableLoading();
        
        console.log('📡 Fetching history from API...');
        
        const response = await fetch(
            `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HISTORY}?limit=100`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }
        );
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // ✅ FIX 4: Handle both response formats
        if (Array.isArray(data)) {
            historyData = data;
        } else if (data.history && Array.isArray(data.history)) {
            historyData = data.history;
        } else {
            historyData = [];
        }
        
        console.log(`✅ Loaded ${historyData.length} records`);
        
        if (historyData.length === 0) {
            showEmptyState();
            showNotification('No prediction history found', 'info');
        } else {
            // Process and display data
            processHistoryData();
            updateHistoryDisplay();
            updateSummaryStats();
            initializeCharts();
            
            showNotification(`Loaded ${historyData.length} predictions`, 'success');
        }
        
    } catch (error) {
        console.error('❌ Error loading history:', error);
        
        // Fallback: Try to load from localStorage
        const savedHistory = localStorage.getItem('thyroscan_local_history');
        if (savedHistory) {
            try {
                historyData = JSON.parse(savedHistory);
                console.log(`⚠️ Using cached data: ${historyData.length} records`);
                
                processHistoryData();
                updateHistoryDisplay();
                updateSummaryStats();
                initializeCharts();
                
                showNotification('Using cached data (database unavailable)', 'warning');
            } catch (parseError) {
                console.error('Error parsing cached data:', parseError);
                showEmptyState();
            }
        } else {
            showEmptyState();
            showNotification('Unable to load history. Please try again.', 'error');
        }
    } finally {
        hideTableLoading();
        hidePageLoader();
    }
}

// Show Table Loading
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
    
    // Also show loading in grid view
    const gridView = document.getElementById('historyGrid');
    if (gridView) {
        gridView.innerHTML = `
            <div class="grid-loading">
                ${Array(6).fill().map((_, i) => `
                    <div class="loading-card" style="animation-delay: ${i * 0.1}s"></div>
                `).join('')}
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
    
    const gridView = document.getElementById('historyGrid');
    if (gridView && gridView.querySelector('.grid-loading')) {
        gridView.innerHTML = '';
    }
}

// Show Empty State
function showEmptyState() {
    const emptyState = document.getElementById('historyEmpty');
    const tableBody = document.getElementById('historyTableBody');
    const gridView = document.getElementById('historyGrid');
    
    if (emptyState) {
        emptyState.classList.remove('hidden');
    }
    
    if (tableBody) tableBody.innerHTML = '';
    if (gridView) gridView.innerHTML = '';
}

// Process History Data
function processHistoryData() {
    console.log('🔄 Processing history data...');
    
    // Sort data based on timestamp
    filteredHistory = [...historyData].sort((a, b) => {
        try {
            let aValue = new Date(a.timestamp || Date.now());
            let bValue = new Date(b.timestamp || Date.now());
            
            if (sortDirection === 'asc') {
                return aValue > bValue ? 1 : -1;
            } else {
                return aValue < bValue ? 1 : -1;
            }
        } catch (error) {
            console.error('Error sorting:', error);
            return 0;
        }
    });
    
    console.log(`✅ Processed ${filteredHistory.length} records`);
    
    // Apply filters
    applyFilters();
    
    // Update pagination
    updatePagination();
}

// Apply Filters
function applyFilters() {
    const riskFilter = document.getElementById('filterRisk')?.value;
    const dateFilter = document.getElementById('filterDate')?.value;
    const predictionFilter = document.getElementById('filterPrediction')?.value;
    const searchTerm = document.getElementById('historySearch')?.value.toLowerCase() || '';
    
    filteredHistory = historyData.filter(item => {
        // Risk filter
        if (riskFilter && riskFilter !== '') {
            const riskPercentage = item.risk_percentage || 0;
            if (riskFilter === 'low' && riskPercentage >= 30) return false;
            if (riskFilter === 'medium' && (riskPercentage < 30 || riskPercentage >= 70)) return false;
            if (riskFilter === 'high' && riskPercentage < 70) return false;
        }
        
        // Date filter
        if (dateFilter && dateFilter !== '') {
            try {
                const itemDate = new Date(item.timestamp || Date.now());
                const now = new Date();
                
                switch (dateFilter) {
                    case 'today':
                        if (itemDate.toDateString() !== now.toDateString()) return false;
                        break;
                    case 'week':
                        const weekAgo = new Date();
                        weekAgo.setDate(now.getDate() - 7);
                        if (itemDate < weekAgo) return false;
                        break;
                    case 'month':
                        const monthAgo = new Date();
                        monthAgo.setMonth(now.getMonth() - 1);
                        if (itemDate < monthAgo) return false;
                        break;
                    case 'year':
                        const yearAgo = new Date();
                        yearAgo.setFullYear(now.getFullYear() - 1);
                        if (itemDate < yearAgo) return false;
                        break;
                }
            } catch (error) {
                console.error('Error filtering by date:', error);
            }
        }
        
        // Prediction filter
        if (predictionFilter && predictionFilter !== '') {
            if (predictionFilter === 'benign' && item.prediction !== 'Benign') return false;
            if (predictionFilter === 'malignant' && item.prediction !== 'Malignant') return false;
        }
        
        // Search filter
        if (searchTerm) {
            const searchFields = [
                item.prediction || '',
                getRiskLevel(item.risk_percentage || 0),
                item.user_data?.Age?.toString() || '',
                item.user_data?.Gender_Male === 1 ? 'male' : 'female'
            ].filter(Boolean).join(' ').toLowerCase();
            
            if (!searchFields.includes(searchTerm)) return false;
        }
        
        return true;
    });
    
    // Reset to first page after filtering
    currentPage = 1;
}

// Update History Display
function updateHistoryDisplay() {
    // Hide both views first
    const listView = document.getElementById('listView');
    const gridView = document.getElementById('gridView');
    
    if (listView) listView.classList.add('hidden');
    if (gridView) gridView.classList.add('hidden');
    
    // Show selected view
    if (currentView === 'list') {
        updateListView();
        if (listView) listView.classList.remove('hidden');
    } else {
        updateGridView();
        if (gridView) gridView.classList.remove('hidden');
    }
    
    updateEmptyState();
    updatePaginationControls();
}

// ✅ FIX 5: Corrected Chart ID references
function initializeCharts() {
    console.log('📊 Initializing charts...');
    
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.warn('⚠️ Chart.js not loaded. Skipping charts initialization.');
        
        // Show placeholder messages
        const distributionChart = document.getElementById('distributionChart');
        const trendChart = document.getElementById('trendChart');
        
        if (distributionChart) {
            distributionChart.innerHTML = `
                <div class="chart-placeholder">
                    <i class="fas fa-chart-pie"></i>
                    <p>Chart.js required for visualization</p>
                    <small>Please include Chart.js library</small>
                </div>
            `;
        }
        
        if (trendChart) {
            trendChart.innerHTML = `
                <div class="chart-placeholder">
                    <i class="fas fa-chart-line"></i>
                    <p>Chart.js required for visualization</p>
                    <small>Please include Chart.js library</small>
                </div>
            `;
        }
        
        return;
    }
    
    // ✅ FIX 6: Initialize with correct IDs
    initDistributionChart();
    initTrendChart();
}

// Initialize Distribution Chart
function initDistributionChart() {
    // ✅ FIX 7: Correct ID - matches HTML
    const ctx = document.getElementById('distributionChart');
    if (!ctx) {
        console.error('❌ Distribution chart element not found');
        return;
    }
    
    // Get canvas or create one
    let canvas = ctx.querySelector('canvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        ctx.appendChild(canvas);
    }
    
    // Destroy existing chart
    if (chartInstances.distributionChart) {
        chartInstances.distributionChart.destroy();
    }
    
    const lowRisk = filteredHistory.filter(item => (item.risk_percentage || 0) < 30).length;
    const mediumRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 30 && (item.risk_percentage || 0) < 70).length;
    const highRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 70).length;
    
    try {
        chartInstances.distributionChart = new Chart(canvas.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Low Risk (0-30%)', 'Medium Risk (31-69%)', 'High Risk (70-100%)'],
                datasets: [{
                    data: [lowRisk, mediumRisk, highRisk],
                    backgroundColor: ['#06d6a0', '#ffd166', '#ef476f'],
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
                            usePointStyle: true
                        }
                    }
                }
            }
        });
        
        console.log('✅ Distribution chart initialized');
    } catch (error) {
        console.error('❌ Error initializing distribution chart:', error);
        ctx.innerHTML = `<div class="chart-error">Chart error: ${error.message}</div>`;
    }
}

// Initialize Trend Chart
function initTrendChart() {
    // ✅ FIX 8: Correct ID - matches HTML
    const ctx = document.getElementById('trendChart');
    if (!ctx) {
        console.error('❌ Trend chart element not found');
        return;
    }
    
    // Get canvas or create one
    let canvas = ctx.querySelector('canvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        ctx.appendChild(canvas);
    }
    
    // Destroy existing chart
    if (chartInstances.trendChart) {
        chartInstances.trendChart.destroy();
    }
    
    // Get trend data
    const trendData = getTrendData(7);
    
    try {
        chartInstances.trendChart = new Chart(canvas.getContext('2d'), {
            type: 'line',
            data: {
                labels: trendData.labels,
                datasets: [{
                    label: 'Average Risk Score',
                    data: trendData.values,
                    borderColor: '#4361ee',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#4361ee',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        },
                        grid: {
                            color: 'rgba(0,0,0,0.05)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0,0,0,0.05)'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Risk: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
        
        console.log('✅ Trend chart initialized');
    } catch (error) {
        console.error('❌ Error initializing trend chart:', error);
        ctx.innerHTML = `<div class="chart-error">Chart error: ${error.message}</div>`;
    }
}

// Get Trend Data
function getTrendData(days) {
    const labels = [];
    const values = [];
    
    for (let i = days - 1; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        labels.push(dateStr);
        
        // Get predictions for this date
        const dayPredictions = filteredHistory.filter(item => {
            try {
                const itemDate = new Date(item.timestamp || Date.now());
                return itemDate.toDateString() === date.toDateString();
            } catch (error) {
                return false;
            }
        });
        
        if (dayPredictions.length > 0) {
            const avgRisk = dayPredictions.reduce((sum, item) => sum + (item.risk_percentage || 0), 0) / dayPredictions.length;
            values.push(Math.round(avgRisk));
        } else {
            values.push(0);
        }
    }
    
    return { labels, values };
}

// Update List View
function updateListView() {
    const tableBody = document.getElementById('historyTableBody');
    if (!tableBody) return;
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    tableBody.innerHTML = '';
    
    if (pageItems.length === 0) {
        tableBody.innerHTML = `
            <tr class="no-data-row">
                <td colspan="6" class="text-center">
                    <div class="no-data-message">
                        <i class="fas fa-search"></i>
                        <h4>No matching records found</h4>
                        <p>Try adjusting your filters or search terms</p>
                    </div>
                </td>
            </tr>
        `;
        return;
    }
    
    pageItems.forEach((item, index) => {
        const row = createHistoryRow(item, startIndex + index);
        tableBody.appendChild(row);
    });
}

// Create History Row
function createHistoryRow(item, index) {
    const row = document.createElement('tr');
    row.className = 'history-item';
    
    try {
        const date = new Date(item.timestamp || Date.now());
        const age = item.user_data?.Age || 'N/A';
        const gender = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
        const riskPercentage = item.risk_percentage || 0;
        const prediction = item.prediction || 'N/A';
        
        row.innerHTML = `
            <td class="history-date">
                <div class="date-display">
                    <div class="date">${date.toLocaleDateString()}</div>
                    <div class="time">${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                </div>
            </td>
            
            <td class="history-patient">
                <div class="patient-info">
                    <div class="patient-avatar">
                        <i class="fas fa-user${gender === 'Male' ? '' : '-female'}"></i>
                    </div>
                    <div class="patient-details">
                        <h4>Patient ${index + 1}</h4>
                        <p><i class="fas fa-birthday-cake"></i> ${age} yrs • <i class="fas fa-${gender === 'Male' ? 'mars' : 'venus'}"></i> ${gender}</p>
                    </div>
                </div>
            </td>
            
            <td class="history-risk">
                <div class="risk-display">
                    <div class="risk-gauge">
                        <svg width="50" height="50">
                            <circle cx="25" cy="25" r="20" fill="none" stroke="rgba(0,0,0,0.1)" stroke-width="3"/>
                            <circle cx="25" cy="25" r="20" fill="none" stroke="${getRiskColor(riskPercentage)}" 
                                    stroke-width="3" stroke-linecap="round" 
                                    stroke-dasharray="126" stroke-dashoffset="${126 - (riskPercentage / 100) * 126}"/>
                        </svg>
                        <div class="gauge-value">${riskPercentage.toFixed(1)}%</div>
                    </div>
                    <div class="risk-level ${getRiskLevelClass(riskPercentage)}">
                        <i class="fas fa-${riskPercentage < 30 ? 'shield-alt' : riskPercentage < 70 ? 'exclamation-circle' : 'exclamation-triangle'}"></i>
                        ${getRiskLevel(riskPercentage)}
                    </div>
                </div>
            </td>
            
            <td class="history-prediction">
                <span class="prediction-badge ${prediction.toLowerCase()}">
                    <i class="fas fa-${prediction === 'Malignant' ? 'exclamation-triangle' : 'check-circle'}"></i>
                    ${prediction}
                </span>
            </td>
            
            <td class="history-factors">
                <div class="factors-tags">
                    ${getTopFactors(item.user_data).map(factor => `
                        <span class="factor-tag">
                            <i class="fas fa-circle"></i>
                            ${factor}
                        </span>
                    `).join('')}
                </div>
            </td>
            
            <td class="history-actions">
                <button class="btn-view" data-id="${index}" title="View Details">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn-download" data-id="${index}" title="Download Report">
                    <i class="fas fa-download"></i>
                </button>
                <button class="btn-delete" data-id="${index}" title="Delete Record">
                    <i class="fas fa-trash-alt"></i>
                </button>
            </td>
        `;
        
        // Add event listeners
        const viewBtn = row.querySelector('.btn-view');
        const downloadBtn = row.querySelector('.btn-download');
        const deleteBtn = row.querySelector('.btn-delete');
        
        if (viewBtn) {
            viewBtn.addEventListener('click', () => showHistoryDetails(item));
        }
        
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => downloadHistoryReport(item));
        }
        
        if (deleteBtn) {
            deleteBtn.addEventListener('click', () => confirmDeleteHistory(item));
        }
        
    } catch (error) {
        console.error('Error creating history row:', error);
        row.innerHTML = `<td colspan="6" class="text-center error">Error displaying record</td>`;
    }
    
    return row;
}

// Get Top Factors from user_data
function getTopFactors(user_data) {
    if (!user_data) return ['No data'];
    
    const factors = [];
    
    // Check risk factors
    if (user_data.Family_History === 1) factors.push('Family History');
    if (user_data.Radiation_Exposure === 1) factors.push('Radiation');
    if (user_data.Iodine_Deficiency === 1) factors.push('Iodine Def');
    if (user_data.Smoking === 1) factors.push('Smoking');
    if (user_data.Obesity === 1) factors.push('Obesity');
    if (user_data.Diabetes === 1) factors.push('Diabetes');
    
    return factors.slice(0, 3);
}

// Update Grid View
function updateGridView() {
    const gridView = document.getElementById('historyGrid');
    if (!gridView) return;
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    gridView.innerHTML = '';
    
    if (pageItems.length === 0) {
        gridView.innerHTML = `
            <div class="no-data-card">
                <div class="no-data-icon">
                    <i class="fas fa-search"></i>
                </div>
                <h4>No matching records found</h4>
                <p>Try adjusting your filters or search terms</p>
            </div>
        `;
        return;
    }
    
    pageItems.forEach((item, index) => {
        const card = createHistoryCard(item, startIndex + index);
        gridView.appendChild(card);
    });
}

// Create History Card
function createHistoryCard(item, index) {
    const card = document.createElement('div');
    card.className = 'history-card';
    
    try {
        const date = new Date(item.timestamp || Date.now());
        const riskPercentage = item.risk_percentage || 0;
        const prediction = item.prediction || 'N/A';
        const age = item.user_data?.Age || 'N/A';
        const gender = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
        
        card.innerHTML = `
            <div class="card-header">
                <div class="card-date">
                    <i class="fas fa-calendar"></i>
                    ${date.toLocaleDateString()}
                </div>
                <div class="card-actions">
                    <button class="btn-view" data-id="${index}">
                        <i class="fas fa-eye"></i>
                    </button>
                </div>
            </div>
            
            <div class="card-risk">
                <div class="risk-circle">
                    <div class="circle-progress">
                        <svg width="100" height="100">
                            <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(0,0,0,0.1)" stroke-width="6"/>
                            <circle cx="50" cy="50" r="45" fill="none" stroke="${getRiskColor(riskPercentage)}" 
                                    stroke-width="6" stroke-linecap="round" 
                                    stroke-dasharray="283" stroke-dashoffset="${283 - (riskPercentage / 100) * 283}"/>
                        </svg>
                        <div class="score-content">
                            <span class="score-value">${riskPercentage.toFixed(1)}%</span>
                            <span class="score-label">Risk Score</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card-prediction">
                <span class="prediction-badge ${prediction.toLowerCase()}">
                    <i class="fas fa-${prediction === 'Malignant' ? 'exclamation-triangle' : 'check-circle'}"></i>
                    ${prediction}
                </span>
            </div>
            
            <div class="card-details">
                <div class="detail-item">
                    <span class="detail-label"><i class="fas fa-user"></i> Patient:</span>
                    <span class="detail-value">${index + 1}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label"><i class="fas fa-birthday-cake"></i> Age:</span>
                    <span class="detail-value">${age} yrs</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label"><i class="fas fa-venus-mars"></i> Gender:</span>
                    <span class="detail-value">${gender}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label"><i class="fas fa-tumor"></i> Nodule:</span>
                    <span class="detail-value">${item.user_data?.Nodule_Size || 'N/A'} cm</span>
                </div>
            </div>
            
            <div class="card-footer">
                <button class="btn-view-full" data-id="${index}">
                    <i class="fas fa-chart-bar"></i>
                    View Full Report
                </button>
            </div>
        `;
        
        // Add event listeners
        const viewBtn = card.querySelector('.btn-view-full');
        const actionBtn = card.querySelector('.btn-view');
        
        if (viewBtn) {
            viewBtn.addEventListener('click', () => showHistoryDetails(item));
        }
        
        if (actionBtn) {
            actionBtn.addEventListener('click', () => showHistoryDetails(item));
        }
        
    } catch (error) {
        console.error('Error creating history card:', error);
        card.innerHTML = `<div class="error">Error displaying card</div>`;
    }
    
    return card;
}

// Update Empty State
function updateEmptyState() {
    const emptyState = document.getElementById('historyEmpty');
    const listView = document.getElementById('listView');
    const gridView = document.getElementById('gridView');
    
    if (filteredHistory.length === 0) {
        if (emptyState) emptyState.classList.remove('hidden');
        if (listView) listView.classList.add('hidden');
        if (gridView) gridView.classList.add('hidden');
    } else {
        if (emptyState) emptyState.classList.add('hidden');
    }
}

// Update Summary Stats
function updateSummaryStats() {
    // Total predictions
    const totalCount = document.getElementById('totalCount');
    if (totalCount) {
        totalCount.textContent = filteredHistory.length;
    }
    
    // Benign cases
    const benignCount = document.getElementById('benignCount');
    if (benignCount) {
        const benignCases = filteredHistory.filter(item => item.prediction === 'Benign').length;
        benignCount.textContent = benignCases;
    }
    
    // Malignant cases
    const malignantCount = document.getElementById('malignantCount');
    if (malignantCount) {
        const malignantCases = filteredHistory.filter(item => item.prediction === 'Malignant').length;
        malignantCount.textContent = malignantCases;
    }
    
    // Average risk
    const avgRisk = document.getElementById('avgRisk');
    if (avgRisk) {
        const totalRisk = filteredHistory.reduce((sum, item) => sum + (item.risk_percentage || 0), 0);
        const average = filteredHistory.length > 0 ? Math.round(totalRisk / filteredHistory.length) : 0;
        avgRisk.textContent = `${average}%`;
    }
}

// Update Charts
function updateCharts() {
    if (!window.Chart) return;
    
    if (chartInstances.distributionChart) {
        const lowRisk = filteredHistory.filter(item => (item.risk_percentage || 0) < 30).length;
        const mediumRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 30 && (item.risk_percentage || 0) < 70).length;
        const highRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 70).length;
        
        chartInstances.distributionChart.data.datasets[0].data = [lowRisk, mediumRisk, highRisk];
        chartInstances.distributionChart.update();
    }
    
    if (chartInstances.trendChart) {
        const trendData = getTrendData(7);
        chartInstances.trendChart.data.labels = trendData.labels;
        chartInstances.trendChart.data.datasets[0].data = trendData.values;
        chartInstances.trendChart.update();
    }
}

// Setup History Event Listeners
function setupHistoryEventListeners() {
    // Refresh button
    const refreshBtn = document.getElementById('refreshHistory');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.classList.add('refreshing');
            refreshHistory().finally(() => {
                setTimeout(() => {
                    this.classList.remove('refreshing');
                }, 500);
            });
        });
    }
    
    // Export button
    const exportBtn = document.getElementById('exportHistory');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            this.classList.add('exporting');
            setTimeout(() => {
                exportHistory();
                this.classList.remove('exporting');
            }, 300);
        });
    }
    
    // Clear button
    const clearBtn = document.getElementById('clearHistory');
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            if (historyData.length > 0) {
                showConfirmModal();
            } else {
                showNotification('No history to clear', 'warning');
            }
        });
    }
    
    // Search input
    const searchInput = document.getElementById('historySearch');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                applyFilters();
                updateHistoryDisplay();
                updateSummaryStats();
                updateCharts();
            }, 300);
        });
    }
    
    // Filter selects
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            applyFilters();
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
        });
    });
    
    // View toggle buttons
    const viewToggleBtns = document.querySelectorAll('.view-toggle-btn');
    viewToggleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const view = this.getAttribute('data-view');
            switchView(view);
        });
    });
    
    // Pagination buttons
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    
    if (prevPageBtn) {
        prevPageBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                updateHistoryDisplay();
                updatePaginationControls();
            }
        });
    }
    
    if (nextPageBtn) {
        nextPageBtn.addEventListener('click', () => {
            const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                updateHistoryDisplay();
                updatePaginationControls();
            }
        });
    }
    
    // Confirm clear button
    const confirmClearBtn = document.getElementById('confirmClear');
    if (confirmClearBtn) {
        confirmClearBtn.addEventListener('click', function() {
            clearAllHistory();
        });
    }
    
    // Cancel clear button
    const cancelClearBtn = document.getElementById('cancelClear');
    if (cancelClearBtn) {
        cancelClearBtn.addEventListener('click', closeConfirmModal);
    }
}

// Refresh History
async function refreshHistory() {
    showNotification('Refreshing history...', 'info');
    await loadHistory();
    await loadStatistics();
}

// Export History - CSV FORMAT
function exportHistory() {
    if (filteredHistory.length === 0) {
        showNotification('No history data to export', 'warning');
        return;
    }
    
    // Prepare CSV data
    const headers = ['Date', 'Risk Score', 'Prediction', 'Age', 'Gender', 'TSH Level', 'Nodule Size'];
    const csvData = filteredHistory.map(item => {
        const date = new Date(item.timestamp || Date.now());
        return [
            date.toLocaleString(),
            `${item.risk_percentage || 0}%`,
            item.prediction || 'N/A',
            item.user_data?.Age || 'N/A',
            item.user_data?.Gender_Male === 1 ? 'Male' : 'Female',
            item.user_data?.TSH_Level || 'N/A',
            item.user_data?.Nodule_Size || 'N/A'
        ];
    });
    
    // Create CSV
    const csvContent = [
        headers.join(','),
        ...csvData.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');
    
    // Download
    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `thyroassess_history_${new Date().toISOString().split('T')[0]}.csv`;
    
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification(`Exported ${filteredHistory.length} records`, 'success');
}

// Clear All History
function clearAllHistory() {
    // Clear local data
    historyData = [];
    filteredHistory = [];
    currentPage = 1;
    
    // Clear localStorage backup
    localStorage.removeItem('thyroscan_local_history');
    
    // Update UI
    updateHistoryDisplay();
    updateSummaryStats();
    updateCharts();
    calculateHeaderStats();
    
    // Close modal
    closeConfirmModal();
    
    showNotification('All history has been cleared', 'success');
}

// Show History Details
function showHistoryDetails(item) {
    const modal = document.getElementById('detailModal');
    if (!modal) return;
    
    // Populate modal
    populateDetailModal(item);
    
    // Show modal
    modal.classList.remove('hidden');
    document.body.classList.add('modal-open');
}

// Populate Detail Modal
function populateDetailModal(item) {
    try {
        const date = new Date(item.timestamp || Date.now());
        const riskPercentage = item.risk_percentage || 0;
        const prediction = item.prediction || 'N/A';
        const age = item.user_data?.Age || 'N/A';
        const gender = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
        
        // Update basic info
        const riskElement = document.getElementById('detailRiskPercentage');
        const predictionElement = document.getElementById('detailPrediction');
        const dateElement = document.getElementById('detailDate');
        const riskLevelElement = document.getElementById('detailRiskLevel');
        
        if (riskElement) riskElement.textContent = `${riskPercentage}%`;
        if (predictionElement) predictionElement.textContent = prediction;
        if (dateElement) dateElement.textContent = `Date: ${date.toLocaleString()}`;
        if (riskLevelElement) riskLevelElement.textContent = getRiskLevel(riskPercentage);
        
        // Update parameters
        document.getElementById('detailAge').textContent = `${age} years`;
        document.getElementById('detailGender').textContent = gender;
        document.getElementById('detailTSH').textContent = `${item.user_data?.TSH_Level || 'N/A'} mIU/L`;
        document.getElementById('detailT3').textContent = `${item.user_data?.T3_Level || 'N/A'} pg/mL`;
        document.getElementById('detailT4').textContent = `${item.user_data?.T4_Level || 'N/A'} μg/dL`;
        document.getElementById('detailNodule').textContent = `${item.user_data?.Nodule_Size || 'N/A'} cm`;
        document.getElementById('detailCancerRisk').textContent = item.user_data?.Thyroid_Cancer_Risk || 'N/A';
        
        // Update risk factors
        const riskFactors = [
            { label: 'Family History', value: item.user_data?.Family_History },
            { label: 'Radiation Exposure', value: item.user_data?.Radiation_Exposure },
            { label: 'Iodine Deficiency', value: item.user_data?.Iodine_Deficiency },
            { label: 'Smoking', value: item.user_data?.Smoking },
            { label: 'Obesity', value: item.user_data?.Obesity },
            { label: 'Diabetes', value: item.user_data?.Diabetes }
        ];
        
        const activeFactors = riskFactors.filter(f => f.value).map(f => f.label);
        const factorsList = document.getElementById('detailFactorsList');
        if (factorsList) {
            if (activeFactors.length > 0) {
                factorsList.innerHTML = activeFactors.map(factor => `
                    <div class="factor-item">
                        <i class="fas fa-check-circle"></i>
                        <span>${factor}</span>
                    </div>
                `).join('');
            } else {
                factorsList.innerHTML = '<div class="no-factors">No risk factors recorded</div>';
            }
        }
        
        // Update recommendations
        const recommendations = generateRecommendations(riskPercentage);
        const recommendationsList = document.getElementById('detailRecommendations');
        if (recommendationsList) {
            recommendationsList.innerHTML = recommendations.map(rec => `
                <li>
                    <i class="fas fa-check-circle"></i>
                    <span>${rec}</span>
                </li>
            `).join('');
        }
        
        // Setup download button
        const downloadBtn = document.getElementById('downloadReport');
        if (downloadBtn) {
            downloadBtn.onclick = () => downloadHistoryReport(item);
        }
        
        // Setup print button
        const printBtn = document.getElementById('printReport');
        if (printBtn) {
            printBtn.onclick = () => printHistoryReport(item);
        }
        
    } catch (error) {
        console.error('Error populating detail modal:', error);
        showNotification('Error loading details', 'error');
    }
}

// Close Detail Modal
function closeDetailModal() {
    const modal = document.getElementById('detailModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
    }
}

// Show Confirm Modal
function showConfirmModal() {
    const modal = document.getElementById('clearConfirmModal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.classList.add('modal-open');
    }
}

// Close Confirm Modal
function closeConfirmModal() {
    const modal = document.getElementById('clearConfirmModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
    }
}

// Download History Report
function downloadHistoryReport(item) {
    // Create report content
    const reportContent = `
ThyroAssess AI Prediction Report
================================

Date: ${new Date(item.timestamp || Date.now()).toLocaleString()}
Prediction: ${item.prediction || 'N/A'}
Risk Score: ${item.risk_percentage || 0}%
Risk Level: ${getRiskLevel(item.risk_percentage || 0)}

Patient Information:
- Age: ${item.user_data?.Age || 'N/A'} years
- Gender: ${item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}

Test Results:
- TSH Level: ${item.user_data?.TSH_Level || 'N/A'} mIU/L
- T3 Level: ${item.user_data?.T3_Level || 'N/A'} pg/mL
- T4 Level: ${item.user_data?.T4_Level || 'N/A'} μg/dL
- Nodule Size: ${item.user_data?.Nodule_Size || 'N/A'} cm

Risk Factors:
${item.user_data?.Family_History ? '- Family History of Thyroid Issues' : ''}
${item.user_data?.Radiation_Exposure ? '- History of Radiation Exposure' : ''}
${item.user_data?.Iodine_Deficiency ? '- Iodine Deficiency' : ''}
${item.user_data?.Smoking ? '- Smoking Habit' : ''}
${item.user_data?.Obesity ? '- Obesity' : ''}
${item.user_data?.Diabetes ? '- Diabetes' : ''}

Recommendations:
${generateRecommendations(item.risk_percentage || 0)
    .map(rec => `- ${rec}`)
    .join('\n')}

---
Generated by ThyroAssess AI
${window.location.origin}
Generated on: ${new Date().toLocaleString()}
    `.trim();

    // Create download
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const timestamp = new Date(item.timestamp || Date.now()).toISOString().split('T')[0];
    a.download = `thyroassess_report_${timestamp}.txt`;
    
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Report downloaded successfully', 'success');
}

// Print History Report
function printHistoryReport(item) {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
        <head>
            <title>ThyroAssess AI Report</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h1 { color: #333; }
                .section { margin-bottom: 20px; }
                .label { font-weight: bold; color: #666; }
                .value { margin-bottom: 10px; }
                @media print { .no-print { display: none; } }
            </style>
        </head>
        <body>
            <button class="no-print" onclick="window.print()" style="padding: 10px 20px; background: #4361ee; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Print Report
            </button>
            
            <h1>ThyroAssess AI Prediction Report</h1>
            
            <div class="section">
                <div class="label">Prediction Date:</div>
                <div class="value">${new Date(item.timestamp || Date.now()).toLocaleString()}</div>
            </div>
            
            <div class="section">
                <h2>Prediction Results</h2>
                <div class="value"><strong>Result:</strong> ${item.prediction || 'N/A'}</div>
                <div class="value"><strong>Risk Score:</strong> ${item.risk_percentage || 0}%</div>
                <div class="value"><strong>Risk Level:</strong> ${getRiskLevel(item.risk_percentage || 0)}</div>
            </div>
            
            <div class="section">
                <h2>Patient Information</h2>
                <div class="value"><strong>Age:</strong> ${item.user_data?.Age || 'N/A'} years</div>
                <div class="value"><strong>Gender:</strong> ${item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</div>
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
                ${generateRecommendations(item.risk_percentage || 0)
                    .map(rec => `<div class="value">• ${rec}</div>`)
                    .join('')}
            </div>
            
            <div class="section">
                <p><em>This report is generated by ThyroAssess AI for informational purposes only. Please consult with a healthcare professional for medical advice.</em></p>
            </div>
        </body>
        </html>
    `);
    printWindow.document.close();
}

// Confirm Delete History
function confirmDeleteHistory(item) {
    if (confirm('Are you sure you want to delete this record?')) {
        deleteHistoryRecord(item);
    }
}

// Delete History Record
function deleteHistoryRecord(item) {
    // Remove from arrays
    const index = historyData.findIndex(h => 
        h.timestamp === item.timestamp && 
        h.prediction === item.prediction
    );
    
    if (index !== -1) {
        historyData.splice(index, 1);
    }
    
    filteredHistory = filteredHistory.filter(h => 
        !(h.timestamp === item.timestamp && h.prediction === item.prediction)
    );
    
    // Update localStorage backup
    localStorage.setItem('thyroscan_local_history', JSON.stringify(historyData));
    
    // Update UI
    updateHistoryDisplay();
    updateSummaryStats();
    updateCharts();
    calculateHeaderStats();
    
    showNotification('Record deleted successfully', 'success');
}

// Switch View
function switchView(view) {
    if (currentView === view) return;
    
    currentView = view;
    
    // Update active button
    document.querySelectorAll('.view-toggle-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-view') === view);
    });
    
    // Update UI
    updateHistoryDisplay();
}

// Update Pagination
function updatePagination() {
    updatePaginationControls();
}

// Update Pagination Controls
function updatePaginationControls() {
    const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    
    if (prevPageBtn) {
        prevPageBtn.disabled = currentPage === 1;
    }
    
    if (nextPageBtn) {
        nextPageBtn.disabled = currentPage === totalPages || totalPages === 0;
    }
    
    // Update page numbers
    const pageNumbers = document.getElementById('pageNumbers');
    if (pageNumbers) {
        pageNumbers.innerHTML = '';
        
        // Show limited page numbers
        const maxPages = 5;
        let startPage = Math.max(1, currentPage - Math.floor(maxPages / 2));
        let endPage = Math.min(totalPages, startPage + maxPages - 1);
        
        if (endPage - startPage + 1 < maxPages) {
            startPage = Math.max(1, endPage - maxPages + 1);
        }
        
        for (let i = startPage; i <= endPage; i++) {
            const pageBtn = document.createElement('span');
            pageBtn.className = `page-number ${i === currentPage ? 'active' : ''}`;
            pageBtn.textContent = i;
            pageBtn.addEventListener('click', () => {
                currentPage = i;
                updateHistoryDisplay();
                updatePaginationControls();
            });
            pageNumbers.appendChild(pageBtn);
        }
    }
}

// Initialize Filters
function initializeFilters() {
    const filterRisk = document.getElementById('filterRisk');
    const filterDate = document.getElementById('filterDate');
    const filterPrediction = document.getElementById('filterPrediction');
    
    [filterRisk, filterDate, filterPrediction].forEach(filter => {
        if (filter) {
            filter.value = '';
        }
    });
}

// Initialize Modals
function initializeModals() {
    // Detail modal
    const detailModal = document.getElementById('detailModal');
    if (detailModal) {
        const overlay = detailModal.querySelector('.modal-overlay');
        const closeBtn = document.getElementById('closeDetailModal');
        
        if (overlay) {
            overlay.addEventListener('click', closeDetailModal);
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', closeDetailModal);
        }
    }
    
    // Confirmation modal
    const confirmModal = document.getElementById('clearConfirmModal');
    if (confirmModal) {
        const overlay = confirmModal.querySelector('.modal-overlay');
        const cancelBtn = document.getElementById('cancelClear');
        
        if (overlay) {
            overlay.addEventListener('click', closeConfirmModal);
        }
        
        if (cancelBtn) {
            cancelBtn.addEventListener('click', closeConfirmModal);
        }
    }
    
    // Escape key to close modals
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const detailModal = document.getElementById('detailModal');
            const confirmModal = document.getElementById('clearConfirmModal');
            
            if (detailModal && !detailModal.classList.contains('hidden')) {
                closeDetailModal();
            }
            if (confirmModal && !confirmModal.classList.contains('hidden')) {
                closeConfirmModal();
            }
        }
    });
}

// Helper Functions
function getRiskLevel(percentage) {
    if (percentage < 30) return 'Low';
    if (percentage < 70) return 'Medium';
    return 'High';
}

function getRiskLevelClass(percentage) {
    if (percentage < 30) return 'low';
    if (percentage < 70) return 'medium';
    return 'high';
}

function getRiskColor(percentage) {
    if (percentage < 30) return '#06d6a0';
    if (percentage < 70) return '#ffd166';
    return '#ef476f';
}

function generateRecommendations(riskPercentage) {
    if (riskPercentage < 30) {
        return [
            'Continue regular checkups',
            'Maintain healthy lifestyle',
            'Annual thyroid screening recommended'
        ];
    } else if (riskPercentage < 70) {
        return [
            'Consult with specialist',
            'Consider ultrasound examination',
            'Monitor symptoms closely',
            'Follow-up in 6 months'
        ];
    } else {
        return [
            'Immediate consultation with endocrinologist',
            'Ultrasound and biopsy recommended',
            'Regular monitoring essential',
            'Consider surgical consultation'
        ];
    }
}

function showNotification(message, type = 'info') {
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 
                          type === 'error' ? 'exclamation-circle' : 
                          type === 'warning' ? 'exclamation-triangle' : 
                          'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on history page
    if (document.getElementById('historyTableBody') || document.getElementById('historyGrid')) {
        setTimeout(() => {
            initializeHistoryPage();
        }, 100);
    }
});

// Export functions globally
window.ThyroAssessHistory = {
    initializeHistoryPage,
    refreshHistory,
    exportHistory,
    clearAllHistory,
    showHistoryDetails
};