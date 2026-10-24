html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jacob Tools - Formations & Solutions Digitales</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        html { scroll-behavior: smooth; }
        body { background-color: #0b1120; color: #e2e8f0; overflow-x: hidden; }
        
        /* --- NAVIGATION --- */
        nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 5%; background: rgba(11, 17, 32, 0.95); position: fixed; width: 100%; top: 0; z-index: 1000; border-bottom: 1px solid #1e293b; backdrop-filter: blur(10px); transition: 0.3s; }
        .logo { font-size: 1.6em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; }
        .logo span { color: #38bdf8; }
        .menu-toggle { display: none; font-size: 1.8em; color: white; cursor: pointer; }
        .nav-links { display: flex; gap: 30px; align-items: center; }
        .nav-links a { color: #cbd5e1; text-decoration: none; font-weight: 500; transition: 0.3s; font-size: 0.95em; }
        .nav-links a:hover { color: #38bdf8; }
        .btn-nav { background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120 !important; padding: 10px 25px; border-radius: 50px; font-weight: 700; box-shadow: 0 4px 15px rgba(56,189,248,0.3); }
        .btn-nav:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(56,189,248,0.5); }

        /* --- HERO SECTION --- */
        .hero { min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 120px 20px 60px; background: radial-gradient(circle at top right, #1e293b 0%, #0b1120 60%); }
        .hero h1 { font-size: 4em; font-weight: 800; margin-bottom: 20px; color: white; line-height: 1.1; max-width: 900px; }
        .hero h1 span { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 1.2em; color: #94a3b8; max-width: 700px; margin-bottom: 40px; }
        .btn { display: inline-block; padding: 16px 40px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120; text-decoration: none; border-radius: 50px; font-weight: 700; font-size: 1.1em; transition: 0.3s; box-shadow: 0 4px 15px rgba(56,189,248,0.4); border: none; cursor: pointer; }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(56,189,248,0.6); }

        /* --- SECTIONS --- */
        section { padding: 100px 5%; }
        .section-titre { text-align: center; font-size: 2.5em; color: white; margin-bottom: 15px; font-weight: 800; }
        .section-sous-titre { text-align: center; color: #94a3b8; margin-bottom: 60px; font-size: 1.1em; }

        /* --- CATALOGUE (VIDEOS) --- */
        .content-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; overflow: hidden; transition: 0.3s; display: flex; flex-direction: column; }
        .card:hover { transform: translateY(-8px); border-color: #38bdf8; box-shadow: 0 15px 30px rgba(0,0,0,0.5); }
        .card-img { height: 200px; width: 100%; object-fit: cover; }
        .card-body { padding: 25px; flex-grow: 1; display: flex; flex-direction: column; position: relative; }
        .card-body h3 { color: white; margin-bottom: 10px; font-size: 1.3em; }
        .card-body p { color: #94a3b8; font-size: 0.95em; margin-bottom: 25px; flex-grow: 1; }
        
        .badge { position: absolute; top: 15px; right: 15px; padding: 6px 15px; border-radius: 50px; font-size: 0.75em; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; z-index: 10; }
        .bg-deblocage { background: #38bdf8; color: #0b1120; }
        .bg-hardreset { background: #f59e0b; color: #0b1120; }
        .bg-frp { background: #ef4444; color: white; }
        .bg-marketing { background: #f472b6; color: white; }
        
        .video-container { width: 100%; height: 200px; background: #000; }
        .video-container iframe { width: 100%; height: 100%; border: none; }

        /* --- POURQUOI NOUS --- */
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; max-width: 1200px; margin: 0 auto; text-align: center; }
        .feature-item { padding: 30px; background: #1e293b; border-radius: 16px; border: 1px solid #334155; transition: 0.3s; }
        .feature-item:hover { border-color: #38bdf8; transform: translateY(-5px); }
        .feature-icon { font-size: 3em; margin-bottom: 20px; }
        .feature-item h3 { color: white; font-size: 1.2em; margin-bottom: 10px; }
        .feature-item p { color: #94a3b8; font-size: 0.9em; }

        /* --- FOOTER --- */
        footer { background: #0f172a; padding: 60px 5% 30px; border-top: 1px solid #1e293b; text-align: center; }
        .footer-content p { color: #94a3b8; margin-bottom: 20px; }
        .footer-links { display: flex; justify-content: center; gap: 30px; margin-bottom: 30px; flex-wrap: wrap; }
        .footer-links a { color: #cbd5e1; text-decoration: none; transition: 0.3s; }
        .footer-links a:hover { color: #38bdf8; }
        .copyright { color: #475569; font-size: 0.9em; }

        /* --- RESPONSIVE MOBILE --- */
        @media (max-width: 768px) {
            .menu-toggle { display: block; }
            .nav-links { display: none; flex-direction: column; position: absolute; top: 70px; left: 0; width: 100%; background: #0f172a; padding: 20px 0; border-bottom: 1px solid #1e293b; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
            .nav-links.active { display: flex; }
            .nav-links a { margin: 15px 0; font-size: 1.1em; width: 100%; text-align: center; }
            .hero h1 { font-size: 2.5em; }
            .section-titre { font-size: 2em; }
        }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <div class="menu-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')">☰</div>
        <div class="nav-links">
            <a href="#accueil">Accueil</a>
            <a href="#formations">Formations</a>
            <a href="#services">Services</a>
            <a href="#contact" class="btn-nav">Contact</a>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <header class="hero" id="accueil">
        <h1>Maîtrisez la Technologie avec <span>Jacob Tools</span></h1>
        <p>Apprenez le déblocage, le marketing digital et les systèmes d'exploitation grâce à des formations vidéo exclusives et des solutions professionnelles.</p>
        <a href="#formations" class="btn">Découvrir les formations</a>
    </header>

    <!-- CATALOGUE -->
    <section id="formations" style="background: #0f172a;">
        <h2 class="section-titre">Nos Dernières Formations</h2>
        <p class="section-sous-titre">Des cours vidéo conçus pour vous mener vers la réussite.</p>
        
        <div class="content-grid">
            {% for item in contenus %}
            <div class="card">
                {% if item.categorie == 'Déblocage' %}<span class="badge bg-deblocage">{{ item.categorie }}</span>
                {% elif item.categorie == 'Hard Reset' %}<span class="badge bg-hardreset">{{ item.categorie }}</span>
                {% elif item.categorie == 'FRP' %}<span class="badge bg-frp">{{ item.categorie }}</span>
                {% else %}<span class="badge bg-marketing">{{ item.categorie }}</span>{% endif %}
                
                {% if item.lien and ('youtube.com' in item.lien or 'youtu.be' in item.lien) %}
                    {% set video_id = item.lien.split('v=')[1].split('&')[0] if 'v=' in item.lien else item.lien.split('/')[-1] %}
                    <div class="video-container">
                        <iframe src="https://www.youtube.com/embed/{{ video_id }}?rel=0" allowfullscreen></iframe>
                    </div>
                {% else %}
                    <img src="{{ item.image_url }}" class="card-img" alt="{{ item.titre }}" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">
                {% endif %}
                
                <div class="card-body">
                    <h3>{{ item.titre }}</h3>
                    <p>{{ item.description }}</p>
                    {% if item.lien %}
                        <a href="{{ item.lien }}" class="btn" target="_blank" style="text-align: center; padding: 12px 20px;">▶ Regarder la vidéo</a>
                    {% endif %}
                </div>
            </div>
            {% else %}
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px; background: #1e293b; border-radius: 16px; border: 1px dashed #475569;">
                <h3 style="color: #38bdf8; margin-bottom: 10px;">Aucune formation pour le moment</h3>
                <p style="color: #94a3b8;">Ajoutez vos vidéos depuis l'espace admin.</p>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- POURQUOI NOUS -->
    <section id="services">
        <h2 class="section-titre">Pourquoi choisir Jacob Tools ?</h2>
        <p class="section-sous-titre">Nous mettons la qualité et la pédagogie au cœur de nos formations.</p>
        
        <div class="features-grid">
            <div class="feature-item">
                <div class="feature-icon">🎥</div>
                <h3>Vidéos HD Exclusives</h3>
                <p>Apprenez avec des vidéos claires et de haute qualité.</p>
            </div>
            <div class="feature-item">
                <div class="feature-icon">⚡</div>
                <h3>Accès à Vie</h3>
                <p>Une fois formé, gardez l'accès à vos contenus pour toujours.</p>
            </div>
            <div class="feature-item">
                <div class="feature-icon">🛠️</div>
                <h3>Support Technique</h3>
                <p>Une équipe disponible pour répondre à toutes vos questions.</p>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer id="contact">
        <div class="footer-content">
            <h2 class="section-titre" style="font-size: 2em; margin-bottom: 10px;">Prêt à commencer ?</h2>
            <p>Rejoignez la communauté Jacob Tools et transformez vos compétences dès aujourd'hui.</p>
            <div class="footer-links">
                <a href="#accueil">Accueil</a>
                <a href="#formations">Formations</a>
                <a href="#services">Services</a>
            </div>
            <div class="copyright">
                &copy; 2026 Jacob Tools. Tous droits réservés. Propulsé par la technologie.
            </div>
        </div>
    </footer>
</body>
</html>"""

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Site professionnalise avec succes !")
