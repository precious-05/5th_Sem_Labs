// ===== CONFIGURATION =====
const API_BASE_URL = 'http://localhost:8000';
const SWIPER_CONFIG = {
    slidesPerView: 1,
    spaceBetween: 20,
    loop: true,
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        640: { slidesPerView: 2 },
        1024: { slidesPerView: 3 },
    }
};

// ===== DOM ELEMENTS =====
let swiperInstance = null;

// ===== MAIN INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

async function initializeApp() {
    try {
        // Hide preloader
        setTimeout(() => {
            document.querySelector('.preloader').classList.add('hidden');
            document.body.classList.add('loaded');
        }, 1000);

        // Initialize components
        initializeNavigation();
        initializeSwiper();
        initializeAnimations();
        initializeEventListeners();
        setupIntersectionObserver();
        
        // Check backend connection
        await checkBackendConnection();
        
        // Update stats with real data
        await updateRealStats();
        
        console.log('✅ ThyroScan Pro initialized successfully');
    } catch (error) {
        console.error('❌ App initialization failed:', error);
        showNotification('Failed to initialize application', 'error');
    }
}

// ===== NAVIGATION =====
function initializeNavigation() {
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    const navbar = document.querySelector('.navbar');

    // Mobile menu toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            mobileToggle.classList.toggle('active');
            document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
        });
    }

    // Close mobile menu when clicking links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            mobileToggle.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navMenu.contains(e.target) && !mobileToggle.contains(e.target)) {
            navMenu.classList.remove('active');
            mobileToggle.classList.remove('active');
            document.body.style.overflow = '';
        }
    });

    // Navbar scroll effect
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // Update active nav link
                navLinks.forEach(link => link.classList.remove('active'));
                this.classList.add('active');
                
                // Scroll to target
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    mobileToggle.classList.remove('active');
                    document.body.style.overflow = '';
                }
            }
        });
    });
}

// ===== SWIPER SLIDER =====
function initializeSwiper() {
    const swiperEl = document.querySelector('.swiper');
    
    if (!swiperEl) return;
    
    try {
        swiperInstance = new Swiper('.swiper', SWIPER_CONFIG);
        
        // Add hover pause
        swiperEl.addEventListener('mouseenter', () => {
            if (swiperInstance.autoplay.running) {
                swiperInstance.autoplay.stop();
            }
        });
        
        swiperEl.addEventListener('mouseleave', () => {
            if (!swiperInstance.autoplay.running) {
                swiperInstance.autoplay.start();
            }
        });
        
        console.log('✅ Swiper initialized');
    } catch (error) {
        console.error('❌ Swiper initialization failed:', error);
    }
}

// ===== ANIMATIONS =====
function initializeAnimations() {
    // Initialize AOS (Animate On Scroll) if available
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 1000,
            once: true,
            offset: 100
        });
    }
    
    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translate3d(0, ${rate}px, 0)`;
        });
    }
    
    // Animate stats on view
    const statCards = document.querySelectorAll('.stat-card');
    if (statCards.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        statCards.forEach(card => observer.observe(card));
    }
}

// ===== EVENT LISTENERS =====
function initializeEventListeners() {
    // CTA buttons
    const ctaButtons = document.querySelectorAll('.btn-glow, .btn-primary, .btn-cta');
    ctaButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const href = button.getAttribute('href');
            
            if (href && href !== '#') {
                // Add click animation
                button.classList.add('clicked');
                setTimeout(() => button.classList.remove('clicked'), 300);
                
                // Navigate after animation
                setTimeout(() => {
                    if (href.startsWith('#')) {
                        const target = document.querySelector(href);
                        if (target) {
                            window.scrollTo({
                                top: target.offsetTop - 80,
                                behavior: 'smooth'
                            });
                        }
                    } else {
                        window.location.href = href;
                    }
                }, 300);
            }
        });
    });
    
    // Video demo button
    const videoBtn = document.querySelector('.btn-video');
    if (videoBtn) {
        videoBtn.addEventListener('click', () => {
            showVideoModal();
        });
    }
    
    // Feature cards hover effect
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
            card.style.boxShadow = 'var(--shadow-xl)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = 'var(--shadow-md)';
        });
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllModals();
        }
        
        // Swiper navigation with keyboard
        if (swiperInstance) {
            if (e.key === 'ArrowLeft') {
                swiperInstance.slidePrev();
            } else if (e.key === 'ArrowRight') {
                swiperInstance.slideNext();
            }
        }
    });
    
    // Window resize handling
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            handleResize();
        }, 250);
    });
}

// ===== BACKEND CONNECTION =====
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Backend connected:', data);
            updateConnectionStatus(true);
            return data;
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.warn('⚠️ Backend connection failed:', error.message);
        updateConnectionStatus(false);
        return null;
    }
}

function updateConnectionStatus(connected) {
    const statusIndicator = document.createElement('div');
    statusIndicator.className = `connection-status ${connected ? 'connected' : 'disconnected'}`;
    statusIndicator.innerHTML = `
        <i class="fas fa-${connected ? 'wifi' : 'wifi-slash'}"></i>
        <span>${connected ? 'Connected' : 'Disconnected'}</span>
    `;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .connection-status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 10px 16px;
            border-radius: var(--radius-md);
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 8px;
            z-index: 1000;
            animation: slideInRight 0.3s ease;
        }
        .connection-status.connected {
            background: var(--success);
            color: white;
        }
        .connection-status.disconnected {
            background: var(--danger);
            color: white;
        }
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    
    // Remove existing status
    const existing = document.querySelector('.connection-status');
    if (existing) existing.remove();
    
    document.head.appendChild(style);
    document.body.appendChild(statusIndicator);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        statusIndicator.remove();
        document.head.removeChild(style);
    }, 3000);
}

// ===== REAL-TIME STATS =====
async function updateRealStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) return;
        
        const data = await response.json();
        
        // Update accuracy stat
        const accuracyStat = document.querySelector('.stat-card:nth-child(1) h3');
        if (accuracyStat && data.model_loaded) {
            accuracyStat.innerHTML = `83<span class="percent">%</span>`;
        }
        
        // Update features count
        const featuresStat = document.querySelector('.stat-card:nth-child(2) h3');
        if (featuresStat && data.features_count) {
            featuresStat.innerHTML = `${data.features_count}<span class="k">+</span>`;
        }
        
    } catch (error) {
        console.warn('Could not update real-time stats:', error);
    }
}

// ===== INTERSECTION OBSERVER =====
function setupIntersectionObserver() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                
                // Animate counters
                if (entry.target.classList.contains('stat-card')) {
                    animateCounter(entry.target);
                }
            }
        });
    }, observerOptions);
    
    // Observe all animate-able elements
    document.querySelectorAll('.stat-card, .feature-card, .step').forEach(el => {
        observer.observe(el);
    });
}

function animateCounter(element) {
    const counter = element.querySelector('h3');
    if (!counter) return;
    
    const target = parseInt(counter.textContent);
    if (isNaN(target)) return;
    
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        counter.textContent = Math.floor(current);
    }, 30);
}

// ===== VIDEO MODAL =====
function showVideoModal() {
    const modal = document.createElement('div');
    modal.className = 'video-modal active';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h3><i class="fas fa-play-circle"></i> ThyroScan Pro Demo</h3>
                <button class="close-modal">&times;</button>
            </div>
            <div class="modal-body">
                <div class="video-placeholder">
                    <i class="fas fa-video"></i>
                    <p>Demo video coming soon</p>
                    <p class="small">Watch how ThyroScan Pro analyzes thyroid data with AI</p>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-outline close-modal">
                    <i class="fas fa-times"></i>
                    Close
                </button>
                <button class="btn-primary" onclick="window.location.href='predict.html'">
                    <i class="fas fa-play-circle"></i>
                    Try Live Demo
                </button>
            </div>
        </div>
    `;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .video-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 2000;
            backdrop-filter: blur(5px);
        }
        .video-modal.active {
            display: flex;
        }
        .video-modal .modal-content {
            background: var(--white);
            border-radius: var(--radius-lg);
            width: 90%;
            max-width: 800px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: var(--shadow-xl);
        }
        .video-modal .modal-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--gray-lighter);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .video-modal .modal-body {
            padding: 2rem;
            text-align: center;
        }
        .video-modal .modal-footer {
            padding: 1.5rem;
            border-top: 1px solid var(--gray-lighter);
            display: flex;
            justify-content: flex-end;
            gap: 1rem;
        }
        .video-placeholder {
            padding: 4rem 2rem;
            background: var(--light);
            border-radius: var(--radius-md);
            border: 2px dashed var(--gray-lighter);
        }
        .video-placeholder i {
            font-size: 4rem;
            color: var(--gray-lighter);
            margin-bottom: 1.5rem;
        }
        .video-placeholder p {
            font-size: 1.2rem;
            color: var(--gray);
            margin-bottom: 0.5rem;
        }
        .video-placeholder .small {
            font-size: 0.9rem;
        }
        .close-modal {
            background: none;
            border: none;
            font-size: 1.5rem;
            color: var(--gray);
            cursor: pointer;
            padding: 5px;
        }
        .close-modal:hover {
            color: var(--danger);
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(modal);
    
    // Close modal
    modal.querySelectorAll('.close-modal').forEach(btn => {
        btn.addEventListener('click', () => {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.remove();
                document.head.removeChild(style);
            }, 300);
        });
    });
    
    // Close on ESC
    document.addEventListener('keydown', function closeOnEsc(e) {
        if (e.key === 'Escape') {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.remove();
                document.head.removeChild(style);
            }, 300);
            document.removeEventListener('keydown', closeOnEsc);
        }
    });
    
    // Close on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.remove();
                document.head.removeChild(style);
            }, 300);
        }
    });
}

// ===== UTILITY FUNCTIONS =====
function handleResize() {
    // Update swiper on resize
    if (swiperInstance) {
        swiperInstance.update();
    }
    
    // Update any responsive elements
    const isMobile = window.innerWidth < 768;
    document.body.classList.toggle('mobile-view', isMobile);
}

function closeAllModals() {
    document.querySelectorAll('.modal.active, .video-modal.active').forEach(modal => {
        modal.classList.remove('active');
        setTimeout(() => modal.remove(), 300);
    });
}

function showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 
                         type === 'error' ? 'exclamation-circle' : 
                         'info-circle'}"></i>
        <span>${message}</span>
        <button class="close-notification">&times;</button>
    `;
    
    // Add styles
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            gap: 10px;
            z-index: 10000;
            animation: slideIn 0.3s ease-out;
            max-width: 400px;
            box-shadow: var(--shadow-lg);
        }
        .notification.success {
            background: var(--success);
            color: white;
        }
        .notification.error {
            background: var(--danger);
            color: white;
        }
        .notification.info {
            background: var(--info);
            color: white;
        }
        .close-notification {
            background: none;
            border: none;
            color: inherit;
            font-size: 1.2rem;
            cursor: pointer;
            margin-left: auto;
        }
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    const autoRemove = setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
            document.head.removeChild(style);
        }
    }, 5000);
    
    // Close button
    notification.querySelector('.close-notification').addEventListener('click', () => {
        clearTimeout(autoRemove);
        notification.remove();
        document.head.removeChild(style);
    });
}

// ===== PERFORMANCE OPTIMIZATIONS =====
// Debounce function for scroll events
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

// Throttle function for resize events
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

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showNotification('An error occurred. Please refresh the page.', 'error');
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    showNotification('Something went wrong. Please try again.', 'error');
});

// ===== SERVICE WORKER FOR PWA (Optional) =====
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(error => {
            console.log('ServiceWorker registration failed:', error);
        });
    });
}

// ===== EXPORT FUNCTIONS FOR GLOBAL USE =====
window.ThyroScan = {
    showNotification,
    checkBackendConnection,
    updateRealStats,
    showVideoModal
};

console.log('ThyroScan Pro JavaScript loaded successfully');