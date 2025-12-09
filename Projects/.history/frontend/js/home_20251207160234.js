// ============================================
// HOME.JS - Home Page JavaScript for ThyroScan AI
// ============================================

// Initialize Home Page
function initializeHomePage() {
    console.log('🏠 Home page initialized');
    
    // Initialize Swiper sliders
    initializeImageSlider();
    initializeTestimonialsSlider();
    
    // Setup event listeners
    setupHomeEventListeners();
}

// Initialize Image Slider - SIMPLIFIED VERSION
function initializeImageSlider() {
    const imageSlider = document.querySelector('.image-slider');
    
    if (imageSlider) {
        const swiper = new Swiper('.image-slider', {
            // Basic settings
            direction: 'horizontal',
            loop: true,
            speed: 800,
            
            // Autoplay - SIMPLE
            autoplay: {
                delay: 4000,
                disableOnInteraction: false,
            },
            
            // Pagination
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            
            // Navigation
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            
            // Simple slide effect
            effect: 'slide',
            
            // On initialization
            on: {
                init: function() {
                    console.log('✅ Image slider initialized');
                    // Force display all images
                    const images = document.querySelectorAll('.swiper-slide img');
                    images.forEach(img => {
                        img.style.display = 'block';
                        img.style.opacity = '1';
                    });
                }
            }
        });
        
        return swiper;
    }
}

// Initialize Testimonials Slider
function initializeTestimonialsSlider() {
    const testimonialsSlider = document.querySelector('.testimonials-swiper');
    
    if (testimonialsSlider) {
        const swiper = new Swiper('.testimonials-swiper', {
            direction: 'horizontal',
            loop: true,
            speed: 600,
            autoplay: {
                delay: 6000,
                disableOnInteraction: false,
            },
            
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            
            centeredSlides: true,
            slidesPerView: 'auto',
            spaceBetween: 30,
            
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
                    console.log('✅ Testimonials slider initialized');
                }
            }
        });
        
        return swiper;
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
}

// Initialize home page
document.addEventListener('DOMContentLoaded', () => {
    if (typeof initializeHomePage === 'function') {
        initializeHomePage();
    }
    
    // Force images to display after page load
    setTimeout(() => {
        const sliderImages = document.querySelectorAll('.image-slider img');
        sliderImages.forEach(img => {
            img.style.display = 'block';
            img.style.opacity = '1';
            img.style.visibility = 'visible';
        });
    }, 1000);
});