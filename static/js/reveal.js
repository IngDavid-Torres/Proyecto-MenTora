document.addEventListener('DOMContentLoaded', function () {
    const reveals = document.querySelectorAll('.reveal');

    if (!('IntersectionObserver' in window)) {
        // If no IntersectionObserver support, reveal everything
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
                // If the element has data-stagger attribute, stagger its direct children
                const stagger = el.getAttribute('data-stagger');
                if (stagger !== null) {
                    const children = Array.from(el.children);
                    children.forEach((child, i) => {
                        // mark child for reveal and set incremental delay
                        child.classList.add('reveal-child');
                        const delay = Math.min(800, (i * (parseInt(stagger || '80', 10))));
                        child.style.transitionDelay = `${delay}ms`;
                    });
                }

                // Small requestAnimationFrame to ensure transition applies
                requestAnimationFrame(() => el.classList.add('active'));
                obs.unobserve(el);
            }
        });
    }, observerOptions);

    reveals.forEach(el => observer.observe(el));
});
