const mockNews = [
    { id: 1, title: "Python 3.13 lanza nuevas características de rendimiento", description: "La nueva versión de Python incluye mejoras significativas en la velocidad de ejecución, optimizaciones en el garbage collector y mejor soporte para type hints.", fullContent: "Python 3.13 representa un avance significativo en el ecosistema del lenguaje, introduciendo un compilador JIT experimental que promete acelerar la ejecución hasta un 60% en ciertos casos de uso. El nuevo garbage collector implementa un algoritmo más eficiente que reduce las pausas y mejora el rendimiento en aplicaciones de alto tráfico.", category: "python", source: "Python.org", author: "Guido van Rossum", readTime: "5 min", tags: ["Python", "Performance", "JIT"], date: "2025-01-15", url: "https://www.python.org/", image: "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800" },
    { id: 2, title: "React 19 RC: Nuevos hooks y mejoras en Server Components", description: "React 19 Release Candidate está disponible con hooks mejorados, mejor soporte para Server Components y optimizaciones de rendimiento que reducen el bundle size hasta un 30%.", fullContent: "El equipo de React ha lanzado la versión Release Candidate de React 19, trayendo innovaciones revolucionarias en el modelo de renderizado del lado del servidor. Los nuevos hooks como useOptimistic y useFormStatus simplifican el manejo de estados optimistas y formularios.", category: "javascript", source: "React Team", author: "Dan Abramov", readTime: "7 min", tags: ["React", "Hooks", "Server Components"], date: "2025-01-14", url: "https://react.dev/", image: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=800" },
    { id: 3, title: "GPT-5 y el futuro de la IA conversacional", description: "OpenAI anuncia avances revolucionarios en modelos de lenguaje con capacidades multimodales mejoradas, mejor razonamiento contextual y comprensión de código más precisa.", fullContent: "OpenAI ha revelado GPT-5, marcando un nuevo hito en la inteligencia artificial conversacional. El modelo presenta capacidades multimodales nativas, procesando simultáneamente texto, imágenes, audio y video con una comprensión contextual sin precedentes.", category: "ai", source: "OpenAI", author: "Sam Altman", readTime: "10 min", tags: ["AI", "GPT-5", "Machine Learning"], date: "2025-01-13", url: "https://openai.com/", image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800" },
    { id: 4, title: "CSS Grid Level 3: Masonry Layout finalmente aprobado", description: "El W3C aprueba oficialmente la especificación de Masonry Layout para CSS Grid, permitiendo diseños estilo Pinterest nativamente sin JavaScript adicional.", fullContent: "El W3C ha aprobado oficialmente CSS Grid Level 3, introduciendo Masonry Layout como una característica nativa del navegador. Esta especificación elimina la necesidad de bibliotecas JavaScript para crear diseños tipo Pinterest.", category: "web", source: "W3C", author: "Rachel Andrew", readTime: "6 min", tags: ["CSS", "Grid", "Masonry"], date: "2025-01-12", url: "https://www.w3.org/", image: "https://images.unsplash.com/photo-1507721999472-8ed4421c4af2?w=800" },
    { id: 5, title: "Node.js 22 LTS disponible con soporte nativo para TypeScript", description: "La nueva versión LTS de Node.js incluye soporte experimental para ejecutar TypeScript directamente sin necesidad de transpilación, mejorando significativamente el DX.", fullContent: "Node.js 22 LTS marca un hito histórico al introducir soporte nativo para TypeScript sin requerir herramientas de transpilación externas. El runtime ahora puede ejecutar archivos .ts directamente, simplificando dramáticamente el flujo de desarrollo.", category: "javascript", source: "Node.js Foundation", author: "Matteo Collina", readTime: "8 min", tags: ["Node.js", "TypeScript", "Backend"], date: "2025-01-11", url: "https://nodejs.org/", image: "https://images.unsplash.com/photo-1627398242454-45a1465c2479?w=800" },
    { id: 6, title: "TensorFlow 2.16: Mejoras en edge computing y mobile", description: "Google lanza TensorFlow 2.16 con optimizaciones significativas para dispositivos móviles, edge computing y mejor integración con frameworks web modernos.", fullContent: "TensorFlow 2.16 transforma el panorama del machine learning en dispositivos edge con optimizaciones revolucionarias. Los modelos ahora se ejecutan hasta 3 veces más rápido en dispositivos móviles gracias al nuevo TensorFlow Lite Converter mejorado.", category: "ai", source: "Google AI", author: "Jeff Dean", readTime: "9 min", tags: ["TensorFlow", "AI", "Mobile"], date: "2025-01-10", url: "https://tensorflow.org/", image: "https://images.unsplash.com/photo-1655720828018-edd2daec9349?w=800" },
    { id: 7, title: "Rust se mantiene como el lenguaje más amado del 2025", description: "Por octavo año consecutivo, Rust es votado como el lenguaje de programación más amado por desarrolladores en la encuesta de Stack Overflow.", fullContent: "La encuesta anual de Stack Overflow confirma a Rust como el lenguaje más amado por desarrolladores por octavo año consecutivo, con un impresionante 87% de satisfacción. El crecimiento del ecosistema es notable con más de 100,000 crates en crates.io y adopción masiva en empresas como Microsoft, Amazon y Google.", category: "web", source: "Stack Overflow", author: "Stack Overflow Team", readTime: "6 min", tags: ["Rust", "Programming", "Survey"], date: "2025-01-09", url: "https://stackoverflow.com/", image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800" },
    { id: 8, title: "GitHub Copilot X integra GPT-4 para asistencia avanzada", description: "GitHub anuncia la integración de GPT-4 en Copilot, ofreciendo sugerencias de código más precisas, contextuales y con mejor comprensión de arquitecturas complejas.", fullContent: "GitHub Copilot X representa la próxima generación de asistentes de programación con IA, integrando GPT-4 para ofrecer capacidades sin precedentes. La nueva versión comprende contexto completo de proyectos, puede explicar código línea por línea, y genera tests unitarios automáticamente con una precisión del 92%.", category: "ai", source: "GitHub Blog", author: "Thomas Dohmke", readTime: "7 min", tags: ["GitHub", "Copilot", "AI", "GPT-4"], date: "2025-01-08", url: "https://github.blog/", image: "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800" },
    { id: 9, title: "Vue 3.4 'Slam Dunk' mejora reactividad y performance", description: "La nueva versión de Vue.js trae mejoras dramáticas en el sistema de reactividad, optimizaciones en el render y mejor soporte para TypeScript.", fullContent: "Vue 3.4, con nombre código 'Slam Dunk', redefine los estándares de performance en frameworks JavaScript modernos. El sistema de reactividad ha sido completamente reescrito usando Proxies optimizados, resultando en un 50% menos de overhead en updates reactivos. El nuevo parser de templates es 2x más rápido.", category: "javascript", source: "Vue.js Team", author: "Evan You", readTime: "6 min", tags: ["Vue.js", "JavaScript", "Framework"], date: "2025-01-07", url: "https://vuejs.org/", image: "https://images.unsplash.com/photo-1619410283995-43d9134e7656?w=800" },
    { id: 10, title: "WebAssembly 2.0 expande capacidades web", description: "La nueva especificación de WebAssembly permite ejecutar aplicaciones más complejas directamente en el navegador con mejor performance y menor consumo de memoria.", fullContent: "WebAssembly 2.0 transforma la web en una plataforma de aplicaciones verdaderamente universal. Las nuevas características incluyen garbage collection nativo, threads y SIMD avanzado que habilitan procesamiento paralelo de alto rendimiento para aplicaciones científicas y de video. La interoperabilidad mejorada con JavaScript elimina el overhead de llamadas.", category: "web", source: "WebAssembly CG", author: "WebAssembly Community", readTime: "8 min", tags: ["WebAssembly", "WASM", "Web"], date: "2025-01-06", url: "https://webassembly.org/", image: "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800" },
    { id: 11, title: "Django 5.1 introduce async views mejorados", description: "Django lanza soporte completo para vistas asíncronas con mejor integración de ASGI, WebSockets y streaming responses para aplicaciones en tiempo real.", fullContent: "Django 5.1 marca la madurez del soporte asíncrono en el framework web más popular de Python. Las async views ahora soportan toda la funcionalidad del ORM sin bloqueo, permitiendo aplicaciones de alto rendimiento con miles de conexiones concurrentes. La integración nativa de WebSockets elimina la necesidad de Channels como dependencia separada.", category: "python", source: "Django Project", author: "Carlton Gibson", readTime: "7 min", tags: ["Django", "Python", "Async", "Web Framework"], date: "2025-01-05", url: "https://www.djangoproject.com/", image: "https://images.unsplash.com/photo-1587620962725-abab7fe55159?w=800" },
    { id: 12, title: "Bun 1.2: El runtime de JavaScript más rápido alcanza estabilidad", description: "Bun continúa superando a Node.js y Deno en benchmarks de rendimiento con su nueva actualización, ahora considerado production-ready por equipos empresariales.", fullContent: "Bun 1.2 consolida su posición como el runtime de JavaScript más rápido del mercado. Los benchmarks muestran que Bun es 3-4x más rápido que Node.js en arranque de aplicaciones y 2x más rápido en ejecución de código TypeScript. El bundler integrado supera a webpack y esbuild en velocidad de compilación. Hot reload instantáneo mejora la experiencia de desarrollo.", category: "javascript", source: "Bun Blog", author: "Jarred Sumner", readTime: "6 min", tags: ["Bun", "JavaScript", "Runtime", "Performance"], date: "2025-01-04", url: "https://bun.sh/", image: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800" }
];

let currentFilter = 'all', currentSort = 'date-asc', allNews = [], filteredNews = [];

async function loadNews() {
    await new Promise(r => setTimeout(r, 1000));
    allNews = mockNews;
    filteredNews = [...allNews];
    displayNews(filteredNews);
    document.getElementById('loading').style.display = 'none';
    document.getElementById('news-grid').style.display = 'grid';
}

function displayNews(news) {
    const grid = document.getElementById('news-grid');
    grid.innerHTML = '';
    if (news.length === 0) {
        grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:3rem;color:#fff;"><h3>No se encontraron noticias</h3><p>Intenta ajustar los filtros</p></div>';
        return;
    }
    const count = Math.min(2, news.length);
    for (let i = 0; i < count; i++) grid.appendChild(createCard(news[i], true));
    news.slice(count).forEach(item => grid.appendChild(createCard(item, false)));
}

function createCard(item, featured) {
    const card = document.createElement('div');
    card.className = featured ? 'featured-article' : 'news-card';
    card.onclick = () => openModal(item);
    card.innerHTML = `
        <div class="${featured?'featured':'news'}-image">
            <img src="${item.image}" alt="${item.title}">
        </div>
        <div class="${featured?'featured':'news'}-content">
            <span class="${featured?'featured':'news'}-tag">${getCategoryName(item.category)}</span>
            <h3 class="${featured?'featured':'news'}-title">${item.title}</h3>
            <p class="${featured?'featured':'news'}-description">${item.description}</p>
            <div class="${featured?'featured':'news'}-meta">
                <span class="news-source">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                    </svg>
                    ${item.source}
                </span>
                <span class="news-date">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <line x1="16" y1="2" x2="16" y2="6"/>
                        <line x1="8" y1="2" x2="8" y2="6"/>
                        <line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>
                    ${formatDate(item.date)}
                </span>
            </div>
            <span class="${featured?'featured':'news'}-link">Leer más →</span>
        </div>
    `;
    return card;
}

function openModal(item) {
    const modal = document.createElement('div');
    modal.className = 'news-modal';
    modal.innerHTML = `
        <div class="modal-container">
            <button class="modal-close-btn" onclick="this.closest('.news-modal').remove();document.body.style.overflow='auto';">×</button>
            <img src="${item.image}" class="modal-header-img">
            <div class="modal-body">
                <span class="modal-category-tag">${getCategoryName(item.category)}</span>
                <h2 class="modal-title">${item.title}</h2>
                <div class="modal-meta-info">
                    <span class="modal-meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
                        </svg>
                        ${item.source}
                    </span>
                    <span class="modal-meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12 6 12 12 16 14"/>
                        </svg>
                        ${item.readTime} lectura
                    </span>
                    <span class="modal-meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                            <line x1="16" y1="2" x2="16" y2="6"/>
                            <line x1="8" y1="2" x2="8" y2="6"/>
                            <line x1="3" y1="10" x2="21" y2="10"/>
                        </svg>
                        ${formatDate(item.date)}
                    </span>
                    <span class="modal-meta-item">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                        ${item.author}
                    </span>
                </div>
                <p class="modal-description">${item.description}</p>
                <div class="modal-additional-info">
                    <h3>Artículo Completo</h3>
                    <p>${item.fullContent}</p>
                </div>
                <div class="modal-tags">
                    ${item.tags.map(tag => `<span class="modal-tag-item">${tag}</span>`).join('')}
                </div>
                <a href="${item.url}" target="_blank" class="modal-external-link">
                    Ver fuente original en ${item.source}
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                        <polyline points="15 3 21 3 21 9"/>
                        <line x1="10" y1="14" x2="21" y2="3"/>
                    </svg>
                </a>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
    modal.onclick = e => { if (e.target === modal) { modal.remove(); document.body.style.overflow = 'auto'; } };
}

function filterNews(cat) {
    currentFilter = cat;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    applyFilters();
}

function applyFilters() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    let filtered = currentFilter === 'all' ? [...allNews] : allNews.filter(n => n.category === currentFilter);
    if (search) filtered = filtered.filter(n => n.title.toLowerCase().includes(search) || n.description.toLowerCase().includes(search) || n.fullContent.toLowerCase().includes(search) || n.tags.some(t => t.toLowerCase().includes(search)));

    filtered.sort((a,b) => new Date(b.date) - new Date(a.date));
    
    displayNews(filtered);
}

function getCategoryName(cat) {
    return { javascript: 'JavaScript', python: 'Python', web: 'Web Dev', ai: 'IA & ML' }[cat] || cat;
}

function formatDate(d) {
    return new Date(d).toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
}

document.getElementById('searchInput').addEventListener('input', applyFilters);
document.addEventListener('DOMContentLoaded', loadNews);
document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); document.getElementById('searchInput').focus(); }
    if (e.key === 'Escape') { const m = document.querySelector('.news-modal'); if (m) { m.remove(); document.body.style.overflow = 'auto'; } }
});
