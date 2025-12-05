/**
 * Performance Optimization Script
 * Mejora el rendimiento de la página disminuyendo jank y optimizando animaciones
 */

// 1. Desabilitar smooth scroll si es mobile
if (window.matchMedia('(max-width: 768px)').matches) {
    document.documentElement.style.scrollBehavior = 'auto';
}

// 2. Lazy Loading de imágenes
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    img.classList.remove('lazy-load');
                }
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: '50px'
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// 3. Throttle scroll events para mejor rendimiento
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 4. Detect high-end devices y deshabilitar animaciones en dispositivos bajos
function canAnimatePerformantly() {
    // Chequear si el dispositivo tiene buena memoria y CPU
    if ('deviceMemory' in navigator) {
        return navigator.deviceMemory >= 4;
    }
    // Fallback: check si es mobile
    return !window.matchMedia('(max-width: 768px)').matches;
}

// 5. Reducir animaciones en dispositivos bajos
if (!canAnimatePerformantly()) {
    const style = document.createElement('style');
    style.textContent = `
        * {
            animation-duration: 0.01ms !important;
            transition-duration: 0.01ms !important;
        }
        .reveal { transition: none !important; opacity: 1 !important; transform: none !important; }
    `;
    document.head.appendChild(style);
}

// 6. Utilizar requestAnimationFrame para scroll events
let ticking = false;
const scrollListeners = [];

function addScrollListener(callback) {
    scrollListeners.push(callback);
}

function onScroll() {
    if (!ticking) {
        requestAnimationFrame(() => {
            scrollListeners.forEach(callback => callback());
            ticking = false;
        });
        ticking = true;
    }
}

window.addEventListener('scroll', onScroll, { passive: true });

// 7. Preload fonts de forma asincrónica
if ('fonts' in document) {
    Promise.all([
        document.fonts.load('400 1em Poppins'),
        document.fonts.load('700 1em Poppins'),
        document.fonts.load('700 1em Exo 2')
    ]).catch(() => console.log('Fonts preload completed'));
}

// 8. Defer no-essential CSS
function deferNonCritical() {
    const links = document.querySelectorAll('link[rel="stylesheet"]');
    links.forEach(link => {
        if (link.getAttribute('data-defer') === 'true') {
            const newLink = document.createElement('link');
            newLink.rel = 'stylesheet';
            newLink.href = link.href;
            document.body.appendChild(newLink);
            link.parentNode.removeChild(link);
        }
    });
}

// Ejecutar después de que la página esté lista
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', deferNonCritical);
} else {
    deferNonCritical();
}

// 9. Usar CSS containment para mejorar performance
const style = document.createElement('style');
style.textContent = `
    .card, .feature, .testimonial, .prof-card, .stat-card {
        contain: layout style paint;
    }
`;
document.head.appendChild(style);

// 10. Monitorear performance
if ('PerformanceObserver' in window) {
    try {
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.duration > 50) {
                    console.warn(`Performance: ${entry.name} took ${entry.duration}ms`);
                }
            }
        });
        observer.observe({ entryTypes: ['measure', 'navigation'] });
    } catch (e) {
        // Performance observer no soportado
    }
}

console.log('✓ Performance optimizations loaded');
