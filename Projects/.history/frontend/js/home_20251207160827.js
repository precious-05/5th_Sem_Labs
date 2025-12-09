// ============================================
// HOME.JS - Home Page JavaScript for ThyroScan AI
// ============================================

// Global variable for swiper instance
let imageSwiper = null;
let testimonialsSwiper = null;

// Initialize Home Page
function initializeHomePage() {
    console.log('🏠 Home page initialized');
    
    // Fix image display issue first
    fixImageDisplayIssue();
    
    // Initialize Swiper sliders after a delay
    setTimeout(() => {
        initializeImageSlider();
        initializeTestimonialsSlider();
    }, 500);
    
    // Setup event listeners
    setupHomeEventListeners();
    
    // Additional fixes
    applyImageDisplayFixes();
}

// FIX IMAGE DISPLAY ISSUE - MOST IMPORTANT
function fixImageDisplayIssue() {
    console.log('🔧 Applying image display fixes...');
    
    // 1. Add CSS to force image display
    const fixCSS = `
        /* FORCE ALL IMAGES TO DISPLAY */
        .swiper-slide,
        .swiper-slide-active,
        .swiper-slide-prev,
        .swiper-slide-next {
            display: block !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        
        .swiper-slide img,
        .swiper-slide-active img,
        .swiper-slide-prev img,
        .swiper-slide-next img {
            display: block !important;
            opacity: 1 !important;
            visibility: visible !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            object-fit: cover !important;
        }
        
        /* Remove any transitions that might hide images */
        .swiper-slide {
            transition: none !important;
        }
        
        .swiper-slide img {
            transition: none !important;
        }
        
        /* Ensure swiper container shows everything */
        .swiper-wrapper {
            display: flex !important;
            position: relative !important;
        }
        
        /* Black background for better visibility */
        .image-slider-container {
            background: #000 !important;
        }
    `;
    
    const style = document.createElement('style');
    style.id = 'image-fix-css';
    style.textContent = fixCSS;
    document.head.appendChild(style);
    
    // 2. Force display all slider images
    setTimeout(() => {
        const sliderImages = document.querySelectorAll('.image-slider img');
        console.log(`Found ${sliderImages.length} slider images`);
        
        sliderImages.forEach((img, index) => {
            img.style.display = 'block';
            img.style.opacity = '1';
            img.style.visibility = 'visible';
            img.style.position = 'absolute';
            img.style.top = '0';
            img.style.left = '0';
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.objectFit = 'cover';
            img.style.zIndex = '1';
            
            console.log(`Fixed image ${index + 1}: ${img.src.substring(0, 50)}...`);
        });
        
        // 3. Force display all slides
        const slides = document.querySelectorAll('.swiper-slide');
        slides.forEach((slide, index) => {
            slide.style.display = 'block';
            slide.style.opacity = '1';
            slide.style.visibility = 'visible';
            slide.style.position = 'relative';
        });
    }, 100);
}

// Apply additional image display fixes
function applyImageDisplayFixes() {
    // Periodically check and fix images
    setInterval(() => {
        const images = document.querySelectorAll('.image-slider img');
        images.forEach(img => {
            if (img.style.opacity !== '1' || img.style.display !== 'block') {
                img.style.display = 'block';
                img.style.opacity = '1';
                img.style.visibility = 'visible';
            }
        });
    }, 1000);
}

// Initialize Image Slider - SIMPLE AND WORKING
function initializeImageSlider() {
    const imageSlider = document.querySelector('.image-slider');
    
    if (!imageSlider) {
        console.error('❌ Image slider not found');
        return;
    }
    
    console.log('🔄 Initializing image slider...');
    
    // Destroy existing swiper if any
    if (imageSwiper && typeof imageSwiper.destroy === 'function') {
        imageSwiper.destroy(true, true);
    }
    
    // Create new swiper with SIMPLE settings
    imageSwiper = new Swiper('.image-slider', {
        // Basic settings
        direction: 'horizontal',
        loop: true,
        speed: 800,
        
        // NO autoplay initially - we'll add it later
        autoplay: false,
        
        // Pagination
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
            dynamicBullets: false, // Simple bullets
        },
        
        // Navigation
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        
        // SIMPLE slide effect (no fade)
        effect: 'slide',
        
        // No fancy transitions
        fadeEffect: {
            crossFade: false
        },
        
        // Responsive
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
                console.log('✅ Image slider initialized successfully');
                
                // Force display all images after init
                setTimeout(() => {
                    const images = this.slides.map(slide => slide.querySelector('img'));
                    images.forEach(img => {
                        if (img) {
                            img.style.display = 'block';
                            img.style.opacity = '1';
                            img.style.visibility = 'visible';
                        }
                    });
                }, 100);
                
                // Start autoplay after ensuring images are visible
                setTimeout(() => {
                    this.autoplay.start();
                    console.log('▶️ Autoplay started');
                }, 1000);
            },
            
            slideChange: function() {
                // Ensure current slide image is visible
                const activeSlide = this.slides[this.activeIndex];
                const activeImg = activeSlide.querySelector('img');
                if (activeImg) {
                    activeImg.style.display = 'block';
                    activeImg.style.opacity = '1';
                    activeImg.style.visibility = 'visible';
                }
            }
        }
    });
    
    // Add autoplay after swiper is ready
    setTimeout(() => {
        if (imageSwiper && imageSwiper.autoplay) {
            imageSwiper.params.autoplay = {
                delay: 4000,
                disableOnInteraction: false,
                pauseOnMouseEnter: true
            };
            imageSwiper.autoplay.init();
            imageSwiper.autoplay.start();
        }
    }, 1500);
    
    return imageSwiper;
}

// Initialize Testimonials Slider
function initializeTestimonialsSlider() {
    const testimonialsSlider = document.querySelector('.testimonials-swiper');
    
    if (!testimonialsSlider) {
        console.error('❌ Testimonials slider not found');
        return;
    }
    
    console.log('🔄 Initializing testimonials slider...');
    
    // Destroy existing swiper if any
    if (testimonialsSwiper && typeof testimonialsSwiper.destroy === 'function') {
        testimonialsSwiper.destroy(true, true);
    }
    
    testimonialsSwiper = new Swiper('.testimonials-swiper', {
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
    
    return testimonialsSwiper;
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

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 Home page DOM loaded');
    
    // Initialize with delay to ensure everything is ready
    setTimeout(() => {
        if (typeof initializeHomePage === 'function') {
            initializeHomePage();
        }
    }, 100);
});

// Also initialize when page is fully loaded
window.addEventListener('load', function() {
    console.log('🖼️ Page fully loaded with images');
    
    // One more fix after all images are loaded
    setTimeout(() => {
        const allImages = document.querySelectorAll('img');
        allImages.forEach(img => {
            if (img.complete && img.naturalHeight !== 0) {
                img.style.display = 'block';
                img.style.opacity = '1';
            }
        });
    }, 500);
});

// Export for debugging
window.HomePage = {
    initializeHomePage,
    initializeImageSlider,
    fixImageDisplayIssue
};

console.log('🏠 home.js loaded successfully');