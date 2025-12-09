// ============================================
// THYROSCAN AI HISTORY.JS - MONGODB COMPATIBLE
// 100% CORRECTED VERSION
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

// API Configuration - MATCHES YOUR BACKEND
const API_CONFIG = {
    BASE_URL: window.API_BASE_URL || 'http://localhost:8000',
    ENDPOINTS: {
        HISTORY: '/history',
        PREDICT: '/predict',
        HEALTH: '/health'
    }
};

// Initialize History Page - FIXED
function initializeHistoryPage() {
    if (isInitialized) {
        console.log('⚠️ Already initialized');
        return;
    }
    
    console.log('📊 Initializing History Page with MongoDB...');
    
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
    
    // Load prediction history from MongoDB
    loadHistory();
    
    isInitialized = true;
    
    // Setup real-time listener for new predictions
    setupRealTimeListener();
}

// Setup Real-time Listener for new predictions
function setupRealTimeListener() {
    // Listen for storage events (when prediction is saved)
    window.addEventListener('storage', function(e) {
        if (e.key === 'thyroscan_new_prediction') {
            console.log('🔄 New prediction detected, refreshing...');
            refreshHistory();
        }
    });
    
    // Check if there's a new prediction from localStorage
    if (localStorage.getItem('thyroscan_new_prediction')) {
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
    // Update current year
    const yearElement = document.getElementById('currentYear');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
        yearElement.classList.add('fade-in');
    }
    
    // Initialize empty state
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
                <button class="btn-primary" onclick="window.location.href='predict.html'">
                    <i class="fas fa-plus"></i>
                    Make Your First Prediction
                </button>
            </div>
        `;
    }
}

// Load Prediction History from MongoDB - FIXED
// Load Prediction History from MongoDB - FIXED FOR FILE PROTOCOL
async function loadHistory() {
    try {
        // Show loading animation
        showTableLoading();
        
        console.log('📡 Fetching history from MongoDB API...');
        
        // FIX: Add mode: 'cors' and credentials: 'include'
        const response = await fetch(
            `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HISTORY}?limit=100`,
            {
                method: 'GET',
                mode: 'cors',  // ✅ Add this
                credentials: 'include',  // ✅ Add this
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            }
        );
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status} - ${await response.text()}`);
        }
        
        const data = await response.json();
        
        // YOUR BACKEND RESPONSE FORMAT: { "history": [...], "count": X }
        historyData = data.history || [];
        
        console.log(`✅ Loaded ${historyData.length} records from MongoDB`);
        
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
        
        // Fallback: Try to load from localStorage as backup
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
        emptyState.classList.add('fade-in');
    }
    
    if (tableBody) tableBody.innerHTML = '';
    if (gridView) gridView.innerHTML = '';
}

// Process History Data - FIXED
function processHistoryData() {
    console.log('🔄 Processing history data...');
    
    // Sort data based on timestamp (from MongoDB)
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

// Apply Filters - FIXED
function applyFilters() {
    const riskFilter = document.getElementById('filterRisk')?.value;
    const dateFilter = document.getElementById('filterDate')?.value;
    const predictionFilter = document.getElementById('filterPrediction')?.value;
    const searchTerm = document.getElementById('historySearch')?.value.toLowerCase() || '';
    
    console.log('🔍 Applying filters:', { riskFilter, dateFilter, predictionFilter, searchTerm });
    
    filteredHistory = historyData.filter(item => {
        // Risk filter
        if (riskFilter && riskFilter !== 'all') {
            const riskPercentage = item.risk_percentage || 0;
            if (riskFilter === 'low' && riskPercentage >= 30) return false;
            if (riskFilter === 'medium' && (riskPercentage < 30 || riskPercentage >= 70)) return false;
            if (riskFilter === 'high' && riskPercentage < 70) return false;
        }
        
        // Date filter
        if (dateFilter && dateFilter !== 'all') {
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
        if (predictionFilter && predictionFilter !== 'all') {
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
    
    console.log(`✅ After filtering: ${filteredHistory.length} records`);
    
    // Reset to first page after filtering
    currentPage = 1;
}

// Update History Display
function updateHistoryDisplay() {
    console.log('🎨 Updating history display...');
    
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

// Update List View - FIXED
function updateListView() {
    const tableBody = document.getElementById('historyTableBody');
    if (!tableBody) {
        console.error('❌ Table body not found');
        return;
    }
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    console.log(`📋 Displaying ${pageItems.length} items in list view (page ${currentPage})`);
    
    tableBody.innerHTML = '';
    
    if (pageItems.length === 0) {
        tableBody.innerHTML = `
            <tr class="no-data-row">
                <td colspan="6" class="text-center">
                    <div class="no-data-message enhanced">
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

// Create History Row - FIXED
function createHistoryRow(item, index) {
    const row = document.createElement('tr');
    row.className = 'history-item enhanced fade-in-up';
    row.style.animationDelay = `${index * 0.05}s`;
    
    try {
        const date = new Date(item.timestamp || Date.now());
        const age = item.user_data?.Age || 'N/A';
        const gender = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
        const riskPercentage = item.risk_percentage || 0;
        const prediction = item.prediction || 'N/A';
        
        row.innerHTML = `
            <td class="history-date enhanced">
                <div class="date-display">
                    <div class="date">${date.toLocaleDateString()}</div>
                    <div class="time">${date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                </div>
            </td>
            
            <td class="history-patient enhanced">
                <div class="patient-info">
                    <div class="patient-avatar pulse-animation" style="--pulse-color: ${getRiskColor(riskPercentage)}">
                        <i class="fas fa-user${gender === 'Male' ? '' : '-female'}"></i>
                    </div>
                    <div class="patient-details">
                        <h4>Patient ${index + 1}</h4>
                        <p><i class="fas fa-birthday-cake"></i> ${age} yrs • <i class="fas fa-${gender === 'Male' ? 'mars' : 'venus'}"></i> ${gender}</p>
                    </div>
                </div>
            </td>
            
            <td class="history-risk enhanced">
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
            
            <td class="history-prediction enhanced">
                <span class="prediction-badge ${prediction.toLowerCase()}">
                    <i class="fas fa-${prediction === 'Malignant' ? 'exclamation-triangle' : 'check-circle'}"></i>
                    ${prediction}
                </span>
            </td>
            
            <td class="history-factors enhanced">
                <div class="factors-tags">
                    ${getTopFactors(item.user_data).map(factor => `
                        <span class="factor-tag">
                            <i class="fas fa-circle"></i>
                            ${factor}
                        </span>
                    `).join('')}
                </div>
            </td>
            
            <td class="history-actions enhanced">
                <button class="btn-view enhanced" data-id="${index}" title="View Details">
                    <i class="fas fa-eye"></i>
                    <span class="tooltip">View Details</span>
                </button>
                <button class="btn-download" data-id="${index}" title="Download Report">
                    <i class="fas fa-download"></i>
                    <span class="tooltip">Download Report</span>
                </button>
                <button class="btn-delete enhanced" data-id="${index}" title="Delete Record">
                    <i class="fas fa-trash-alt"></i>
                    <span class="tooltip">Delete Record</span>
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
            deleteBtn.addEventListener('click', () => confirmDeleteHistory(index));
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

// Update Grid View - FIXED
function updateGridView() {
    const gridView = document.getElementById('historyGrid');
    if (!gridView) {
        console.error('❌ Grid view not found');
        return;
    }
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    console.log(`📱 Displaying ${pageItems.length} items in grid view (page ${currentPage})`);
    
    gridView.innerHTML = '';
    
    if (pageItems.length === 0) {
        gridView.innerHTML = `
            <div class="no-data-card enhanced">
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

// Create History Card - FIXED
function createHistoryCard(item, index) {
    const card = document.createElement('div');
    card.className = 'history-card enhanced fade-in-up';
    card.style.animationDelay = `${index * 0.05}s`;
    
    try {
        const date = new Date(item.timestamp || Date.now());
        const riskPercentage = item.risk_percentage || 0;
        const prediction = item.prediction || 'N/A';
        const age = item.user_data?.Age || 'N/A';
        const gender = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
        
        card.innerHTML = `
            <div class="card-header enhanced">
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
                            <span class="score-value">${riskPercentage.toFixed(1)}%</span>
                            <span class="score-label">Risk Score</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card-prediction enhanced">
                <span class="prediction-badge ${prediction.toLowerCase()}">
                    <i class="fas fa-${prediction === 'Malignant' ? 'exclamation-triangle' : 'check-circle'}"></i>
                    ${prediction}
                </span>
            </div>
            
            <div class="card-details enhanced">
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
            
            <div class="card-footer enhanced">
                <button class="btn-view-full ripple" data-id="${index}">
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
        console.log('📭 Showing empty state');
        if (emptyState) {
            emptyState.classList.remove('hidden');
            emptyState.classList.add('fade-in');
        }
        if (listView) listView.classList.add('hidden');
        if (gridView) gridView.classList.add('hidden');
    } else {
        console.log('📊 Hiding empty state');
        if (emptyState) emptyState.classList.add('hidden');
    }
}

// Update Summary Stats
function updateSummaryStats() {
    console.log('📈 Updating summary stats...');
    
    // Total predictions
    const totalCount = document.getElementById('totalCount');
    if (totalCount) {
        totalCount.textContent = filteredHistory.length;
        totalCount.classList.add('pulse');
        setTimeout(() => totalCount.classList.remove('pulse'), 500);
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
    
    console.log('✅ Summary stats updated');
}

// Initialize Charts - FIXED (Chart.js check added)
function initializeCharts() {
    console.log('📊 Initializing charts...');
    
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.warn('⚠️ Chart.js not loaded. Skipping charts initialization.');
        
        // Show placeholder messages
        const distributionChart = document.getElementById('riskDistributionChart');
        const trendChart = document.getElementById('riskTrendChart');
        
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
    
    // Initialize distribution chart
    initDistributionChart();
    
    // Initialize trend chart
    initTrendChart();
}

// Initialize Distribution Chart - FIXED
function initDistributionChart() {
    const ctx = document.getElementById('riskDistributionChart');
    if (!ctx) {
        console.error('❌ Distribution chart canvas not found');
        return;
    }
    
    // Destroy existing chart
    if (chartInstances.distributionChart) {
        chartInstances.distributionChart.destroy();
    }
    
    const lowRisk = filteredHistory.filter(item => (item.risk_percentage || 0) < 30).length;
    const mediumRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 30 && (item.risk_percentage || 0) < 70).length;
    const highRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 70).length;
    
    console.log('📊 Distribution data:', { lowRisk, mediumRisk, highRisk });
    
    try {
        chartInstances.distributionChart = new Chart(ctx, {
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

// Initialize Trend Chart - FIXED
function initTrendChart() {
    const ctx = document.getElementById('riskTrendChart');
    if (!ctx) {
        console.error('❌ Trend chart canvas not found');
        return;
    }
    
    // Destroy existing chart
    if (chartInstances.trendChart) {
        chartInstances.trendChart.destroy();
    }
    
    // Get last 7 days of data
    const trendData = getTrendData(7);
    
    console.log('📈 Trend data:', trendData);
    
    try {
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

// Get Trend Data - FIXED
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

// Update Charts
function updateCharts() {
    if (!window.Chart) {
        console.warn('⚠️ Chart.js not available');
        return;
    }
    
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

// Setup History Event Listeners - FIXED
function setupHistoryEventListeners() {
    console.log('🔗 Setting up event listeners...');
    
    // Refresh button
    const refreshBtn = document.getElementById('refreshHistory');
    if (refreshBtn) {
        console.log('✅ Found refresh button');
        refreshBtn.addEventListener('click', function() {
            console.log('🔄 Refresh button clicked');
            this.classList.add('refreshing');
            this.disabled = true;
            
            refreshHistory().finally(() => {
                setTimeout(() => {
                    this.classList.remove('refreshing');
                    this.disabled = false;
                }, 500);
            });
        });
    } else {
        console.warn('⚠️ Refresh button not found');
    }
    
    // Export button
    const exportBtn = document.getElementById('exportHistory');
    if (exportBtn) {
        console.log('✅ Found export button');
        exportBtn.addEventListener('click', function() {
            console.log('💾 Export button clicked');
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
        console.log('✅ Found clear button');
        clearBtn.addEventListener('click', function() {
            console.log('🗑️ Clear button clicked');
            this.classList.add('warning-pulse');
            setTimeout(() => this.classList.remove('warning-pulse'), 1000);
            
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
        console.log('✅ Found search input');
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            console.log('🔍 Search input:', this.value);
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
    console.log(`✅ Found ${filterSelects.length} filter selects`);
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            console.log(`📊 Filter changed: ${this.id} = ${this.value}`);
            applyFilters();
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
        });
    });
    
    // View toggle buttons
    const viewToggleBtns = document.querySelectorAll('.view-toggle-btn');
    console.log(`✅ Found ${viewToggleBtns.length} view toggle buttons`);
    viewToggleBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const view = this.getAttribute('data-view');
            console.log(`Switching to ${view} view`);
            switchView(view);
        });
    });
    
    // Pagination buttons
    const prevPageBtn = document.getElementById('prevPage');
    const nextPageBtn = document.getElementById('nextPage');
    
    if (prevPageBtn) {
        console.log('✅ Found previous page button');
        prevPageBtn.addEventListener('click', () => {
            console.log('◀️ Previous page clicked');
            if (currentPage > 1) {
                currentPage--;
                updateHistoryDisplay();
                updatePaginationControls();
            }
        });
    }
    
    if (nextPageBtn) {
        console.log('✅ Found next page button');
        nextPageBtn.addEventListener('click', () => {
            console.log('▶️ Next page clicked');
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
        console.log('✅ Found confirm clear button');
        confirmClearBtn.addEventListener('click', function() {
            console.log('✅ Confirm clear clicked');
            this.classList.add('processing');
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Clearing...';
            this.disabled = true;
            
            setTimeout(() => {
                clearAllHistory();
                this.classList.remove('processing');
                this.innerHTML = 'Yes, Clear All';
                this.disabled = false;
            }, 500);
        });
    }
    
    // Cancel clear button
    const cancelClearBtn = document.getElementById('cancelClear');
    if (cancelClearBtn) {
        console.log('✅ Found cancel clear button');
        cancelClearBtn.addEventListener('click', closeConfirmModal);
    }
    
    console.log('✅ Event listeners setup complete');
}

// Refresh History
async function refreshHistory() {
    console.log('🔄 Refreshing history...');
    showNotification('Refreshing history...', 'info');
    await loadHistory();
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
    a.download = `thyroscan_history_${new Date().toISOString().split('T')[0]}.csv`;
    
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification(`Exported ${filteredHistory.length} records`, 'success');
}

// Clear All History
function clearAllHistory() {
    console.log('🗑️ Clearing all history...');
    
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
    
    // Close modal
    closeConfirmModal();
    
    showNotification('All history has been cleared', 'success');
}

// Show History Details
function showHistoryDetails(item) {
    console.log('🔍 Showing history details:', item);
    const modal = document.getElementById('detailModal');
    if (!modal) {
        console.error('❌ Detail modal not found');
        return;
    }
    
    // Populate modal
    populateDetailModal(item);
    
    // Show modal
    modal.classList.remove('hidden');
    modal.classList.add('active');
    document.body.classList.add('modal-open');
}

// Populate Detail Modal - FIXED
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
        modal.classList.remove('active');
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
        document.body.classList.remove('modal-open');
    }
}

// Show Confirm Modal
function showConfirmModal() {
    const modal = document.getElementById('clearConfirmModal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('active');
        document.body.classList.add('modal-open');
    }
}

// Close Confirm Modal
function closeConfirmModal() {
    const modal = document.getElementById('clearConfirmModal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
        document.body.classList.remove('modal-open');
    }
}

// Download History Report
function downloadHistoryReport(item) {
    // Create report content
    const reportContent = `
ThyroScan AI Prediction Report
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
Generated by ThyroScan AI
${window.location.origin}
Generated on: ${new Date().toLocaleString()}
    `.trim();

    // Create download
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const timestamp = new Date(item.timestamp || Date.now()).toISOString().split('T')[0];
    a.download = `thyroscan_report_${timestamp}.txt`;
    
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
            
            <h1>ThyroScan AI Prediction Report</h1>
            
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
                <p><em>This report is generated by ThyroScan AI for informational purposes only. Please consult with a healthcare professional for medical advice.</em></p>
            </div>
        </body>
        </html>
    `);
    printWindow.document.close();
}

// Confirm Delete History
function confirmDeleteHistory(index) {
    if (confirm('Are you sure you want to delete this record?')) {
        deleteHistoryRecord(index);
    }
}

// Delete History Record
function deleteHistoryRecord(index) {
    // Remove from arrays
    historyData.splice(index, 1);
    filteredHistory = filteredHistory.filter((_, i) => i !== index);
    
    // Update localStorage backup
    localStorage.setItem('thyroscan_local_history', JSON.stringify(historyData));
    
    // Update UI
    updateHistoryDisplay();
    updateSummaryStats();
    updateCharts();
    
    showNotification('Record deleted successfully', 'success');
}

// Switch View
function switchView(view) {
    if (currentView === view) return;
    
    console.log(`👁️ Switching view from ${currentView} to ${view}`);
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
    
    console.log(`📄 Pagination: Page ${currentPage} of ${totalPages}`);
}

// Initialize Modals
function initializeModals() {
    console.log('🚪 Initializing modals...');
    
    // Detail modal
    const detailModal = document.getElementById('detailModal');
    if (detailModal) {
        console.log('✅ Found detail modal');
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
        console.log('✅ Found confirmation modal');
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
    
    console.log('✅ Modals initialized');
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

// Initialize when DOM is loaded - FIXED
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOM Content Loaded - Checking history page');
    
    // Check if we're on history page
    if (document.getElementById('historyTableBody') || document.getElementById('historyGrid')) {
        console.log('✅ History page detected');
        setTimeout(() => {
            initializeHistoryPage();
        }, 100);
    } else {
        console.log('❌ Not on history page');
    }
});

// Export functions globally
window.ThyroScanHistory = {
    initializeHistoryPage,
    refreshHistory,
    exportHistory,
    clearAllHistory,
    showHistoryDetails,
    closeDetailModal,
    closeConfirmModal,
    getRiskLevel,
    getRiskColor,
    generateRecommendations
};

console.log('✅ history.js loaded successfully');