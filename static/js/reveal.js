document.addEventListener('DOMContentLoaded', function () {
    const reveals = document.querySelectorAll('.reveal');

    if (!('IntersectionObserver' in window)) {
        reveals.forEach(el => el.classList.add('active'));
        return;
    }

    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -8% 0px',
        threshold: 0.12
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const stagger = el.getAttribute('data-stagger');
                if (stagger !== null) {
                    const children = Array.from(el.children);
                    children.forEach((child, i) => {
                        child.classList.add('reveal-child');
                        const delay = Math.min(800, (i * (parseInt(stagger || '80', 10))));
                        child.style.transitionDelay = `${delay}ms`;
                    });
                }
                
                requestAnimationFrame(() => el.classList.add('active'));
                obs.unobserve(el);
            }
        });
    }, observerOptions);

    reveals.forEach(el => observer.observe(el));
});
