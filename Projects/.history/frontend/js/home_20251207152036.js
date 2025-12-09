// ============================================
// HOME.JS - Home Page JavaScript for ThyroScan AI
// ============================================

// Initialize Home Page
function initializeHomePage() {
    console.log('🏠 Home page initialized');
    
    // Initialize Swiper sliders
    initializeImageSlider();
    initializeTestimonialsSlider();
    
    // Initialize counters
    initializeCounters();
    
    // Initialize floating elements
    initializeFloatingElements();
    
    // Initialize scroll animations
    initializeHomeAnimations();
    
    // Setup event listeners
    setupHomeEventListeners();
    
    // Initialize interactive elements
    initializeInteractiveElements();
}

// Initialize Image Slider
function initializeImageSlider() {
    const imageSlider = document.querySelector('.image-slider');
    
    if (imageSlider) {
        const swiper = new Swiper('.image-slider', {
            // Optional parameters
            direction: 'horizontal',
            loop: true,
            speed: 800,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            
            // Pagination
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                dynamicBullets: true,
            },
            
            // Navigation arrows
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            
            // Fade effect
            effect: 'fade',
            fadeEffect: {
                crossFade: true
            },
            
            // Parallax effect
            parallax: true,
            
            // Responsive breakpoints
            breakpoints: {
                320: {
                    slidesPerView: 1,
                    spaceBetween: 10
                },
                768: {
                    slidesPerView: 1,
                    spaceBetween: 20
                },
                1024: {
                    slidesPerView: 1,
                    spaceBetween: 30
                }
            },
            
            // Callbacks
            on: {
                init: function() {
                    console.log('🖼️ Image slider initialized');
                },
                slideChange: function() {
                    // Add active class to current slide
                    const slides = document.querySelectorAll('.swiper-slide');
                    slides.forEach(slide => slide.classList.remove('active'));
                    this.slides[this.activeIndex].classList.add('active');
                }
            }
        });
        
        // Pause autoplay on hover
        imageSlider.addEventListener('mouseenter', () => {
            swiper.autoplay.stop();
        });
        
        imageSlider.addEventListener('mouseleave', () => {
            swiper.autoplay.start();
        });
        
        return swiper;
    }
}

// Initialize Testimonials Slider
function initializeTestimonialsSlider() {
    const testimonialsSlider = document.querySelector('.testimonials-swiper');
    
    if (testimonialsSlider) {
        const swiper = new Swiper('.testimonials-swiper', {
            // Optional parameters
            direction: 'horizontal',
            loop: true,
            speed: 600,
            autoplay: {
                delay: 7000,
                disableOnInteraction: false,
            },
            
            // Pagination
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
                dynamicBullets: true,
            },
            
            // Centered slides
            centeredSlides: true,
            slidesPerView: 'auto',
            spaceBetween: 30,
            
            // Responsive breakpoints
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
            
            // Callbacks
            on: {
                init: function() {
                    console.log('💬 Testimonials slider initialized');
                }
            }
        });
        
        return swiper;
    }
}

// Initialize Animated Counters
function initializeCounters() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = +counter.getAttribute('data-target');
        const increment = target / 100;
        let current = 0;
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.ceil(current);
                setTimeout(updateCounter, 20);
            } else {
                counter.textContent = target;
            }
        };
        
        // Start counter when in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(counter);
                }
            });
        });
        
        observer.observe(counter);
    });
}

// Initialize Floating Elements
function initializeFloatingElements() {
    const floatingCards = document.querySelectorAll('.floating-card');
    
    floatingCards.forEach((card, index) => {
        // Add delay based on index
        card.style.animationDelay = `${index * 0.2}s`;
        
        // Add hover effect
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px) scale(1.05)';
            card.style.boxShadow = '0 20px 40px rgba(45, 91, 255, 0.2)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
            card.style.boxShadow = '';
        });
    });
}

// Initialize Home Animations
function initializeHomeAnimations() {
    // Add animation classes to elements
    const elementsToAnimate = [
        '.hero-text',
        '.hero-visual',
        '.feature-card',
        '.step-card',
        '.testimonial-card'
    ];
    
    elementsToAnimate.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        elements.forEach((element, index) => {
            element.classList.add('animate-on-scroll');
            element.style.animationDelay = `${index * 0.1}s`;
        });
    });
    
    // Initialize scroll indicator
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            const featuresSection = document.querySelector('#features');
            if (featuresSection) {
                window.scrollTo({
                    top: featuresSection.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    }
}

// Setup Home Event Listeners
function setupHomeEventListeners() {
    // CTA button effects
    const ctaButtons = document.querySelectorAll('.btn-primary');
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
    
    // Feature card interactions
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            const icon = card.querySelector('.feature-icon');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            const icon = card.querySelector('.feature-icon');
            if (icon) {
                icon.style.transform = '';
            }
        });
    });
    
    // Step card interactions
    const stepCards = document.querySelectorAll('.step-card');
    stepCards.forEach((card, index) => {
        card.addEventListener('mouseenter', () => {
            const arrow = card.querySelector('.step-arrow');
            if (arrow && index < 2) { // Don't animate last arrow
                arrow.style.transform = 'translateY(-50%) translateX(5px)';
                arrow.style.color = '#2D5BFF';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            const arrow = card.querySelector('.step-arrow');
            if (arrow && index < 2) {
                arrow.style.transform = 'translateY(-50%)';
                arrow.style.color = '';
            }
        });
    });
}

// Initialize Interactive Elements
function initializeInteractiveElements() {
    // Trust badges hover effect
    const trustItems = document.querySelectorAll('.trust-item');
    trustItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            const icon = item.querySelector('i');
            icon.style.transform = 'scale(1.2)';
            icon.style.color = '#2D5BFF';
        });
        
        item.addEventListener('mouseleave', () => {
            const icon = item.querySelector('i');
            icon.style.transform = '';
            icon.style.color = '';
        });
    });
    
    // Tag badges click effect
    const tagBadges = document.querySelectorAll('.tag-badge');
    tagBadges.forEach(badge => {
        badge.addEventListener('click', () => {
            badge.style.transform = 'scale(0.95)';
            setTimeout(() => {
                badge.style.transform = '';
            }, 200);
        });
    });
    
    // Stats floating card interaction
    const statsCard = document.querySelector('.stats-floating-card');
    if (statsCard) {
        statsCard.addEventListener('mouseenter', () => {
            statsCard.style.transform = 'translateX(-50%) translateY(-5px)';
        });
        
        statsCard.addEventListener('mouseleave', () => {
            statsCard.style.transform = 'translateX(-50%)';
        });
    }
}

// Initialize Image Lazy Loading
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.classList.add('loaded');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize Parallax Effect
function initializeParallax() {
    const heroSection = document.querySelector('.hero');
    if (!heroSection) return;
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        const shapes = document.querySelectorAll('.shape');
        shapes.forEach((shape, index) => {
            const speed = 0.3 + (index * 0.1);
            shape.style.transform = `translateY(${rate * speed}px)`;
        });
    });
}

// Initialize Typewriter Effect (Optional)
function initializeTypewriter() {
    const typewriterElement = document.querySelector('.typewriter-text');
    if (!typewriterElement) return;
    
    const texts = [
        'Thyroid Disease Prediction',
        'AI-Powered Diagnosis',
        'Medical Grade Accuracy',
        'Instant Risk Assessment'
    ];
    
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    
    function typeWriter() {
        const currentText = texts[textIndex];
        
        if (isDeleting) {
            typewriterElement.textContent = currentText.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typewriterElement.textContent = currentText.substring(0, charIndex + 1);
            charIndex++;
        }
        
        if (!isDeleting && charIndex === currentText.length) {
            // Pause at end of typing
            isDeleting = true;
            setTimeout(typeWriter, 2000);
        } else if (isDeleting && charIndex === 0) {
            // Move to next text
            isDeleting = false;
            textIndex = (textIndex + 1) % texts.length;
            setTimeout(typeWriter, 500);
        } else {
            // Continue typing/deleting
            const speed = isDeleting ? 50 : 100;
            setTimeout(typeWriter, speed);
        }
    }
    
    // Start typewriter effect
    setTimeout(typeWriter, 1000);
}

// Initialize Page Load Animation
function initializePageLoadAnimation() {
    // Add loading animation
    document.body.classList.add('page-loading');
    
    // Remove loading class after page load
    window.addEventListener('load', () => {
        setTimeout(() => {
            document.body.classList.remove('page-loading');
            document.body.classList.add('page-loaded');
        }, 500);
    });
    
    // Add loading styles
    const style = document.createElement('style');
    style.textContent = `
        .page-loading {
            opacity: 0;
        }
        .page-loaded {
            animation: pageFadeIn 0.5s ease;
        }
        @keyframes pageFadeIn {
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

// Initialize Stats Counter with Real Data
async function initializeRealStats() {
    try {
        const response = await fetch(`${window.API_BASE_URL || 'http://localhost:8000'}/stats`);
        if (response.ok) {
            const data = await response.json();
            
            // Update stats on page
            const totalPredictions = document.querySelector('#totalPredictions');
            const accuracyRate = document.querySelector('#accuracyRate');
            const avgResponseTime = document.querySelector('#avgResponseTime');
            
            if (totalPredictions && data.total_predictions) {
                animateCounter(totalPredictions, data.total_predictions);
            }
            
            if (accuracyRate && data.accuracy) {
                accuracyRate.textContent = `${data.accuracy}%`;
            }
            
            if (avgResponseTime && data.avg_response_time) {
                avgResponseTime.textContent = `${data.avg_response_time}ms`;
            }
        }
    } catch (error) {
        console.log('Using default stats - API not available');
    }
}

// Animate Counter
function animateCounter(element, target) {
    const duration = 2000; // 2 seconds
    const step = target / (duration / 16); // 60fps
    let current = 0;
    
    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

// Initialize all home page features
document.addEventListener('DOMContentLoaded', () => {
    if (typeof initializeHomePage === 'function') {
        initializeHomePage();
    }
    
    // Initialize additional features
    initializeLazyLoading();
    initializeParallax();
    initializePageLoadAnimation();
    
    // Initialize real stats after a delay
    setTimeout(initializeRealStats, 1000);
});

// Export functions for debugging
window.HomePage = {
    initializeHomePage,
    initializeImageSlider,
    initializeTestimonialsSlider,
    initializeCounters,
    initializeFloatingElements
};