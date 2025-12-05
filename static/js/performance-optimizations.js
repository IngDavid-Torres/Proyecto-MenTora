// ========================================
// OPTIMIZACIONES DE RENDIMIENTO GLOBAL
// ========================================

// 1. Debounce para funciones costosas
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

// 2. Throttle para eventos frecuentes
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => {
                inThrottle = false;
            }, limit);
        }
    };
}

// 3. Optimización de scroll - usar passive listeners
document.addEventListener('scroll', function() {
    // El navegador puede optimizar mejor con passive: true
}, { passive: true });

// 4. Preload crítico - precarga de fonts y recursos importantes
function preloadCriticalResources() {
    if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
            // Precargar fuentes después de contenido crítico
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'font';
            link.href = 'https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap';
            link.crossOrigin = 'anonymous';
            document.head.appendChild(link);
        });
    }
}

// 5. Monitorear memoria y performance
function checkPerformance() {
    if ('memory' in performance) {
        const usedMemory = performance.memory.usedJSHeapSize / 1048576;
        const totalMemory = performance.memory.jsHeapSizeLimit / 1048576;
        
        // Si memoria es baja, deshabilitar animaciones
        if (usedMemory > totalMemory * 0.8) {
            document.documentElement.style.setProperty('--transition-fast', '0s');
            document.documentElement.style.setProperty('--transition-normal', '0s');
        }
    }
}

// 6. Medir Core Web Vitals
function measureWebVitals() {
    // LCP - Largest Contentful Paint
    if ('PerformanceObserver' in window) {
        try {
            const lcpObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                console.log('LCP:', lastEntry.renderTime || lastEntry.loadTime);
            });
            lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
        } catch (e) {}

        // FID - First Input Delay
        try {
            const fidObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach((entry) => {
                    console.log('FID:', entry.processingDuration);
                });
            });
            fidObserver.observe({ entryTypes: ['first-input'] });
        } catch (e) {}
    }
}

// 7. Limpiar event listeners cuando no se necesiten
function setupEventListenerCleanup() {
    const observers = [];
    
    window.addEventListener('beforeunload', () => {
        observers.forEach(observer => {
            if (observer.disconnect) observer.disconnect();
        });
    });
    
    return observers;
}

// 8. Optimizar re-flows con batching
function batchDOMUpdates(updates) {
    requestAnimationFrame(() => {
        updates.forEach(update => update());
    });
}

// 9. Cache DOM queries
const domCache = new Map();

function getCachedElement(selector) {
    if (!domCache.has(selector)) {
        domCache.set(selector, document.querySelector(selector));
    }
    return domCache.get(selector);
}

// 10. Network info API - reducir calidad en conexiones lentas
function optimizeForSlowNetwork() {
    if ('connection' in navigator) {
        const conn = navigator.connection;
        const effectiveType = conn.effectiveType;
        
        if (effectiveType === '4g') {
            // Calidad alta
        } else if (effectiveType === '3g') {
            // Calidad media - reducir transiciones
            document.documentElement.style.setProperty('--transition-fast', '0.05s');
            document.documentElement.style.setProperty('--transition-normal', '0.1s');
        } else if (effectiveType === '2g' || effectiveType === 'slow-2g') {
            // Calidad baja - sin animaciones
            document.documentElement.style.setProperty('--transition-fast', '0s');
            document.documentElement.style.setProperty('--transition-normal', '0s');
        }
    }
}

// Ejecutar optimizaciones
document.addEventListener('DOMContentLoaded', function() {
    preloadCriticalResources();
    checkPerformance();
    measureWebVitals();
    optimizeForSlowNetwork();
    
    // Revisar performance periódicamente
    setInterval(checkPerformance, 5000);
}, { passive: true });

// Exportar funciones
window.PerformanceOptimizations = {
    debounce,
    throttle,
    batchDOMUpdates,
    getCachedElement,
    setupEventListenerCleanup
};
