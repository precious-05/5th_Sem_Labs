// ===== CONFIGURATION =====
const API_BASE_URL = 'http://localhost:8000';
let historyTable = null;
let riskChart = null;
let trendChart = null;
let allPredictions = [];

// ===== DOM ELEMENTS =====
const elements = {
    // Table elements
    historyTable: document.getElementById('historyTable'),
    historyTableBody: document.getElementById('historyTableBody'),
    loadingState: document.getElementById('loadingState'),
    emptyState: document.getElementById('emptyState'),
    
    // Control elements
    refreshHistory: document.getElementById('refreshHistory'),
    exportHistory: document.getElementById('exportHistory'),
    clearHistory: document.getElementById('clearHistory'),
    searchInput: document.getElementById('searchInput'),
    filterRisk: document.getElementById('filterRisk'),
    filterPrediction: document.getElementById('filterPrediction'),
    filterDate: document.getElementById('filterDate'),
    
    // Analytics elements
    totalPredictions: document.getElementById('totalPredictions'),
    malignantCount: document.getElementById('malignantCount'),
    benignCount: document.getElementById('benignCount'),
    avgRisk: document.getElementById('avgRisk'),
    avgRiskBar: document.getElementById('avgRiskBar'),
    
    // Chart elements
    riskDistributionChart: document.getElementById('riskDistributionChart'),
    trendChart: document.getElementById('trendChart'),
    trendPeriod: document.getElementById('trendPeriod'),
    riskHeatmap: document.getElementById('riskHeatmap'),
    
    // Modal elements
    detailModal: document.getElementById('detailModal'),
    closeModal: document.getElementById('closeModal'),
    printReport: document.getElementById('printReport')
};

// ===== CHART CONFIGURATIONS =====
const CHART_CONFIGS = {
    riskDistribution: {
        type: 'doughnut',
        data: {
            labels: ['Low Risk (0-30%)', 'Moderate Risk (31-70%)', 'High Risk (71-100%)'],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                borderWidth: 2,
                borderColor: '#ffffff'
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
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw} predictions`;
                        }
                    }
                }
            },
            cutout: '70%'
        }
    },
    
    trendAnalysis: {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Average Risk',
                data: [],
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
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
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return `Risk: ${context.raw}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    }
};

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    initializeHistoryPage();
});

async function initializeHistoryPage() {
    try {
        // Hide preloader
        setTimeout(() => {
            document.querySelector('.preloader')?.classList.add('hidden');
            document.body.classList.add('loaded');
        }, 800);

        // Initialize components
        initializeEventListeners();
        initializeCharts();
        initializeDataTable();
        await loadHistoryData();
        setupFilters();
        checkBackendConnection();
        
        console.log('✅ History page initialized');
    } catch (error) {
        console.error('❌ History page initialization failed:', error);
        showNotification('Failed to initialize history page', 'error');
    }
}

// ===== EVENT LISTENERS =====
function initializeEventListeners() {
    // Refresh button
    if (elements.refreshHistory) {
        elements.refreshHistory.addEventListener('click', () => {
            loadHistoryData();
            showNotification('History refreshed', 'success');
        });
    }
    
    // Export button
    if (elements.exportHistory) {
        elements.exportHistory.addEventListener('click', exportHistoryAsCSV);
    }
    
    // Clear button
    if (elements.clearHistory) {
        elements.clearHistory.addEventListener('click', clearAllHistory);
    }
    
    // Search input
    if (elements.searchInput) {
        elements.searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
    
    // Filter changes
    if (elements.filterRisk) {
        elements.filterRisk.addEventListener('change', applyFilters);
    }
    
    if (elements.filterPrediction) {
        elements.filterPrediction.addEventListener('change', applyFilters);
    }
    
    if (elements.filterDate) {
        elements.filterDate.addEventListener('change', applyFilters);
    }
    
    // Trend period change
    if (elements.trendPeriod) {
        elements.trendPeriod.addEventListener('change', updateTrendChart);
    }
    
    // Modal close
    if (elements.closeModal) {
        elements.closeModal.addEventListener('click', () => {
            elements.detailModal.classList.remove('active');
        });
    }
    
    // Print report
    if (elements.printReport) {
        elements.printReport.addEventListener('click', printCurrentReport);
    }
    
    // Close modal on background click
    if (elements.detailModal) {
        elements.detailModal.addEventListener('click', (e) => {
            if (e.target === elements.detailModal) {
                elements.detailModal.classList.remove('active');
            }
        });
    }
    
    // Close modal on ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && elements.detailModal.classList.contains('active')) {
            elements.detailModal.classList.remove('active');
        }
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + F to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
            e.preventDefault();
            if (elements.searchInput) {
                elements.searchInput.focus();
            }
        }
        
        // Ctrl/Cmd + R to refresh
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            loadHistoryData();
        }
    });
}

// ===== DATA TABLE INITIALIZATION =====
function initializeDataTable() {
    if (!elements.historyTable) return;
    
    try {
        historyTable = $('#historyTable').DataTable({
            pageLength: 10,
            lengthMenu: [5, 10, 25, 50],
            order: [[0, 'desc']], // Sort by date descending
            language: {
                search: 'Search predictions:',
                lengthMenu: 'Show _MENU_ entries',
                info: 'Showing _START_ to _END_ of _TOTAL_ entries',
                paginate: {
                    first: 'First',
                    last: 'Last',
                    next: 'Next',
                    previous: 'Previous'
                }
            },
            columnDefs: [
                { orderable: true, targets: [0, 1, 2, 3, 4] },
                { orderable: false, targets: [5] }, // Actions column
                { className: 'dt-body-center', targets: [2, 3, 4] },
                { width: '15%', targets: [5] }
            ],
            initComplete: function() {
                // Hide DataTable's built-in search
                $('.dataTables_filter').hide();
            }
        });
        
        console.log('✅ DataTable initialized');
    } catch (error) {
        console.error('❌ DataTable initialization failed:', error);
        // Fallback to manual table if DataTable fails
        initializeManualTable();
    }
}

function initializeManualTable() {
    console.log('Using manual table implementation');
    // Simple table implementation without DataTable
}

// ===== DATA LOADING =====
async function loadHistoryData() {
    try {
        showLoadingState(true);
        
        const response = await fetch(`${API_BASE_URL}/history?limit=100`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        allPredictions = data.history || [];
        
        // Update UI with data
        updateStats(allPredictions);
        updateTable(allPredictions);
        updateCharts(allPredictions);
        updateHeatmap(allPredictions);
        
        showLoadingState(false);
        
        // Show empty state if no data
        if (allPredictions.length === 0) {
            showEmptyState(true);
        } else {
            showEmptyState(false);
        }
        
        console.log(`✅ Loaded ${allPredictions.length} predictions`);
        
    } catch (error) {
        console.error('❌ Error loading history:', error);
        showNotification('Failed to load prediction history', 'error');
        showLoadingState(false);
        showEmptyState(true);
        
        // Load sample data for demo
        loadSampleData();
    }
}

function showLoadingState(show) {
    if (elements.loadingState) {
        elements.loadingState.style.display = show ? 'flex' : 'none';
    }
    
    if (elements.emptyState) {
        elements.emptyState.style.display = 'none';
    }
    
    if (historyTable) {
        historyTable.style.display = show ? 'none' : 'table';
    }
}

function showEmptyState(show) {
    if (elements.emptyState) {
        elements.emptyState.style.display = show ? 'block' : 'none';
    }
    
    if (historyTable) {
        historyTable.style.display = show ? 'none' : 'table';
    }
}

// ===== STATS UPDATES =====
function updateStats(predictions) {
    if (!predictions || predictions.length === 0) {
        resetStats();
        return;
    }
    
    // Total predictions
    if (elements.totalPredictions) {
        elements.totalPredictions.textContent = predictions.length;
    }
    
    // Malignant/Benign counts
    const malignantCount = predictions.filter(p => p.prediction === 'Malignant').length;
    const benignCount = predictions.filter(p => p.prediction === 'Benign').length;
    
    if (elements.malignantCount) {
        elements.malignantCount.textContent = malignantCount;
    }
    
    if (elements.benignCount) {
        elements.benignCount.textContent = benignCount;
    }
    
    // Average risk
    const totalRisk = predictions.reduce((sum, p) => sum + (p.risk_percentage || 0), 0);
    const avgRisk = predictions.length > 0 ? totalRisk / predictions.length : 0;
    
    if (elements.avgRisk) {
        elements.avgRisk.textContent = `${avgRisk.toFixed(1)}%`;
    }
    
    if (elements.avgRiskBar) {
        elements.avgRiskBar.style.width = `${avgRisk}%`;
    }
    
    // Update trend indicators
    updateTrendIndicators(predictions);
}

function resetStats() {
    const elementsToReset = [
        elements.totalPredictions,
        elements.malignantCount,
        elements.benignCount,
        elements.avgRisk
    ];
    
    elementsToReset.forEach(el => {
        if (el) el.textContent = '0';
    });
    
    if (elements.avgRiskBar) {
        elements.avgRiskBar.style.width = '0%';
    }
}

function updateTrendIndicators(predictions) {
    // Calculate week-over-week change
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
    
    const recentPredictions = predictions.filter(p => {
        const predDate = new Date(p.timestamp);
        return predDate >= oneWeekAgo;
    });
    
    const olderPredictions = predictions.filter(p => {
        const predDate = new Date(p.timestamp);
        return predDate < oneWeekAgo;
    });
    
    if (olderPredictions.length > 0 && recentPredictions.length > 0) {
        const oldAvg = olderPredictions.reduce((sum, p) => sum + p.risk_percentage, 0) / olderPredictions.length;
        const newAvg = recentPredictions.reduce((sum, p) => sum + p.risk_percentage, 0) / recentPredictions.length;
        
        const change = ((newAvg - oldAvg) / oldAvg) * 100;
        
        // Update trend indicator (simplified - you could add visual indicators)
        console.log(`Trend change: ${change.toFixed(1)}%`);
    }
}

// ===== TABLE UPDATES =====
function updateTable(predictions) {
    if (!elements.historyTableBody) return;
    
    // Clear existing rows
    elements.historyTableBody.innerHTML = '';
    
    if (!predictions || predictions.length === 0) {
        showEmptyState(true);
        return;
    }
    
    // Add rows for each prediction
    predictions.forEach((prediction, index) => {
        const row = createTableRow(prediction, index);
        elements.historyTableBody.appendChild(row);
    });
    
    // Update DataTable if available
    if (historyTable) {
        historyTable.clear();
        predictions.forEach(prediction => {
            historyTable.row.add([
                formatDateTime(prediction.timestamp),
                createPatientInfoCell(prediction),
                createRiskCell(prediction.risk_percentage),
                createPredictionCell(prediction.prediction),
                createConfidenceCell(prediction),
                createActionsCell(prediction)
            ]);
        });
        historyTable.draw();
    }
}

function createTableRow(prediction, index) {
    const row = document.createElement('tr');
    row.className = 'fade-in';
    row.style.animationDelay = `${index * 0.05}s`;
    
    const riskLevel = getRiskLevel(prediction.risk_percentage);
    const riskClass = riskLevel.toLowerCase().replace(' ', '-');
    
    row.innerHTML = `
        <td>${formatDateTime(prediction.timestamp)}</td>
        <td>
            <div class="patient-info">
                <span class="patient-age">${prediction.user_data?.Age || 'N/A'} yrs</span>
                <span class="patient-gender">${prediction.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</span>
            </div>
        </td>
        <td>
            <span class="risk-badge ${riskClass}">
                ${prediction.risk_percentage.toFixed(1)}%
            </span>
        </td>
        <td>
            <span class="prediction-badge ${prediction.prediction === 'Malignant' ? 'malignant' : 'benign'}">
                <i class="fas fa-${prediction.prediction === 'Malignant' ? 'exclamation-triangle' : 'check-circle'}"></i>
                ${prediction.prediction}
            </span>
        </td>
        <td>
            <div class="confidence-indicator">
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${prediction.risk_percentage}%"></div>
                </div>
                <span class="confidence-text">${getConfidenceText(prediction.risk_percentage)}</span>
            </div>
        </td>
        <td>
            <div class="action-buttons">
                <button class="view-btn" data-id="${index}">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="delete-btn" data-id="${index}">
                    <i class="fas fa-trash"></i>
                </button>
                <button class="export-btn" data-id="${index}">
                    <i class="fas fa-download"></i>
                </button>
            </div>
        </td>
    `;
    
    // Add event listeners to buttons
    const viewBtn = row.querySelector('.view-btn');
    const deleteBtn = row.querySelector('.delete-btn');
    const exportBtn = row.querySelector('.export-btn');
    
    if (viewBtn) {
        viewBtn.addEventListener('click', () => showPredictionDetails(prediction));
    }
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', () => deletePrediction(index));
    }
    
    if (exportBtn) {
        exportBtn.addEventListener('click', () => exportSinglePrediction(prediction));
    }
    
    return row;
}

function createPatientInfoCell(prediction) {
    return `
        <div class="patient-info">
            <span class="patient-age">${prediction.user_data?.Age || 'N/A'} yrs</span>
            <span class="patient-gender">${prediction.user_data?.Gender_Male === 1 ? 'Male' : 'Female'}</span>
        </div>
    `;
}

function createRiskCell(riskPercentage) {
    const riskLevel = getRiskLevel(riskPercentage);
    const riskClass = riskLevel.toLowerCase().replace(' ', '-');
    
    return `
        <span class="risk-badge ${riskClass}">
            ${riskPercentage.toFixed(1)}%
        </span>
    `;
}

function createPredictionCell(prediction) {
    const isMalignant = prediction === 'Malignant';
    return `
        <span class="prediction-badge ${isMalignant ? 'malignant' : 'benign'}">
            <i class="fas fa-${isMalignant ? 'exclamation-triangle' : 'check-circle'}"></i>
            ${prediction}
        </span>
    `;
}

function createConfidenceCell(prediction) {
    const confidence = getConfidenceText(prediction.risk_percentage);
    return `
        <div class="confidence-cell">
            <span class="confidence-text">${confidence}</span>
            <div class="confidence-meter">
                <div class="meter-fill" style="width: ${prediction.risk_percentage}%"></div>
            </div>
        </div>
    `;
}

function createActionsCell(prediction) {
    return `
        <div class="action-buttons">
            <button class="view-btn" title="View Details">
                <i class="fas fa-eye"></i>
            </button>
            <button class="delete-btn" title="Delete">
                <i class="fas fa-trash"></i>
            </button>
            <button class="export-btn" title="Export">
                <i class="fas fa-download"></i>
            </button>
        </div>
    `;
}

// ===== FILTERS AND SEARCH =====
function setupFilters() {
    // Initialize filter values
    if (elements.filterDate) {
        elements.filterDate.value = '';
    }
    
    if (elements.filterRisk) {
        elements.filterRisk.value = '';
    }
    
    if (elements.filterPrediction) {
        elements.filterPrediction.value = '';
    }
}

function handleSearch() {
    const searchTerm = elements.searchInput.value.toLowerCase().trim();
    
    if (!searchTerm) {
        applyFilters();
        return;
    }
    
    const filtered = allPredictions.filter(prediction => {
        // Search in various fields
        const searchableFields = [
            prediction.prediction,
            formatDateTime(prediction.timestamp),
            prediction.user_data?.Age?.toString(),
            prediction.user_data?.Gender_Male === 1 ? 'male' : 'female',
            getRiskLevel(prediction.risk_percentage),
            getConfidenceText(prediction.risk_percentage)
        ].filter(Boolean);
        
        return searchableFields.some(field => 
            field.toLowerCase().includes(searchTerm)
        );
    });
    
    updateTable(filtered);
    updateStats(filtered);
}

function applyFilters() {
    let filtered = [...allPredictions];
    
    // Apply risk filter
    const riskFilter = elements.filterRisk.value;
    if (riskFilter) {
        filtered = filtered.filter(prediction => {
            const riskLevel = getRiskLevel(prediction.risk_percentage);
            return riskLevel.toLowerCase().includes(riskFilter);
        });
    }
    
    // Apply prediction filter
    const predictionFilter = elements.filterPrediction.value;
    if (predictionFilter) {
        filtered = filtered.filter(prediction => 
            prediction.prediction === predictionFilter
        );
    }
    
    // Apply date filter
    const dateFilter = elements.filterDate.value;
    if (dateFilter) {
        const now = new Date();
        let cutoffDate;
        
        switch (dateFilter) {
            case 'today':
                cutoffDate = new Date(now.setHours(0, 0, 0, 0));
                break;
            case 'week':
                cutoffDate = new Date(now.setDate(now.getDate() - 7));
                break;
            case 'month':
                cutoffDate = new Date(now.setMonth(now.getMonth() - 1));
                break;
        }
        
        if (cutoffDate) {
            filtered = filtered.filter(prediction => {
                const predDate = new Date(prediction.timestamp);
                return predDate >= cutoffDate;
            });
        }
    }
    
    // Update UI with filtered data
    updateTable(filtered);
    updateStats(filtered);
    updateCharts(filtered);
}

// ===== CHARTS INITIALIZATION =====
function initializeCharts() {
    // Risk Distribution Chart
    if (elements.riskDistributionChart) {
        const ctx = elements.riskDistributionChart.getContext('2d');
        riskChart = new Chart(ctx, CHART_CONFIGS.riskDistribution);
    }
    
    // Trend Analysis Chart
    if (elements.trendChart) {
        const ctx = elements.trendChart.getContext('2d');
        trendChart = new Chart(ctx, CHART_CONFIGS.trendAnalysis);
    }
}

function updateCharts(predictions) {
    updateRiskDistributionChart(predictions);
    updateTrendChart(predictions);
}

function updateRiskDistributionChart(predictions) {
    if (!riskChart || !predictions.length) return;
    
    // Categorize predictions by risk level
    const lowRisk = predictions.filter(p => p.risk_percentage < 30).length;
    const moderateRisk = predictions.filter(p => p.risk_percentage >= 30 && p.risk_percentage < 70).length;
    const highRisk = predictions.filter(p => p.risk_percentage >= 70).length;
    
    // Update chart data
    riskChart.data.datasets[0].data = [lowRisk, moderateRisk, highRisk];
    
    // Update labels with percentages
    const total = predictions.length;
    riskChart.data.labels = [
        `Low Risk (${total > 0 ? Math.round((lowRisk/total)*100) : 0}%)`,
        `Moderate Risk (${total > 0 ? Math.round((moderateRisk/total)*100) : 0}%)`,
        `High Risk (${total > 0 ? Math.round((highRisk/total)*100) : 0}%)`
    ];
    
    riskChart.update();
}

function updateTrendChart(predictions = null) {
    if (!trendChart) return;
    
    const period = elements.trendPeriod?.value || 'week';
    const dataToUse = predictions || allPredictions;
    
    if (!dataToUse.length) {
        trendChart.data.labels = [];
        trendChart.data.datasets[0].data = [];
        trendChart.update();
        return;
    }
    
    // Group predictions by time period
    const groupedData = groupPredictionsByPeriod(dataToUse, period);
    
    // Update chart
    trendChart.data.labels = Object.keys(groupedData);
    trendChart.data.datasets[0].data = Object.values(groupedData).map(group => 
        group.length > 0 ? 
        group.reduce((sum, p) => sum + p.risk_percentage, 0) / group.length : 
        0
    );
    
    trendChart.update();
}

function groupPredictionsByPeriod(predictions, period) {
    const groups = {};
    const now = new Date();
    
    predictions.forEach(prediction => {
        const predDate = new Date(prediction.timestamp);
        let groupKey;
        
        switch (period) {
            case 'week':
                // Group by day for last 7 days
                const daysAgo = Math.floor((now - predDate) / (1000 * 60 * 60 * 24));
                if (daysAgo <= 7) {
                    groupKey = `${daysAgo === 0 ? 'Today' : daysAgo === 1 ? 'Yesterday' : `${daysAgo} days ago`}`;
                }
                break;
                
            case 'month':
                // Group by week for last 30 days
                const weeksAgo = Math.floor((now - predDate) / (1000 * 60 * 60 * 24 * 7));
                if (weeksAgo <= 4) {
                    groupKey = `Week ${4 - weeksAgo}`;
                }
                break;
                
            case 'year':
                // Group by month for last 12 months
                const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                const monthIndex = predDate.getMonth();
                const year = predDate.getFullYear();
                const currentYear = now.getFullYear();
                
                if (year === currentYear || year === currentYear - 1) {
                    groupKey = `${monthNames[monthIndex]} ${year}`;
                }
                break;
        }
        
        if (groupKey) {
            if (!groups[groupKey]) {
                groups[groupKey] = [];
            }
            groups[groupKey].push(prediction);
        }
    });
    
    // Sort groups chronologically
    const sortedGroups = {};
    Object.keys(groups).sort((a, b) => {
        // Simple sorting for demo - in real app, use proper date parsing
        return Object.keys(groups).indexOf(a) - Object.keys(groups).indexOf(b);
    }).forEach(key => {
        sortedGroups[key] = groups[key];
    });
    
    return sortedGroups;
}

function updateHeatmap(predictions) {
    if (!elements.riskHeatmap || !predictions.length) return;
    
    // Calculate correlation between features (simplified)
    const featureImportance = calculateFeatureImportance(predictions);
    
    // Create heatmap HTML
    let heatmapHTML = '';
    Object.entries(featureImportance).forEach(([feature, importance]) => {
        const intensity = Math.min(100, importance * 1000); // Scale for visualization
        heatmapHTML += `
            <div class="heatmap-item" style="opacity: ${intensity/100}" title="${feature}: ${importance.toFixed(3)}">
                <span class="heatmap-label">${formatFeatureName(feature)}</span>
                <div class="heatmap-intensity" style="height: ${intensity}%"></div>
            </div>
        `;
    });
    
    elements.riskHeatmap.innerHTML = heatmapHTML;
}

function calculateFeatureImportance(predictions) {
    // Simplified feature importance calculation
    // In a real app, this would come from your ML model
    const features = [
        'Age', 'TSH_Level', 'T3_Level', 'T4_Level', 'Nodule_Size',
        'Family_History', 'Radiation_Exposure', 'Iodine_Deficiency',
        'Smoking', 'Obesity', 'Diabetes', 'Thyroid_Cancer_Risk'
    ];
    
    const importance = {};
    
    features.forEach(feature => {
        // Simple correlation with risk percentage
        const values = predictions.map(p => p.user_data?.[feature] || 0);
        const risks = predictions.map(p => p.risk_percentage);
        
        if (values.length > 1) {
            const correlation = calculateCorrelation(values, risks);
            importance[feature] = Math.abs(correlation);
        } else {
            importance[feature] = 0;
        }
    });
    
    return importance;
}

function calculateCorrelation(x, y) {
    // Simple Pearson correlation
    const n = x.length;
    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = y.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
    const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);
    const sumY2 = y.reduce((sum, yi) => sum + yi * yi, 0);
    
    const numerator = n * sumXY - sumX * sumY;
    const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
    
    return denominator === 0 ? 0 : numerator / denominator;
}

// ===== PREDICTION DETAILS MODAL =====
function showPredictionDetails(prediction) {
    if (!elements.detailModal) return;
    
    // Populate modal content
    const modalBody = elements.detailModal.querySelector('.detail-view');
    if (!modalBody) return;
    
    const riskLevel = getRiskLevel(prediction.risk_percentage);
    const riskClass = riskLevel.toLowerCase().replace(' ', '-');
    
    modalBody.innerHTML = `
        <div class="detail-header">
            <div class="detail-title">
                <h3>Prediction Analysis Report</h3>
                <span class="detail-date">${formatDateTime(prediction.timestamp)}</span>
            </div>
            <div class="detail-risk-indicator">
                <span class="risk-badge ${riskClass}">${prediction.risk_percentage.toFixed(1)}% Risk</span>
                <span class="prediction-badge ${prediction.prediction === 'Malignant' ? 'malignant' : 'benign'}">
                    ${prediction.prediction}
                </span>
            </div>
        </div>
        
        <div class="detail-sections">
            <div class="detail-section">
                <h4><i class="fas fa-user-circle"></i> Patient Information</h4>
                <div class="detail-grid">
                    ${Object.entries(prediction.user_data || {}).map(([key, value]) => `
                        <div class="detail-item">
                            <span class="detail-label">${formatFeatureName(key)}:</span>
                            <span class="detail-value">${formatValue(key, value)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="detail-section">
                <h4><i class="fas fa-chart-line"></i> Risk Analysis</h4>
                <div class="risk-breakdown">
                    <div class="risk-meter-large">
                        <div class="meter-fill" style="width: ${prediction.risk_percentage}%"></div>
                        <div class="meter-labels">
                            <span>Low</span>
                            <span>Moderate</span>
                            <span>High</span>
                        </div>
                    </div>
                    <div class="risk-stats">
                        <div class="risk-stat">
                            <span class="stat-label">Risk Level</span>
                            <span class="stat-value ${riskClass}">${riskLevel}</span>
                        </div>
                        <div class="risk-stat">
                            <span class="stat-label">Confidence</span>
                            <span class="stat-value">${getConfidenceText(prediction.risk_percentage)}</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="detail-section">
                <h4><i class="fas fa-lightbulb"></i> AI Insights</h4>
                <div class="insights">
                    <div class="insight">
                        <i class="fas fa-robot"></i>
                        <p>This prediction was made using Logistic Regression with 83% accuracy.</p>
                    </div>
                    <div class="insight">
                        <i class="fas fa-database"></i>
                        <p>Based on analysis of 300,000+ clinical records.</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Show modal
    elements.detailModal.classList.add('active');
    
    // Add print functionality
    const printBtn = elements.detailModal.querySelector('#printReport');
    if (printBtn) {
        printBtn.onclick = () => printPredictionReport(prediction);
    }
}

function printPredictionReport(prediction) {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>Thyroid Prediction Report</title>
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    .header { text-align: center; margin-bottom: 30px; }
                    .section { margin-bottom: 20px; }
                    .section h3 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 5px; }
                    .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
                    .item { margin-bottom: 8px; }
                    .label { font-weight: bold; color: #666; }
                    @media print {
                        .no-print { display: none; }
                    }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Thyroid Cancer Risk Assessment Report</h1>
                    <p>Generated: ${new Date().toLocaleString()}</p>
                </div>
                
                <div class="section">
                    <h3>Patient Information</h3>
                    <div class="grid">
                        ${Object.entries(prediction.user_data || {}).map(([key, value]) => `
                            <div class="item">
                                <span class="label">${formatFeatureName(key)}:</span>
                                <span>${formatValue(key, value)}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="section">
                    <h3>Analysis Results</h3>
                    <p><strong>Prediction:</strong> ${prediction.prediction}</p>
                    <p><strong>Risk Percentage:</strong> ${prediction.risk_percentage.toFixed(1)}%</p>
                    <p><strong>Risk Level:</strong> ${getRiskLevel(prediction.risk_percentage)}</p>
                    <p><strong>Confidence:</strong> ${getConfidenceText(prediction.risk_percentage)}</p>
                </div>
                
                <div class="section">
                    <h3>Disclaimer</h3>
                    <p>This report is for educational and research purposes only. Not for medical diagnosis.</p>
                </div>
                
                <button class="no-print" onclick="window.print()">Print Report</button>
                <button class="no-print" onclick="window.close()">Close</button>
            </body>
        </html>
    `);
    printWindow.document.close();
}

function printCurrentReport() {
    printPredictionReport(currentDetailPrediction || allPredictions[0]);
}

// ===== DATA EXPORT =====
function exportHistoryAsCSV() {
    if (!allPredictions.length) {
        showNotification('No data to export', 'warning');
        return;
    }
    
    try {
        // Create CSV header
        const headers = [
            'Timestamp',
            'Age',
            'Gender',
            'TSH_Level',
            'T3_Level',
            'T4_Level',
            'Nodule_Size',
            'Thyroid_Cancer_Risk',
            'Risk_Percentage',
            'Prediction',
            'Family_History',
            'Radiation_Exposure',
            'Iodine_Deficiency',
            'Smoking',
            'Obesity',
            'Diabetes'
        ];
        
        // Create CSV rows
        const rows = allPredictions.map(prediction => {
            const data = prediction.user_data || {};
            return [
                prediction.timestamp,
                data.Age || '',
                data.Gender_Male === 1 ? 'Male' : 'Female',
                data.TSH_Level || '',
                data.T3_Level || '',
                data.T4_Level || '',
                data.Nodule_Size || '',
                data.Thyroid_Cancer_Risk || '',
                prediction.risk_percentage,
                prediction.prediction,
                data.Family_History || 0,
                data.Radiation_Exposure || 0,
                data.Iodine_Deficiency || 0,
                data.Smoking || 0,
                data.Obesity || 0,
                data.Diabetes || 0
            ].map(value => `"${value}"`).join(',');
        });
        
        // Combine header and rows
        const csvContent = [headers.join(','), ...rows].join('\n');
        
        // Create download link
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `thyroid_predictions_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification('Data exported successfully', 'success');
        
    } catch (error) {
        console.error('Export error:', error);
        showNotification('Failed to export data', 'error');
    }
}

function exportSinglePrediction(prediction) {
    try {
        const report = generateSingleReport(prediction);
        
        // Create download link
        const blob = new Blob([report], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `thyroid_prediction_${prediction.timestamp.replace(/[:.]/g, '-')}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification('Prediction exported', 'success');
        
    } catch (error) {
        console.error('Export error:', error);
        showNotification('Failed to export prediction', 'error');
    }
}

function generateSingleReport(prediction) {
    const riskLevel = getRiskLevel(prediction.risk_percentage);
    
    return `
Thyroid Prediction Report
=========================
Date: ${formatDateTime(prediction.timestamp)}
Prediction ID: THY-${Date.parse(prediction.timestamp).toString().slice(-8)}

PATIENT DATA:
------------
${Object.entries(prediction.user_data || {}).map(([key, value]) => 
    `${formatFeatureName(key)}: ${formatValue(key, value)}`
).join('\n')}

RESULTS:
-------
Prediction: ${prediction.prediction}
Risk Percentage: ${prediction.risk_percentage.toFixed(1)}%
Risk Level: ${riskLevel}
Confidence: ${getConfidenceText(prediction.risk_percentage)}

AI MODEL INFO:
-------------
Algorithm: Logistic Regression
Accuracy: 83%
Training Data: 300,000+ records

DISCLAIMER:
----------
For educational and research purposes only.
Not for medical diagnosis.

Generated by ThyroScan Pro AI System
====================================
    `;
}

// ===== DATA MANAGEMENT =====
function deletePrediction(index) {
    if (!confirm('Are you sure you want to delete this prediction?')) {
        return;
    }
    
    try {
        // Remove from local array
        allPredictions.splice(index, 1);
        
        // Update UI
        updateTable(allPredictions);
        updateStats(allPredictions);
        updateCharts(allPredictions);
        
        showNotification('Prediction deleted', 'success');
        
        // In a real app, you would also delete from backend
        // await deleteFromBackend(prediction.id);
        
    } catch (error) {
        console.error('Delete error:', error);
        showNotification('Failed to delete prediction', 'error');
    }
}

async function clearAllHistory() {
    if (!confirm('Are you sure you want to clear ALL prediction history? This action cannot be undone.')) {
        return;
    }
    
    try {
        // Clear local data
        allPredictions = [];
        
        // Update UI
        updateTable(allPredictions);
        updateStats(allPredictions);
        updateCharts(allPredictions);
        
        showNotification('All history cleared', 'success');
        
        // In a real app, you would also clear backend
        // await clearBackendHistory();
        
    } catch (error) {
        console.error('Clear error:', error);
        showNotification('Failed to clear history', 'error');
    }
}

// ===== UTILITY FUNCTIONS =====
function formatDateTime(timestamp) {
    if (!timestamp) return 'N/A';
    
    try {
        const date = new Date(timestamp);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        return timestamp;
    }
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

function formatValue(feature, value) {
    if (feature === 'Gender_Male') {
        return value === 1 ? 'Male' : 'Female';
    }
    
    if (feature.includes('_History') || feature.includes('_Exposure') || 
        feature.includes('_Deficiency') || feature === 'Smoking' || 
        feature === 'Obesity' || feature === 'Diabetes') {
        return value === 1 ? 'Yes' : 'No';
    }
    
    return value;
}

function getRiskLevel(percentage) {
    if (percentage < 30) return 'Low Risk';
    if (percentage < 70) return 'Moderate Risk';
    return 'High Risk';
}

function getConfidenceText(percentage) {
    if (percentage < 30) return 'Low';
    if (percentage < 70) return 'Medium';
    return 'High';
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

// ===== SAMPLE DATA FOR DEMO =====
function loadSampleData() {
    // Generate sample data for demo purposes
    const samplePredictions = [];
    const now = new Date();
    
    for (let i = 0; i < 15; i++) {
        const timestamp = new Date(now.getTime() - (i * 24 * 60 * 60 * 1000));
        const riskPercentage = Math.random() * 100;
        
        samplePredictions.push({
            timestamp: timestamp.toISOString(),
            prediction: riskPercentage > 60 ? 'Malignant' : 'Benign',
            risk_percentage: parseFloat(riskPercentage.toFixed(1)),
            confidence: riskPercentage < 30 ? 'Low' : riskPercentage < 70 ? 'Medium' : 'High',
            user_data: {
                Age: Math.floor(Math.random() * 50) + 20,
                Gender_Male: Math.random() > 0.5 ? 1 : 0,
                TSH_Level: parseFloat((Math.random() * 10).toFixed(1)),
                T3_Level: parseFloat((Math.random() * 3).toFixed(1)),
                T4_Level: parseFloat((Math.random() * 2).toFixed(1)),
                Nodule_Size: parseFloat((Math.random() * 5).toFixed(1)),
                Thyroid_Cancer_Risk: Math.floor(Math.random() * 5),
                Family_History: Math.random() > 0.7 ? 1 : 0,
                Radiation_Exposure: Math.random() > 0.8 ? 1 : 0,
                Iodine_Deficiency: Math.random() > 0.6 ? 1 : 0,
                Smoking: Math.random() > 0.5 ? 1 : 0,
                Obesity: Math.random() > 0.4 ? 1 : 0,
                Diabetes: Math.random() > 0.3 ? 1 : 0
            }
        });
    }
    
    allPredictions = samplePredictions;
    updateTable(allPredictions);
    updateStats(allPredictions);
    updateCharts(allPredictions);
    showEmptyState(false);
    
    showNotification('Loaded sample data for demonstration', 'info');
}

// ===== BACKEND CONNECTION =====
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend connected for history');
            updateConnectionStatus(true);
        } else {
            throw new Error('Backend not responding');
        }
    } catch (error) {
        console.warn('⚠️ Backend connection failed for history');
        updateConnectionStatus(false);
    }
}

function updateConnectionStatus(connected) {
    const statusIndicator = document.querySelector('.connection-status');
    if (!statusIndicator) return;
    
    statusIndicator.innerHTML = connected ? 
        '<i class="fas fa-wifi"></i> Connected' :
        '<i class="fas fa-wifi-slash"></i> Disconnected';
    
    statusIndicator.className = `connection-status ${connected ? 'connected' : 'disconnected'}`;
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

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('History page error:', e.error);
    showNotification('An error occurred in the history system', 'error');
});

// ===== EXPORT FUNCTIONS =====
window.ThyroScanHistory = {
    loadHistoryData,
    exportHistoryAsCSV,
    clearAllHistory,
    showPredictionDetails,
    updateCharts
};

console.log('📊 History module loaded successfully');