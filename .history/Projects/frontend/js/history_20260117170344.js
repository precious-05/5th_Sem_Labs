// ============================================
// HISTORY.JS - FIXED & IMPROVED VERSION
// ============================================

(function() {
    'use strict';

    // Simple variables
    let historyData = [];
    let filteredHistory = [];
    let currentPage = 1;
    const itemsPerPage = 10;

    // API Configuration
    const API_BASE_URL = window.API_BASE_URL || 'http://localhost:8000';

    // Initialize History Page
    function initializeHistoryPage() {
        console.log('📊 Initializing History Page...');
        
        // Setup event listeners
        setupEventListeners();
        
        // Load history
        loadHistory();
        
        // Set current page indicators
        updatePageIndicator();
    }

    // Setup Event Listeners
    function setupEventListeners() {
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
        
        // Search input
        const searchInput = document.getElementById('historySearch');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                clearTimeout(this.searchTimer);
                this.searchTimer = setTimeout(() => {
                    filterHistory();
                    currentPage = 1;
                    updatePageIndicator();
                }, 300);
            });
        }
        
        // Filter selects
        document.querySelectorAll('.filter-select').forEach(select => {
            select.addEventListener('change', function() {
                filterHistory();
                currentPage = 1;
                updatePageIndicator();
            });
        });
        
        // Pagination buttons
        const prevBtn = document.querySelector('.pagination-btn:first-child');
        const nextBtn = document.querySelector('.pagination-btn:last-child');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', goToPreviousPage);
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', goToNextPage);
        }
        
        // Page number clicks
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('page-number')) {
                const pageNum = parseInt(e.target.textContent);
                if (!isNaN(pageNum)) {
                    currentPage = pageNum;
                    updateHistoryDisplay();
                    updatePageIndicator();
                }
            }
        });
        
        // Clear filters button (if exists)
        const clearFiltersBtn = document.getElementById('clearFilters');
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', clearFilters);
        }
    }

    // Load History
    async function loadHistory() {
        try {
            showLoading();
            
            const response = await fetch(`${API_BASE_URL}/history?limit=100`);
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.history && Array.isArray(data.history)) {
                // Sort by timestamp descending (newest first)
                historyData = data.history.sort((a, b) => {
                    return new Date(b.timestamp || 0) - new Date(a.timestamp || 0);
                });
                filteredHistory = [...historyData];
                
                if (historyData.length === 0) {
                    showEmptyState();
                } else {
                    updateHistoryDisplay();
                    updateSummaryStats();
                    updatePagination();
                }
            } else {
                showEmptyState();
            }
            
        } catch (error) {
            console.error('❌ Error loading history:', error);
            showError('Failed to load history. Please try again.');
        } finally {
            hideLoading();
        }
    }

    // Filter History
    function filterHistory() {
        const riskFilter = document.getElementById('filterRisk')?.value;
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
            
            // Prediction filter
            if (predictionFilter && predictionFilter !== '') {
                if (predictionFilter === 'benign' && item.prediction !== 'Benign') return false;
                if (predictionFilter === 'malignant' && item.prediction !== 'Malignant') return false;
            }
            
            // Search filter
            if (searchTerm) {
                const searchable = [
                    item.prediction || '',
                    getRiskLevel(item.risk_percentage || 0),
                    item.user_data?.Age?.toString() || '',
                    item.user_data?.Gender_Male === 1 ? 'male' : 'female',
                    getTopFactors(item.user_data).join(' ')
                ].join(' ').toLowerCase();
                
                return searchable.includes(searchTerm);
            }
            
            return true;
        });
        
        currentPage = 1;
        updateHistoryDisplay();
        updateSummaryStats();
        updatePagination();
    }

    // Clear All Filters
    function clearFilters() {
        const searchInput = document.getElementById('historySearch');
        const riskFilter = document.getElementById('filterRisk');
        const predictionFilter = document.getElementById('filterPrediction');
        
        if (searchInput) searchInput.value = '';
        if (riskFilter) riskFilter.value = '';
        if (predictionFilter) predictionFilter.value = '';
        
        filteredHistory = [...historyData];
        currentPage = 1;
        updateHistoryDisplay();
        updateSummaryStats();
        updatePagination();
        updatePageIndicator();
    }

    // Update History Display
    function updateHistoryDisplay() {
        const tableBody = document.getElementById('historyTableBody');
        if (!tableBody) return;
        
        tableBody.innerHTML = '';
        
        if (filteredHistory.length === 0) {
            tableBody.innerHTML = `
                <tr>
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
        
        // Calculate pagination
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, filteredHistory.length);
        const currentItems = filteredHistory.slice(startIndex, endIndex);
        
        currentItems.forEach((item, index) => {
            const row = createHistoryRow(item, startIndex + index);
            tableBody.appendChild(row);
        });
    }

    // Create History Row
    function createHistoryRow(item, index) {
        const row = document.createElement('tr');
        row.className = 'history-item';
        row.setAttribute('data-index', index);
        
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
                            <div class="gauge-value">${riskPercentage.toFixed(1)}%</div>
                        </div>
                        <div class="risk-level ${getRiskLevelClass(riskPercentage)}">
                            ${getRiskLevel(riskPercentage)}
                        </div>
                    </div>
                </td>
                
                <td class="history-prediction">
                    <span class="prediction-badge ${prediction.toLowerCase()}">
                        ${prediction}
                    </span>
                </td>
                
                <td class="history-factors">
                    <div class="factors-tags">
                        ${getTopFactors(item.user_data).slice(0, 2).map(factor => `
                            <span class="factor-tag">${factor}</span>
                        `).join('')}
                    </div>
                </td>
                
                <td class="history-actions">
                    <button class="btn-view" onclick="showDetailsModal(${index})" title="View Details">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            `;
            
        } catch (error) {
            console.error('Error creating row:', error);
            row.innerHTML = '<td colspan="6" class="text-center">Error displaying</td>';
        }
        
        return row;
    }

    // Show Details Modal
    function showDetailsModal(index) {
        if (filteredHistory[index]) {
            const item = filteredHistory[index];
            const originalIndex = historyData.findIndex(h => h.timestamp === item.timestamp);
            
            // Create modal HTML
            const modalHTML = `
                <div class="detail-modal active" id="historyDetailModal">
                    <div class="modal-overlay" onclick="window.closeDetailModal()"></div>
                    <div class="modal-container large-modal">
                        <div class="modal-header">
                            <h2><i class="fas fa-file-medical-alt"></i> Patient Details</h2>
                            <button class="modal-close" onclick="window.closeDetailModal()">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                        <div class="modal-content">
                            <div class="detail-header">
                                <div class="detail-risk-score">
                                    <div class="detail-risk-circle">
                                        <div class="circle-progress">
                                            <svg width="180" height="180" viewBox="0 0 180 180">
                                                <circle cx="90" cy="90" r="54" stroke-width="12" />
                                                <circle cx="90" cy="90" r="54" stroke-width="12" 
                                                    stroke-dasharray="339" 
                                                    stroke-dashoffset="${339 - (item.risk_percentage || 0) * 3.39}"/>
                                            </svg>
                                        </div>
                                        <div class="score-content">
                                            <div class="score-value">${item.risk_percentage || 0}%</div>
                                            <div class="score-label">Risk Score</div>
                                        </div>
                                    </div>
                                    <div class="detail-risk-info">
                                        <h3>Patient ${originalIndex + 1} Analysis</h3>
                                        <div class="detail-date">
                                            <i class="far fa-calendar"></i>
                                            ${new Date(item.timestamp || Date.now()).toLocaleString()}
                                        </div>
                                        <div class="detail-badges">
                                            <div class="detail-badge">
                                                <i class="fas fa-chart-line"></i>
                                                ${item.prediction || 'N/A'}
                                            </div>
                                            <div class="detail-badge">
                                                <i class="fas fa-shield-alt"></i>
                                                ${getRiskLevel(item.risk_percentage || 0)} Risk
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="detail-tabs">
                                <button class="tab-btn active" onclick="window.switchDetailTab('parameters')">
                                    <i class="fas fa-user-circle"></i> Parameters
                                </button>
                                <button class="tab-btn" onclick="window.switchDetailTab('factors')">
                                    <i class="fas fa-exclamation-triangle"></i> Risk Factors
                                </button>
                                <button class="tab-btn" onclick="window.switchDetailTab('insights')">
                                    <i class="fas fa-lightbulb"></i> Insights
                                </button>
                            </div>
                            
                            <div id="parametersTab" class="tab-content active">
                                <div class="parameters-grid">
                                    <div class="parameter-section">
                                        <h4><i class="fas fa-user"></i> Personal Information</h4>
                                        <div class="parameter-list">
                                            <div class="parameter-item">
                                                <span class="param-label">Patient ID</span>
                                                <span class="param-value">#${originalIndex + 1}</span>
                                            </div>
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
                                        <h4><i class="fas fa-heartbeat"></i> Medical Factors</h4>
                                        <div class="parameter-list">
                                            <div class="parameter-item">
                                                <span class="param-label">Family History</span>
                                                <span class="param-value ${item.user_data?.Family_History === 1 ? 'factor-yes' : 'factor-no'}">
                                                    ${item.user_data?.Family_History === 1 ? 'Present' : 'Absent'}
                                                </span>
                                            </div>
                                            <div class="parameter-item">
                                                <span class="param-label">Radiation Exposure</span>
                                                <span class="param-value ${item.user_data?.Radiation_Exposure === 1 ? 'factor-yes' : 'factor-no'}">
                                                    ${item.user_data?.Radiation_Exposure === 1 ? 'Present' : 'Absent'}
                                                </span>
                                            </div>
                                            <div class="parameter-item">
                                                <span class="param-label">Iodine Deficiency</span>
                                                <span class="param-value ${item.user_data?.Iodine_Deficiency === 1 ? 'factor-yes' : 'factor-no'}">
                                                    ${item.user_data?.Iodine_Deficiency === 1 ? 'Present' : 'Absent'}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="parameter-section">
                                        <h4><i class="fas fa-chart-bar"></i> Prediction Details</h4>
                                        <div class="parameter-list">
                                            <div class="parameter-item">
                                                <span class="param-label">Risk Score</span>
                                                <span class="param-value risk-highlight">${item.risk_percentage || 0}%</span>
                                            </div>
                                            <div class="parameter-item">
                                                <span class="param-label">Prediction</span>
                                                <span class="param-value ${item.prediction === 'Malignant' ? 'prediction-malignant' : 'prediction-benign'}">
                                                    ${item.prediction || 'N/A'}
                                                </span>
                                            </div>
                                            <div class="parameter-item">
                                                <span class="param-label">Risk Level</span>
                                                <span class="param-value ${getRiskLevelClass(item.risk_percentage || 0)}">
                                                    ${getRiskLevel(item.risk_percentage || 0)}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div id="factorsTab" class="tab-content">
                                <div class="factors-analysis">
                                    <h4><i class="fas fa-chart-pie"></i> Risk Factors Contribution</h4>
                                    <div class="factors-chart">
                                        <div class="factor-bars">
                                            ${getFactorBars(item.user_data)}
                                        </div>
                                        <div class="factor-summary">
                                            <h5><i class="fas fa-list-check"></i> Active Risk Factors</h5>
                                            <ul>
                                                ${getActiveFactors(item.user_data).map(factor => `
                                                    <li><i class="fas fa-circle"></i> ${factor}</li>
                                                `).join('')}
                                                ${getActiveFactors(item.user_data).length === 0 ? 
                                                    '<li class="no-factors"><i class="fas fa-check-circle"></i> No significant risk factors detected</li>' : ''}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div id="insightsTab" class="tab-content">
                                <div class="insights-content">
                                    <div class="insight-card">
                                        <h4><i class="fas fa-brain"></i> AI Analysis Insights</h4>
                                        <div class="insight-text">
                                            <p>The model analyzed this case with <strong>${getConfidenceLevel(item.risk_percentage || 0)} confidence</strong>. 
                                            ${getPredictionInsights(item)}</p>
                                            
                                            <div class="insight-points">
                                                <div class="insight-point">
                                                    <i class="fas fa-check-circle"></i>
                                                    <span>Prediction based on ${getActiveFactors(item.user_data).length} key factors</span>
                                                </div>
                                                <div class="insight-point">
                                                    <i class="fas fa-clock"></i>
                                                    <span>Analysis completed in real-time</span>
                                                </div>
                                                <div class="insight-point">
                                                    <i class="fas fa-shield-alt"></i>
                                                    <span>${getRecommendationLevel(item.risk_percentage || 0)} follow-up recommended</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="insight-card">
                                        <h4><i class="fas fa-stethoscope"></i> Medical Recommendations</h4>
                                        <div class="recommendations-list">
                                            ${getRecommendations(item)}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Add modal to body
            const modalContainer = document.createElement('div');
            modalContainer.innerHTML = modalHTML;
            document.body.appendChild(modalContainer.firstElementChild);
            
            // Prevent body scroll
            document.body.classList.add('modal-open');
        }
    }

    // Close Detail Modal
    function closeDetailModal() {
        const modal = document.getElementById('historyDetailModal');
        if (modal) {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.remove();
                document.body.classList.remove('modal-open');
            }, 300);
        }
    }

    // Switch Detail Tab
    function switchDetailTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Remove active from all buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Show selected tab
        const tabElement = document.getElementById(tabName + 'Tab');
        if (tabElement) {
            tabElement.classList.add('active');
        }
        
        // Activate clicked button
        if (event && event.target) {
            event.target.classList.add('active');
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
        
        // High risk cases
        const highRiskCount = document.getElementById('highRiskCount');
        if (highRiskCount) {
            const highRiskCases = filteredHistory.filter(item => {
                const risk = item.risk_percentage || 0;
                return risk >= 70;
            }).length;
            highRiskCount.textContent = highRiskCases;
        }
    }

    // Refresh History
    async function refreshHistory() {
        showNotification('Refreshing history...', 'info');
        await loadHistory();
        showNotification('History refreshed successfully', 'success');
    }

    // Export History
    function exportHistory() {
        if (filteredHistory.length === 0) {
            showNotification('No data to export', 'warning');
            return;
        }
        
        try {
            // Prepare CSV data
            const headers = ['Date', 'Time', 'Patient ID', 'Age', 'Gender', 'Risk Score', 'Risk Level', 'Prediction', 'Family History', 'Radiation Exposure', 'Iodine Deficiency'];
            
            const csvData = filteredHistory.map((item, index) => {
                const date = new Date(item.timestamp || Date.now());
                return [
                    date.toLocaleDateString(),
                    date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    `PAT${index + 1}`,
                    item.user_data?.Age || 'N/A',
                    item.user_data?.Gender_Male === 1 ? 'Male' : 'Female',
                    `${item.risk_percentage || 0}%`,
                    getRiskLevel(item.risk_percentage || 0),
                    item.prediction || 'N/A',
                    item.user_data?.Family_History === 1 ? 'Yes' : 'No',
                    item.user_data?.Radiation_Exposure === 1 ? 'Yes' : 'No',
                    item.user_data?.Iodine_Deficiency === 1 ? 'Yes' : 'No'
                ];
            });
            
            // Create CSV content
            const csvContent = [
                headers.join(','),
                ...csvData.map(row => row.join(','))
            ].join('\n');
            
            // Create and trigger download
            const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `thyroscan_history_${new Date().toISOString().split('T')[0]}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
            
            showNotification(`Exported ${filteredHistory.length} records to CSV`, 'success');
            
        } catch (error) {
            console.error('Export error:', error);
            showNotification('Failed to export data', 'error');
        }
    }

    // Pagination Functions
    function goToPreviousPage() {
        if (currentPage > 1) {
            currentPage--;
            updateHistoryDisplay();
            updatePageIndicator();
            scrollToTop();
        }
    }

    function goToNextPage() {
        const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            updateHistoryDisplay();
            updatePageIndicator();
            scrollToTop();
        }
    }

    function updatePagination() {
        const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
        const pageNumbers = document.querySelector('.page-numbers');
        if (!pageNumbers) return;
        
        pageNumbers.innerHTML = '';
        
        // Show max 5 page numbers
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, startPage + 4);
        
        if (endPage - startPage < 4) {
            startPage = Math.max(1, endPage - 4);
        }
        
        for (let i = startPage; i <= endPage; i++) {
            const pageNumber = document.createElement('div');
            pageNumber.className = `page-number ${i === currentPage ? 'active' : ''}`;
            pageNumber.textContent = i;
            pageNumbers.appendChild(pageNumber);
        }
        
        // Update button states
        const prevBtn = document.querySelector('.pagination-btn:first-child');
        const nextBtn = document.querySelector('.pagination-btn:last-child');
        
        if (prevBtn) {
            prevBtn.disabled = currentPage === 1;
        }
        if (nextBtn) {
            nextBtn.disabled = currentPage === totalPages;
        }
    }

    function updatePageIndicator() {
        const pageIndicator = document.getElementById('pageIndicator');
        if (pageIndicator) {
            const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
            const startItem = (currentPage - 1) * itemsPerPage + 1;
            const endItem = Math.min(currentPage * itemsPerPage, filteredHistory.length);
            
            pageIndicator.textContent = `Showing ${startItem}-${endItem} of ${filteredHistory.length} records`;
        }
    }

    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Helper Functions
    function getTopFactors(user_data) {
        if (!user_data) return ['No factors'];
        const factors = [];
        if (user_data.Family_History === 1) factors.push('Family History');
        if (user_data.Radiation_Exposure === 1) factors.push('Radiation Exposure');
        if (user_data.Iodine_Deficiency === 1) factors.push('Iodine Deficiency');
        return factors.length > 0 ? factors : ['No significant factors'];
    }

    function getActiveFactors(user_data) {
        if (!user_data) return [];
        const factors = [];
        if (user_data.Family_History === 1) factors.push('Family History of Thyroid Issues');
        if (user_data.Radiation_Exposure === 1) factors.push('History of Radiation Exposure');
        if (user_data.Iodine_Deficiency === 1) factors.push('Iodine Deficiency');
        return factors;
    }

    function getFactorBars(user_data) {
        if (!user_data) return '<p class="no-data">No factor data available</p>';
        
        const factors = [
            { name: 'Family History', value: user_data.Family_History || 0, max: 1 },
            { name: 'Radiation Exposure', value: user_data.Radiation_Exposure || 0, max: 1 },
            { name: 'Iodine Deficiency', value: user_data.Iodine_Deficiency || 0, max: 1 }
        ];
        
        return factors.map(factor => `
            <div class="factor-bar-item">
                <div class="factor-label">${factor.name}</div>
                <div class="factor-bar">
                    <div class="factor-fill ${factor.value === 1 ? 'active' : 'inactive'}" 
                         style="width: ${(factor.value / factor.max) * 100}%"></div>
                </div>
                <div class="factor-status">${factor.value === 1 ? 'Present' : 'Absent'}</div>
            </div>
        `).join('');
    }

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

    function getConfidenceLevel(percentage) {
        if (percentage < 20 || percentage > 80) return 'High';
        if (percentage < 40 || percentage > 60) return 'Moderate';
        return 'Medium';
    }

    function getRecommendationLevel(percentage) {
        if (percentage >= 70) return 'Immediate';
        if (percentage >= 40) return 'Regular';
        return 'Routine';
    }

    function getPredictionInsights(item) {
        const risk = item.risk_percentage || 0;
        const prediction = item.prediction || '';
        
        if (prediction === 'Malignant' && risk >= 70) {
            return 'This case was flagged as high-risk malignant. Immediate medical consultation is strongly recommended.';
        } else if (prediction === 'Malignant') {
            return 'The model detected potential malignancy. Further investigation through biopsy is advised.';
        } else if (risk >= 50) {
            return 'Elevated risk score suggests monitoring and follow-up testing in 6 months.';
        } else {
            return 'Low risk profile. Routine annual check-up recommended.';
        }
    }

    function getRecommendations(item) {
        const risk = item.risk_percentage || 0;
        const prediction = item.prediction || '';
        
        let recommendations = [];
        
        if (prediction === 'Malignant' || risk >= 70) {
            recommendations = [
                'Schedule immediate consultation with endocrinologist',
                'Ultrasound-guided fine needle aspiration biopsy recommended',
                'Complete thyroid function tests (T3, T4, TSH)',
                'Consider genetic testing if family history is present'
            ];
        } else if (risk >= 40) {
            recommendations = [
                'Follow-up ultrasound in 6 months',
                'Monitor thyroid hormone levels quarterly',
                'Dietary assessment for iodine intake',
                'Regular self-examination technique training'
            ];
        } else {
            recommendations = [
                'Annual thyroid ultrasound screening',
                'Maintain balanced iodine-rich diet',
                'Regular physical examination',
                'Report any new symptoms promptly'
            ];
        }
        
        return recommendations.map(rec => `
            <div class="recommendation-item">
                <i class="fas fa-check-circle"></i>
                <span>${rec}</span>
            </div>
        `).join('');
    }

    function showLoading() {
        const loading = document.getElementById('historyLoading');
        if (loading) loading.classList.remove('hidden');
        
        const tableBody = document.getElementById('historyTableBody');
        if (tableBody) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6">
                        <div class="loading-state">
                            <div class="loading-spinner">
                                <i class="fas fa-spinner fa-spin"></i>
                            </div>
                            <p>Loading history data...</p>
                        </div>
                    </td>
                </tr>
            `;
        }
    }

    function hideLoading() {
        const loading = document.getElementById('historyLoading');
        if (loading) loading.classList.add('hidden');
    }

    function showEmptyState() {
        const empty = document.getElementById('historyEmpty');
        if (empty) empty.classList.remove('hidden');
    }

    function showNotification(message, type = 'info') {
        // Remove existing notification
        const existingNotification = document.querySelector('.history-notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        // Create new notification
        const notification = document.createElement('div');
        notification.className = `history-notification notification-${type}`;
        
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${icons[type] || 'fa-info-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="notification-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 4000);
    }

    function showError(message) {
        const tableBody = document.getElementById('historyTableBody');
        if (tableBody) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center">
                        <div class="error-state">
                            <i class="fas fa-exclamation-triangle"></i>
                            <h4>Error Loading Data</h4>
                            <p>${message}</p>
                            <button class="btn-primary" onclick="window.initializeHistoryPage()">
                                <i class="fas fa-redo"></i> Try Again
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }
    }

    // Initialize when page loads
    document.addEventListener('DOMContentLoaded', function() {
        if (document.getElementById('historyTableBody')) {
            initializeHistoryPage();
        }
    });

    // Export functions to window object for onclick handlers
    window.showDetailsModal = showDetailsModal;
    window.closeDetailModal = closeDetailModal;
    window.switchDetailTab = switchDetailTab;
    window.initializeHistoryPage = initializeHistoryPage;

})();