
        // Evitar cache del navegador
        if (window.performance && window.performance.navigation && window.performance.navigation.type === 2) {
            window.location.reload();
        }

        // Menú desplegable usuario
        const userMenuBtn = document.getElementById('userMenuBtn');
        const userMenu = document.getElementById('userMenu');
        
        if (userMenuBtn && userMenu) {
            userMenuBtn.onclick = function(e) {
                e.stopPropagation();
                userMenu.style.display = userMenu.style.display === 'flex' ? 'none' : 'flex';
            };
            
            document.body.addEventListener('click', function() {
                userMenu.style.display = 'none';
            });
            
            userMenu.onclick = function(e) {
                e.stopPropagation();
            };
        }

        

        // Scroll a sección
        function scrollToSection(id) {
            const el = document.getElementById(id);
            if (el) {
                el.scrollIntoView({behavior:'smooth', block:'start'});
                if (userMenu) userMenu.style.display = 'none';
            }
        }

        // Modal functions
        function showModal() {
            const modal = document.getElementById('logoutModal');
            if (modal) {
                modal.style.display = 'flex';
                modal.focus();
            }
        }

        function hideModal() {
            const modal = document.getElementById('logoutModal');
            if (modal) {
                modal.style.display = 'none';
            }
        }

        function submitLogout(e) {
            e.preventDefault();
            const form = document.getElementById('logoutForm');
            if (form) form.submit();
        }

        // Cerrar modal con Escape o clic fuera
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') hideModal();
        });

        const logoutModal = document.getElementById('logoutModal');
        if (logoutModal) {
            logoutModal.addEventListener('click', function(e) {
                if (e.target === this) hideModal();
            });
        }

        // Chat en Vivo: abrir/cerrar
        function toggleLiveChat() {
            const box = document.getElementById('livechat-box');
            const btn = document.getElementById('livechat-toggle');
            if (box && btn) {
                if (box.style.display === 'none' || box.style.display === '') {
                    box.style.display = 'flex';
                    btn.style.display = 'none';
                } else {
                    box.style.display = 'none';
                    btn.style.display = 'flex';
                }
            }
        }

        // Chatbot: abrir/cerrar
        function toggleChatbot() {
            const box = document.getElementById('chatbot-box');
            const btn = document.getElementById('chatbot-toggle');
            if (box && btn) {
                if (box.style.display === 'none' || box.style.display === '') {
                    box.style.display = 'flex';
                    btn.style.display = 'none';
                } else {
                    box.style.display = 'none';
                    btn.style.display = 'flex';
                }
            }
        }

        // Chatbot: enviar mensaje
        async function sendChatbotMessage(e) {
            e.preventDefault();
            const input = document.getElementById('chatbot-input');
            const messages = document.getElementById('chatbot-messages');
            
            if (!input || !messages) return;
            
            const userMsg = input.value.trim();
            if (!userMsg) return;
            
            messages.innerHTML += `<div style='margin-bottom:0.5rem;text-align:right;'><span style='background:#5f7f81;color:#fff;padding:0.5rem 1rem;border-radius:14px 14px 2px 14px;display:inline-block;'>${userMsg}</span></div>`;
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
            
            // Llamar al backend
            try {
                const res = await fetch('/chatbot', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userMsg })
                });
                const data = await res.json();
                messages.innerHTML += `<div style='margin-bottom:0.5rem;text-align:left;'><span style='background:#e0ffff;color:#4a6668;padding:0.5rem 1rem;border-radius:14px 14px 14px 2px;display:inline-block;'>${data.response}</span></div>`;
                messages.scrollTop = messages.scrollHeight;
            } catch (err) {
                messages.innerHTML += `<div style='margin-bottom:0.5rem;text-align:left;'><span style='background:#e0ffff;color:#4a6668;padding:0.5rem 1rem;border-radius:14px 14px 14px 2px;display:inline-block;'>Error de conexión con el bot.</span></div>`;
            }
        }

        // Inicializar socket.io para chat en vivo
        let socket;
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof io !== 'undefined') {
                socket = io();
                socket.on('receive_message', function(data) {
                    const usernameInput = document.getElementById('livechat-username');
                    const messages = document.getElementById('livechat-messages');
                    
                    if (!messages) return;
                    
                    const isUser = usernameInput && data.username === usernameInput.value.trim();
                    const msgDiv = document.createElement('div');
                    msgDiv.style.marginBottom = '0.5rem';
                    msgDiv.style.textAlign = isUser ? 'right' : 'left';
                    msgDiv.innerHTML = `<span style='font-size:0.9rem;color:#94a1ac;margin:0 0.5rem;'>${data.username}</span><span style='max-width:70%;padding:0.7rem 1.1rem;border-radius:16px;background:${isUser ? '#5f7f81' : '#e0ffff'};color:${isUser ? '#fff' : '#4a6668'};font-weight:500;font-size:1.05rem;box-shadow:0 1px 4px rgba(0,0,0,0.1);display:inline-block;'>${data.message}</span>`;
                    messages.appendChild(msgDiv);
                    messages.scrollTop = messages.scrollHeight;
                    
                    // Sonido solo si el mensaje es de otro usuario
                    if (!isUser) {
                        const sound = document.getElementById('livechat-sound');
                        if (sound) {
                            sound.currentTime = 0;
                            sound.play().catch(()=>{});
                        }
                    }
                });
            }

            // Chat en Vivo: enviar mensaje
            const livechatForm = document.getElementById('livechat-form');
            if (livechatForm && typeof io !== 'undefined') {
                livechatForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    const input = document.getElementById('livechat-input');
                    const usernameInput = document.getElementById('livechat-username');
                    
                    if (!input || !socket) return;
                    
                    const msg = input.value.trim();
                    const username = usernameInput && usernameInput.value.trim() ? usernameInput.value.trim() : 'Invitado';
                    
                    if (!msg) return;
                    
                    socket.emit('send_message', { message: msg, username: username });
                    input.value = '';
                });
            }

            // Inicializar toggle del menú principal en móviles
            (function initNavToggle(){
                const navToggle = document.getElementById('navToggle');
                const navLinks = document.querySelector('.navbar-links');
                if (!navToggle || !navLinks) return;

                navToggle.addEventListener('click', function(e){
                    e.stopPropagation();
                    const current = window.getComputedStyle(navLinks).display;
                    if (current === 'none' || navLinks.style.display === 'none' || navLinks.style.display === '') {
                        navLinks.style.display = 'flex';
                    } else {
                        navLinks.style.display = 'none';
                    }
                });

                // evitar que clics dentro del menú lo cierren
                navLinks.addEventListener('click', function(e){ e.stopPropagation(); });

                // cerrar al hacer clic fuera
                document.body.addEventListener('click', function(){ navLinks.style.display = ''; });

                // al redimensionar, restablecer para escritorio
                window.addEventListener('resize', function(){ if (window.innerWidth > 768) navLinks.style.display = ''; });
            })();
        });