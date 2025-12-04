const CONFIG = {
    PREVIEW_AUTOPLAY_DELAY: 5000,
    TOAST_DURATION: 4500,
    ALERT_DURATION: 2600,
    MODAL_ANIMATION_DELAY: 300,
    LOGIN_REDIRECT_DELAY: 4000,
    REGISTER_REDIRECT_DELAY: 1800
};

const Utils = {
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

const ModalSystem = {
    data: {
        nosotros: {
            title: "Sobre MenTora",
            text: `
                <div style="padding: 10px;">
                    <p>
                        Somos <strong>MenTora</strong>, una plataforma de EdTech innovadora comprometida con la 
                        <strong>transformación del aprendizaje profesional</strong>. Nuestra misión es desatar el
                         potencial de cada usuario a través de una metodología de <strong>aprendizaje basado en retos</strong>
                          (Challenge-Based Learning) altamente gamificada.
                    </p>
                    <p>
                        Nuestra visión es ser la plataforma líder a nivel global en el desarrollo de habilidades críticas del
                         siglo XXI (pensamiento crítico, resolución de problemas complejos, y creatividad), ofreciendo una experiencia
                          inmersiva, social y estratégicamente divertida. Fundada en la premisa de que <strong>aprender haciendo</strong>
                           es el camino más efectivo, nos dedicamos a construir un ecosistema donde la educación y la práctica profesional 
                           convergen.
                    </p>
                </div>
            `
        },
        privacidad: {
            title: "Política de Privacidad (Aviso de Privacidad)",
            text: `
                <div style="padding: 10px;">
                    <h2>Actualización: 17 de Noviembre de 2025</h2>
                <br>
                <h3 style="color:#6A2C3D;">1. Recopilación de Información Personal</h3>
                <p> MenTora (referida en adelante como "la Plataforma") recaba información que usted nos proporciona
                directamente al crear una cuenta, participar en desafíos o interactuar con la comunidad. Esta 
                información puede incluir:
               </p>

               <ul style="margin-left: 50px;">
               <li><strong>Datos de Identificación:</strong> Nombre completo, correo electrónico, nombre de usuario y contraseña (cifrada).</li>
               <li><strong>Datos de Uso y Desempeño:</strong> Progreso en retos, puntuaciones, insignias obtenidas, participación en cursos, comentarios en foros y cualquier interacción dentro de la Plataforma.</li>
               <li><strong>Datos Técnicos:</strong> Dirección IP, tipo de dispositivo, sistema operativo, fecha y hora de acceso,  
                y datos de navegación recopilados mediante cookies y tecnologías similares.</li>
              <li><strong>Datos Opcionales:</strong> Preferencias educativas, áreas de interés, o información que usted proporcione voluntariamente para personalizar su experiencia.</li>
            </ul>

            <br>

            <h3 style="color:#6A2C3D;">2. Finalidad del Tratamiento de Datos</h3>
            <p>
        Los datos recopilados son utilizados con los siguientes fines:
    </p>

    <ul style="margin-left: 50px;">
        <li><strong>Prestación del Servicio:</strong> Crear y gestionar su cuenta, permitir su participación en retos, foros y actividades educativas.</li>
        <li><strong>Mejora de la Experiencia:</strong> Personalizar contenido, recomendaciones y actividades según su progreso y preferencias.</li>
        <li><strong>Optimización y Seguridad:</strong> Analizar el uso de la Plataforma para mejorar su rendimiento, detectar actividades sospechosas y reforzar la seguridad.</li>
        <li><strong>Comunicaciones:</strong> Envío de avisos, notificaciones relacionadas con su cuenta, actualizaciones importantes y cambios en la Plataforma.</li>
        <li><strong>Fines Estadísticos:</strong> Generar métricas sobre desempeño, niveles de participación y evolución de los usuarios para mejora interna.</li>
    </ul>

    <br>

    <h3 style="color:#6A2C3D;">3. Compartición y Transferencia de Datos</h3>
    <p>
        <strong>MenTora NO vende ni alquila su información personal.</strong> Sus datos solo serán compartidos en 
        los siguientes escenarios limitados:
    </p>

    <ul style="margin-left: 50px;">
        <li><strong>Proveedores de Servicios:</strong> Con terceros que nos ayudan a operar la Plataforma (ej. 
            alojamiento web, servicios de correo, analítica, seguridad), los cuales están obligados por contrato 
            a mantener la confidencialidad y a utilizar los datos únicamente para los fines establecidos.</li>
        <li><strong>Cumplimiento Legal:</strong> Cuando sea requerido por ley, orden judicial o para proteger 
            los derechos legales de MenTora, la seguridad de otros usuarios o la integridad de la Plataforma.</li>
        <li><strong>Transferencias Académicas:</strong> En proyectos educativos vinculados con instituciones 
            oficiales, únicamente con fines estadísticos o de mejora, y siempre bajo estrictas medidas de protección.</li>
    </ul>

    <br>

    <h3 style="color:#6A2C3D;">4. Derechos del Usuario (ARCO)</h3>
    <p>
        Usted tiene derecho a acceder, rectificar, cancelar u oponerse al tratamiento de sus 
        datos personales (<strong>Derechos ARCO</strong>). También puede solicitar la limitación del uso de sus 
        datos o la portabilidad de los mismos.
    </p>

    <p>
        Para ejercer cualquiera de estos derechos, envíe una solicitud formal a:  
        <a href="mailto:mentora@gmail.com">mentora@gmail.com</a>
    </p>

    <br>

    <h3 style="color:#6A2C3D;">5. Uso de Cookies y Tecnologías de Rastreo</h3>
    <p>
        Utilizamos cookies y tecnologías similares para rastrear la actividad en la Plataforma y mejorar 
        su experiencia. Las cookies pueden ser:
    </p>

    <ul style="margin-left: 50px;">
        <li><strong>Esenciales:</strong> Necesarias para el funcionamiento básico de la Plataforma.</li>
        <li><strong>De Rendimiento:</strong> Utilizadas para análisis estadísticos y medición de uso.</li>
        <li><strong>De Funcionalidad:</strong> Permiten recordar configuraciones y preferencias del usuario.</li>
    </ul>

    <p>
        Al utilizar la Plataforma, usted acepta el uso de estas tecnologías. Puede deshabilitar las cookies 
        desde la configuración de su navegador, aunque esto podría limitar algunas funciones.
    </p>

    <p style="margin-top: 20px; font-size: 0.9em; color: #555;">
        <em>MenTora se reserva el derecho de modificar esta Política de Privacidad en cualquier 
        momento. Las modificaciones entrarán en vigor inmediatamente después de su publicación en la Plataforma. 
        Le recomendamos revisar esta sección periódicamente.</em>
    </p>
                </div>
            `
        },
        terminos: {
            title: "Términos y Condiciones de Uso",
            text: `
                <div style="padding: 10px;">
                    <p>
                        Al acceder o utilizar los servicios de <strong>MenTora</strong>, usted acepta quedar sujeto a los presentes
                        Términos y Condiciones. <strong> (Si no está de acuerdo con alguna parte de los términos, 
                        de ninguna manera usted debe utilizar la Plataforma.) </strong>
                    </p>
                    <br>
                    <h3 style="color:#6A2C3D;"> 1. Elegibilidad y Cuentas de Usuario</h3>
                    <p>
                        El uso de la Plataforma está disponible solo para personas que puedan formar contratos legalmente vinculantes. 
                        Usted es <strong>responsable</strong> de mantener la confidencialidad de su contraseña y de todas las actividades
                         que ocurran bajo su cuenta.
                    </p>

                    <br>
                    <h3 style="color:#6A2C3D;"> 2. Actividades de Uso Prohibido</h3>
                    <p>
                        Queda <strong>estrictamente prohibido</strong>: 
                       <ul style="margin-left: 50px;">
                      <li>El uso de la Plataforma para cualquier fin ilegal.</li>
                      <li>La publicación de contenido ofensivo, difamatorio o que viole derechos de propiedad.</li>
                      <li>El intento de interferir con el funcionamiento adecuado de la Plataforma. 
                         (El incumplimiento resultará en la baja inmediata de la cuenta.) </li>
                      <li>  El intento de obtener información confidencial de otros usuarios, incluyendo
                          contraseñas o datos personales.</li>
                      <li>La distribución de malware, virus, enlaces maliciosos o cualquier software dañino 
                      a través de la Plataforma.</li>
                      <li>Cualquier conducta que busque vulnerar la seguridad, integridad o disponibilidad
                     de los servicios proporcionados por la Plataforma.</li>
                   </ul> </p>
                    <br>
                    <h3 style="color:#6A2C3D;"> 3. Propiedad Intelectual</h3>
                    <p>
                        Todo el contenido de <strong>MenTora</strong>, incluyendo el diseño de los retos, el software, los gráficos y 
                        el material educativo, es propiedad exclusiva de MenTora o de sus licenciantes y está protegido por derechos 
                        de autor. Usted solo tiene licencia para el uso personal y no comercial del contenido.
                    </p>
                </div>
            `
        },
        contacto: {
            title: "Información de Contacto",
            text: `
                <div style="padding: 10px;">
                    <p>Para consultas generales, soporte técnico o preguntas sobre su cuenta, contáctenos a través de los siguientes medios:</p>
                    <p><strong>Email:</strong> <a href="mailto:mentora@gmail.com">mentora@gmail.com</a></p>
                    <p><strong>Teléfono:</strong> 5619174545 (Horario: Lunes a Viernes, 9:00 - 17:00 CST)</p>
                    <p><strong>Dirección Postal:</strong> Instituto Tecnológico Nacional de México.</p>
                </div>
            `
        },
        equipo: {
            title: "Conoce a Nuestro Equipo",
            text: `
              <div style="display: flex; gap: 2rem; flex-wrap: wrap; justify-content: center; padding: 25px;">

    <div style="text-align:center; min-width: 150px;">
        <!-- Avatar desde GitHub -->
        <img src="https://github.com/IngDavid-Torres.png" 
             width="80" 
             style="margin-bottom: 5px; border-radius: 50%;">

        <h4 style="color:#6A2C3D; text-align:left;">David Iván Torres Martínez</h4>
        <p><strong>Fundador del Proyecto</strong></p>
        <p style="font-size: 0.9em; color: #555;">
           Líder con pensamiento estratégico y enfoque en la resolución de problemas 
           complejos. Cuenta con amplia experiencia en el desarrollo backend, integración
           de servicios, creación de APIs seguras y administración de bases de datos. 
           Posee capacidad para coordinar equipos de trabajo, diseñar arquitecturas
           escalables y garantizar que cada módulo del sistema funcione de manera eficiente.
        </p>

        <!-- GitHub link con texto -->
        <a href="https://github.com/IngDavid-Torres" target="_blank"
           style="display:flex; align-items:center; gap:6px; justify-content:center; margin-top:10px; text-decoration:none; color:#333; font-size:0.85em;">
            
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg"
                 width="20" style="opacity:0.8;">
            
            <span style="font-weight:500;">Visitar perfil</span>
        </a>
    </div>

    <div style="text-align:center; min-width: 150px;">
        <!-- Avatar desde GitHub -->
        <img src="https://github.com/Vonneromero.png" 
             width="80" 
             style="margin-bottom: 5px; border-radius: 50%;">

        <h4 style="color:#6A2C3D; text-align:left;">Karla Ivonne Romero Gonzalez</h4>
        <p><strong>Diseñadora UX/UI</strong></p>
        <p style="font-size: 0.9em; color: #555;">
            Combina habilidades creativas con conocimientos técnicos en frontend para transformar 
            ideas en interfaces funcionales, accesibles y visualmente atractivas.
            Especialista en diseño de interacción, arquitectura visual y principios de 
            usabilidad. Su enfoque está basado en comprender las necesidades del usuario, 
            crear flujos claros y desarrollar prototipos que mejoren la interacción en cada 
            pantalla. Además, domina herramientas de diseño y tecnologías web para garantizar
            una implementación fiel y eficiente.
        </p>

        <!-- GitHub link con texto -->
        <a href="https://github.com/Vonneromero" target="_blank"
           style="display:flex; align-items:center; gap:6px; justify-content:center; margin-top:10px; text-decoration:none; color:#333; font-size:0.85em;">
            
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg"
                 width="20" style="opacity:0.8;">
            
            <span style="font-weight:500;">Visitar perfil</span>
        </a>
    </div>

</div>

            `
        }
    },

    lastScroll: 0,

    init() {
        const closeBtn = document.getElementById('close-modal');
        const overlay = document.getElementById('modal-overlay');

        if (closeBtn) closeBtn.onclick = () => this.close();
        if (overlay) overlay.onclick = () => this.close();
    },

    open(type) {
        if (!this.data[type]) return;

        this.lastScroll = window.scrollY;

        const titleEl = document.getElementById('modal-title');
        const textEl = document.getElementById('modal-text');
        const modalBox = document.getElementById('modal-box');
        const overlay = document.getElementById('modal-overlay');

        if (titleEl) titleEl.innerHTML = this.data[type].title;
        if (textEl) textEl.innerHTML = this.data[type].text;

        if (modalBox) modalBox.style.display = 'block';
        if (overlay) overlay.style.display = 'block';

        document.body.style.overflow = 'hidden';
    },

    close() {
        const modalBox = document.getElementById('modal-box');
        const overlay = document.getElementById('modal-overlay');

        document.body.style.overflow = 'auto';

        if (modalBox) modalBox.style.display = 'none';
        if (overlay) overlay.style.display = 'none';

        setTimeout(() => {
            window.scrollTo({
                top: this.lastScroll,
                behavior: 'instant'
            });
        }, 1);
    }
};

// Global function for onclick handlers
function openModal(type) {
    ModalSystem.open(type);
}

function cerrarModal() {
    ModalSystem.close();
}

// ========== NAVIGATION SYSTEM ==========
const NavigationSystem = {
    init() {
        const hamburger = document.getElementById('hamburger');
        const navLinks = document.getElementById('navLinks');
        const navOverlay = document.querySelector('.nav-overlay');

        if (!hamburger || !navLinks) return;

        hamburger.addEventListener('click', () => {
            this.toggle(hamburger, navLinks, navOverlay);
        });

        // Close on link click
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                this.close(hamburger, navLinks, navOverlay);
            });
        });

        // Close on overlay click
        if (navOverlay) {
            navOverlay.addEventListener('click', () => {
                this.close(hamburger, navLinks, navOverlay);
            });
        }

        // Close on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && navLinks.classList.contains('active')) {
                this.close(hamburger, navLinks, navOverlay);
            }
        });
    },

    toggle(hamburger, navLinks, overlay) {
        const isActive = navLinks.classList.toggle('active');
        hamburger.classList.toggle('open', isActive);
        if (overlay) overlay.classList.toggle('visible', isActive);
        document.body.style.overflow = isActive ? 'hidden' : '';
    },

    close(hamburger, navLinks, overlay) {
        navLinks.classList.remove('active');
        hamburger.classList.remove('open');
        if (overlay) overlay.classList.remove('visible');
        document.body.style.overflow = '';
    }
};

// ========== TOAST NOTIFICATION SYSTEM ==========
const ToastSystem = {
    container: null,

    ensureContainer() {
        if (!this.container) {
            this.container = document.querySelector('.toast-container');
            if (!this.container) {
                this.container = document.createElement('div');
                this.container.className = 'toast-container';
                document.body.appendChild(this.container);
            }
        }
        return this.container;
    },

    show(category, message, options = {}) {
        const { duration = CONFIG.TOAST_DURATION } = options;
        const container = this.ensureContainer();
        
        const toast = document.createElement('div');
        const cls = `toast toast-${category === 'success' ? 'success' : category === 'error' ? 'error' : 'info'}`;
        toast.className = cls;

        const icon = document.createElement('div');
        icon.className = 'icon';
        icon.innerHTML = category === 'success' ? '✓' : (category === 'error' ? '✕' : 'ℹ');

        const text = document.createElement('div');
        text.className = 'text';
        text.textContent = message;

        const closeBtn = document.createElement('button');
        closeBtn.className = 'close-toast';
        closeBtn.style.cssText = 'margin-left: auto; border: none; background: transparent; color: rgba(255,255,255,0.9); cursor: pointer; font-size: 14px;';
        closeBtn.textContent = '✖';

        closeBtn.addEventListener('click', () => {
            this.remove(toast);
        });

        toast.appendChild(icon);
        toast.appendChild(text);
        toast.appendChild(closeBtn);

        container.appendChild(toast);

        setTimeout(() => {
            if (toast.parentElement) {
                this.remove(toast);
            }
        }, duration);
    },

    remove(toast) {
        toast.style.animation = 'toastOut 220ms forwards';
        setTimeout(() => toast.remove(), 230);
    }
};

// Global function for legacy compatibility
function showToast(category, message, duration) {
    ToastSystem.show(category, message, { duration });
}

// ========== ALERT SYSTEM ==========
const AlertSystem = {
    show(element, text, options = {}) {
        const { duration = CONFIG.ALERT_DURATION, autoHide = true } = options;
        
        if (!element) return false;
        
        try {
            element.textContent = text;
            element.classList.remove('alert-hidden');
            element.classList.add('alert-visible');
            element.style.display = 'block';
            
            if (autoHide) {
                setTimeout(() => {
                    element.classList.remove('alert-visible');
                    element.classList.add('alert-hidden');
                    setTimeout(() => element.style.display = 'none', 360);
                }, duration);
            }
            return true;
        } catch (e) {
            console.warn('showAlertElement failed', e);
            return false;
        }
    },

    showOrToast(type, text, duration = CONFIG.ALERT_DURATION) {
        const elId = type === 'success' ? 'alert-success' : 'alert-error';
        const el = document.getElementById(elId);
        
        if (el) {
            this.show(el, text, { duration });
        } else {
            ToastSystem.show(type === 'success' ? 'success' : 'error', text, { duration });
        }
    }
};

// ========== PREVIEW CAROUSEL SYSTEM ==========
const PreviewCarousel = {
    index: 0,
    autoplayInterval: null,

    init() {
        const track = document.getElementById('previewTrack');
        const dotsContainer = document.getElementById('previewDots');
        
        if (!track || !dotsContainer) return;
        
        const slides = track.querySelectorAll('.preview-slide');
        
        slides.forEach((_, i) => {
            const dot = document.createElement('div');
            dot.className = 'preview-dot';
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => this.goTo(i));
            dotsContainer.appendChild(dot);
        });
        
        this.updatePosition();
        this.startAutoplay();
        
        const carousel = document.querySelector('.preview-carousel');
        if (carousel) {
            carousel.addEventListener('mouseenter', () => this.stopAutoplay());
            carousel.addEventListener('mouseleave', () => this.startAutoplay());
        }

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (!this.isInViewport()) return;
            
            if (e.key === 'ArrowLeft') {
                this.move(-1);
            } else if (e.key === 'ArrowRight') {
                this.move(1);
            }
        });

        // Touch swipe support
        this.initTouchSwipe(carousel);
    },

    initTouchSwipe(element) {
        if (!element) return;

        let touchStartX = 0;
        let touchEndX = 0;

        element.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        element.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe(touchStartX, touchEndX);
        }, { passive: true });
    },

    handleSwipe(startX, endX) {
        const threshold = 50;
        const diff = startX - endX;

        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                this.move(1); // Swipe left
            } else {
                this.move(-1); // Swipe right
            }
        }
    },

    move(direction) {
        const track = document.getElementById('previewTrack');
        if (!track) return;
        
        const slides = track.querySelectorAll('.preview-slide');
        
        this.index += direction;
        
        if (this.index < 0) {
            this.index = slides.length - 1;
        } else if (this.index >= slides.length) {
            this.index = 0;
        }
        
        this.updatePosition();
        this.resetAutoplay();
    },

    goTo(index) {
        this.index = index;
        this.updatePosition();
        this.resetAutoplay();
    },

    updatePosition() {
        const track = document.getElementById('previewTrack');
        const dots = document.querySelectorAll('#previewDots .preview-dot');
        
        if (!track) return;
        
        const offset = -this.index * 100;
        track.style.transform = `translateX(${offset}%)`;
        
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === this.index);
        });
    },

    startAutoplay() {
        this.autoplayInterval = setInterval(() => {
            this.move(1);
        }, CONFIG.PREVIEW_AUTOPLAY_DELAY);
    },

    stopAutoplay() {
        if (this.autoplayInterval) {
            clearInterval(this.autoplayInterval);
            this.autoplayInterval = null;
        }
    },

    resetAutoplay() {
        this.stopAutoplay();
        this.startAutoplay();
    },

    isInViewport() {
        const carousel = document.querySelector('.preview-carousel');
        if (!carousel) return false;
        
        const rect = carousel.getBoundingClientRect();
        return rect.top >= 0 && rect.bottom <= window.innerHeight;
    }
};

// Global functions for onclick handlers
function movePreview(direction) {
    PreviewCarousel.move(direction);
}

// ========== REVEAL ANIMATIONS SYSTEM ==========
const RevealAnimations = {
    init() {
        const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        
        if (prefersReduced) {
            document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-revealed'));
            return;
        }

        const defaultOptions = {
            root: null,
            rootMargin: '0px 0px -8% 0px',
            threshold: 0.12
        };

        document.querySelectorAll('.reveal').forEach(el => {
            const rootMargin = el.getAttribute('data-root-margin') || defaultOptions.rootMargin;
            const threshold = parseFloat(el.getAttribute('data-threshold') || defaultOptions.threshold);

            const observer = new IntersectionObserver((entries, obs) => {
                entries.forEach(entry => {
                    const target = entry.target;
                    const once = target.hasAttribute('data-once');
                    
                    if (entry.isIntersecting) {
                        if (target.hasAttribute('data-stagger')) {
                            const gap = parseInt(target.getAttribute('data-stagger-gap')) || 80;
                            this.revealWithStagger(target, gap);
                        }
                        requestAnimationFrame(() => target.classList.add('is-revealed'));
                        if (once) obs.unobserve(target);
                    } else {
                        if (!once) {
                            if (target.hasAttribute('data-stagger')) this.clearStagger(target);
                            target.classList.remove('is-revealed');
                        }
                    }
                });
            }, { root: null, rootMargin, threshold });

            observer.observe(el);
        });
    },

    revealWithStagger(parent, gap) {
        const children = Array.from(parent.children);
        children.forEach((child, i) => {
            child.style.transitionDelay = `${i * gap}ms`;
        });
    },

    clearStagger(parent) {
        Array.from(parent.children).forEach(child => {
            child.style.transitionDelay = '';
        });
    }
};

// ========== AUTH FORMS SYSTEM ==========
const AuthForms = {
    init() {
        this.initLoginForm();
        this.initRegisterForm();
        this.displayFlashedMessages();
    },

    initLoginForm() {
        const loginForm = document.getElementById('loginForm');
        const alertMentoraModal = document.getElementById('alert-mentora-modal');

        if (!loginForm) return;

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const errorEl = document.getElementById('alert-error');
            if (errorEl) {
                errorEl.style.display = 'none';
                errorEl.classList.add('alert-hidden');
            }

            const formData = new FormData(loginForm);

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: formData,
                    credentials: 'same-origin'
                });

                let res = null;
                const contentType = response.headers.get('content-type');

                if (contentType && contentType.includes('application/json')) {
                    try {
                        res = await response.json();
                    } catch (err) {
                        console.error('Error parsing JSON:', err);
                    }
                }

                if (response.ok) {
                    if (res && res.success) {
                        if (alertMentoraModal) alertMentoraModal.style.display = 'flex';
                        setTimeout(() => {
                            window.location.href = res.redirect || '/dashboard';
                        }, CONFIG.LOGIN_REDIRECT_DELAY);
                    } else {
                        AlertSystem.showOrToast('error', (res && res.message) || 'Usuario o contraseña incorrectos');
                    }
                } else {
                    const errorMsg = (res && res.message) || 'Usuario o contraseña incorrectos';
                    AlertSystem.showOrToast('error', errorMsg);
                    console.error('Login error:', response.status, res);

                    // Mostrar detalles del error en consola para debugging
                    if (res && res.error) {
                        console.error('Error detallado:', res.error);
                        if (res.traceback) {
                            console.error('Traceback:', res.traceback);
                        }
                    }
                }
            } catch (err) {
                console.error('Login exception:', err);
                AlertSystem.showOrToast('error', 'Error de conexión. Verifica tu conexión a internet.');
            }
        });
    },

    initRegisterForm() {
        const registerForm = document.getElementById('registerForm');

        if (!registerForm) return;

        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (registerForm.dataset.processing === '1') return;
            registerForm.dataset.processing = '1';

            const formData = new FormData(registerForm);

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    body: formData,
                    credentials: 'same-origin'
                });

                let res = null;
                const contentType = response.headers.get('content-type');

                if (contentType && contentType.includes('application/json')) {
                    try {
                        res = await response.json();
                    } catch (err) {
                        console.error('Error parsing JSON:', err);
                    }
                }

                if (response.ok) {
                    if (res && res.success) {
                        AlertSystem.showOrToast('success', res.message || 'Registro exitoso. Ahora puedes iniciar sesión.');
                        setTimeout(() => {
                            window.location.href = '/login';
                        }, CONFIG.REGISTER_REDIRECT_DELAY);
                    } else {
                        AlertSystem.showOrToast('error', (res && res.message) || 'Error en el registro.');
                    }
                } else {
                    const errorMsg = (res && res.message) || `Error en el registro (${response.status})`;
                    AlertSystem.showOrToast('error', errorMsg);
                    console.error('Register error:', response.status, res);
                }
            } catch (err) {
                console.error('Register exception:', err);
                AlertSystem.showOrToast('error', 'Error de conexión. Verifica tu conexión a internet.');
            } finally {
                try {
                    registerForm.dataset.processing = '0';
                } catch (e) {}
            }
        });
    },

    displayFlashedMessages() {
        try {
            const flashed = document.getElementById('flashed-messages');
            if (flashed) {
                const items = flashed.querySelectorAll('.flashed');
                items.forEach(it => {
                    const cat = it.getAttribute('data-category') || 'info';
                    const msg = it.textContent.trim();
                    if (msg) ToastSystem.show(cat, msg);
                });
            }
        } catch (e) {
            console.warn('Error mostrando toasts:', e);
        }

        // Handle login error message
        const errorMsg = document.getElementById('login-error-msg');
        if (errorMsg) {
            AlertSystem.showOrToast('error', errorMsg.textContent || 'Usuario o contraseña incorrectos');
        }
    }
};

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all systems
    ModalSystem.init();
    NavigationSystem.init();
    PreviewCarousel.init();
    RevealAnimations.init();
    AuthForms.init();

    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            PreviewCarousel.updatePosition();
        }, 250);
    });

    console.log('✅ MenTora initialized successfully');
});

// ========== PERFORMANCE OPTIMIZATION ==========
// Lazy load images
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[data-src]');
    images.forEach(img => {
        img.src = img.dataset.src;
    });
} else {
    // Fallback for older browsers
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
    document.body.appendChild(script);
}

// Service Worker registration (if available)
if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(() => {
            // Silent fail - service worker is optional
        });
    });
}