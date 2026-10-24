index_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jacob Tools - Formations & Solutions Digitales</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        /* --- RESET & BASE --- */
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        html { scroll-behavior: smooth; }
        body { background-color: #0b1120; color: #e2e8f0; line-height: 1.6; overflow-x: hidden; }
        
        /* --- NAVIGATION --- */
        nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 5%; background: rgba(11, 17, 32, 0.95); position: fixed; width: 100%; top: 0; z-index: 1000; border-bottom: 1px solid #1e293b; backdrop-filter: blur(10px); transition: all 0.3s; }
        .logo { font-size: 1.8em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; }
        .logo span { color: #38bdf8; }
        .nav-links { display: flex; gap: 30px; align-items: center; }
        .nav-links a { color: #cbd5e1; text-decoration: none; font-weight: 500; transition: color 0.3s; font-size: 0.95em; }
        .nav-links a:hover { color: #38bdf8; }
        .btn-nav { background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120 !important; padding: 10px 25px; border-radius: 50px; font-weight: 700 !important; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3); }
        .btn-nav:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(56, 189, 248, 0.5); }

        /* --- HERO SECTION --- */
        .hero { min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 120px 20px 60px 20px; background: radial-gradient(circle at top right, #1e293b 0%, #0b1120 60%); position: relative; }
        .hero h1 { font-size: 4.5em; font-weight: 800; margin-bottom: 20px; color: white; line-height: 1.1; max-width: 900px; animation: fadeUp 0.8s ease-out; }
        .hero h1 span { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 1.3em; color: #94a3b8; max-width: 700px; margin: 0 auto 40px auto; animation: fadeUp 1s ease-out; }
        .hero-btns { display: flex; gap: 20px; animation: fadeUp 1.2s ease-out; }
        .btn { display: inline-block; padding: 16px 40px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120; text-decoration: none; border-radius: 50px; font-weight: 700; font-size: 1.1em; transition: all 0.3s; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4); border: none; cursor: pointer; }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(56, 189, 248, 0.6); }
        .btn-outline { background: transparent; border: 2px solid #38bdf8; color: #38bdf8; box-shadow: none; }
        .btn-outline:hover { background: rgba(56, 189, 248, 0.1); box-shadow: 0 0 15px rgba(56, 189, 248, 0.3); }

        /* --- SECTIONS GENERALES --- */
        section { padding: 100px 5%; }
        .section-titre { text-align: center; font-size: 2.8em; margin-bottom: 15px; color: white; font-weight: 800; }
        .section-sous-titre { text-align: center; color: #94a3b8; font-size: 1.1em; max-width: 600px; margin: 0 auto 60px auto; }

        /* --- RUBRIQUES (CATEGORIES) --- */
        .rubriques-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .rubrique-card { background: #1e293b; padding: 40px 30px; border-radius: 20px; text-align: center; border: 1px solid #334155; transition: all 0.4s; position: relative; overflow: hidden; }
        .rubrique-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #38bdf8, #818cf8); transform: scaleX(0); transition: transform 0.4s; transform-origin: left; }
        .rubrique-card:hover { transform: translateY(-10px); border-color: #475569; box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
        .rubrique-card:hover::before { transform: scaleX(1); }
        .rubrique-icon { font-size: 3em; margin-bottom: 20px; }
        .rubrique-card h3 { color: #38bdf8; font-size: 1.4em; margin-bottom: 10px; }
        .rubrique-card p { color: #94a3b8; font-size: 0.95em; }

        /* --- CATALOGUE (VIDEOS/COURS) --- */
        .content-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; overflow: hidden; transition: transform 0.3s, border-color 0.3s; display: flex; flex-direction: column; }
        .card:hover { transform: translateY(-5px); border-color: #38bdf8; box-shadow: 0 15px 30px rgba(0,0,0,0.5); }
        .card-img { height: 180px; background: linear-gradient(135deg, #1e293b, #0f172a); display: flex; justify-content: center; align-items: center; color: #475569; font-size: 3em; border-bottom: 1px solid #334155; }
        .card-body { padding: 25px; display: flex; flex-direction: column; flex-grow: 1; }
        .card-body h3 { color: white; font-size: 1.3em; margin-bottom: 10px; font-weight: 600; }
        .card-body p { color: #94a3b8; font-size: 0.95em; flex-grow: 1; margin-bottom: 20px; }
        .card-body .btn { padding: 10px 20px; font-size: 0.95em; text-align: center; width: 100%; }

        /* --- FEATURES (POURQUOI NOUS) --- */
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; max-width: 1200px; margin: 0 auto; text-align: center; }
        .feature-item h3 { color: white; font-size: 1.3em; margin-bottom: 10px; }
        .feature-item p { color: #94a3b8; font-size: 0.95em; }
        .feature-icon { font-size: 2.5em; margin-bottom: 15px; }

        /* --- FOOTER --- */
        footer { background: #0f172a; padding: 60px 5% 30px 5%; border-top: 1px solid #1e293b; text-align: center; }
        .footer-content { max-width: 800px; margin: 0 auto; }
        .footer-content p { color: #64748b; margin-bottom: 20px; }
        .footer-links { display: flex; justify-content: center; gap: 30px; margin-bottom: 30px; }
        .footer-links a { color: #94a3b8; text-decoration: none; transition: color 0.3s; }
        .footer-links a:hover { color: #38bdf8; }
        .copyright { color: #475569; font-size: 0.9em; }

        /* --- ANIMATIONS --- */
        @keyframes fadeUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

    <!-- NAVIGATION -->
    <nav>
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <div class="nav-links">
            <a href="#formations">Formations</a>
            <a href="#services">Services</a>
            <a href="#contact" class="btn-nav">Nous Contacter</a>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <header class="hero">
        <h1>Maîtrisez la Technologie avec <span>Jacob Tools</span></h1>
        <p>Apprenez le déblocage, le marketing digital et les systèmes d'exploitation grâce à des formations vidéo exclusives et des solutions professionnelles.</p>
        <div class="hero-btns">
            <a href="#formations" class="btn">Voir les formations</a>
            <a href="#services" class="btn btn-outline">Nos services</a>
        </div>
    </header>

    <!-- RUBRIQUES -->
    <section id="services">
        <h2 class="section-titre">Nos Domaines d'Expertise</h2>
        <p class="section-sous-titre">Découvrez nos pôles de compétences pour propulser vos projets et développer vos connaissances.</p>
        
        <div class="rubriques-grid">
            <div class="rubrique-card">
                <div class="rubrique-icon">📱</div>
                <h3>Déblocage Mobile</h3>
                <p>Apprenez à débloquer, flasher et réparer les smartphones en toute sécurité grâce à nos tutoriels exclusifs.</p>
            </div>
            <div class="rubrique-card">
                <div class="rubrique-icon">💻</div>
                <h3>Systèmes d'Exploitation</h3>
                <p>Formations complètes sur Windows, Linux et macOS : installation, optimisation et dépannage.</p>
            </div>
            <div class="rubrique-card">
                <div class="rubrique-icon">📈</div>
                <h3>Marketing Digital</h3>
                <p>Stratégies avancées pour vendre en ligne, créer un business et dominer les réseaux sociaux.</p>
            </div>
        </div>
    </section>

    <!-- CATALOGUE (CONTENUS DYNAMIQUES) -->
    <section id="formations" style="background: #0f172a;">
        <h2 class="section-titre">Nos Dernières Formations</h2>
        <p class="section-sous-titre">Des cours vidéo conçus par des experts pour vous mener vers la réussite.</p>
        
        <div class="content-grid">
            {% for item in contenus %}
            <div class="card">
                <div class="card-img">▶️</div>
                <div class="card-body">
                    <h3>{{ item.titre }}</h3>
                    <p>{{ item.description }}</p>
                    {% if item.lien %}
                    <a href="{{ item.lien }}" class="btn" target="_blank">Accéder à la formation</a>
                    {% else %}
                    <a href="#" class="btn" style="background: #334155; color: #94a3b8;">Bientôt disponible</a>
                    {% endif %}
                </div>
            </div>
            {% else %}
            <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 60px;">
                <div class="card-body" style="align-items: center;">
                    <h3 style="color: #38bdf8;">Aucune formation disponible</h3>
                    <p>Revenez bientôt pour découvrir de nouveaux cours exclusifs.</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- FEATURES -->
    <section>
        <h2 class="section-titre">Pourquoi choisir Jacob Tools ?</h2>
        <p class="section-sous-titre">Nous mettons la qualité et la pédagogie au cœur de nos formations.</p>
        
        <div class="features-grid">
            <div class="feature-item">
                <div class="feature-icon">🎥</div>
                <h3>Vidéos HD Exclusives</h3>
                <p>Apprenez avec des vidéos claires, animées et de haute qualité.</p>
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
                <a href="/">Accueil</a>
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

with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)
print("✅ Page d'accueil professionnelle creee avec succes !")
