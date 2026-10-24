import re

# On lit le fichier index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Ajouter le bouton Hamburger dans la balise <nav>
ancien_nav = """<div class="nav-links">
            <a href="#formations">Formations</a>
            <a href="#services">Services</a>
            <a href="#contact" class="btn-nav">Contact</a>
        </div>"""

nouveau_nav = """<div class="menu-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')">
            ☰
        </div>
        <div class="nav-links">
            <a href="#formations">Formations</a>
            <a href="#services">Services</a>
            <a href="#contact" class="btn-nav">Contact</a>
        </div>"""

html = html.replace(ancien_nav, nouveau_nav)

# 2. Ajouter le CSS pour le menu mobile
ancien_css = """@media (max-width: 768px) {
            .nav-links { display: none; }
            .slide-content h2 { font-size: 2em; }
            .slider-container { height: 50vh; }
        }"""

nouveau_css = """@media (max-width: 768px) {
            .menu-toggle { display: block; font-size: 2em; color: white; cursor: pointer; }
            .nav-links { 
                display: none; 
                flex-direction: column; 
                position: absolute; 
                top: 60px; 
                left: 0; 
                width: 100%; 
                background: #0f172a; 
                padding: 20px; 
                border-bottom: 1px solid #1e293b;
            }
            .nav-links.active { display: flex; }
            .nav-links a { margin: 10px 0; font-size: 1.1em; }
            .slide-content h2 { font-size: 2em; }
            .slider-container { height: 50vh; }
        }
        
        .menu-toggle { display: none; }"""

html = html.replace(ancien_css, nouveau_css)

# On sauvegarde le fichier
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Menu mobile ajouté avec succès !")
