

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
            const livechatBox = document.getElementById('livechat-box');
            const livechatBtn = document.getElementById('livechat-toggle');
            const chatbotBox = document.getElementById('chatbot-box');
            const chatbotBtn = document.getElementById('chatbot-toggle');
            
            if (livechatBox && livechatBtn) {
                // Close chatbot if it's open
                if (chatbotBox && chatbotBox.style.display === 'flex') {
                    chatbotBox.style.display = 'none';
                    if (chatbotBtn) chatbotBtn.style.display = 'flex';
                }
                
                // Toggle live chat
                if (livechatBox.style.display === 'none' || livechatBox.style.display === '') {
                    livechatBox.style.display = 'flex';
                    livechatBtn.style.display = 'none';
                } else {
                    livechatBox.style.display = 'none';
                    livechatBtn.style.display = 'flex';
                }
            }
        }

 
        let chatbotInitialized = false;

        function toggleChatbot() {
            const chatbotBox = document.getElementById('chatbot-box');
            const chatbotBtn = document.getElementById('chatbot-toggle');
            const livechatBox = document.getElementById('livechat-box');
            const livechatBtn = document.getElementById('livechat-toggle');
            const chatbotMessages = document.getElementById('chatbot-messages');
            
            if (chatbotBox && chatbotBtn) {
                // Close live chat if it's open
                if (livechatBox && livechatBox.style.display === 'flex') {
                    livechatBox.style.display = 'none';
                    if (livechatBtn) livechatBtn.style.display = 'flex';
                }
                
                // Toggle chatbot
                if (chatbotBox.style.display === 'none' || chatbotBox.style.display === '') {
                    chatbotBox.style.display = 'flex';
                    chatbotBtn.style.display = 'none';
                    
                    // Add welcome message on first open
                    if (!chatbotInitialized && chatbotMessages) {
                        chatbotMessages.innerHTML = `<div style='margin-bottom:0.5rem;text-align:left;'><span style='background:linear-gradient(135deg, #f3e5e8, #fef8f9);color:#4a3840;padding:0.5rem 1rem;border-radius:14px 14px 14px 2px;display:inline-block;border:1px solid #d4a5b0;box-shadow:0 2px 8px rgba(106,44,61,0.1);'>¡Hola! 👋 Soy MenToraBot, tu asistente de programación. Puedo ayudarte con temas como Python, JavaScript, HTML/CSS, estructuras de datos, POO, bases de datos, Git y más. ¿Qué te gustaría aprender hoy?</span></div>`;
                        chatbotInitialized = true;
                    }
                } else {
                    chatbotBox.style.display = 'none';
                    chatbotBtn.style.display = 'flex';
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
            
            messages.innerHTML += `<div style='margin-bottom:0.5rem;text-align:right;'><span style='background:linear-gradient(135deg, #6A2C3D, #8A4255);color:#fff;padding:0.5rem 1rem;border-radius:14px 14px 2px 14px;display:inline-block;box-shadow:0 2px 8px rgba(106,44,61,0.3);'>${userMsg}</span></div>`;
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
            

            try {
                const res = await fetch('/chatbot', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userMsg })
                });
                const data = await res.json();
                messages.innerHTML += `<div style='margin-bottom:0.5rem;text-align:left;'><span style='background:linear-gradient(135deg, #f3e5e8, #fef8f9);color:#4a3840;padding:0.5rem 1rem;border-radius:14px 14px 14px 2px;display:inline-block;border:1px solid #d4a5b0;box-shadow:0 2px 8px rgba(106,44,61,0.1);'>${data.response}</span></div>`;
                messages.scrollTop = messages.scrollHeight;
            } catch (err) {
                messages.innerHTML += `<div style='margin-bottom:0.5rem;text-align:left;'><span style='background:#ffe5e5;color:#a03030;padding:0.5rem 1rem;border-radius:14px 14px 14px 2px;display:inline-block;border:1px solid #ffb3b3;'>Error de conexión con el bot.</span></div>`;
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
                    msgDiv.innerHTML = `<span style='font-size:0.85rem;color:#8A4255;margin:0 0.5rem;font-weight:600;'>${data.username}</span><span style='max-width:70%;padding:0.7rem 1.1rem;border-radius:16px;background:${isUser ? 'linear-gradient(135deg, #6A2C3D, #8A4255)' : 'linear-gradient(135deg, #f3e5e8, #fef8f9)'};color:${isUser ? '#fff' : '#4a3840'};font-weight:500;font-size:1rem;box-shadow:0 2px 8px rgba(106,44,61,0.2);display:inline-block;border:${isUser ? 'none' : '1px solid #d4a5b0'};'>${data.message}</span>`;
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
