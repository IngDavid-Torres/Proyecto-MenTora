document.addEventListener('DOMContentLoaded', function () {
    const reveals = document.querySelectorAll('.reveal');

    // Deshabilitar animaciones en mobile o dispositivos bajos en memoria
    const isMobile = window.matchMedia('(max-width: 768px)').matches;
    const lowMemory = navigator.deviceMemory && navigator.deviceMemory < 4;
    
    if (isMobile || lowMemory) {
        reveals.forEach(el => el.classList.add('is-revealed'));
        return;
    }

    if (!('IntersectionObserver' in window)) {
        reveals.forEach(el => el.classList.add('is-revealed'));
        return;
    }

    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -5% 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.classList.add('is-revealed');
                
                const stagger = el.getAttribute('data-stagger');
                if (stagger !== null) {
                    const children = Array.from(el.children);
                    children.forEach((child, i) => {
                        const delay = Math.min(400, i * (parseInt(stagger || '40', 10)));
                        setTimeout(() => {
                            child.classList.add('is-revealed');
                        }, delay);
                    });
                }
                
                obs.unobserve(el);
            }
        });
    }, observerOptions);

    reveals.forEach(el => observer.observe(el));
});
