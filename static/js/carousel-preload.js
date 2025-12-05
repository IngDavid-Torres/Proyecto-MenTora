/**
 * Carousel Image Preloader - Aggressive Version
 * Ensures carousel maintains consistent size during transitions
 */

(function() {
    'use strict';

    const CarouselPreloader = {
        images: [],
        
        init() {
            // Get carousel container
            const carousel = document.querySelector('.preview-carousel');
            const track = document.getElementById('previewTrack');
            
            if (!carousel || !track) return;
            
            // Force container size immediately
            this.enforceContainerSize(carousel);
            
            // Get all preview carousel images
            const slides = document.querySelectorAll('.preview-slide img');
            if (slides.length === 0) return;
            
            this.images = Array.from(slides);
            
            // Pre-load and enforce size on all images
            this.images.forEach((img, index) => {
                this.enforceImageSize(img);
                this.preloadImage(img, index);
            });
            
            // Enforce size on window resize
            window.addEventListener('resize', () => {
                this.enforceContainerSize(carousel);
                this.images.forEach(img => this.enforceImageSize(img));
            }, { passive: true });
            
            // Observer for mutations
            this.observeMutations(carousel);
        },
        
        enforceContainerSize(carousel) {
            carousel.style.height = '500px';
            carousel.style.minHeight = '500px';
            carousel.style.maxHeight = '500px';
            
            const track = carousel.querySelector('.preview-track');
            if (track) {
                track.style.height = '500px';
                track.style.minHeight = '500px';
            }
        },
        
        enforceImageSize(img) {
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.minWidth = '100%';
            img.style.minHeight = '100%';
            img.style.objectFit = 'cover';
            img.style.objectPosition = 'center';
            img.style.margin = '0';
            img.style.padding = '0';
            img.style.border = 'none';
            img.style.display = 'block';
        },
        
        preloadImage(img, index) {
            const src = img.src;
            if (!src) return;
            
            // Create preload image
            const preloadImg = new Image();
            
            preloadImg.onload = () => {
                this.enforceImageSize(img);
                img.style.opacity = '1';
            };
            
            preloadImg.onerror = () => {
                console.warn('Failed to load image:', src);
                this.enforceImageSize(img);
            };
            
            preloadImg.src = src;
        },
        
        observeMutations(carousel) {
            // Monitor for any DOM changes that might affect size
            const observer = new MutationObserver((mutations) => {
                // Re-enforce sizes on any DOM change
                const track = carousel.querySelector('.preview-track');
                if (track) {
                    track.style.height = '500px';
                }
                
                this.images.forEach(img => {
                    if (img.offsetHeight !== 500) {
                        this.enforceImageSize(img);
                    }
                });
            });
            
            observer.observe(carousel, {
                attributes: true,
                attributeFilter: ['style', 'class'],
                subtree: true,
                childList: false
            });
        }
    };
    
    // Initialize immediately
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => CarouselPreloader.init(), 100);
        });
    } else {
        setTimeout(() => CarouselPreloader.init(), 100);
    }
    
    // Re-init on window load
    window.addEventListener('load', () => {
        setTimeout(() => CarouselPreloader.init(), 200);
    });
})();
