// Visitor tracking and click events
function trackClick(elementType) {
    // إرسال بيانات النقرة إلى الخادم
    fetch('/track-click/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            'element_clicked': elementType,
            'page_url': window.location.pathname,
            'timestamp': new Date().toISOString()
        })
    }).catch(error => {
        console.log('Click tracking error:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// تتبع مدة البقاء في الصفحة
let pageStartTime = Date.now();
let isPageVisible = true;

document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        isPageVisible = false;
        // حفظ مدة البقاء عند إخفاء الصفحة
        const timeSpent = Math.floor((Date.now() - pageStartTime) / 1000);
        updateSessionDuration(timeSpent);
    } else {
        isPageVisible = true;
        pageStartTime = Date.now();
    }
});

window.addEventListener('beforeunload', function() {
    if (isPageVisible) {
        const timeSpent = Math.floor((Date.now() - pageStartTime) / 1000);
        updateSessionDuration(timeSpent);
    }
});

function updateSessionDuration(duration) {
    if (duration > 5) { // فقط إذا كان الوقت أكثر من 5 ثواني
        fetch('/update-session/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                'session_duration': duration
            })
        }).catch(error => {
            console.log('Session tracking error:', error);
        });
    }
}

// Smooth scroll and navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    // Navigation functionality
    const navbar = document.querySelector('.navbar');
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Mobile menu toggle
    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    });
    
    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                
                // Add staggered animation for service cards
                if (entry.target.classList.contains('service-card')) {
                    const delay = entry.target.dataset.delay || 0;
                    setTimeout(() => {
                        entry.target.style.transform = 'translateY(0)';
                        entry.target.style.opacity = '1';
                    }, delay);
                }
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    animateElements.forEach(el => observer.observe(el));
    
    // Parallax effect for hero background
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.hero-background');
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
    
    // Dynamic typing effect for hero title
    function typeWriter(element, text, speed = 100) {
        let i = 0;
        element.innerHTML = '';
        
        function type() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        // Start typing after a delay
        setTimeout(type, 1000);
    }
    
    // Initialize typing effect
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const originalText = heroTitle.textContent;
        typeWriter(heroTitle, originalText, 80);
    }
    
    // Floating animation for service icons
    function addFloatingAnimation() {
        const serviceIcons = document.querySelectorAll('.service-icon');
        
        serviceIcons.forEach((icon, index) => {
            const delay = index * 0.5;
            icon.style.animationDelay = `${delay}s`;
            icon.classList.add('floating');
        });
    }
    
    // Add floating animation after page load
    setTimeout(addFloatingAnimation, 2000);
    
    // Particle system for background
    function createParticles() {
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'particles-container';
        particlesContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        `;
        
        document.body.appendChild(particlesContainer);
        
        function createParticle() {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            const size = Math.random() * 4 + 1;
            const startX = Math.random() * window.innerWidth;
            const duration = Math.random() * 20000 + 10000;
            
            particle.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                background: rgba(255, 215, 0, ${Math.random() * 0.3 + 0.1});
                border-radius: 50%;
                left: ${startX}px;
                top: 100vh;
                animation: floatUp ${duration}ms linear infinite;
            `;
            
            particlesContainer.appendChild(particle);
            
            // Remove particle after animation
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, duration);
        }
        
        // Create particles periodically
        setInterval(createParticle, 2000);
    }
    
    // Add particle animation CSS
    const particleStyles = document.createElement('style');
    particleStyles.textContent = `
        @keyframes floatUp {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }
        
        .floating {
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-10px);
            }
        }
        
        .service-card:hover .service-icon.floating {
            animation-play-state: paused;
        }
    `;
    document.head.appendChild(particleStyles);
    
    // Initialize particles
    createParticles();
    
    // Button ripple effect
    function createRipple(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s linear;
            pointer-events: none;
        `;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
    
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.cta-button, .cta-button-large');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });
    
    // Add ripple animation CSS
    const rippleStyles = document.createElement('style');
    rippleStyles.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyles);
    
    // Scroll progress indicator
    function createScrollProgress() {
        const progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 3px;
            background: linear-gradient(90deg, #ffd700, #ffed4e);
            z-index: 9999;
            transition: width 0.25s ease;
        `;
        
        document.body.appendChild(progressBar);
        
        window.addEventListener('scroll', () => {
            const scrollTop = window.pageYOffset;
            const docHeight = document.body.scrollHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            
            progressBar.style.width = scrollPercent + '%';
        });
    }
    
    createScrollProgress();
    
    // Magnetic effect for buttons
    function addMagneticEffect() {
        const magneticElements = document.querySelectorAll('.cta-button, .cta-button-large, .social-link');
        
        magneticElements.forEach(element => {
            element.addEventListener('mousemove', (e) => {
                const rect = element.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                const moveX = x * 0.1;
                const moveY = y * 0.1;
                
                element.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
            
            element.addEventListener('mouseleave', () => {
                element.style.transform = 'translate(0px, 0px)';
            });
        });
    }
    
    addMagneticEffect();
    
    // Image loading animation
    function animateImageLoad() {
        const images = document.querySelectorAll('img');
        
        images.forEach(img => {
            if (img.complete) {
                img.style.opacity = '1';
            } else {
                img.style.opacity = '0';
                img.style.transition = 'opacity 0.5s ease';
                
                img.addEventListener('load', () => {
                    img.style.opacity = '1';
                });
            }
        });
    }
    
    animateImageLoad();
    
    // Performance optimization - throttle scroll events
    function throttle(func, delay) {
        let timeoutId;
        let lastExecTime = 0;
        
        return function (...args) {
            const currentTime = Date.now();
            
            if (currentTime - lastExecTime > delay) {
                func.apply(this, args);
                lastExecTime = currentTime;
            } else {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    func.apply(this, args);
                    lastExecTime = Date.now();
                }, delay - (currentTime - lastExecTime));
            }
        };
    }
    
    // Apply throttling to scroll events
    const throttledScrollHandler = throttle(() => {
        // Existing scroll logic here
    }, 16); // ~60fps
    
    window.addEventListener('scroll', throttledScrollHandler);
    
    // Preload critical resources
    function preloadResources() {
        const criticalImages = ['../abo.png', '../logo.png'];
        
        criticalImages.forEach(src => {
            const img = new Image();
            img.src = src;
        });
    }
    
    preloadResources();
    
    // Add loading screen
    function showLoadingScreen() {
        const loader = document.createElement('div');
        loader.className = 'page-loader';
        loader.innerHTML = `
            <div class="loader-content">
                <div class="loader-logo">
                    <img src="../logo.png" alt="Loading..." style="height: 80px;">
                </div>
                <div class="loader-spinner"></div>
                <p>جاري التحميل...</p>
            </div>
        `;
        
        loader.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            transition: opacity 0.5s ease, visibility 0.5s ease;
        `;
        
        const loaderStyles = document.createElement('style');
        loaderStyles.textContent = `
            .loader-content {
                text-align: center;
                color: white;
            }
            
            .loader-spinner {
                width: 50px;
                height: 50px;
                border: 3px solid rgba(255, 215, 0, 0.3);
                border-top: 3px solid #ffd700;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        
        document.head.appendChild(loaderStyles);
        document.body.appendChild(loader);
        
        // Hide loader when page is loaded
        window.addEventListener('load', () => {
            setTimeout(() => {
                loader.style.opacity = '0';
                loader.style.visibility = 'hidden';
                setTimeout(() => {
                    if (loader.parentNode) {
                        loader.parentNode.removeChild(loader);
                    }
                }, 500);
            }, 1000);
        });
    }
    
    showLoadingScreen();
});

// Additional utility functions
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

// Smooth reveal animations for elements
function revealOnScroll() {
    const reveals = document.querySelectorAll('.animate-on-scroll');
    
    for (let i = 0; i < reveals.length; i++) {
        const windowHeight = window.innerHeight;
        const elementTop = reveals[i].getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < windowHeight - elementVisible) {
            reveals[i].classList.add('animated');
        }
    }
}

window.addEventListener('scroll', debounce(revealOnScroll, 10));

// Initialize reveal on page load
document.addEventListener('DOMContentLoaded', revealOnScroll);

// تحسين تفاعل القائمة المنسدلة
document.addEventListener('DOMContentLoaded', function() {
    const serviceSelect = document.getElementById('service');
    const selectWrapper = document.querySelector('.select-wrapper');
    
    if (serviceSelect && selectWrapper) {
        // تحسين ظهور النص المحدد
        serviceSelect.addEventListener('change', function() {
            if (this.value !== '') {
                this.style.color = '#ffffff';
                this.style.fontWeight = '500';
                selectWrapper.classList.add('has-value');
            } else {
                this.style.color = '#b8b8b8';
                this.style.fontWeight = '400';
                selectWrapper.classList.remove('has-value');
            }
        });
        
        // تأثير عند فتح القائمة
        serviceSelect.addEventListener('focus', function() {
            selectWrapper.classList.add('focused');
        });
        
        serviceSelect.addEventListener('blur', function() {
            selectWrapper.classList.remove('focused');
        });
        
        // تأثير عند النقر
        serviceSelect.addEventListener('click', function(e) {
            // إضافة تأثير بصري عند النقر
            this.style.transform = 'scale(1.01)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
        
        // إضافة تأثير keyboard navigation
        serviceSelect.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                this.click();
            }
        });
        
        // تأثير تحرك السهم
        const selectArrow = selectWrapper.querySelector('.select-arrow');
        if (selectArrow) {
            serviceSelect.addEventListener('focus', function() {
                selectArrow.style.transform = 'translateY(-50%) rotate(180deg)';
            });
            
            serviceSelect.addEventListener('blur', function() {
                selectArrow.style.transform = 'translateY(-50%) rotate(0deg)';
            });
        }
    }
});