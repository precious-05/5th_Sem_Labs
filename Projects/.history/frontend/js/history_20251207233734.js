// ============================================
// ENHANCED HISTORY.JS - COMPLETE FIXED VERSION
// ThyroScan AI History Page JavaScript
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

// Initialize History Page
function initializeHistoryPage() {
    if (isInitialized) return;
    
    console.log('📊 Initializing Enhanced History Page...');
    
    // Show loading animation
    showPageLoader();
    
    // Initialize page elements
    initializePageElements();
    
    // Load prediction history
    loadHistory();
    
    // Setup event listeners
    setupHistoryEventListeners();
    
    // Initialize filters
    initializeFilters();
    
    // Initialize modals
    initializeModals();
    
    isInitialized = true;
    
    // Listen for new predictions from prediction page
    setupPredictionListener();
}

// Listen for new predictions
function setupPredictionListener() {
    // Listen for storage events (when prediction page saves data)
    window.addEventListener('storage', (e) => {
        if (e.key === 'thyroscan_new_prediction') {
            const newPrediction = JSON.parse(e.newValue);
            if (newPrediction) {
                console.log('🔄 New prediction detected, refreshing history...');
                refreshHistory();
            }
        }
    });
    
    // Also check if there's a new prediction in localStorage
    const newPrediction = localStorage.getItem('thyroscan_new_prediction');
    if (newPrediction) {
        console.log('🔄 New prediction found, refreshing...');
        refreshHistory();
        localStorage.removeItem('thyroscan_new_prediction');
    }
}

// Show Page Loader
function showPageLoader() {
    const loadingState = document.getElementById('historyLoading');
    if (loadingState) {
        loadingState.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <p>Loading History...</p>
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
    // Update current year
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
    
    // Initialize view toggle
    const listViewBtn = document.querySelector('[data-view="list"]');
    const gridViewBtn = document.querySelector('[data-view="grid"]');
    
    if (listViewBtn && gridViewBtn) {
        if (currentView === 'list') {
            listViewBtn.classList.add('active');
            gridViewBtn.classList.remove('active');
        } else {
            gridViewBtn.classList.add('active');
            listViewBtn.classList.remove('active');
        }
    }
    
    // Initialize empty state
    const emptyState = document.getElementById('historyEmpty');
    if (emptyState) {
        emptyState.classList.add('hidden');
        emptyState.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <i class="fas fa-history"></i>
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
}

// Load Prediction History
async function loadHistory() {
    try {
        showTableLoading();
        
        // Try to load from API
        const response = await fetch(`${window.API_BASE_URL || 'http://localhost:8000'}/history?limit=100`);
        
        if (response.ok) {
            const data = await response.json();
            historyData = data.history || [];
            console.log(`📈 Loaded ${historyData.length} history records from API`);
        } else {
            throw new Error('API request failed');
        }
        
    } catch (error) {
        console.warn('⚠️ Using demo data:', error.message);
        
        // Try to load from localStorage
        const savedHistory = localStorage.getItem('thyroscan_history');
        if (savedHistory) {
            historyData = JSON.parse(savedHistory);
            console.log(`📈 Loaded ${historyData.length} history records from localStorage`);
        } else {
            // Generate demo data
            historyData = generateDemoHistory();
            console.log(`📈 Generated ${historyData.length} demo history records`);
        }
    }
    
    // Process and display data
    processHistoryData();
    updateHistoryDisplay();
    updateSummaryStats();
    initializeCharts();
    
    hideTableLoading();
    hidePageLoader();
}

// Show Table Loading
function showTableLoading() {
    const tableBody = document.getElementById('historyTableBody');
    if (tableBody) {
        tableBody.innerHTML = `
            <tr class="loading-row">
                <td colspan="6">
                    <div class="loading-spinner small">
                        <div class="spinner"></div>
                        <span>Loading history...</span>
                    </div>
                </td>
            </tr>
        `;
    }
}

// Hide Table Loading
function hideTableLoading() {
    const tableBody = document.getElementById('historyTableBody');
    if (tableBody) {
        tableBody.innerHTML = '';
    }
}

// Generate Demo History Data
function generateDemoHistory() {
    const demoData = [];
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);
    
    for (let i = 0; i < 15; i++) {
        const date = new Date(startDate);
        date.setDate(date.getDate() + Math.floor(Math.random() * 30));
        
        const riskPercentage = Math.floor(Math.random() * 100);
        const prediction = riskPercentage > 70 ? 'Malignant' : 'Benign';
        
        demoData.push({
            id: `demo_${Date.now()}_${i}`,
            timestamp: date.toISOString(),
            risk_percentage: riskPercentage,
            prediction: prediction,
            confidence: `${Math.floor(Math.random() * 15) + 80}%`,
            user_data: {
                Age: Math.floor(Math.random() * 50) + 20,
                Gender_Male: Math.random() > 0.5 ? 1 : 0,
                TSH_Level: (Math.random() * 5).toFixed(2),
                Nodule_Size: (Math.random() * 4).toFixed(1)
            },
            features_importance: {
                'Nodule Size': Math.random() * 0.3 + 0.4,
                'Age': Math.random() * 0.2 + 0.2,
                'TSH Level': Math.random() * 0.15 + 0.1
            },
            recommendations: [
                'Regular checkup recommended',
                'Maintain healthy lifestyle',
                'Monitor thyroid levels'
            ]
        });
    }
    
    // Save to localStorage for persistence
    localStorage.setItem('thyroscan_history', JSON.stringify(demoData));
    
    return demoData.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
}

// Process History Data
function processHistoryData() {
    // Sort data
    filteredHistory = [...historyData].sort((a, b) => {
        let aValue = a[sortColumn];
        let bValue = b[sortColumn];
        
        if (sortColumn === 'timestamp') {
            aValue = new Date(a.timestamp);
            bValue = new Date(b.timestamp);
        } else if (sortColumn === 'risk_percentage') {
            aValue = a.risk_percentage || 0;
            bValue = b.risk_percentage || 0;
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
    const searchTerm = document.getElementById('historySearch')?.value?.toLowerCase() || '';
    
    filteredHistory = historyData.filter(item => {
        // Risk filter
        if (riskFilter) {
            const riskPercentage = item.risk_percentage || 0;
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
                    const weekAgo = new Date();
                    weekAgo.setDate(now.getDate() - 7);
                    if (itemDate < weekAgo) return false;
                    break;
                case 'month':
                    const monthAgo = new Date();
                    monthAgo.setMonth(now.getMonth() - 1);
                    if (itemDate < monthAgo) return false;
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
            const searchStr = [
                item.prediction,
                getRiskLevel(item.risk_percentage),
                item.user_data?.Age?.toString(),
                item.user_data?.Gender_Male === 1 ? 'male' : 'female'
            ].filter(Boolean).join(' ').toLowerCase();
            
            if (!searchStr.includes(searchTerm)) return false;
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
                        <p>No matching records found</p>
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
    
    updatePaginationControls();
}

// Create History Row
function createHistoryRow(item, index) {
    const row = document.createElement('tr');
    row.className = 'history-item';
    row.setAttribute('data-id', item.id);
    
    const date = new Date(item.timestamp);
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
                <div class="patient-id">Patient ${index + 1}</div>
                <div class="patient-details">${age} yrs, ${gender}</div>
            </div>
        </td>
        
        <td class="history-risk">
            <div class="risk-display">
                <div class="risk-percentage">${riskPercentage}%</div>
                <div class="risk-level ${getRiskLevelClass(riskPercentage)}">
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
                ${Object.entries(item.features_importance || {})
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 2)
                    .map(([factor]) => `
                        <span class="factor-tag">${factor}</span>
                    `).join('')}
            </div>
        </td>
        
        <td class="history-actions">
            <button class="btn-view" data-id="${item.id}" title="View Details">
                <i class="fas fa-eye"></i>
            </button>
            <button class="btn-download" data-id="${item.id}" title="Download Report">
                <i class="fas fa-download"></i>
            </button>
            <button class="btn-delete" data-id="${item.id}" title="Delete Record">
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
        deleteBtn.addEventListener('click', () => confirmDeleteHistory(item.id));
    }
    
    // Click on row to view details
    row.addEventListener('click', (e) => {
        if (!e.target.closest('.history-actions')) {
            showHistoryDetails(item);
        }
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
    
    if (pageItems.length === 0) {
        gridView.innerHTML = `
            <div class="no-data-card">
                <i class="fas fa-search"></i>
                <p>No matching records found</p>
            </div>
        `;
        return;
    }
    
    pageItems.forEach((item, index) => {
        const card = createHistoryCard(item, startIndex + index);
        gridView.appendChild(card);
    });
    
    updatePaginationControls();
}

// Create History Card
function createHistoryCard(item, index) {
    const card = document.createElement('div');
    card.className = 'history-card';
    card.setAttribute('data-id', item.id);
    
    const date = new Date(item.timestamp);
    const riskPercentage = item.risk_percentage || 0;
    const prediction = item.prediction || 'N/A';
    
    card.innerHTML = `
        <div class="card-header">
            <div class="card-date">
                <i class="fas fa-calendar"></i>
                ${date.toLocaleDateString()}
            </div>
            <div class="card-actions">
                <button class="btn-view" data-id="${item.id}">
                    <i class="fas fa-eye"></i>
                </button>
            </div>
        </div>
        
        <div class="card-body">
            <div class="risk-display">
                <div class="risk-circle">
                    <div class="circle-progress" style="--progress: ${riskPercentage}%">
                        <span class="risk-value">${riskPercentage}%</span>
                    </div>
                </div>
                <div class="prediction-badge ${prediction.toLowerCase()}">
                    ${prediction}
                </div>
            </div>
            
            <div class="patient-info">
                <div class="info-item">
                    <i class="fas fa-user"></i>
                    <span>Patient ${index + 1}</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-birthday-cake"></i>
                    <span>${item.user_data?.Age || 'N/A'} yrs</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-${item.user_data?.Gender_Male === 1 ? 'mars' : 'venus'}"></i>
                    <span>${item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</span>
                </div>
            </div>
        </div>
        
        <div class="card-footer">
            <button class="btn-download" data-id="${item.id}">
                <i class="fas fa-download"></i>
                Download
            </button>
            <button class="btn-view-full" data-id="${item.id}">
                View Details
            </button>
        </div>
    `;
    
    // Add event listeners
    const viewBtn = card.querySelector('.btn-view');
    const viewFullBtn = card.querySelector('.btn-view-full');
    const downloadBtn = card.querySelector('.btn-download');
    
    if (viewBtn) {
        viewBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            showHistoryDetails(item);
        });
    }
    
    if (viewFullBtn) {
        viewFullBtn.addEventListener('click', () => showHistoryDetails(item));
    }
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            downloadHistoryReport(item);
        });
    }
    
    // Click on card to view details
    card.addEventListener('click', (e) => {
        if (!e.target.closest('.card-actions') && !e.target.closest('.card-footer')) {
            showHistoryDetails(item);
        }
    });
    
    return card;
}

// Update Empty State
function updateEmptyState() {
    const emptyState = document.getElementById('historyEmpty');
    const listView = document.getElementById('listView');
    const gridView = document.getElementById('gridView');
    
    if (filteredHistory.length === 0 && historyData.length === 0) {
        if (emptyState) emptyState.classList.remove('hidden');
        if (listView) listView.classList.add('hidden');
        if (gridView) gridView.classList.add('hidden');
    } else {
        if (emptyState) emptyState.classList.add('hidden');
        if (listView) listView.classList.remove('hidden');
        if (gridView) gridView.classList.remove('hidden');
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

// Initialize Charts
function initializeCharts() {
    // Distribution chart
    initDistributionChart();
    
    // Trend chart
    initTrendChart();
}

// Initialize Distribution Chart
function initDistributionChart() {
    const ctx = document.getElementById('riskDistributionChart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (chartInstances.distributionChart) {
        chartInstances.distributionChart.destroy();
    }
    
    // Calculate data
    const lowRisk = filteredHistory.filter(item => (item.risk_percentage || 0) < 30).length;
    const mediumRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 30 && (item.risk_percentage || 0) < 70).length;
    const highRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 70).length;
    
    chartInstances.distributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk (0-30%)', 'Medium Risk (31-69%)', 'High Risk (70-100%)'],
            datasets: [{
                data: [lowRisk, mediumRisk, highRisk],
                backgroundColor: ['#06d6a0', '#ffd166', '#ef476f'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Initialize Trend Chart
function initTrendChart() {
    const ctx = document.getElementById('riskTrendChart');
    if (!ctx) return;
    
    if (chartInstances.trendChart) {
        chartInstances.trendChart.destroy();
    }
    
    // Get trend data for last 7 days
    const trendData = getTrendData(7);
    
    chartInstances.trendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: trendData.labels,
            datasets: [{
                label: 'Average Risk Score',
                data: trendData.values,
                borderColor: '#4361ee',
                backgroundColor: 'rgba(67, 97, 238, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
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
            const itemDate = new Date(item.timestamp);
            return itemDate.toDateString() === date.toDateString();
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

// Update Charts
function updateCharts() {
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

// Setup History Event Listeners
function setupHistoryEventListeners() {
    // Refresh button
    const refreshBtn = document.getElementById('refreshHistory');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshHistory);
    }
    
    // Export button
    const exportBtn = document.getElementById('exportHistory');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportHistory);
    }
    
    // Clear button
    const clearBtn = document.getElementById('clearHistory');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
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
        searchInput.addEventListener('input', debounce(() => {
            applyFilters();
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
        }, 300));
    }
    
    // Filter selects
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', () => {
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
    
    // Chart period selects
    const distributionPeriod = document.getElementById('distributionPeriod');
    const trendPeriod = document.getElementById('trendPeriod');
    
    if (distributionPeriod) {
        distributionPeriod.addEventListener('change', () => {
            // Recalculate distribution based on period
            updateCharts();
        });
    }
    
    if (trendPeriod) {
        trendPeriod.addEventListener('change', () => {
            // Update trend chart with new period
            if (chartInstances.trendChart) {
                const days = parseInt(trendPeriod.value) || 7;
                const trendData = getTrendData(days);
                chartInstances.trendChart.data.labels = trendData.labels;
                chartInstances.trendChart.data.datasets[0].data = trendData.values;
                chartInstances.trendChart.update();
            }
        });
    }
}

// Refresh History
async function refreshHistory() {
    const refreshBtn = document.getElementById('refreshHistory');
    if (refreshBtn) {
        refreshBtn.classList.add('refreshing');
        refreshBtn.disabled = true;
    }
    
    showNotification('Refreshing history...', 'info');
    
    // Clear cached data
    localStorage.removeItem('thyroscan_history');
    
    // Reload from server
    await loadHistory();
    
    if (refreshBtn) {
        refreshBtn.classList.remove('refreshing');
        refreshBtn.disabled = false;
    }
    
    showNotification('History refreshed successfully', 'success');
}

// Export History
function exportHistory() {
    if (filteredHistory.length === 0) {
        showNotification('No history data to export', 'warning');
        return;
    }
    
    // Prepare CSV data
    const headers = ['Date', 'Risk Score', 'Prediction', 'Confidence', 'Age', 'Gender', 'Nodule Size'];
    const csvData = filteredHistory.map(item => [
        new Date(item.timestamp).toLocaleString(),
        `${item.risk_percentage}%`,
        item.prediction,
        item.confidence || 'N/A',
        item.user_data?.Age || 'N/A',
        item.user_data?.Gender_Male === 1 ? 'Male' : 'Female',
        item.user_data?.Nodule_Size || 'N/A'
    ]);
    
    // Create CSV content
    const csvContent = [
        headers.join(','),
        ...csvData.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');
    
    // Create download link
    const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `thyroscan_history_${new Date().toISOString().split('T')[0]}.csv`;
    
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification(`Exported ${filteredHistory.length} records`, 'success');
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

// Clear All History
function clearAllHistory() {
    // Clear local data
    historyData = [];
    filteredHistory = [];
    currentPage = 1;
    
    // Clear localStorage
    localStorage.removeItem('thyroscan_history');
    
    // Update UI
    updateHistoryDisplay();
    updateSummaryStats();
    updateCharts();
    
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
    const date = new Date(item.timestamp);
    const riskPercentage = item.risk_percentage || 0;
    
    // Update basic info
    document.getElementById('detailRiskPercentage').textContent = `${riskPercentage}%`;
    document.getElementById('detailPrediction').textContent = item.prediction || 'N/A';
    document.getElementById('detailDate').textContent = date.toLocaleString();
    document.getElementById('detailRiskLevel').textContent = getRiskLevel(riskPercentage);
    document.getElementById('detailConfidence').textContent = item.confidence || '85%';
    
    // Update parameters
    document.getElementById('detailAge').textContent = `${item.user_data?.Age || 'N/A'} years`;
    document.getElementById('detailGender').textContent = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
    document.getElementById('detailTSH').textContent = `${item.user_data?.TSH_Level || 'N/A'} mIU/L`;
    document.getElementById('detailT3').textContent = `${item.user_data?.T3_Level || 'N/A'} pg/mL`;
    document.getElementById('detailT4').textContent = `${item.user_data?.T4_Level || 'N/A'} μg/dL`;
    document.getElementById('detailNodule').textContent = `${item.user_data?.Nodule_Size || 'N/A'} cm`;
    
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
    const recommendations = item.recommendations || generateRecommendations(riskPercentage);
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
}

// Close Detail Modal
function closeDetailModal() {
    const modal = document.getElementById('detailModal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
    }
}

// Download History Report
function downloadHistoryReport(item) {
    // Create report content
    const reportContent = `
        ThyroScan AI Prediction Report
        ==============================
        
        Date: ${new Date(item.timestamp).toLocaleString()}
        Prediction: ${item.prediction}
        Risk Score: ${item.risk_percentage}%
        Confidence: ${item.confidence}
        Risk Level: ${getRiskLevel(item.risk_percentage)}
        
        Patient Information:
        - Age: ${item.user_data?.Age || 'N/A'} years
        - Gender: ${item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}
        
        Test Results:
        - TSH Level: ${item.user_data?.TSH_Level || 'N/A'} mIU/L
        - T3 Level: ${item.user_data?.T3_Level || 'N/A'} pg/mL
        - T4 Level: ${item.user_data?.T4_Level || 'N/A'} μg/dL
        - Nodule Size: ${item.user_data?.Nodule_Size || 'N/A'} cm
        
        Key Risk Factors:
        ${Object.entries(item.features_importance || {})
            .sort((a, b) => b[1] - a[1])
            .map(([factor, importance]) => `- ${factor}: ${Math.round(importance * 100)}%`)
            .join('\n')}
        
        Recommendations:
        ${(item.recommendations || generateRecommendations(item.risk_percentage))
            .map(rec => `- ${rec}`)
            .join('\n')}
        
        ---
        Generated by ThyroScan AI
        ${window.location.origin}
    `;
    
    // Create download
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `thyroscan_report_${new Date(item.timestamp).toISOString().split('T')[0]}.txt`;
    
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
            <title>ThyroScan AI Report</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h1 { color: #333; border-bottom: 2px solid #4361ee; padding-bottom: 10px; }
                .section { margin-bottom: 20px; }
                .label { font-weight: bold; color: #666; }
                .value { margin-bottom: 10px; }
                .recommendation { background: #f0f8ff; padding: 10px; border-left: 4px solid #4361ee; margin: 10px 0; }
                @media print {
                    .no-print { display: none; }
                    button { display: none; }
                }
            </style>
        </head>
        <body>
            <button class="no-print" onclick="window.print()" style="padding: 10px 20px; background: #4361ee; color: white; border: none; border-radius: 5px; cursor: pointer;">
                Print Report
            </button>
            
            <h1>ThyroScan AI Prediction Report</h1>
            
            <div class="section">
                <div class="label">Report Date:</div>
                <div class="value">${new Date().toLocaleString()}</div>
            </div>
            
            <div class="section">
                <div class="label">Prediction Date:</div>
                <div class="value">${new Date(item.timestamp).toLocaleString()}</div>
            </div>
            
            <div class="section">
                <h2>Prediction Results</h2>
                <div class="value"><strong>Result:</strong> ${item.prediction}</div>
                <div class="value"><strong>Risk Score:</strong> ${item.risk_percentage}%</div>
                <div class="value"><strong>Confidence:</strong> ${item.confidence}</div>
                <div class="value"><strong>Risk Level:</strong> ${getRiskLevel(item.risk_percentage)}</div>
            </div>
            
            <div class="section">
                <h2>Patient Information</h2>
                <div class="value"><strong>Age:</strong> ${item.user_data?.Age || 'N/A'} years</div>
                <div class="value"><strong>Gender:</strong> ${item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</div>
            </div>
            
            <div class="section">
                <h2>Test Results</h2>
                <div class="value"><strong>TSH Level:</strong> ${item.user_data?.TSH_Level || 'N/A'} mIU/L</div>
                <div class="value"><strong>T3 Level:</strong> ${item.user_data?.T3_Level || 'N/A'} pg/mL</div>
                <div class="value"><strong>T4 Level:</strong> ${item.user_data?.T4_Level || 'N/A'} μg/dL</div>
                <div class="value"><strong>Nodule Size:</strong> ${item.user_data?.Nodule_Size || 'N/A'} cm</div>
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
                ${(item.recommendations || generateRecommendations(item.risk_percentage))
                    .map(rec => `<div class="recommendation">${rec}</div>`)
                    .join('')}
            </div>
            
            <div class="section">
                <p><em>This report is generated by ThyroScan AI for informational purposes only. Please consult with a healthcare professional for medical advice.</em></p>
            </div>
        </body>
        </html>
    `);
    printWindow.document.close();
}

// Confirm Delete History
function confirmDeleteHistory(id) {
    if (confirm('Are you sure you want to delete this record?')) {
        deleteHistoryRecord(id);
    }
}

// Delete History Record
function deleteHistoryRecord(id) {
    // Remove from arrays
    historyData = historyData.filter(item => item.id !== id);
    filteredHistory = filteredHistory.filter(item => item.id !== id);
    
    // Update localStorage
    localStorage.setItem('thyroscan_history', JSON.stringify(historyData));
    
    // Update UI
    updateHistoryDisplay();
    updateSummaryStats();
    updateCharts();
    
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
    
    // Show/hide views
    const listView = document.getElementById('listView');
    const gridView = document.getElementById('gridView');
    
    if (view === 'list') {
        if (listView) listView.classList.remove('hidden');
        if (gridView) gridView.classList.add('hidden');
    } else {
        if (listView) listView.classList.add('hidden');
        if (gridView) gridView.classList.remove('hidden');
    }
    
    updateHistoryDisplay();
}

// Update Pagination
function updatePagination() {
    currentPage = 1;
    updatePaginationControls();
}

// Update Pagination Controls
function updatePaginationControls() {
    const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    const pageInfo = document.getElementById('pageInfo');
    
    if (prevPageBtn) {
        prevPageBtn.disabled = currentPage === 1;
    }
    
    if (nextPageBtn) {
        nextPageBtn.disabled = currentPage === totalPages || totalPages === 0;
    }
    
    if (pageInfo) {
        const startIndex = (currentPage - 1) * itemsPerPage + 1;
        const endIndex = Math.min(currentPage * itemsPerPage, filteredHistory.length);
        pageInfo.textContent = `Showing ${startIndex}-${endIndex} of ${filteredHistory.length}`;
    }
    
    // Update page numbers
    const pageNumbers = document.getElementById('pageNumbers');
    if (pageNumbers) {
        pageNumbers.innerHTML = '';
        
        for (let i = 1; i <= totalPages; i++) {
            const pageBtn = document.createElement('button');
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
        
        const confirmBtn = document.getElementById('confirmClear');
        if (confirmBtn) {
            confirmBtn.addEventListener('click', clearAllHistory);
        }
    }
    
    // Escape key to close modals
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const detailModal = document.getElementById('detailModal');
            const confirmModal = document.getElementById('clearConfirmModal');
            
            if (!detailModal.classList.contains('hidden')) {
                closeDetailModal();
            } else if (!confirmModal.classList.contains('hidden')) {
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
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());
    
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
    
    // Show with animation
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Auto remove
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
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

// Add a new prediction to history (called from prediction page)
function addNewPrediction(predictionData) {
    const newRecord = {
        id: `pred_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        timestamp: new Date().toISOString(),
        ...predictionData
    };
    
    // Add to beginning of array
    historyData.unshift(newRecord);
    
    // Save to localStorage
    localStorage.setItem('thyroscan_history', JSON.stringify(historyData));
    
    // Update UI if history page is active
    if (document.getElementById('historyTableBody')) {
        processHistoryData();
        updateHistoryDisplay();
        updateSummaryStats();
        updateCharts();
    }
    
    // Also save a flag that new prediction was added
    localStorage.setItem('thyroscan_new_prediction', JSON.stringify(newRecord));
    
    console.log('✅ New prediction added to history:', newRecord);
    return newRecord;
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

// Make functions available globally
window.ThyroScanHistory = {
    initializeHistoryPage,
    refreshHistory,
    exportHistory,
    clearAllHistory,
    addNewPrediction,
    showHistoryDetails,
    closeDetailModal,
    closeConfirmModal
};