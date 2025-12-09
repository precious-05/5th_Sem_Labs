// ============================================
// MAIN.JS - Common JavaScript for ThyroScan AI
// ============================================

// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
let currentPage = window.location.pathname.split('/').pop() || 'index.html';

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    console.log(`🚀 ThyroScan AI - ${currentPage} loaded`);
    
    // Initialize common components
    initializeCommonFeatures();
    
    // Test backend connection
    testBackendConnection();
    
    // Initialize page-specific features
    initializePageFeatures();
    
    // Setup event listeners
    setupCommonEventListeners();
    
    // Add animations on scroll
    initializeScrollAnimations();
});

// Initialize Common Features
function initializeCommonFeatures() {
    // Initialize theme (dark/light mode)
    initializeTheme();
    
    // Initialize mobile menu
    initializeMobileMenu();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize notifications
    initializeNotifications();
}

// Test Backend Connection
async function testBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Backend connected:', data.message || 'Server is running');
            showConnectionStatus(true);
        } else {
            console.warn('⚠️ Backend connection issue');
            showConnectionStatus(false);
        }
    } catch (error) {
        console.error('❌ Backend connection error:', error);
        showConnectionStatus(false);
    }
}

// Show Connection Status
function showConnectionStatus(isConnected) {
    const connectionBadge = document.getElementById('connectionStatus');
    if (connectionBadge) {
        if (isConnected) {
            connectionBadge.innerHTML = '<i class="fas fa-check-circle"></i> Connected';
            connectionBadge.className = 'connection-status connected';
        } else {
            connectionBadge.innerHTML = '<i class="fas fa-exclamation-circle"></i> Offline';
            connectionBadge.className = 'connection-status offline';
        }
    }
    
    // Add connection status CSS if not exists
    if (!document.querySelector('#connectionStatusCSS')) {
        const style = document.createElement('style');
        style.id = 'connectionStatusCSS';
        style.textContent = `
            .connection-status {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 500;
                z-index: 10000;
                display: flex;
                align-items: center;
                gap: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }
            .connection-status.connected {
                background: rgba(46, 213, 115, 0.2);
                color: #2ED573;
                border: 1px solid rgba(46, 213, 115, 0.3);
            }
            .connection-status.offline {
                background: rgba(255, 71, 87, 0.2);
                color: #FF4757;
                border: 1px solid rgba(255, 71, 87, 0.3);
            }
            .connection-status i {
                font-size: 1rem;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Create or update connection badge
    if (!connectionBadge) {
        const badge = document.createElement('div');
        badge.id = 'connectionStatus';
        document.body.appendChild(badge);
        showConnectionStatus(isConnected);
    }
}

// Initialize Theme (Dark/Light Mode)
function initializeTheme() {
    const themeToggle = document.querySelector('.theme-toggle');
    const savedTheme = localStorage.getItem('thyroscan-theme') || 'light';
    
    // Apply saved theme
    document.body.setAttribute('data-theme', savedTheme);
    
    if (themeToggle) {
        // Update toggle icon
        const icon = themeToggle.querySelector('i');
        icon.className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        
        // Add click event
        themeToggle.addEventListener('click', toggleTheme);
    }
}

// Toggle Theme
function toggleTheme() {
    const currentTheme = document.body.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    // Update body attribute
    document.body.setAttribute('data-theme', newTheme);
    
    // Update toggle icon
    const themeToggle = document.querySelector('.theme-toggle i');
    if (themeToggle) {
        themeToggle.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
    
    // Save to localStorage
    localStorage.setItem('thyroscan-theme', newTheme);
    
    // Dispatch theme change event
    document.dispatchEvent(new CustomEvent('themeChange', { detail: newTheme }));
}

// Initialize Mobile Menu
function initializeMobileMenu() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            mobileMenuBtn.classList.toggle('active');
            
            // Update hamburger icon
            const icon = mobileMenuBtn.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.className = 'fas fa-times';
            } else {
                icon.className = 'fas fa-bars';
            }
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                navLinks.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('i');
                icon.className = 'fas fa-bars';
            }
        });
    }
}

// Initialize Smooth Scrolling
function initializeSmoothScrolling() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            
            // Skip if it's just "#"
            if (href === '#') return;
            
            // Check if it's an internal page link
            if (href.includes('.html')) {
                return; // Let browser handle page navigation
            }
            
            e.preventDefault();
            
            const targetElement = document.querySelector(href);
            if (targetElement) {
                // Update active nav link
                document.querySelectorAll('.nav-links a').forEach(link => {
                    link.classList.remove('active');
                });
                this.classList.add('active');
                
                // Smooth scroll to target
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Initialize Tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

// Show Tooltip
function showTooltip(e) {
    const element = e.currentTarget;
    const tooltipText = element.getAttribute('data-tooltip');
    
    // Create tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = tooltipText;
    
    // Position tooltip
    const rect = element.getBoundingClientRect();
    tooltip.style.position = 'fixed';
    tooltip.style.top = `${rect.top - 40}px`;
    tooltip.style.left = `${rect.left + (rect.width / 2)}px`;
    tooltip.style.transform = 'translateX(-50%)';
    
    // Add to DOM
    document.body.appendChild(tooltip);
    
    // Add tooltip styles if not exists
    if (!document.querySelector('#tooltipStyles')) {
        const style = document.createElement('style');
        style.id = 'tooltipStyles';
        style.textContent = `
            .custom-tooltip {
                background: rgba(26, 26, 46, 0.95);
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 0.85rem;
                font-weight: 500;
                z-index: 10000;
                white-space: nowrap;
                pointer-events: none;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                animation: tooltipFadeIn 0.2s ease;
            }
            .custom-tooltip::after {
                content: '';
                position: absolute;
                bottom: -6px;
                left: 50%;
                transform: translateX(-50%);
                border-width: 6px 6px 0;
                border-style: solid;
                border-color: rgba(26, 26, 46, 0.95) transparent transparent;
            }
            @keyframes tooltipFadeIn {
                from {
                    opacity: 0;
                    transform: translateX(-50%) translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0);
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Hide Tooltip
function hideTooltip() {
    const tooltip = document.querySelector('.custom-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// Initialize Notifications
function initializeNotifications() {
    // Create notification container if not exists
    if (!document.querySelector('.notification-container')) {
        const container = document.createElement('div');
        container.className = 'notification-container';
        document.body.appendChild(container);
        
        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .notification-container {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                display: flex;
                flex-direction: column;
                gap: 10px;
                max-width: 400px;
            }
            .notification {
                background: white;
                border-radius: 12px;
                padding: 16px 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border-left: 4px solid #2D5BFF;
                display: flex;
                align-items: flex-start;
                gap: 12px;
                animation: notificationSlideIn 0.3s ease;
                transform-origin: top right;
                max-width: 100%;
            }
            .notification.success {
                border-left-color: #2ED573;
            }
            .notification.error {
                border-left-color: #FF4757;
            }
            .notification.warning {
                border-left-color: #FFA502;
            }
            .notification.info {
                border-left-color: #3498DB;
            }
            .notification-icon {
                font-size: 1.2rem;
                margin-top: 2px;
                flex-shrink: 0;
            }
            .notification.success .notification-icon {
                color: #2ED573;
            }
            .notification.error .notification-icon {
                color: #FF4757;
            }
            .notification.warning .notification-icon {
                color: #FFA502;
            }
            .notification.info .notification-icon {
                color: #3498DB;
            }
            .notification-content {
                flex: 1;
            }
            .notification-title {
                font-weight: 600;
                color: #1A1A2E;
                margin-bottom: 4px;
                font-size: 0.95rem;
            }
            .notification-message {
                color: #6b7280;
                font-size: 0.9rem;
                line-height: 1.4;
            }
            .notification-close {
                background: none;
                border: none;
                color: #9CA3AF;
                cursor: pointer;
                padding: 4px;
                font-size: 1rem;
                transition: color 0.2s;
                flex-shrink: 0;
            }
            .notification-close:hover {
                color: #4B5563;
            }
            @keyframes notificationSlideIn {
                from {
                    opacity: 0;
                    transform: translateX(100%) scale(0.9);
                }
                to {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                }
            }
            @keyframes notificationSlideOut {
                from {
                    opacity: 1;
                    transform: translateX(0) scale(1);
                }
                to {
                    opacity: 0;
                    transform: translateX(100%) scale(0.9);
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Show Notification
function showNotification(options) {
    const {
        title = 'Notification',
        message = '',
        type = 'info', // success, error, warning, info
        duration = 5000,
        icon = true
    } = options;
    
    const container = document.querySelector('.notification-container');
    if (!container) return;
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    // Set icon based on type
    let iconClass = 'fas fa-info-circle';
    switch (type) {
        case 'success':
            iconClass = 'fas fa-check-circle';
            break;
        case 'error':
            iconClass = 'fas fa-exclamation-circle';
            break;
        case 'warning':
            iconClass = 'fas fa-exclamation-triangle';
            break;
        case 'info':
            iconClass = 'fas fa-info-circle';
            break;
    }
    
    notification.innerHTML = `
        ${icon ? `<div class="notification-icon"><i class="${iconClass}"></i></div>` : ''}
        <div class="notification-content">
            <div class="notification-title">${title}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add to container
    container.appendChild(notification);
    
    // Auto-remove after duration
    const autoRemove = setTimeout(() => {
        removeNotification(notification);
    }, duration);
    
    // Close button event
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        clearTimeout(autoRemove);
        removeNotification(notification);
    });
    
    // Return notification element for manual control
    return notification;
}

// Remove Notification
function removeNotification(notification) {
    notification.style.animation = 'notificationSlideOut 0.3s ease';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

// Quick notification functions
function showSuccess(message, title = 'Success') {
    return showNotification({ title, message, type: 'success' });
}

function showError(message, title = 'Error') {
    return showNotification({ title, message, type: 'error' });
}

function showWarning(message, title = 'Warning') {
    return showNotification({ title, message, type: 'warning' });
}

function showInfo(message, title = 'Info') {
    return showNotification({ title, message, type: 'info' });
}

// Initialize Scroll Animations
function initializeScrollAnimations() {
    // Add scroll event for navbar
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
        
        // Add animation to elements when they come into view
        animateOnScroll();
    });
    
    // Initial animation check
    animateOnScroll();
}

// Animate elements on scroll
function animateOnScroll() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    animatedElements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.classList.add('animated');
        }
    });
}

// Add animation styles
function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .animate-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        .animate-on-scroll.animated {
            opacity: 1;
            transform: translateY(0);
        }
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
}

// Initialize Page Features
function initializePageFeatures() {
    switch (currentPage) {
        case 'index.html':
            // Home page specific initialization
            if (typeof initializeHomePage === 'function') {
                initializeHomePage();
            }
            break;
        case 'predict.html':
            // Predict page specific initialization
            if (typeof initializePredictPage === 'function') {
                initializePredictPage();
            }
            break;
        case 'history.html':
            // History page specific initialization
            if (typeof initializeHistoryPage === 'function') {
                initializeHistoryPage();
            }
            break;
        case 'about.html':
            // About page specific initialization
            if (typeof initializeAboutPage === 'function') {
                initializeAboutPage();
            }
            break;
    }
}

// Setup Common Event Listeners
function setupCommonEventListeners() {
    // Add active class to current page nav link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (currentPath.includes(linkPath) && linkPath !== 'index.html') {
            link.classList.add('active');
        }
        
        // Home page special case
        if (currentPath.endsWith('/') || currentPath.endsWith('/index.html')) {
            if (linkPath === 'index.html') {
                link.classList.add('active');
            }
        }
    });
    
    // Add year to footer
    const yearSpan = document.querySelector('.current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
}

// Format Date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Format Percentage
function formatPercentage(value) {
    return `${Math.round(value)}%`;
}

// Generate Random ID
function generateId(length = 8) {
    return Math.random().toString(36).substring(2, 2 + length);
}

// Debounce function for performance
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

// Throttle function for performance
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Validate Email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate Number
function validateNumber(value, min = null, max = null) {
    const num = parseFloat(value);
    if (isNaN(num)) return false;
    if (min !== null && num < min) return false;
    if (max !== null && num > max) return false;
    return true;
}

// Show Loading State
function showLoading(element, text = 'Loading...') {
    const originalHTML = element.innerHTML;
    element.innerHTML = `
        <i class="fas fa-spinner fa-spin"></i>
        ${text}
    `;
    element.disabled = true;
    return originalHTML;
}

// Hide Loading State
function hideLoading(element, originalHTML) {
    element.innerHTML = originalHTML;
    element.disabled = false;
}

// Export functions for use in other files
window.ThyroScan = {
    showSuccess,
    showError,
    showWarning,
    showInfo,
    formatDate,
    formatPercentage,
    generateId,
    validateEmail,
    validateNumber,
    showLoading,
    hideLoading,
    debounce,
    throttle
};

// Add animation styles on load
addAnimationStyles();

// Log initialization
console.log('📦 ThyroScan AI - Main.js initialized successfully');