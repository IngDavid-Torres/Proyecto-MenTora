// Lazy loading de imágenes con Intersection Observer
document.addEventListener('DOMContentLoaded', function() {
    // Detectar soporte para lazy loading nativo
    if ('loading' in HTMLImageElement.prototype) {
        // El navegador soporta loading="lazy" nativo
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        // No necesitamos hacer nada, el navegador lo maneja
        return;
    }

    // Fallback: Usar Intersection Observer
    if (!('IntersectionObserver' in window)) {
        // Cargar todas las imágenes si IntersectionObserver no está disponible
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
        return;
    }

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                
                // Cargar imagen
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                
                // Cargar srcset si existe
                if (img.dataset.srcset) {
                    img.srcset = img.dataset.srcset;
                    img.removeAttribute('data-srcset');
                }
                
                // Agregar clase de cargada
                img.classList.add('lazy-loaded');
                observer.unobserve(img);
            }
        });
    }, {
        rootMargin: '50px',
        threshold: 0.01
    });

    // Observar todas las imágenes lazy
    document.querySelectorAll('img[data-src], img[loading="lazy"]').forEach(img => {
        imageObserver.observe(img);
    });
});

// Lazy loading de iframes (embeds, videos)
document.addEventListener('DOMContentLoaded', function() {
    if (!('IntersectionObserver' in window)) return;

    const iframeObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const iframe = entry.target;
                
                if (iframe.dataset.src) {
                    iframe.src = iframe.dataset.src;
                    iframe.removeAttribute('data-src');
                }
                
                observer.unobserve(iframe);
            }
        });
    }, {
        rootMargin: '100px'
    });

    document.querySelectorAll('iframe[data-src]').forEach(iframe => {
        iframeObserver.observe(iframe);
    });
});
