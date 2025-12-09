// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initPreloader();
    initNavbar();
    initThemeToggle();
    initScrollAnimations();
    initSkillAnimations();
    initProjectModals();
    initContactForm();
    initScrollToTop();
    initTypewriter();
    initFloatingIcons();
    initResumeDownload();
    initCertificateLinks();
});

// Preloader
function initPreloader() {
    const preloader = document.getElementById('preloader');
    
    window.addEventListener('load', function() {
        setTimeout(function() {
            preloader.style.opacity = '0';
            setTimeout(function() {
                preloader.style.display = 'none';
            }, 500);
        }, 1000);
    });
}

// Navbar functionality
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Hamburger menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (hamburger) {
                hamburger.classList.remove('active');
            }
            navMenu.classList.remove('active');
        });
    });
}

// Theme toggle functionality
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    
    if (!themeToggle) return;
    
    const themeIcon = themeToggle.querySelector('i');
    
    // Check for saved theme preference or default to dark
    const currentTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });
    
    function updateThemeIcon(theme) {
        if (theme === 'dark') {
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        } else {
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }
    }
}

// Scroll animations with Intersection Observer
function initScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                
                // Special handling for skill progress bars
                if (entry.target.classList.contains('skill-progress')) {
                    const width = entry.target.getAttribute('data-width');
                    setTimeout(() => {
                        entry.target.style.width = width + '%';
                    }, 200);
                }
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll(
        '.about-text, .skill-category, .skill-item, .project-card, ' +
        '.certification-card, .timeline-item, .quote-text, ' +
        '.contact-form-container, .contact-info, .skill-progress'
    );
    
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Skill progress animations
function initSkillAnimations() {
    // Already handled in scroll animations
}

// Project modals
function initProjectModals() {
    const modal = document.getElementById('project-modal');
    if (!modal) return;
    
    const modalContent = modal.querySelector('.modal-body');
    const closeModal = modal.querySelector('.close-modal');
    const viewButtons = document.querySelectorAll('.project-view-btn');
    
    // Project data with actual project information
    const projects = {
        1: {
            title: "Prosperous Farmer",
            description: "A comprehensive Streamlit application for agricultural data analysis and visualization. This tool helps farmers and agricultural analysts make data-driven decisions by providing insights into crop yields, weather patterns, and market trends. The app features interactive dashboards, predictive analytics, and real-time data processing capabilities.",
            tech: ["Python", "Streamlit", "Pandas", "Plotly", "Scikit-learn", "SQL"],
            images: ["images/Prosperous_Farmer.png"],
            links: {
                live: "https://prosperous-farmer.streamlit.app/",
                github: "https://github.com/precious-05/prosperous-farmer",
                demo: "#"
            }
        },
        2: {
            title: "EDA on US Natural Resources Revenue",
            description: "An exploratory data analysis project on US natural resources revenue data from Kaggle. This comprehensive analysis uncovers patterns and trends in resource extraction, government revenue generation, and environmental impact across different states and time periods. The project includes data cleaning, visualization, and statistical analysis.",
            tech: ["Python", "Pandas", "Seaborn", "Matplotlib", "Jupyter", "NumPy"],
            images: ["images/time_series.png"],
            links: {
                kaggle: "https://www.kaggle.com/code/alinaliaquat/eda-on-us-natural-resources-revenue",
                github: "https://github.com/precious-05/natural-resources-analysis",
                notebook: "#"
            }
        },
        4: {
            title: "Thyroid Cancer Prediction",
            description: "A machine learning project for thyroid cancer prediction using patient demographic data, medical history, and diagnostic test results. This ongoing project aims to develop an accurate diagnostic tool to assist healthcare professionals in early detection and risk assessment. Features include data preprocessing, feature engineering, and multiple ML model comparisons.",
            tech: ["Python", "Scikit-learn",  "Pandas", "NumPy", "Seaborn"],
            images: ["images/tsh.png"],
            links: {
                github: "https://github.com/precious-05/thyroid-cancer-prediction",
                kaggle: "#",
                research: "#"
            }
        }
    };
    
    // Open modal when project view button is clicked
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const projectId = this.getAttribute('data-project');
            const project = projects[projectId];
            
            if (project) {
                openModal(project);
            }
        });
    });
    
    // Close modal when X is clicked
    closeModal.addEventListener('click', closeModalFunc);
    
    // Close modal when clicking outside content
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModalFunc();
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModalFunc();
        }
    });
    
    function openModal(project) {
        modalContent.innerHTML = `
            <div class="modal-project">
                <h2 class="modal-title">${project.title}</h2>
                <div class="modal-carousel">
                    <div class="carousel-container">
                        ${project.images.map(img => `
                            <div class="carousel-slide">
                                <img src="${img}" alt="${project.title}" onerror="this.src='images/placeholder.jpg'">
                            </div>
                        `).join('')}
                    </div>
                    ${project.images.length > 1 ? `
                        <div class="carousel-controls">
                            <button class="carousel-prev">‹</button>
                            <button class="carousel-next">›</button>
                        </div>
                        <div class="carousel-indicators">
                            ${project.images.map((_, index) => `
                                <span class="indicator ${index === 0 ? 'active' : ''}" data-slide="${index}"></span>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
                <div class="modal-details">
                    <div class="modal-description">
                        <h3>Description</h3>
                        <p>${project.description}</p>
                    </div>
                    <div class="modal-tech">
                        <h3>Technologies Used</h3>
                        <div class="tech-tags">
                            ${project.tech.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                        </div>
                    </div>
                    <div class="modal-links">
                        <h3>Project Links</h3>
                        <div class="link-buttons">
                            ${project.links.live ? `<a href="${project.links.live}" class="btn btn-primary" target="_blank" rel="noopener"> Live App</a>` : ''}
                            ${project.links.github ? `<a href="${project.links.github}" class="btn btn-secondary" target="_blank" rel="noopener">GitHub</a>` : ''}
                            ${project.links.kaggle ? `<a href="${project.links.kaggle}" class="btn btn-secondary" target="_blank" rel="noopener">Kaggle</a>` : ''}
                            ${project.links.demo ? `<a href="${project.links.demo}" class="btn btn-secondary" target="_blank" rel="noopener"> Demo</a>` : ''}
                            ${project.links.notebook ? `<a href="${project.links.notebook}" class="btn btn-secondary" target="_blank" rel="noopener"> Notebook</a>` : ''}
                            ${project.links.research ? `<a href="${project.links.research}" class="btn btn-secondary" target="_blank" rel="noopener"> Research</a>` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Initialize carousel if there are multiple images
        if (project.images.length > 1) {
            initCarousel();
        }
    }
    
    function closeModalFunc() {
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';
        
        // Reset modal content with a slight delay for smooth transition
        setTimeout(() => {
            modalContent.innerHTML = '';
        }, 300);
    }
    
    function initCarousel() {
        const carouselContainer = document.querySelector('.carousel-container');
        const slides = document.querySelectorAll('.carousel-slide');
        const indicators = document.querySelectorAll('.indicator');
        const prevBtn = document.querySelector('.carousel-prev');
        const nextBtn = document.querySelector('.carousel-next');
        
        let currentSlide = 0;
        
        // Function to show a specific slide
        function showSlide(index) {
            if (index < 0) {
                index = slides.length - 1;
            } else if (index >= slides.length) {
                index = 0;
            }
            
            carouselContainer.style.transform = `translateX(-${index * 100}%)`;
            
            // Update indicators
            indicators.forEach((indicator, i) => {
                indicator.classList.toggle('active', i === index);
            });
            
            currentSlide = index;
        }
        
        // Event listeners for controls
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                showSlide(currentSlide - 1);
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                showSlide(currentSlide + 1);
            });
        }
        
        // Event listeners for indicators
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                showSlide(index);
            });
        });
        
        // Auto-advance carousel
        let carouselInterval = setInterval(() => {
            showSlide(currentSlide + 1);
        }, 5000);
        
        // Pause auto-advance on hover
        carouselContainer.addEventListener('mouseenter', () => {
            clearInterval(carouselInterval);
        });
        
        carouselContainer.addEventListener('mouseleave', () => {
            carouselInterval = setInterval(() => {
                showSlide(currentSlide + 1);
            }, 5000);
        });
        
        // Touch/swipe support for mobile
        let startX = 0;
        let endX = 0;
        
        carouselContainer.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });
        
        carouselContainer.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            handleSwipe();
        });
        
        function handleSwipe() {
            const swipeThreshold = 50;
            const diff = startX - endX;
            
            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    // Swipe left - next slide
                    showSlide(currentSlide + 1);
                } else {
                    // Swipe right - previous slide
                    showSlide(currentSlide - 1);
                }
            }
        }
    }
}

// Contact form functionality with REAL Formspree implementation
function initContactForm() {
    const contactForm = document.getElementById('contact-form');
    if (!contactForm) return;
    
    const toast = document.getElementById('toast');
    
    // Update form action to your actual Formspree endpoint
    contactForm.setAttribute('action', 'https://formspree.io/f/your-actual-form-id');
    contactForm.setAttribute('method', 'POST');
    
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Basic form validation
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();
        
        if (!name || !email || !message) {
            showMessage('Please fill in all fields', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage('Please enter a valid email address', 'error');
            return;
        }
        
        // Real form submission
        await submitContactForm(name, email, message);
    });
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    async function submitContactForm(name, email, message) {
        // Show loading state
        const submitBtn = contactForm.querySelector('.submit-btn');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;
        
        try {
            // REAL Formspree API call
            const response = await fetch('https://formspree.io/f/your-actual-form-id', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    message: message,
                    _subject: `New Portfolio Message from ${name}`,
                    _replyto: email
                })
            });
            
            if (response.ok) {
                // Show success message
                showToast('Message sent successfully! 🎉 I\'ll get back to you soon.');
                
                // Reset form
                contactForm.reset();
                
                // Log success
                console.log('Form submitted successfully:', { name, email, message });
            } else {
                throw new Error('Form submission failed');
            }
            
        } catch (error) {
            console.error('Form submission error:', error);
            showMessage('Sorry, there was an error sending your message. Please try again or email me directly at lnliaquat@gmail.com', 'error');
        } finally {
            // Reset button
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }
    
    function showToast(message) {
        if (!toast) return;
        
        const toastMessage = toast.querySelector('.toast-message');
        toastMessage.textContent = message;
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 5000);
    }
    
    function showMessage(message, type = 'info') {
        // Create a temporary message element
        const messageEl = document.createElement('div');
        messageEl.className = `form-message ${type}`;
        messageEl.innerHTML = `
            <i class="fas ${type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        `;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'error' ? '#ff6b6b' : '#4ecdc4'};
            color: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: 10000;
            animation: slideInRight 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            max-width: 400px;
            font-weight: 500;
        `;
        
        document.body.appendChild(messageEl);
        
        setTimeout(() => {
            messageEl.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => {
                if (document.body.contains(messageEl)) {
                    document.body.removeChild(messageEl);
                }
            }, 300);
        }, 5000);
    }
}

// Scroll to top functionality
function initScrollToTop() {
    const scrollBtn = document.getElementById('scroll-top');
    if (!scrollBtn) return;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    });
    
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Typewriter effect
function initTypewriter() {
    // Already implemented in CSS with animations
    // Additional JS enhancements can be added here if needed
}

// Floating icons animation
function initFloatingIcons() {
    // Already implemented in CSS with animations
    // Additional JS interactions can be added here
}

// Resume download functionality
function initResumeDownload() {
    const resumeBtn = document.getElementById('resume-btn');
    if (!resumeBtn) return;
    
    resumeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Actual resume PDF path
        const resumeUrl = 'documents/Alina_Liaquat_Resume.pdf';
        
        // Create a temporary link to trigger download
        const link = document.createElement('a');
        link.href = resumeUrl;
        link.download = 'Alina_Liaquat_Data_Analyst_Resume.pdf';
        link.target = '_blank';
        
        // Show loading state
        const originalText = resumeBtn.innerHTML;
        resumeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Downloading...';
        resumeBtn.disabled = true;
        
        // Append to body and click
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Reset button after a delay
        setTimeout(() => {
            resumeBtn.innerHTML = originalText;
            resumeBtn.disabled = false;
            
            // Show success message
            showDownloadMessage('Resume downloaded successfully! 📄');
        }, 1500);
    });
}

// Certificate links functionality
function initCertificateLinks() {
    const certificateLinks = document.querySelectorAll('.certification-link');
    
    certificateLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const certificateTitle = this.closest('.certification-card').querySelector('.certification-title').textContent;
            let certificateUrl = '';
            
            // Map certificate titles to actual PDF paths
            switch(certificateTitle) {
                case 'Google Prompting Essentials':
                    certificateUrl = 'Prompt_Engineering.pdf';
                    break;
                case 'Google Advanced Data Analytics':
                    certificateUrl = 'data analytics.pdf';
                    break;
                default:
                    certificateUrl = 'certificates/sample_certificate.pdf';
            }
            
            // Open certificate in new tab
            window.open(certificateUrl, '_blank');
            
            // Show confirmation message
            showDownloadMessage(`Opening ${certificateTitle} certificate 📜`);
        });
    });
}

// Helper function to show download messages
function showDownloadMessage(message) {
    // Create a temporary message element
    const messageEl = document.createElement('div');
    messageEl.className = 'download-message';
    messageEl.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>${message}</span>
    `;
    messageEl.style.cssText = `
        position: fixed;
        bottom: 100px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(255, 255, 255, 0.95);
        color: #1a1a2e;
        padding: 1rem 2rem;
        border-radius: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: slideInUp 0.3s ease;
    `;
    
    document.body.appendChild(messageEl);
    
    setTimeout(() => {
        messageEl.style.animation = 'slideOutDown 0.3s ease';
        setTimeout(() => {
            if (document.body.contains(messageEl)) {
                document.body.removeChild(messageEl);
            }
        }, 300);
    }, 3000);
}

// Enhanced smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Account for fixed header
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Initialize smooth scrolling
initSmoothScrolling();

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes slideInUp {
        from { transform: translate(-50%, 100px); opacity: 0; }
        to { transform: translate(-50%, 0); opacity: 1; }
    }
    
    @keyframes slideOutDown {
        from { transform: translate(-50%, 0); opacity: 1; }
        to { transform: translate(-50%, 100px); opacity: 0; }
    }
    
    .form-message, .download-message {
        font-family: 'Poppins', sans-serif;
    }
    
    .fa-spinner {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Modal carousel styles */
    .modal-carousel {
        position: relative;
        overflow: hidden;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    .carousel-container {
        display: flex;
        transition: transform 0.5s ease;
    }
    
    .carousel-slide {
        min-width: 100%;
    }
    
    .carousel-slide img {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 15px;
    }
    
    .carousel-controls {
        position: absolute;
        top: 50%;
        width: 100%;
        display: flex;
        justify-content: space-between;
        transform: translateY(-50%);
        padding: 0 1rem;
    }
    
    .carousel-prev,
    .carousel-next {
        background: rgba(255, 255, 255, 0.9);
        border: none;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .carousel-prev:hover,
    .carousel-next:hover {
        background: white;
        transform: scale(1.1);
    }
    
    .carousel-indicators {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .indicator {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .indicator.active {
        background: white;
        transform: scale(1.2);
    }
    
    /* Modal content styles */
    .modal-project {
        padding: 1rem;
    }
    
    .modal-title {
        color: var(--secondary-color);
        margin-bottom: 1.5rem;
        text-align: center;
        font-size: 2rem;
    }
    
    .modal-details {
        display: grid;
        gap: 2rem;
    }
    
    .modal-description h3,
    .modal-tech h3,
    .modal-links h3 {
        color: var(--accent-color);
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .modal-description p {
        line-height: 1.7;
        color: var(--text-color);
        opacity: 0.9;
    }
    
    .tech-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .tech-tag {
        background: rgba(255, 107, 107, 0.1);
        color: var(--secondary-color);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        border: 1px solid rgba(255, 107, 107, 0.3);
    }
    
    .link-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .link-buttons .btn {
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
`;
document.head.appendChild(style);

// Performance optimization: Debounce scroll events
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

// Update scroll event listeners with debouncing
window.addEventListener('scroll', debounce(function() {
    // Existing scroll functionality
    const navbar = document.querySelector('.navbar');
    const scrollBtn = document.getElementById('scroll-top');
    
    if (window.scrollY > 50) {
        navbar?.classList.add('scrolled');
    } else {
        navbar?.classList.remove('scrolled');
    }
    
    if (scrollBtn) {
        if (window.scrollY > 300) {
            scrollBtn.classList.add('show');
        } else {
            scrollBtn.classList.remove('show');
        }
    }
}, 10));

// Add error handling for images
document.addEventListener('error', function(e) {
    if (e.target.tagName === 'IMG') {
        e.target.src = 'images/placeholder.jpg';
        e.target.alt = 'Image not available';
    }
}, true);

// Formspree setup instructions
console.log(`
📧 Form Submission Setup Instructions:

1. Go to https://formspree.io/ and create a free account
2. Create a new form and get your form ID
3. Replace 'your-actual-form-id' in the contact form function with your actual Formspree form ID
4. Test the form submission to make sure it works

Current form endpoint: https://formspree.io/f/your-actual-form-id
`);

// Export functions for potential module use (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initPreloader,
        initNavbar,
        initThemeToggle,
        initScrollAnimations,
        initProjectModals,
        initContactForm,
        initScrollToTop,
        initResumeDownload,
        initCertificateLinks
    };
}