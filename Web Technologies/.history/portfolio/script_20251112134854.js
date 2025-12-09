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
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
    
    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
}

// Theme toggle functionality
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
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
    const modalContent = modal.querySelector('.modal-body');
    const closeModal = modal.querySelector('.close-modal');
    const viewButtons = document.querySelectorAll('.project-view-btn');
    
    // Project data
    const projects = {
        1: {
            title: "Prosperous Farmer",
            description: "A comprehensive Streamlit application for agricultural data analysis and visualization. This tool helps farmers and agricultural analysts make data-driven decisions by providing insights into crop yields, weather patterns, and market trends.",
            tech: ["Python", "Streamlit", "Pandas", "Plotly"],
            images: ["assets/images/project1.jpg"],
            links: {
                live: "#",
                github: "#",
                kaggle: "#"
            }
        },
        2: {
            title: "EDA on US Natural Resources Revenue",
            description: "An exploratory data analysis project on US natural resources revenue data. This analysis uncovers patterns and trends in resource extraction, government revenue, and environmental impact.",
            tech: ["Python", "Pandas", "Seaborn", "Jupyter"],
            images: ["assets/images/project2.jpg"],
            links: {
                live: "#",
                github: "#",
                kaggle: "#"
            }
        },
        3: {
            title: "Smart Irrigation Manager",
            description: "An IoT and Streamlit application for smart irrigation management. This system uses sensor data to optimize water usage in agricultural settings, reducing waste while maintaining crop health.",
            tech: ["Python", "Streamlit", "IoT", "SQL"],
            images: ["assets/images/project3.jpg"],
            links: {
                live: "#",
                github: "#",
                video: "#"
            }
        },
        4: {
            title: "Thyroid Cancer Prediction",
            description: "A machine learning project for thyroid cancer prediction using patient data and medical imaging. This ongoing project aims to develop an accurate diagnostic tool to assist healthcare professionals.",
            tech: ["Python", "Scikit-learn", "TensorFlow", "OpenCV"],
            images: ["assets/images/project4.jpg"],
            links: {
                github: "#",
                status: "In Progress"
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
                                <img src="${img}" alt="${project.title}">
                            </div>
                        `).join('')}
                    </div>
                    <div class="carousel-controls">
                        <button class="carousel-prev">‹</button>
                        <button class="carousel-next">›</button>
                    </div>
                    <div class="carousel-indicators">
                        ${project.images.map((_, index) => `
                            <span class="indicator ${index === 0 ? 'active' : ''}" data-slide="${index}"></span>
                        `).join('')}
                    </div>
                </div>
                <div class="modal-details">
                    <div class="modal-description">
                        <h3>Description</h3>
                        <p>${project.description}</p>
                    </div>
                    <div class="modal-tech">
                        <h3>Technologies</h3>
                        <div class="tech-tags">
                            ${project.tech.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                        </div>
                    </div>
                    <div class="modal-links">
                        <h3>Links</h3>
                        <div class="link-buttons">
                            ${project.links.live ? `<a href="${project.links.live}" class="btn btn-primary" target="_blank">Live App</a>` : ''}
                            ${project.links.github ? `<a href="${project.links.github}" class="btn btn-secondary" target="_blank">GitHub</a>` : ''}
                            ${project.links.kaggle ? `<a href="${project.links.kaggle}" class="btn btn-secondary" target="_blank">Kaggle</a>` : ''}
                            ${project.links.video ? `<a href="${project.links.video}" class="btn btn-secondary" target="_blank">Video Demo</a>` : ''}
                            ${project.links.status ? `<span class="status-badge">${project.links.status}</span>` : ''}
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Initialize carousel
        initCarousel();
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
    }
}

// Contact form functionality
function initContactForm() {
    const contactForm = document.getElementById('contact-form');
    const toast = document.getElementById('toast');
    
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Basic form validation
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const message = document.getElementById('message').value.trim();
        
        if (!name || !email || !message) {
            alert('Please fill in all fields');
            return;
        }
        
        if (!isValidEmail(email)) {
            alert('Please enter a valid email address');
            return;
        }
        
        // Simulate form submission
        simulateFormSubmission();
    });
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function simulateFormSubmission() {
        // Show loading state
        const submitBtn = contactForm.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;
        
        // Simulate API call delay
        setTimeout(() => {
            // Show success toast
            showToast();
            
            // Reset form
            contactForm.reset();
            
            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 2000);
    }
    
    function showToast() {
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// Scroll to top functionality
function initScrollToTop() {
    const scrollBtn = document.getElementById('scroll-top');
    
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
}

// Floating icons animation
function initFloatingIcons() {
    // Already implemented in CSS with animations
}

// Resume download button
document.getElementById('resume-btn').addEventListener('click', function(e) {
    e.preventDefault();
    
    // Create a temporary link to trigger download
    const link = document.createElement('a');
    link.href = '#'; // Replace with actual resume URL
    link.download = 'Alina_Liaquat_Resume.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Show a message (since we don't have an actual resume file)
    alert('Resume download would start here. In a real implementation, this would link to your actual resume PDF.');
});

// Stats counter animation (optional enhancement)
function initStatsCounter() {
    const stats = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                const duration = 2000; // 2 seconds
                const step = target / (duration / 16); // 60fps
                let current = 0;
                
                const timer = setInterval(() => {
                    current += step;
                    if (current >= target) {
                        current = target;
                        clearInterval(timer);
                    }
                    entry.target.textContent = Math.floor(current);
                }, 16);
                
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    stats.forEach(stat => {
        observer.observe(stat);
    });
}

// Initialize stats counter if stats section exists
if (document.querySelector('.stats')) {
    initStatsCounter();
}