// ============================================
// ABOUT.JS - About Page JavaScript for ThyroScan AI
// ============================================

// Initialize About Page
function initializeAboutPage() {
    console.log('ℹ️ About page initialized');
    
    // Initialize interactive elements
    initializeInteractiveElements();
    
    // Initialize timeline animations
    initializeTimeline();
    
    // Initialize FAQ accordion
    initializeFAQ();
    
    // Initialize team cards
    initializeTeamCards();
    
    // Initialize technology cards
    initializeTechCards();
    
    // Initialize floating elements
    initializeFloatingElements();
    
    // Initialize mission points
    initializeMissionPoints();
    
    // Initialize performance metrics
    initializePerformanceMetrics();
    
    // Setup event listeners
    setupAboutEventListeners();
    
    // Initialize animations
    initializeAboutAnimations();
}

// Initialize Interactive Elements
function initializeInteractiveElements() {
    // Technology cards hover effect
    const techCards = document.querySelectorAll('.tech-card');
    techCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.tech-icon');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
                icon.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.2)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.tech-icon');
            if (icon) {
                icon.style.transform = '';
                icon.style.boxShadow = '';
            }
        });
    });
    
    // Team cards hover effect
    const teamCards = document.querySelectorAll('.team-card');
    teamCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const avatar = this.querySelector('.team-avatar');
            if (avatar) {
                avatar.style.transform = 'scale(1.1)';
                avatar.style.boxShadow = '0 15px 35px rgba(45, 91, 255, 0.2)';
            }
            
            // Animate skills
            const skills = this.querySelectorAll('.skill');
            skills.forEach((skill, index) => {
                skill.style.transform = 'translateY(0)';
                skill.style.opacity = '1';
                skill.style.transitionDelay = `${index * 0.1}s`;
            });
        });
        
        card.addEventListener('mouseleave', function() {
            const avatar = this.querySelector('.team-avatar');
            if (avatar) {
                avatar.style.transform = '';
                avatar.style.boxShadow = '';
            }
            
            // Reset skills
            const skills = this.querySelectorAll('.skill');
            skills.forEach(skill => {
                skill.style.transform = 'translateY(10px)';
                skill.style.opacity = '0';
                skill.style.transitionDelay = '0s';
            });
        });
    });
    
    // Mission points hover effect
    const missionPoints = document.querySelectorAll('.mission-point');
    missionPoints.forEach(point => {
        point.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.point-icon');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(10deg)';
            }
        });
        
        point.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.point-icon');
            if (icon) {
                icon.style.transform = '';
            }
        });
    });
}

// Initialize Timeline
function initializeTimeline() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    
    // Add intersection observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                
                // Animate badges
                const badge = entry.target.querySelector('.timeline-badge');
                if (badge) {
                    setTimeout(() => {
                        badge.style.transform = 'scale(1)';
                        badge.style.opacity = '1';
                    }, 300);
                }
            }
        });
    }, {
        threshold: 0.3,
        rootMargin: '0px 0px -100px 0px'
    });
    
    timelineItems.forEach(item => {
        observer.observe(item);
        
        // Add hover effect
        item.addEventListener('mouseenter', function() {
            const content = this.querySelector('.timeline-content');
            if (content) {
                content.style.transform = 'translateY(-5px)';
                content.style.boxShadow = '0 15px 35px rgba(0, 0, 0, 0.1)';
            }
        });
        
        item.addEventListener('mouseleave', function() {
            const content = this.querySelector('.timeline-content');
            if (content) {
                content.style.transform = '';
                content.style.boxShadow = '';
            }
        });
    });
    
    // Add timeline animation styles
    const style = document.createElement('style');
    style.textContent = `
        .timeline-item {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.6s ease, transform 0.6s ease;
        }
        .timeline-item.animated {
            opacity: 1;
            transform: translateY(0);
        }
        .timeline-badge {
            transform: scale(0.8);
            opacity: 0;
            transition: transform 0.3s ease, opacity 0.3s ease;
        }
    `;
    document.head.appendChild(style);
}

// Initialize FAQ Accordion
function initializeFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        
        // Set initial height
        answer.style.maxHeight = '0';
        answer.style.overflow = 'hidden';
        answer.style.transition = 'max-height 0.3s ease';
        
        question.addEventListener('click', () => {
            // Close other items
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    const otherAnswer = otherItem.querySelector('.faq-answer');
                    otherAnswer.style.maxHeight = '0';
                    otherItem.classList.remove('active');
                }
            });
            
            // Toggle current item
            if (item.classList.contains('active')) {
                answer.style.maxHeight = '0';
                item.classList.remove('active');
            } else {
                answer.style.maxHeight = `${answer.scrollHeight}px`;
                item.classList.add('active');
            }
        });
        
        // Add hover effect
        question.addEventListener('mouseenter', () => {
            question.style.transform = 'translateX(5px)';
        });
        
        question.addEventListener('mouseleave', () => {
            question.style.transform = '';
        });
    });
    
    // Open first FAQ item by default
    if (faqItems.length > 0) {
        const firstItem = faqItems[0];
        const firstAnswer = firstItem.querySelector('.faq-answer');
        firstAnswer.style.maxHeight = `${firstAnswer.scrollHeight}px`;
        firstItem.classList.add('active');
    }
}

// Initialize Team Cards
function initializeTeamCards() {
    const teamCards = document.querySelectorAll('.team-card');
    
    // Add animation delay based on index
    teamCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
        card.classList.add('animate-on-scroll');
        
        // Initialize skills animation
        const skills = card.querySelectorAll('.skill');
        skills.forEach(skill => {
            skill.style.transform = 'translateY(10px)';
            skill.style.opacity = '0';
            skill.style.transition = 'transform 0.3s ease, opacity 0.3s ease';
        });
    });
}

// Initialize Tech Cards
function initializeTechCards() {
    const techCards = document.querySelectorAll('.tech-card');
    
    techCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-on-scroll');
        
        // Add click effect for tech tags
        const techTags = card.querySelectorAll('.tech-tag');
        techTags.forEach(tag => {
            tag.addEventListener('click', function(e) {
                e.stopPropagation();
                
                // Create ripple effect
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.cssText = `
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.5);
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    width: ${size}px;
                    height: ${size}px;
                    top: ${y}px;
                    left: ${x}px;
                    pointer-events: none;
                `;
                
                this.appendChild(ripple);
                
                // Remove ripple after animation
                setTimeout(() => {
                    ripple.remove();
                }, 600);
                
                // Show tooltip with technology info
                const techName = this.textContent;
                showTechTooltip(techName, this);
            });
        });
    });
    
    // Add ripple animation
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
}

// Show Tech Tooltip
function showTechTooltip(techName, element) {
    const techInfo = {
        'FastAPI': 'High-performance Python web framework for building APIs',
        'Scikit-learn': 'Machine learning library for Python',
        'MongoDB': 'NoSQL document database for scalable applications',
        'Plotly.js': 'JavaScript graphing library for interactive visualizations',
        'Python 3.9+': 'Programming language for backend and ML',
        'NumPy': 'Library for numerical computing in Python',
        'Atlas Cloud': 'MongoDB cloud hosting service',
        'Encryption': 'Data encryption for security',
        'Backup': 'Automated data backup systems',
        'HTML5': 'Latest version of HTML markup language',
        'CSS3': 'Latest version of CSS styling language',
        'JavaScript': 'Programming language for web interactivity',
        'Logistic Regression': 'Statistical model for classification',
        'Random Forest': 'Ensemble learning method',
        'Feature Engineering': 'Process of creating features from raw data',
        'Cross-Validation': 'Model validation technique'
    };
    
    const info = techInfo[techName] || 'Technology information not available';
    
    ThyroScan.showInfo(info, techName);
}

// Initialize Floating Elements
function initializeFloatingElements() {
    const floatingElements = document.querySelectorAll('.element');
    
    floatingElements.forEach((element, index) => {
        // Add random floating animation
        const duration = 6 + Math.random() * 4;
        const delay = Math.random() * 2;
        
        element.style.animation = `float ${duration}s ease-in-out ${delay}s infinite`;
        
        // Add hover effect
        element.addEventListener('mouseenter', function() {
            this.style.animationPlayState = 'paused';
            this.style.transform = 'scale(1.2)';
            this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.3)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.animationPlayState = 'running';
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
}

// Initialize Mission Points
function initializeMissionPoints() {
    const missionPoints = document.querySelectorAll('.mission-point');
    
    missionPoints.forEach((point, index) => {
        point.style.animationDelay = `${index * 0.2}s`;
        point.classList.add('animate-on-scroll');
        
        // Add click to expand
        point.addEventListener('click', function() {
            const content = this.querySelector('.point-content p');
            if (content.style.maxHeight && content.style.maxHeight !== '0px') {
                content.style.maxHeight = '0';
                this.classList.remove('expanded');
            } else {
                content.style.maxHeight = `${content.scrollHeight}px`;
                this.classList.add('expanded');
            }
        });
    });
}

// Initialize Performance Metrics
function initializePerformanceMetrics() {
    const metricCards = document.querySelectorAll('.metric-card');
    
    metricCards.forEach(card => {
        const metricValue = card.querySelector('.metric-value');
        const barFill = card.querySelector('.bar-fill');
        
        if (metricValue && barFill) {
            const value = parseFloat(metricValue.textContent);
            const isPercentage = metricValue.textContent.includes('%');
            
            // Animate metric value
            animateCounter(metricValue, value, isPercentage);
            
            // Animate bar fill
            setTimeout(() => {
                barFill.style.transition = 'width 1.5s ease';
                barFill.style.width = `${value}%`;
            }, 500);
        }
    });
}

// Animate Counter
function animateCounter(element, target, isPercentage = false) {
    const duration = 2000;
    const step = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = isPercentage ? `${Math.round(target)}%` : target.toFixed(2);
            clearInterval(timer);
        } else {
            element.textContent = isPercentage ? `${Math.round(current)}%` : current.toFixed(2);
        }
    }, 16);
}

// Setup About Event Listeners
function setupAboutEventListeners() {
    // CTA button effects
    const ctaButtons = document.querySelectorAll('.btn-primary, .btn-secondary');
    ctaButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            const glowEffect = this.querySelector('.btn-glow-effect');
            if (glowEffect) {
                glowEffect.style.left = '100%';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            const glowEffect = this.querySelector('.btn-glow-effect');
            if (glowEffect) {
                glowEffect.style.left = '-100%';
            }
        });
    });
    
    // Social link hover effects
    const socialLinks = document.querySelectorAll('.social-link');
    socialLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'rotate(360deg) scale(1.2)';
            }
        });
        
        link.addEventListener('mouseleave', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = '';
            }
        });
    });
    
    // Footer link hover effects
    const footerLinks = document.querySelectorAll('.footer-links a');
    footerLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = 'translateX(5px)';
                icon.style.color = 'var(--primary)';
            }
        });
        
        link.addEventListener('mouseleave', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.transform = '';
                icon.style.color = '';
            }
        });
    });
    
    // Tech badge click effects
    const techBadges = document.querySelectorAll('.tech-badge');
    techBadges.forEach(badge => {
        badge.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Add pulse animation
            this.style.animation = 'pulse 0.5s ease';
            setTimeout(() => {
                this.style.animation = '';
            }, 500);
            
            // Show technology info
            const techName = this.textContent;
            showTechTooltip(techName, this);
        });
    });
}

// Initialize About Animations
function initializeAboutAnimations() {
    // Add animation classes to elements
    const elementsToAnimate = [
        '.mission-text',
        '.mission-point',
        '.tech-card',
        '.team-card',
        '.timeline-item',
        '.faq-item',
        '.metric-card'
    ];
    
    elementsToAnimate.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach((element, index) => {
            element.classList.add('animate-on-scroll');
            element.style.animationDelay = `${index * 0.1}s`;
        });
    });
    
    // Initialize scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });
    
    document.querySelectorAll('.animate-on-scroll').forEach(element => {
        observer.observe(element);
    });
}

// Initialize About Statistics
async function initializeAboutStats() {
    try {
        const response = await fetch(`${window.API_BASE_URL || 'http://localhost:8000'}/about-stats`);
        if (response.ok) {
            const data = await response.json();
            
            // Update stats if elements exist
            updateStatsElements(data);
        }
    } catch (error) {
        console.log('Using default about stats');
        showDefaultStats();
    }
}

// Update Stats Elements
function updateStatsElements(data) {
    // Update accuracy if element exists
    const accuracyElement = document.querySelector('[data-stat="accuracy"]');
    if (accuracyElement && data.accuracy) {
        animateCounter(accuracyElement, data.accuracy, true);
    }
    
    // Update predictions count
    const predictionsElement = document.querySelector('[data-stat="predictions"]');
    if (predictionsElement && data.total_predictions) {
        animateCounter(predictionsElement, data.total_predictions);
    }
    
    // Update active users
    const usersElement = document.querySelector('[data-stat="users"]');
    if (usersElement && data.active_users) {
        animateCounter(usersElement, data.active_users);
    }
}

// Show Default Stats
function showDefaultStats() {
    const defaultStats = {
        accuracy: 83,
        total_predictions: 1500,
        active_users: 250
    };
    
    updateStatsElements(defaultStats);
}

// Initialize Technology Details Modal
function initializeTechModal() {
    // Create modal for detailed technology view
    const modalHTML = `
        <div id="techModal" class="modal hidden">
            <div class="modal-overlay"></div>
            <div class="modal-container">
                <div class="modal-header">
                    <h3>Technology Details</h3>
                    <button class="modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-content">
                    <div id="techModalContent"></div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to page if not exists
    if (!document.getElementById('techModal')) {
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Add modal styles
        const modalStyle = document.createElement('style');
        modalStyle.textContent = `
            .modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 2000;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .modal.hidden {
                display: none;
            }
            .modal-overlay {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                backdrop-filter: blur(5px);
            }
            .modal-container {
                position: relative;
                background: white;
                border-radius: 16px;
                max-width: 600px;
                width: 100%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
                animation: modalSlideIn 0.3s ease;
            }
            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 24px;
                border-bottom: 1px solid #e5e7eb;
            }
            .modal-header h3 {
                margin: 0;
                color: #1A1A2E;
            }
            .modal-close {
                background: none;
                border: none;
                font-size: 1.2rem;
                color: #6b7280;
                cursor: pointer;
                padding: 8px;
                border-radius: 8px;
                transition: all 0.2s;
            }
            .modal-close:hover {
                background: #f3f4f6;
                color: #374151;
            }
            .modal-content {
                padding: 24px;
            }
            @keyframes modalSlideIn {
                from {
                    opacity: 0;
                    transform: translateY(-50px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(modalStyle);
        
        // Add event listeners
        const modal = document.getElementById('techModal');
        const closeBtn = modal.querySelector('.modal-close');
        const overlay = modal.querySelector('.modal-overlay');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.classList.add('hidden');
                document.body.style.overflow = '';
            });
        }
        
        if (overlay) {
            overlay.addEventListener('click', () => {
                modal.classList.add('hidden');
                document.body.style.overflow = '';
            });
        }
        
        // Escape key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
                modal.classList.add('hidden');
                document.body.style.overflow = '';
            }
        });
    }
}

// Show Technology Details
function showTechnologyDetails(techName) {
    const techDetails = {
        'FastAPI': {
            description: 'FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.',
            features: [
                'Fast: Very high performance, on par with NodeJS and Go',
                'Fast to code: Increase the speed to develop features by about 200% to 300%',
                'Fewer bugs: Reduce about 40% of human (developer) induced errors',
                'Intuitive: Great editor support. Completion everywhere. Less time debugging',
                'Easy: Designed to be easy to use and learn. Less time reading docs'
            ],
            useCase: 'Used as our backend API framework for handling prediction requests and data management.'
        },
        'Scikit-learn': {
            description: 'Scikit-learn is a free software machine learning library for the Python programming language.',
            features: [
                'Simple and efficient tools for predictive data analysis',
                'Accessible to everybody, and reusable in various contexts',
                'Built on NumPy, SciPy, and matplotlib',
                'Open source, commercially usable - BSD license'
            ],
            useCase: 'Used for implementing our Logistic Regression model for thyroid cancer prediction.'
        },
        'MongoDB': {
            description: 'MongoDB is a source-available cross-platform document-oriented database program.',
            features: [
                'Document-oriented database with flexible schema',
                'Full cloud-based deployment with MongoDB Atlas',
                'Rich query language with aggregation pipeline',
                'Horizontal scaling through sharding'
            ],
            useCase: 'Used for storing prediction history, user data (anonymized), and model metadata.'
        },
        'Plotly.js': {
            description: 'Plotly.js is a high-level, declarative charting library built on top of d3.js and stack.gl.',
            features: [
                '20+ chart types including 3D charts',
                'Interactive charts with zoom, pan, and hover',
                'Responsive design for all screen sizes',
                'Export charts as PNG, SVG, or PDF'
            ],
            useCase: 'Used for visualizing prediction results, feature importance, and risk trends.'
        }
    };
    
    const details = techDetails[techName];
    if (!details) return;
    
    // Initialize modal if not already
    initializeTechModal();
    
    const modal = document.getElementById('techModal');
    const content = document.getElementById('techModalContent');
    
    if (modal && content) {
        content.innerHTML = `
            <h4>${techName}</h4>
            <p class="tech-description">${details.description}</p>
            
            <div class="tech-section">
                <h5>Key Features:</h5>
                <ul>
                    ${details.features.map(feature => `<li>${feature}</li>`).join('')}
                </ul>
            </div>
            
            <div class="tech-section">
                <h5>Our Implementation:</h5>
                <p>${details.useCase}</p>
            </div>
            
            <div class="tech-links">
                <a href="#" class="btn-secondary">
                    <i class="fas fa-book"></i>
                    Documentation
                </a>
                <a href="#" class="btn-secondary">
                    <i class="fab fa-github"></i>
                    GitHub
                </a>
            </div>
        `;
        
        // Add styles for modal content
        const contentStyle = document.createElement('style');
        contentStyle.textContent = `
            .tech-description {
                font-size: 1.1rem;
                line-height: 1.6;
                color: #4b5563;
                margin-bottom: 24px;
            }
            .tech-section {
                margin-bottom: 20px;
            }
            .tech-section h5 {
                color: #1A1A2E;
                margin-bottom: 8px;
                font-size: 1rem;
            }
            .tech-section ul {
                padding-left: 20px;
                margin: 0;
            }
            .tech-section li {
                margin-bottom: 4px;
                color: #6b7280;
            }
            .tech-links {
                display: flex;
                gap: 12px;
                margin-top: 24px;
            }
        `;
        
        // Remove previous style if exists
        const oldStyle = document.getElementById('techModalContentStyle');
        if (oldStyle) oldStyle.remove();
        
        contentStyle.id = 'techModalContentStyle';
        document.head.appendChild(contentStyle);
        
        // Show modal
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

// Initialize about page
document.addEventListener('DOMContentLoaded', () => {
    if (typeof initializeAboutPage === 'function') {
        initializeAboutPage();
    }
    
    // Load stats after a delay
    setTimeout(initializeAboutStats, 1000);
    
    // Initialize tech modal
    initializeTechModal();
    
    // Add tech card click events
    document.querySelectorAll('.tech-card').forEach(card => {
        card.addEventListener('click', function() {
            const techName = this.querySelector('h3')?.textContent;
            if (techName) {
                showTechnologyDetails(techName);
            }
        });
    });
});

// Export functions for debugging
window.AboutPage = {
    initializeAboutPage,
    initializeFAQ,
    initializeTimeline,
    showTechnologyDetails
};