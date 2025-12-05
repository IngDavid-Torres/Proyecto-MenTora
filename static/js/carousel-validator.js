/**
 * Carousel Size Validator
 * Continuously monitors and enforces proper carousel dimensions
 */

(function() {
    'use strict';

    const CarouselValidator = {
        
        validate() {
            const carousel = document.querySelector('.preview-carousel');
            const track = document.getElementById('previewTrack');
            const slides = document.querySelectorAll('.preview-slide');
            
            if (!carousel || !track || slides.length === 0) {
                return;
            }
            
            // Check and fix carousel height
            const carouselRect = carousel.getBoundingClientRect();
            if (carouselRect.height < 400 || carouselRect.height > 600) {
                carousel.style.setProperty('height', '500px', 'important');
                carousel.style.setProperty('min-height', '500px', 'important');
            }
            
            // Check and fix track height
            const trackRect = track.getBoundingClientRect();
            if (trackRect.height < 400 || trackRect.height > 600) {
                track.style.setProperty('height', '500px', 'important');
                track.style.setProperty('min-height', '500px', 'important');
            }
            
            // Check and fix each slide
            slides.forEach((slide, index) => {
                const slideRect = slide.getBoundingClientRect();
                if (slideRect.height < 400 || slideRect.height > 600) {
                    slide.style.setProperty('height', '500px', 'important');
                    slide.style.setProperty('min-height', '500px', 'important');
                }
                
                // Check image inside slide
                const img = slide.querySelector('img');
                if (img) {
                    const imgRect = img.getBoundingClientRect();
                    if (imgRect.height < 400 || imgRect.height > 600) {
                        img.style.setProperty('height', '500px', 'important');
                        img.style.setProperty('min-height', '500px', 'important');
                    }
                }
            });
        },
        
        init() {
            // Validate immediately
            this.validate();
            
            // Validate every 500ms
            setInterval(() => this.validate(), 500);
            
            // Validate on any scroll
            window.addEventListener('scroll', () => this.validate(), { passive: true });
            
            // Validate on any resize
            window.addEventListener('resize', () => this.validate(), { passive: true });
            
            // Validate on any click
            document.addEventListener('click', () => {
                setTimeout(() => this.validate(), 50);
            }, { passive: true });
        }
    };
    
    // Initialize validator
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => CarouselValidator.init(), 200);
        });
    } else {
        setTimeout(() => CarouselValidator.init(), 200);
    }
})();
