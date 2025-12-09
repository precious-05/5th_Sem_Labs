// ============================================
// HISTORY.JS - History Page JavaScript for ThyroScan AI
// ============================================

// Global variables
let historyData = [];
let filteredHistory = [];
let currentPage = 1;
let itemsPerPage = 10;
let currentView = 'list';
let sortColumn = 'timestamp';
let sortDirection = 'desc';

// Initialize History Page
function initializeHistoryPage() {
    console.log('📊 History page initialized');
    
    // Initialize page elements
    initializePageElements();
    
    // Load prediction history
    loadHistory();
    
    // Initialize charts
    initializeCharts();
    
    // Initialize interactive elements
    initializeInteractiveElements();
    
    // Setup event listeners
    setupHistoryEventListeners();
    
    // Initialize filters
    initializeFilters();
    
    // Initialize modals
    initializeModals();
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
}

// Load Prediction History
async function loadHistory() {
    try {
        const limit = 100; // Load more items for filtering
        const response = await fetch(`${window.API_BASE_URL || 'http://localhost:8000'}/history?limit=${limit}`);
        
        if (response.ok) {
            const data = await response.json();
            historyData = data.history || [];
            
            // If no data from API, load demo data
            if (historyData.length === 0) {
                historyData = generateDemoHistory();
                ThyroScan.showInfo('Showing demo history data', 'Demo Mode');
            }
            
            // Process and display history
            processHistoryData();
            updateHistoryDisplay();
            updateSummaryStats();
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
        updateCharts();
        
        ThyroScan.showWarning('Using demo data - API not available', 'Offline Mode');
    } finally {
        // Hide loading state
        const loadingState = document.getElementById('historyLoading');
        if (loadingState) {
            loadingState.classList.add('hidden');
        }
    }
}

// Generate Demo History Data
function generateDemoHistory() {
    const demoData = [];
    const riskLevels = ['Low', 'Medium', 'High'];
    const predictions = ['Benign', 'Malignant'];
    const genders = ['Male', 'Female'];
    
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30); // Last 30 days
    
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
    
    // Sort by date
    return demoData.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
}

// Process History Data
function processHistoryData() {
    // Sort data
    filteredHistory = [...historyData].sort((a, b) => {
        let aValue = a[sortColumn];
        let bValue = b[sortColumn];
        
        // Handle nested properties
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
    
    // Apply filters
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
    
    // Update pagination
    updatePagination();
}

// Update History Display
function updateHistoryDisplay() {
    if (currentView === 'list') {
        updateListView();
    } else {
        updateGridView();
    }
    
    // Update empty state
    const emptyState = document.getElementById('historyEmpty');
    const tableBody = document.getElementById('historyTableBody');
    const gridView = document.getElementById('historyGrid');
    
    if (filteredHistory.length === 0) {
        if (emptyState) emptyState.classList.remove('hidden');
        if (tableBody) tableBody.classList.add('hidden');
        if (gridView) gridView.classList.add('hidden');
    } else {
        if (emptyState) emptyState.classList.add('hidden');
        if (tableBody) tableBody.classList.remove('hidden');
        if (gridView) gridView.classList.remove('hidden');
    }
}

// Update List View
function updateListView() {
    const tableBody = document.getElementById('historyTableBody');
    if (!tableBody) return;
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    // Clear existing rows
    tableBody.innerHTML = '';
    
    // Add rows for current page
    pageItems.forEach((item, index) => {
        const row = createHistoryRow(item, startIndex + index);
        tableBody.appendChild(row);
    });
    
    // Update pagination controls
    updatePaginationControls();
}

// Create History Row
function createHistoryRow(item, index) {
    const row = document.createElement('div');
    row.className = 'history-item fade-in';
    row.style.animationDelay = `${index * 0.05}s`;
    
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
    
    // Add event listeners
    const viewBtn = row.querySelector('.btn-view');
    const deleteBtn = row.querySelector('.btn-delete');
    
    if (viewBtn) {
        viewBtn.addEventListener('click', () => showHistoryDetails(item));
    }
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', () => confirmDeleteHistory(item.id, index));
    }
    
    return row;
}

// Update Grid View
function updateGridView() {
    const gridView = document.getElementById('historyGrid');
    if (!gridView) return;
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageItems = filteredHistory.slice(startIndex, endIndex);
    
    // Clear existing cards
    gridView.innerHTML = '';
    
    // Add cards for current page
    pageItems.forEach((item, index) => {
        const card = createHistoryCard(item, startIndex + index);
        gridView.appendChild(card);
    });
    
    // Update pagination controls
    updatePaginationControls();
}

// Create History Card
function createHistoryCard(item, index) {
    const card = document.createElement('div');
    card.className = 'history-card fade-in';
    card.style.animationDelay = `${index * 0.05}s`;
    
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
    
    // Add event listeners
    const viewBtn = card.querySelector('.btn-view-full');
    const deleteBtn = card.querySelector('.btn-delete');
    
    if (viewBtn) {
        viewBtn.addEventListener('click', () => showHistoryDetails(item));
    }
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', () => confirmDeleteHistory(item.id, index));
    }
    
    return card;
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
        const average = filteredHistory.length > 0 ? totalRisk / filteredHistory.length : 0;
        avgRisk.textContent = `${Math.round(average)}%`;
    }
    
    // Update header stats
    updateHeaderStats();
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
    // Create chart containers if they don't exist
    createChartContainers();
    
    // Initialize distribution chart
    initializeDistributionChart();
    
    // Initialize trend chart
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
    
    // Destroy existing chart
    if (window.riskDistributionChart) {
        window.riskDistributionChart.destroy();
    }
    
    // Create chart
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
                    backgroundColor: 'rgba(26, 26, 46, 0.9)',
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
            cutout: '70%'
        }
    });
}

// Initialize Trend Chart
function initializeTrendChart() {
    const ctx = document.getElementById('riskTrendChart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (window.riskTrendChart) {
        window.riskTrendChart.destroy();
    }
    
    // Create chart
    window.riskTrendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Risk Score Trend',
                data: [],
                borderColor: 'rgba(45, 91, 255, 1)',
                backgroundColor: 'rgba(45, 91, 255, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(45, 91, 255, 1)',
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
                    backgroundColor: 'rgba(26, 26, 46, 0.9)',
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
    if (!window.riskDistributionChart) return;
    
    // Calculate risk distribution
    const lowRisk = filteredHistory.filter(item => (item.risk_percentage || 0) < 30).length;
    const mediumRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 30 && (item.risk_percentage || 0) < 70).length;
    const highRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 70).length;
    
    // Update chart data
    window.riskDistributionChart.data.datasets[0].data = [lowRisk, mediumRisk, highRisk];
    window.riskDistributionChart.update();
}

// Update Trend Chart
function updateTrendChart() {
    if (!window.riskTrendChart) return;
    
    // Get period selection
    const period = document.getElementById('trendPeriod')?.value || 'month';
    
    // Calculate date range
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
    
    // Filter data by period
    const periodData = filteredHistory.filter(item => {
        const itemDate = new Date(item.timestamp);
        return itemDate >= startDate && itemDate <= now;
    });
    
    // Group data by day
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
    
    // Prepare chart data
    const labels = Object.keys(groupedData).sort();
    const data = labels.map(date => {
        const group = groupedData[date];
        return group.count > 0 ? Math.round(group.total / group.count) : 0;
    });
    
    // Update chart
    window.riskTrendChart.data.labels = labels;
    window.riskTrendChart.data.datasets[0].data = data;
    window.riskTrendChart.update();
}

// Initialize Interactive Elements
function initializeInteractiveElements() {
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
        searchInput.addEventListener('input', ThyroScan.debounce(() => {
            applyFilters();
            updateHistoryDisplay();
            updateSummaryStats();
            updateCharts();
        }, 300));
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
}

// Switch View
function switchView(view) {
    currentView = view;
    
    // Update active button
    document.querySelectorAll('.view-toggle-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-view') === view) {
            btn.classList.add('active');
        }
    });
    
    // Show/hide views
    const listView = document.getElementById('listView');
    const gridView = document.getElementById('gridView');
    
    if (listView) listView.classList.toggle('active', view === 'list');
    if (gridView) gridView.classList.toggle('hidden', view !== 'grid');
    
    // Update display
    updateHistoryDisplay();
}

// Initialize Filters
function initializeFilters() {
    // Set default values
    const filterRisk = document.getElementById('filterRisk');
    const filterDate = document.getElementById('filterDate');
    const filterPrediction = document.getElementById('filterPrediction');
    
    if (filterRisk) filterRisk.value = '';
    if (filterDate) filterDate.value = '';
    if (filterPrediction) filterPrediction.value = '';
}

// Initialize Modals
function initializeModals() {
    // Detail modal
    const detailModal = document.getElementById('detailModal');
    if (detailModal) {
        // Close modal when clicking overlay
        const overlay = detailModal.querySelector('.modal-overlay');
        if (overlay) {
            overlay.addEventListener('click', closeDetailModal);
        }
        
        // Close modal when clicking close button
        const closeButton = document.getElementById('closeDetailModal');
        if (closeButton) {
            closeButton.addEventListener('click', closeDetailModal);
        }
        
        // Escape key to close modal
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

// Setup History Event Listeners
function setupHistoryEventListeners() {
    // Refresh button
    const refreshBtn = document.getElementById('refreshHistory');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
            refreshBtn.disabled = true;
            
            loadHistory().finally(() => {
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
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
        clearBtn.addEventListener('click', () => {
            showConfirmModal();
        });
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

// Update Pagination
function updatePagination() {
    const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
    
    // Reset to first page if current page is invalid
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
    
    // Update button states
    if (prevPageBtn) {
        prevPageBtn.disabled = currentPage === 1;
    }
    
    if (nextPageBtn) {
        nextPageBtn.disabled = currentPage === totalPages || totalPages === 0;
    }
    
    // Update page numbers
    if (pageNumbers && totalPages > 0) {
        pageNumbers.innerHTML = '';
        
        // Show max 5 page numbers
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
    
    // Show/hide pagination
    const pagination = document.getElementById('historyPagination');
    if (pagination) {
        pagination.classList.toggle('hidden', filteredHistory.length <= itemsPerPage);
    }
}

// Show History Details
function showHistoryDetails(item) {
    const modal = document.getElementById('detailModal');
    if (!modal) return;
    
    // Populate modal with item data
    populateDetailModal(item);
    
    // Show modal
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Populate Detail Modal
function populateDetailModal(item) {
    // Basic info
    const date = new Date(item.timestamp);
    document.getElementById('detailRiskPercentage').textContent = `${item.risk_percentage || 0}%`;
    document.getElementById('detailPrediction').textContent = item.prediction || 'N/A';
    document.getElementById('detailDate').textContent = `Date: ${date.toLocaleString()}`;
    document.getElementById('detailRiskLevel').textContent = getRiskLevel(item.risk_percentage || 0);
    document.getElementById('detailConfidence').textContent = item.confidence || '85% confidence';
    
    // Parameters
    document.getElementById('detailAge').textContent = `${item.user_data?.Age || 'N/A'} years`;
    document.getElementById('detailGender').textContent = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
    document.getElementById('detailTSH').textContent = `${item.user_data?.TSH_Level || 'N/A'} mIU/L`;
    document.getElementById('detailT3').textContent = `${item.user_data?.T3_Level || 'N/A'} pg/mL`;
    document.getElementById('detailT4').textContent = `${item.user_data?.T4_Level || 'N/A'} μg/dL`;
    document.getElementById('detailNodule').textContent = `${item.user_data?.Nodule_Size || 'N/A'} cm`;
    document.getElementById('detailCancerRisk').textContent = item.user_data?.Thyroid_Cancer_Risk || 'N/A';
    
    // Risk factors
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
            factorsList.innerHTML = activeFactors.map(f => `
                <div class="factor-item">
                    <i class="fas fa-check-circle"></i>
                    <span>${f.label}</span>
                </div>
            `).join('');
        } else {
            factorsList.innerHTML = '<div class="no-factors">No risk factors recorded</div>';
        }
    }
    
    // Recommendations
    const recommendationsList = document.getElementById('detailRecommendations');
    if (recommendationsList) {
        const recommendations = item.recommendations || generateRecommendations(item.risk_percentage || 0);
        recommendationsList.innerHTML = recommendations.map(rec => `
            <li><i class="fas fa-check"></i> ${rec}</li>
        `).join('');
    }
    
    // Tab functionality
    const tabBtns = modal.querySelectorAll('.tab-btn');
    const tabContents = modal.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Update active tab
            tabBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding content
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `${tabId}Tab`) {
                    content.classList.add('active');
                }
            });
        });
    });
    
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
    
    // Download report button
    const downloadBtn = document.getElementById('downloadReport');
    if (downloadBtn) {
        downloadBtn.onclick = () => downloadHistoryReport(item);
    }
    
    // Print report button
    const printBtn = document.getElementById('printReport');
    if (printBtn) {
        printBtn.onclick = () => printHistoryReport(item);
    }
}

// Close Detail Modal
function closeDetailModal() {
    const modal = document.getElementById('detailModal');
    if (!modal) return;
    
    modal.classList.add('hidden');
    document.body.style.overflow = '';
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
        ThyroScan.showWarning('No history data to export', 'Export Failed');
        return;
    }
    
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
    
    // Convert to CSV
    const headers = Object.keys(exportData[0]);
    const csv = [
        headers.join(','),
        ...exportData.map(row => headers.map(header => `"${row[header]}"`).join(','))
    ].join('\n');
    
    // Create download link
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `thyroscan_history_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    ThyroScan.showSuccess(`Exported ${exportData.length} records`, 'Export Complete');
}

// Clear All History
function clearAllHistory() {
    // Clear local data
    historyData = [];
    filteredHistory = [];
    currentPage = 1;
    
    // Update display
    updateHistoryDisplay();
    updateSummaryStats();
    updateCharts();
    
    // Close modal
    closeConfirmModal();
    
    // Show success message
    ThyroScan.showSuccess('All history has been cleared', 'History Cleared');
    
    // Try to clear server data
    clearServerHistory();
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
    ThyroScan.showInfo(
        'Are you sure you want to delete this record?',
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
    // Remove from local data
    historyData = historyData.filter(item => item.id !== id);
    filteredHistory = filteredHistory.filter(item => item.id !== id);
    
    // Update display
    updateHistoryDisplay();
    updateSummaryStats();
    updateCharts();
    
    // Show success message
    ThyroScan.showSuccess('Record deleted successfully', 'Deleted');
    
    // Try to delete from server
    deleteServerRecord(id);
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
    
    ThyroScan.showSuccess('Report downloaded', 'Download Complete');
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
                    h1 { color: #2D5BFF; }
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
    if (percentage < 30) return '#2ED573';
    if (percentage < 70) return '#FFA502';
    return '#FF4757';
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

// Initialize history page
document.addEventListener('DOMContentLoaded', () => {
    if (typeof initializeHistoryPage === 'function') {
        initializeHistoryPage();
    }
});

// Export functions for debugging
window.HistoryPage = {
    initializeHistoryPage,
    loadHistory,
    updateHistoryDisplay,
    showHistoryDetails,
    exportHistory,
    clearAllHistory
};