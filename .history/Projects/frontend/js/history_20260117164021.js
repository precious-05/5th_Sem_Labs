// ============================================
// HISTORY.JS - UPDATED VERSION (NO ACTIONS COLUMN)
// ============================================

(function() {
    'use strict';

    // Simple variables
    let historyData = [];
    let filteredHistory = [];

    // API Configuration
    const API_BASE_URL = window.API_BASE_URL || 'http://localhost:8000';

    // Initialize History Page
    function initializeHistoryPage() {
        console.log('📊 Initializing History Page...');
        
        // Setup event listeners
        setupEventListeners();
        
        // Load history
        loadHistory();
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
                setTimeout(() => {
                    filterHistory();
                }, 300);
            });
        }
        
        // Filter selects
        document.querySelectorAll('.filter-select').forEach(select => {
            select.addEventListener('change', filterHistory);
        });
    }

    // Load History
    async function loadHistory() {
        try {
            showLoading();
            
            const response = await fetch(`${API_BASE_URL}/history?limit=50`);
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.history && Array.isArray(data.history)) {
                historyData = data.history;
                filteredHistory = [...historyData];
                
                if (historyData.length === 0) {
                    showEmptyState();
                } else {
                    updateHistoryDisplay();
                    updateSummaryStats();
                }
            } else {
                showEmptyState();
            }
            
        } catch (error) {
            console.error('❌ Error loading history:', error);
            showEmptyState();
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
                    item.user_data?.Gender_Male === 1 ? 'male' : 'female'
                ].join(' ').toLowerCase();
                
                return searchable.includes(searchTerm);
            }
            
            return true;
        });
        
        updateHistoryDisplay();
        updateSummaryStats();
    }

    // Update History Display
    function updateHistoryDisplay() {
        const tableBody = document.getElementById('historyTableBody');
        if (!tableBody) return;
        
        tableBody.innerHTML = '';
        
        if (filteredHistory.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center">
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
        
        filteredHistory.forEach((item, index) => {
            const row = createHistoryRow(item, index);
            tableBody.appendChild(row);
        });
    }

    // Create History Row (UPDATED - NO ACTIONS COLUMN)
    function createHistoryRow(item, index) {
        const row = document.createElement('tr');
        row.className = 'history-item';
        
        try {
            const date = new Date(item.timestamp || Date.now());
            const age = item.user_data?.Age || 'N/A';
            const gender = item.user_data?.Gender_Male === 1 ? 'Male' : 'Female';
            const riskPercentage = item.risk_percentage || 0;
            const prediction = item.prediction || 'N/A';
            
            // UPDATED: 5 columns instead of 6 (removed Actions column)
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
            `;
            
        } catch (error) {
            console.error('Error creating row:', error);
            row.innerHTML = '<td colspan="5" class="text-center">Error displaying</td>';
        }
        
        return row;
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
    }

    // Refresh History
    async function refreshHistory() {
        await loadHistory();
    }

    // Export History
    function exportHistory() {
        if (filteredHistory.length === 0) {
            alert('No data to export');
            return;
        }
        
        const csvData = filteredHistory.map(item => {
            const date = new Date(item.timestamp || Date.now());
            return [
                date.toLocaleString(),
                `${item.risk_percentage || 0}%`,
                item.prediction || 'N/A',
                item.user_data?.Age || 'N/A',
                item.user_data?.Gender_Male === 1 ? 'Male' : 'Female'
            ];
        });
        
        const csvContent = [
            ['Date', 'Risk Score', 'Prediction', 'Age', 'Gender'],
            ...csvData
        ].map(row => row.join(',')).join('\n');
        
        const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `history_export.csv`;
        a.click();
        
        alert(`Exported ${filteredHistory.length} records`);
    }

    // Helper Functions
    function getTopFactors(user_data) {
        if (!user_data) return [];
        const factors = [];
        if (user_data.Family_History === 1) factors.push('Family History');
        if (user_data.Radiation_Exposure === 1) factors.push('Radiation');
        if (user_data.Iodine_Deficiency === 1) factors.push('Iodine Def');
        return factors;
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

    function showLoading() {
        const loading = document.getElementById('historyLoading');
        if (loading) loading.classList.remove('hidden');
    }

    function hideLoading() {
        const loading = document.getElementById('historyLoading');
        if (loading) loading.classList.add('hidden');
    }

    function showEmptyState() {
        const empty = document.getElementById('historyEmpty');
        if (empty) empty.classList.remove('hidden');
    }

    // Initialize when page loads
    document.addEventListener('DOMContentLoaded', function() {
        if (document.getElementById('historyTableBody')) {
            initializeHistoryPage();
        }
    });

})();