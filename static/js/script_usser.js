

        if (window.performance && window.performance.navigation && window.performance.navigation.type === 2) {
            window.location.reload();
        }

        // User menu toggle - debounced
        const userMenuBtn = document.getElementById('userMenuBtn');
        const userMenu = document.getElementById('userMenu');
        let menuTimeout;

        if (userMenuBtn && userMenu) {
            userMenuBtn.onclick = function(e) {
                e.stopPropagation();
                clearTimeout(menuTimeout);
                userMenu.style.display = userMenu.style.display === 'flex' ? 'none' : 'flex';
            };

            document.body.addEventListener('click', function() {
                menuTimeout = setTimeout(() => {
                    userMenu.style.display = 'none';
                }, 50);
            }, { passive: true });

            userMenu.onclick = function(e) {
                e.stopPropagation();
            };
        }


        function scrollToSection(id) {
            const el = document.getElementById(id);
            if (el) {
                const navbar = document.querySelector('.main-navbar');
                const navHeight = navbar ? navbar.offsetHeight : 0;
                const targetPosition = el.offsetTop - navHeight - 20;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'auto'
                });
                // Close mobile menu if open
                const navLinks = document.getElementById('navLinks');
                if (navLinks && navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                }
                // Close user menu if open
                if (userMenu) {
                    userMenu.style.display = 'none';
                }
            }
        }


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


        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') hideModal();
        }, { passive: true });

        const logoutModal = document.getElementById('logoutModal');
        if (logoutModal) {
            logoutModal.addEventListener('click', function(e) {
                if (e.target === this) hideModal();
            }, { passive: true });
        }


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


        let socket;
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof io !== 'undefined') {
                socket = io({ reconnectionDelay: 1000, reconnection: true });
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
                    

                    if (!isUser) {
                        const sound = document.getElementById('livechat-sound');
                        if (sound) {
                            sound.currentTime = 0;
                            sound.play().catch(()=>{});
                        }
                    }
                });
            }

           
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
                }, { passive: false });
            }

            // Mobile menu toggle
            const navToggle = document.getElementById('navToggle');
            const navLinks = document.getElementById('navLinks');

            if (navToggle && navLinks) {
                navToggle.addEventListener('click', function() {
                    navLinks.classList.toggle('active');
                }, { passive: true });
            }

            // Smooth scroll function - using auto instead of smooth
            window.scrollToSection = function(sectionId) {
                const section = document.getElementById(sectionId);
                if (section) {
                    const navbar = document.querySelector('.main-navbar');
                    const navHeight = navbar ? navbar.offsetHeight : 0;
                    const targetPosition = section.offsetTop - navHeight - 20;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'auto'
                    });
                    // Close mobile menu if open
                    if (navLinks && navLinks.classList.contains('active')) {
                        navLinks.classList.remove('active');
                    }
                    // Close user menu if open
                    const userMenu = document.getElementById('userMenu');
                    if (userMenu) {
                        userMenu.style.display = 'none';
                    }
                }
                return false;
            };
        }, { passive: true });
