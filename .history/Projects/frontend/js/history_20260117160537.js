// ============================================
// HISTORY.JS - FIXED VERSION (NO FREEZING ISSUES)
// ============================================

(function() {
    'use strict';

    // Scoped variables
    let historyData = [];
    let filteredHistory = [];
    let currentPage = 1;
    let itemsPerPage = 10;
    let currentView = 'list';
    let isInitialized = false;
    let chartInstances = {};

    // API Configuration
    const API_CONFIG = {
        BASE_URL: window.API_BASE_URL || 'http://localhost:8000',
        ENDPOINTS: {
            HISTORY: '/history',
            STATS: '/stats'
        }
    };

    // Initialize History Page
    function initializeHistoryPage() {
        if (isInitialized) {
            console.log('⚠️ History page already initialized');
            return;
        }
        
        console.log('📊 Initializing History Page...');
        
        // Show loading animation
        showPageLoader();
        
        // Initialize page elements
        initializePageElements();
        
        // Setup event listeners (REMOVED problematic ones)
        setupHistoryEventListeners();
        
        // Load prediction history and statistics
        loadHistory();
        loadStatistics();
        
        isInitialized = true;
        console.log('✅ History page initialized successfully');
    }

    // Show Page Loader
    function showPageLoader() {
        const loadingState = document.getElementById('historyLoading');
        if (loadingState) {
            loadingState.innerHTML = `
                <div class="loading-spinner">
                    <i class="fas fa-spinner fa-spin"></i>
                </div>
                <p>Loading History...</p>
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
        // Remove Grid View buttons since they cause freezing
        const viewToggle = document.querySelector('.history-view-toggle');
        if (viewToggle) {
            viewToggle.innerHTML = `
                <button class="view-toggle-btn active" data-view="list">
                    <i class="fas fa-list"></i>
                    List View
                </button>
            `;
        }
        
        // Remove Clear All button from DOM (it's causing freezing)
        const clearHistoryBtn = document.getElementById('clearHistory');
        if (clearHistoryBtn) {
            clearHistoryBtn.style.display = 'none';
        }
        
        // Initialize empty state
        const emptyState = document.getElementById('historyEmpty');
        if (emptyState) {
            emptyState.classList.add('hidden');
        }
    }

    // Load Statistics for Header
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
            updateHeaderStats(stats);
            
        } catch (error) {
            console.error('❌ Error loading statistics:', error);
            calculateHeaderStats();
        }
    }

    // Update Header Statistics
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
                lastUpdatedElement.textContent = latest.timestamp.split(' ')[0];
            }
        }
    }

    // Load Prediction History
    async function loadHistory() {
        try {
            showTableLoading();
            console.log('📡 Fetching history from API...');
            
            const response = await fetch(
                `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.HISTORY}?limit=50`,
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
            
            // Handle response format
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
                processHistoryData();
                updateHistoryDisplay();
                updateSummaryStats();
                initializeCharts();
                
                showNotification(`Loaded ${historyData.length} predictions`, 'success');
            }
            
        } catch (error) {
            console.error('❌ Error loading history:', error);
            
            // Fallback to localStorage
            const savedHistory = localStorage.getItem('thyroscan_local_history');
            if (savedHistory) {
                try {
                    historyData = JSON.parse(savedHistory);
                    console.log(`⚠️ Using cached data: ${historyData.length} records`);
                    
                    processHistoryData();
                    updateHistoryDisplay();
                    updateSummaryStats();
                    
                    showNotification('Using cached data', 'warning');
                } catch (parseError) {
                    console.error('Error parsing cached data:', parseError);
                    showEmptyState();
                }
            } else {
                showEmptyState();
                showNotification('Unable to load history', 'error');
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
                    <div class="loading-spinner-large">
                        <i class="fas fa-spinner fa-spin"></i>
                    </div>
                    <p>Loading prediction history...</p>
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

    // Show Empty State
    function showEmptyState() {
        const emptyState = document.getElementById('historyEmpty');
        const tableBody = document.getElementById('historyTableBody');
        
        if (emptyState) {
            emptyState.classList.remove('hidden');
        }
        
        if (tableBody) tableBody.innerHTML = '';
    }

    // Process History Data
    function processHistoryData() {
        filteredHistory = [...historyData].sort((a, b) => {
            try {
                let aValue = new Date(a.timestamp || Date.now());
                let bValue = new Date(b.timestamp || Date.now());
                return bValue - aValue; // Descending order (newest first)
            } catch (error) {
                return 0;
            }
        });
        
        applyFilters();
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
        
        currentPage = 1;
    }

    // Update History Display
    function updateHistoryDisplay() {
        updateListView();
        updateEmptyState();
        updatePaginationControls();
    }

    // ✅ SIMPLIFIED: Initialize Charts (only if needed)
    function initializeCharts() {
        console.log('📊 Initializing charts...');
        
        // Only initialize if Chart.js is available and elements exist
        if (typeof Chart === 'undefined') {
            console.warn('⚠️ Chart.js not loaded');
            return;
        }
        
        // Initialize only distribution chart
        initDistributionChart();
        
        console.log('✅ Charts initialized');
    }

    // Initialize Distribution Chart
    function initDistributionChart() {
        const ctx = document.getElementById('distributionChart');
        if (!ctx) {
            console.error('❌ Distribution chart element not found');
            return;
        }
        
        // Clear existing content
        ctx.innerHTML = '';
        
        // Create canvas
        const canvas = document.createElement('canvas');
        canvas.id = 'distributionChartCanvas';
        ctx.appendChild(canvas);
        
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
        } catch (error) {
            console.error('❌ Error initializing distribution chart:', error);
            ctx.innerHTML = `
                <div class="chart-placeholder">
                    <i class="fas fa-chart-pie"></i>
                    <p>Chart visualization</p>
                </div>
            `;
        }
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
                            <p>Try adjusting your filters</p>
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

    // ✅ FIXED: Create History Row (NO DELETE BUTTON)
    function createHistoryRow(item, index) {
        const row = document.createElement('tr');
        row.className = 'history-item';
        
        try {
            const date = new Date(item.timestamp || Date.now());
            const age = item.user_data?.Age || 'N/A';
            const gender = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
            const riskPercentage = item.risk_percentage || 0;
            const prediction = item.prediction || 'N/A';
            
            // ✅ REMOVED DELETE BUTTON from actions column
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
                    <!-- DELETE BUTTON REMOVED -->
                </td>
            `;
            
            // Add event listeners
            row.querySelector('.btn-view')?.addEventListener('click', () => showHistoryDetails(item));
            row.querySelector('.btn-download')?.addEventListener('click', () => downloadHistoryReport(item));
            // Delete event listener removed
            
        } catch (error) {
            console.error('Error creating history row:', error);
            row.innerHTML = `<td colspan="6" class="text-center error">Error displaying record</td>`;
        }
        
        return row;
    }

    // Get Top Factors
    function getTopFactors(user_data) {
        if (!user_data) return ['No data'];
        
        const factors = [];
        if (user_data.Family_History === 1) factors.push('Family History');
        if (user_data.Radiation_Exposure === 1) factors.push('Radiation');
        if (user_data.Iodine_Deficiency === 1) factors.push('Iodine Def');
        if (user_data.Smoking === 1) factors.push('Smoking');
        if (user_data.Obesity === 1) factors.push('Obesity');
        if (user_data.Diabetes === 1) factors.push('Diabetes');
        
        return factors.slice(0, 3);
    }

    // Update Empty State
    function updateEmptyState() {
        const emptyState = document.getElementById('historyEmpty');
        
        if (filteredHistory.length === 0) {
            if (emptyState) emptyState.classList.remove('hidden');
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

    // ✅ FIXED: Setup History Event Listeners (REMOVED problematic buttons)
    function setupHistoryEventListeners() {
        // Refresh button
        const refreshBtn = document.getElementById('refreshHistory');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function() {
                this.classList.add('refreshing');
                refreshHistory().finally(() => {
                    setTimeout(() => this.classList.remove('refreshing'), 500);
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
        
        // REMOVED: Clear button event listener (it's causing freezing)
        
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
                    if (chartInstances.distributionChart) {
                        updateDistributionChart();
                    }
                }, 300);
            });
        }
        
        // Filter selects
        document.querySelectorAll('.filter-select').forEach(select => {
            select.addEventListener('change', function() {
                applyFilters();
                updateHistoryDisplay();
                updateSummaryStats();
                if (chartInstances.distributionChart) {
                    updateDistributionChart();
                }
            });
        });
        
        // View toggle buttons (only list view available)
        const viewToggleBtn = document.querySelector('.view-toggle-btn');
        if (viewToggleBtn) {
            viewToggleBtn.addEventListener('click', function() {
                // Only list view available, no switching
                this.classList.add('active');
            });
        }
        
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
    }

    // Refresh History
    async function refreshHistory() {
        showNotification('Refreshing history...', 'info');
        await loadHistory();
        await loadStatistics();
    }

    // Export History
    function exportHistory() {
        if (filteredHistory.length === 0) {
            showNotification('No history data to export', 'warning');
            return;
        }
        
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
        
        const csvContent = [
            headers.join(','),
            ...csvData.map(row => row.map(cell => `"${cell}"`).join(','))
        ].join('\n');
        
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

    // REMOVED: clearAllHistory() function

    // Show History Details
    function showHistoryDetails(item) {
        const modal = document.getElementById('detailModal');
        if (!modal) return;
        
        populateDetailModal(item);
        modal.classList.remove('hidden');
        setTimeout(() => {
            modal.classList.add('active');
            document.body.classList.add('modal-open');
        }, 10);
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
            document.getElementById('detailRiskPercentage').textContent = `${riskPercentage}%`;
            document.getElementById('detailPrediction').textContent = prediction;
            document.getElementById('detailDate').textContent = `Date: ${date.toLocaleString()}`;
            document.getElementById('detailRiskLevel').textContent = getRiskLevel(riskPercentage);
            
            // Update parameters
            document.getElementById('detailAge').textContent = `${age} years`;
            document.getElementById('detailGender').textContent = gender;
            document.getElementById('detailTSH').textContent = `${item.user_data?.TSH_Level || 'N/A'} mIU/L`;
            document.getElementById('detailT3').textContent = `${item.user_data?.T3_Level || 'N/A'} pg/mL`;
            document.getElementById('detailT4').textContent = `${item.user_data?.T4_Level || 'N/A'} μg/dL`;
            document.getElementById('detailNodule').textContent = `${item.user_data?.Nodule_Size || 'N/A'} cm`;
            document.getElementById('detailCancerRisk').textContent = item.user_data?.Thyroid_Cancer_Risk || 'N/A';
            
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
                document.body.classList.remove('modal-open');
            }, 300);
        }
    }

    // Download History Report
    function downloadHistoryReport(item) {
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

    // REMOVED: confirmDeleteHistory() and deleteHistoryRecord() functions

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
        
        const pageNumbers = document.getElementById('pageNumbers');
        if (pageNumbers) {
            pageNumbers.innerHTML = '';
            
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

    // Update Distribution Chart
    function updateDistributionChart() {
        if (!chartInstances.distributionChart) return;
        
        const lowRisk = filteredHistory.filter(item => (item.risk_percentage || 0) < 30).length;
        const mediumRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 30 && (item.risk_percentage || 0) < 70).length;
        const highRisk = filteredHistory.filter(item => (item.risk_percentage || 0) >= 70).length;
        
        chartInstances.distributionChart.data.datasets[0].data = [lowRisk, mediumRisk, highRisk];
        chartInstances.distributionChart.update();
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
        // Simple notification implementation
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
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
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

    // Close modals with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const detailModal = document.getElementById('detailModal');
            if (detailModal && !detailModal.classList.contains('hidden')) {
                closeDetailModal();
            }
        }
    });

    // Export functions globally
    window.ThyroAssessHistory = {
        initializeHistoryPage,
        refreshHistory,
        exportHistory,
        showHistoryDetails
    };

})();