// ============================================
// HOME.JS - Modern Home Page JavaScript for ThyroScan AI
// ============================================

// Global variables
let imageSwiper = null;
let testimonialsSwiper = null;
let scrollY = 0;
let animationFrameId = null;

// Modern effects configuration
const CONFIG = {
    PARALLAX_INTENSITY: 0.05,
    FLOAT_AMPLITUDE: 10,
    FLOAT_SPEED: 0.002,
    GLITCH_INTERVAL: 5000,
    PARTICLES_COUNT: 50,
    TYPING_SPEED: 50,
    SCROLL_TRIGGER: 100
};

// Initialize Home Page
function initializeHomePage() {
    console.log('🏠 Modern home page initialized');
    
    // Apply modern effects
    applyModernEffects();
    
    // Initialize components with staggered delay
    setTimeout(() => {
        initializeImageSlider();
        initializeTestimonialsSlider();
        initializeStatsCounter();
        initializeScrollAnimations();
        initializeParallaxEffects();
        initializeParticleEffects();
        initializeGlitchEffect();
        initializeTypewriterEffect();
    }, 300);
    
    // Setup event listeners
    setupHomeEventListeners();
    
    // Apply floating animations
    applyFloatingAnimations();
    
    // Start animation loop
    startAnimationLoop();
}

// MODERN EFFECTS ======================================

function applyModernEffects() {
    // Add CSS for modern effects
    const modernCSS = `
        /* Modern effects */
        .float-animation {
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(1deg); }
        }
        
        .pulse-animation {
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .glitch-effect {
            position: relative;
        }
        
        .glitch-effect::before,
        .glitch-effect::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.8;
        }
        
        .glitch-effect::before {
            animation: glitch-1 2s infinite linear alternate-reverse;
            left: 2px;
            text-shadow: -2px 0 #ff00ff;
            clip-path: polygon(0 0, 100% 0, 100% 35%, 0 35%);
        }
        
        .glitch-effect::after {
            animation: glitch-2 3s infinite linear alternate-reverse;
            left: -2px;
            text-shadow: 2px 0 #00ffff;
            clip-path: polygon(0 65%, 100% 65%, 100% 100%, 0 100%);
        }
        
        @keyframes glitch-1 {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }
        
        @keyframes glitch-2 {
            0% { transform: translate(0); }
            10% { transform: translate(2px, -2px); }
            30% { transform: translate(-2px, 2px); }
            50% { transform: translate(2px, 2px); }
            70% { transform: translate(-2px, -2px); }
            90% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }
        
        /* Particle effects */
        .particle {
            position: absolute;
            pointer-events: none;
            border-radius: 50%;
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            opacity: 0;
            z-index: 1;
        }
        
        /* Gradient text animation */
        .gradient-text {
            background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent));
            background-size: 200% 200%;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: gradient-shift 3s ease infinite;
        }
        
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Hover effects */
        .feature-card, .step-card, .testimonial-card {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .feature-card:hover, .step-card:hover, .testimonial-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        }
        
        /* Scroll reveal animation */
        .reveal-on-scroll {
            opacity: 0;
            transform: translateY(50px);
            transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .reveal-on-scroll.revealed {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Button shine effect */
        .btn-shine {
            position: relative;
            overflow: hidden;
        }
        
        .btn-shine::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 50%;
            height: 200%;
            background: linear-gradient(
                to right,
                rgba(255, 255, 255, 0) 0%,
                rgba(255, 255, 255, 0.3) 50%,
                rgba(255, 255, 255, 0) 100%
            );
            transform: rotate(30deg);
            transition: all 0.6s;
        }
        
        .btn-shine:hover::after {
            left: 150%;
        }
    `;
    
    const style = document.createElement('style');
    style.id = 'modern-effects-css';
    style.textContent = modernCSS;
    document.head.appendChild(style);
}

// Initialize Typewriter Effect
function initializeTypewriterEffect() {
    const heroTitle = document.querySelector('.hero-title');
    if (!heroTitle) return;
    
    const text = heroTitle.textContent;
    heroTitle.textContent = '';
    heroTitle.classList.add('typewriter-container');
    
    let i = 0;
    const typeWriter = () => {
        if (i < text.length) {
            heroTitle.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, CONFIG.TYPING_SPEED);
        }
    };
    
    // Start typing after a delay
    setTimeout(typeWriter, 1000);
}

// Initialize Glitch Effect
function initializeGlitchEffect() {
    const aiTexts = document.querySelectorAll('.ai-text, .gradient-text');
    
    aiTexts.forEach(text => {
        text.classList.add('glitch-effect');
        text.setAttribute('data-text', text.textContent);
    });
    
    // Random glitch trigger
    setInterval(() => {
        aiTexts.forEach(text => {
            if (Math.random() > 0.7) {
                text.style.animation = 'none';
                setTimeout(() => {
                    text.style.animation = '';
                }, 100);
            }
        });
    }, CONFIG.GLITCH_INTERVAL);
}

// Initialize Particle Effects
function initializeParticleEffects() {
    const heroSection = document.querySelector('.hero');
    if (!heroSection) return;
    
    for (let i = 0; i < CONFIG.PARTICLES_COUNT; i++) {
        createParticle(heroSection);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.classList.add('particle');
    
    const size = Math.random() * 4 + 1;
    const x = Math.random() * container.offsetWidth;
    const y = Math.random() * container.offsetHeight;
    
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.left = `${x}px`;
    particle.style.top = `${y}px`;
    
    container.appendChild(particle);
    
    // Animate particle
    anime({
        targets: particle,
        opacity: [
            { value: 0.3, duration: 0 },
            { value: 0.8, duration: 1000 },
            { value: 0, duration: 1000 }
        ],
        translateX: Math.random() * 200 - 100,
        translateY: Math.random() * 200 - 100,
        scale: [0, 1, 0],
        easing: 'easeInOutSine',
        duration: Math.random() * 3000 + 2000,
        complete: () => {
            particle.remove();
            setTimeout(() => createParticle(container), Math.random() * 1000);
        }
    });
}

// Initialize Parallax Effects
function initializeParallaxEffects() {
    const parallaxElements = document.querySelectorAll('.floating-shapes .shape, .hero-background');
    
    window.addEventListener('scroll', () => {
        parallaxElements.forEach((element, index) => {
            const speed = (index + 1) * CONFIG.PARALLAX_INTENSITY;
            const yPos = -(window.scrollY * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// Apply Floating Animations
function applyFloatingAnimations() {
    const shapes = document.querySelectorAll('.shape');
    const featureIcons = document.querySelectorAll('.feature-icon, .step-icon');
    
    shapes.forEach((shape, index) => {
        shape.style.animationDelay = `${index * 0.5}s`;
        shape.classList.add('float-animation');
    });
    
    featureIcons.forEach((icon, index) => {
        icon.style.animationDelay = `${index * 0.2}s`;
        icon.classList.add('float-animation');
    });
}

// Initialize Stats Counter
function initializeStatsCounter() {
    const statValues = document.querySelectorAll('.stat-content h3');
    
    statValues.forEach(stat => {
        const originalValue = stat.textContent;
        const numericValue = parseInt(originalValue) || 0;
        
        if (numericValue > 0) {
            stat.textContent = '0';
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        animateCounter(stat, numericValue, originalValue);
                        observer.unobserve(stat);
                    }
                });
            });
            
            observer.observe(stat);
        }
    });
}

function animateCounter(element, target, originalText) {
    let current = 0;
    const increment = target / 50;
    const duration = 1500;
    const interval = duration / 50;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = originalText;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, interval);
}

// Initialize Scroll Animations
function initializeScrollAnimations() {
    const revealElements = document.querySelectorAll('.feature-card, .step-card, .testimonial-card, .section-header');
    
    revealElements.forEach(element => {
        element.classList.add('reveal-on-scroll');
    });
    
    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    revealElements.forEach(element => {
        scrollObserver.observe(element);
    });
}

// SLIDER INITIALIZATION ======================================

// Initialize Image Slider
function initializeImageSlider() {
    const imageSlider = document.querySelector('.image-slider');
    if (!imageSlider) return;
    
    console.log('🎨 Initializing modern image slider...');
    
    // Clean up existing swiper
    if (imageSwiper) {
        imageSwiper.destroy(true, true);
    }
    
    // Create modern swiper with enhanced effects
    imageSwiper = new Swiper('.image-slider', {
        direction: 'horizontal',
        loop: true,
        speed: 1000,
        grabCursor: true,
        
        // Enhanced autoplay
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
        },
        
        // Creative effect
        effect: 'creative',
        creativeEffect: {
            prev: {
                shadow: true,
                translate: [0, 0, -400],
            },
            next: {
                translate: ['100%', 0, 0],
            },
        },
        
        // Navigation
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        
        // Pagination
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
            dynamicBullets: true,
        },
        
        // Keyboard control
        keyboard: {
            enabled: true,
        },
        
        // Mousewheel control
        mousewheel: {
            forceToAxis: true,
        },
        
        // Breakpoints
        breakpoints: {
            320: {
                slidesPerView: 1,
                spaceBetween: 0
            },
            768: {
                slidesPerView: 1,
                spaceBetween: 0
            },
            1024: {
                slidesPerView: 1,
                spaceBetween: 0
            }
        },
        
        // Callbacks
        on: {
            init: function() {
                console.log('✅ Modern image slider ready');
                addImageHoverEffects();
            },
            slideChange: function() {
                updateActiveSlideEffects(this);
            }
        }
    });
    
    // Add 3D perspective to container
    imageSlider.parentElement.style.perspective = '1000px';
    
    return imageSwiper;
}

// Initialize Testimonials Slider
function initializeTestimonialsSlider() {
    const testimonialsSlider = document.querySelector('.testimonials-swiper');
    if (!testimonialsSlider) return;
    
    console.log('💬 Initializing testimonials slider...');
    
    // Clean up existing swiper
    if (testimonialsSwiper) {
        testimonialsSwiper.destroy(true, true);
    }
    
    testimonialsSwiper = new Swiper('.testimonials-swiper', {
        direction: 'horizontal',
        loop: true,
        speed: 800,
        grabCursor: true,
        
        autoplay: {
            delay: 8000,
            disableOnInteraction: false,
        },
        
        // Coverflow effect for testimonials
        effect: 'coverflow',
        coverflowEffect: {
            rotate: 0,
            stretch: 0,
            depth: 100,
            modifier: 2.5,
            slideShadows: true,
        },
        
        centeredSlides: true,
        slidesPerView: 'auto',
        spaceBetween: 30,
        
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
            dynamicBullets: true,
        },
        
        breakpoints: {
            320: {
                slidesPerView: 1,
                spaceBetween: 20
            },
            768: {
                slidesPerView: 1.2,
                spaceBetween: 30
            },
            1024: {
                slidesPerView: 1.5,
                spaceBetween: 40
            }
        },
        
        on: {
            init: function() {
                console.log('✅ Testimonials slider ready');
            }
        }
    });
    
    return testimonialsSwiper;
}

// SLIDER EFFECTS ======================================

function addImageHoverEffects() {
    const slides = document.querySelectorAll('.swiper-slide');
    
    slides.forEach(slide => {
        slide.addEventListener('mouseenter', () => {
            if (imageSwiper && !imageSwiper.autoplay.running) return;
            imageSwiper.autoplay.stop();
        });
        
        slide.addEventListener('mouseleave', () => {
            if (imageSwiper && !imageSwiper.autoplay.running) {
                imageSwiper.autoplay.start();
            }
        });
    });
}

function updateActiveSlideEffects(swiper) {
    const slides = swiper.slides;
    
    slides.forEach((slide, index) => {
        const img = slide.querySelector('img');
        if (!img) return;
        
        if (index === swiper.activeIndex) {
            // Enhance active slide
            img.style.transform = 'scale(1.05)';
            img.style.filter = 'brightness(1.1)';
            img.style.transition = 'all 0.5s ease';
        } else {
            // Reset other slides
            img.style.transform = 'scale(1)';
            img.style.filter = 'brightness(0.9)';
        }
    });
}

// EVENT LISTENERS ======================================

function setupHomeEventListeners() {
    // Add shine effect to buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    buttons.forEach(btn => {
        btn.classList.add('btn-shine');
        
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.2)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
    });
    
    // Feature card interactions
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.feature-icon');
            if (icon) {
                icon.style.transform = 'scale(1.2) rotate(5deg)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.feature-icon');
            if (icon) {
                icon.style.transform = '';
            }
        });
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Theme toggle
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
    
    // Mobile menu
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    }
    
    // Window resize handler
    window.addEventListener('resize', debounce(handleResize, 250));
}

// THEME TOGGLE ======================================

function toggleTheme() {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-toggle i');
    
    body.classList.toggle('dark-theme');
    
    if (body.classList.contains('dark-theme')) {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
        localStorage.setItem('theme', 'dark');
    } else {
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
        localStorage.setItem('theme', 'light');
    }
}

// MOBILE MENU ======================================

function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    const menuIcon = document.querySelector('.mobile-menu-btn i');
    
    navLinks.classList.toggle('active');
    
    if (navLinks.classList.contains('active')) {
        menuIcon.classList.remove('fa-bars');
        menuIcon.classList.add('fa-times');
    } else {
        menuIcon.classList.remove('fa-times');
        menuIcon.classList.add('fa-bars');
    }
}

// UTILITY FUNCTIONS ======================================

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

function handleResize() {
    if (window.innerWidth >= 768) {
        const navLinks = document.querySelector('.nav-links');
        const menuIcon = document.querySelector('.mobile-menu-btn i');
        
        if (navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        }
    }
}

// ANIMATION LOOP ======================================

function startAnimationLoop() {
    let lastTime = 0;
    
    function animate(currentTime) {
        const deltaTime = currentTime - lastTime;
        lastTime = currentTime;
        
        // Update floating animations
        updateFloatingElements(deltaTime);
        
        // Continue animation loop
        animationFrameId = requestAnimationFrame(animate);
    }
    
    animationFrameId = requestAnimationFrame(animate);
}

function updateFloatingElements(deltaTime) {
    const time = Date.now() * CONFIG.FLOAT_SPEED;
    const floatingElements = document.querySelectorAll('.float-animation');
    
    floatingElements.forEach((element, index) => {
        const offset = index * 0.5;
        const y = Math.sin(time + offset) * CONFIG.FLOAT_AMPLITUDE;
        element.style.transform = `translateY(${y}px)`;
    });
}

// CLEANUP ======================================

function cleanup() {
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
    }
    
    if (imageSwiper) {
        imageSwiper.destroy(true, true);
    }
    
    if (testimonialsSwiper) {
        testimonialsSwiper.destroy(true, true);
    }
}

// INITIALIZATION ======================================

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(initializeHomePage, 100);
    });
} else {
    setTimeout(initializeHomePage, 100);
}

// Cleanup on page unload
window.addEventListener('beforeunload', cleanup);

// Export for debugging
window.HomePage = {
    initializeHomePage,
    initializeImageSlider,
    initializeTestimonialsSlider,
    toggleTheme,
    toggleMobileMenu,
    cleanup
};

console.log('Modern home.js loaded successfully');