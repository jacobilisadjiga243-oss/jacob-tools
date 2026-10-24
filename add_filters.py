import os

# On lit le fichier index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. On ajoute les boutons de filtres et la barre de recherche AVANT la grille de contenus
ancien_titre_catalogue = """<h2 class="section-titre">Nos Dernières Formations</h2>
        <p class="section-sous-titre">Des cours vidéo conçus pour vous mener vers la réussite.</p>
        
        <div class="content-grid">"""

nouveau_titre_catalogue = """<h2 class="section-titre">Nos Dernières Formations</h2>
        <p class="section-sous-titre">Des cours vidéo conçus pour vous mener vers la réussite.</p>
        
        <!-- BARRE DE RECHERCHE ET FILTRES -->
        <div class="filters-container">
            <input type="text" id="searchInput" placeholder="Rechercher une formation..." onkeyup="filterCards()">
            <div class="filter-buttons">
                <button class="filter-btn active" onclick="filterCategory('all', this)">Tout</button>
                <button class="filter-btn" onclick="filterCategory('Déblocage', this)">Déblocage</button>
                <button class="filter-btn" onclick="filterCategory('Hard Reset', this)">Hard Reset</button>
                <button class="filter-btn" onclick="filterCategory('FRP', this)">FRP</button>
                <button class="filter-btn" onclick="filterCategory('Marketing', this)">Marketing</button>
            </div>
        </div>
        
        <div class="content-grid" id="cardsGrid">"""

html = html.replace(ancien_titre_catalogue, nouveau_titre_catalogue)

# 2. On ajoute l'attribut data-category sur les cartes pour pouvoir les filtrer
ancien_card = """<div class="card">
                {% if item.categorie == 'Déblocage' %}<span class="badge bg-deblocage">{{ item.categorie }}</span>"""
nouveau_card = """<div class="card" data-category="{{ item.categorie }}" data-title="{{ item.titre|lower }}">
                {% if item.categorie == 'Déblocage' %}<span class="badge bg-deblocage">{{ item.categorie }}</span>"""
html = html.replace(ancien_card, nouveau_card)

# 3. On ajoute le CSS pour la barre de recherche et les boutons
ancien_css = """/* --- POURQUOI NOUS (AVEC IMAGES) --- */"""
nouveau_css = """/* --- FILTRES ET RECHERCHE --- */
        .filters-container { max-width: 1200px; margin: 0 auto 40px auto; display: flex; flex-direction: column; gap: 20px; align-items: center; }
        #searchInput { width: 100%; max-width: 500px; padding: 15px 25px; border-radius: 50px; border: 1px solid #475569; background: #1e293b; color: white; font-family: inherit; font-size: 1em; outline: none; transition: 0.3s; }
        #searchInput:focus { border-color: #38bdf8; box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }
        .filter-buttons { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; }
        .filter-btn { padding: 10px 20px; border-radius: 50px; border: 1px solid #334155; background: transparent; color: #cbd5e1; font-weight: 600; cursor: pointer; transition: 0.3s; font-family: inherit; }
        .filter-btn:hover { background: #1e293b; color: white; }
        .filter-btn.active { background: #38bdf8; color: #0b1120; border-color: #38bdf8; }

        /* --- POURQUOI NOUS (AVEC IMAGES) --- */"""
html = html.replace(ancien_css, nouveau_css)

# 4. On ajoute le script JavaScript pour filtrer
ancien_script = """slideInterval = setInterval(nextSlide, 5000);
    </script>"""

nouveau_script = """slideInterval = setInterval(nextSlide, 5000);

        // --- SCRIPT POUR RECHERCHE ET FILTRES ---
        let currentCategory = 'all';

        function filterCategory(category, btn) {
            currentCategory = category;
            // Gérer l'apparence des boutons
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            // Filtrer
            filterCards();
        }

        function filterCards() {
            const searchText = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('#cardsGrid .card');

            cards.forEach(card => {
                const category = card.getAttribute('data-category');
                const title = card.getAttribute('data-title') || '';
                
                const matchCategory = (currentCategory === 'all' || category === currentCategory);
                const matchSearch = title.includes(searchText);

                if (matchCategory && matchSearch) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>"""

html = html.replace(ancien_script, nouveau_script)

# On sauvegarde le fichier
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Barre de recherche et filtres ajoutes avec succes !")
