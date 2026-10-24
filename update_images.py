index_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jacob Tools - Formations & Solutions Digitales</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        html { scroll-behavior: smooth; }
        body { background-color: #0b1120; color: #e2e8f0; line-height: 1.6; overflow-x: hidden; }
        
        /* NAVIGATION */
        nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 5%; background: rgba(11, 17, 32, 0.95); position: fixed; width: 100%; top: 0; z-index: 1000; border-bottom: 1px solid #1e293b; backdrop-filter: blur(10px); }
        .logo { font-size: 1.8em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; }
        .logo span { color: #38bdf8; }
        .nav-links { display: flex; gap: 30px; align-items: center; }
        .nav-links a { color: #cbd5e1; text-decoration: none; font-weight: 500; transition: color 0.3s; font-size: 0.95em; }
        .nav-links a:hover { color: #38bdf8; }
        .btn-nav { background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120 !important; padding: 10px 25px; border-radius: 50px; font-weight: 700 !important; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3); }
        
        /* SLIDER ANIMÉ */
        .slider-container { position: relative; width: 100%; height: 70vh; overflow: hidden; background: #0f172a; margin-top: 70px; }
        .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; display: flex; align-items: center; justify-content: center; }
        .slide.active { opacity: 1; z-index: 1; }
        .slide img { width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0; opacity: 0.4; }
        .slide-content { position: relative; z-index: 2; text-align: center; max-width: 800px; padding: 20px; background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(5px); border-radius: 20px; border: 1px solid #334155; }
        .slide-content h2 { font-size: 3em; color: white; margin-bottom: 15px; }
        .slide-content p { font-size: 1.2em; color: #cbd5e1; margin-bottom: 25px; }
        .slider-dots { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 10; display: flex; gap: 10px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; background: #475569; cursor: pointer; transition: 0.3s; }
        .dot.active { background: #38bdf8; transform: scale(1.2); }

        /* SECTIONS */
        section { padding: 100px 5%; }
        .section-titre { text-align: center; font-size: 2.8em; margin-bottom: 15px; color: white; font-weight: 800; }
        .section-sous-titre { text-align: center; color: #94a3b8; font-size: 1.1em; max-width: 600px; margin: 0 auto 60px auto; }

        /* RUBRIQUES (AVEC VRAIES IMAGES) */
        .rubriques-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .rubrique-card { background: #1e293b; border-radius: 20px; overflow: hidden; border: 1px solid #334155; transition: all 0.4s; display: flex; flex-direction: column; }
        .rubrique-card:hover { transform: translateY(-10px); border-color: #38bdf8; box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
        .rubrique-img { width: 100%; height: 200px; object-fit: cover; border-bottom: 1px solid #334155; }
        .rubrique-content { padding: 30px; text-align: center; flex-grow: 1; }
        .rubrique-content h3 { color: #38bdf8; font-size: 1.5em; margin-bottom: 15px; }
        .rubrique-content p { color: #94a3b8; font-size: 0.95em; }

        /* CATALOGUE DYNAMIQUE */
        .content-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; overflow: hidden; transition: transform 0.3s, border-color 0.3s; display: flex; flex-direction: column; }
        .card:hover { transform: translateY(-5px); border-color: #38bdf8; box-shadow: 0 15px 30px rgba(0,0,0,0.5); }
        .card-img { height: 200px; width: 100%; object-fit: cover; border-bottom: 1px solid #334155; }
        .card-body { padding: 25px; display: flex; flex-direction: column; flex-grow: 1; }
        .card-body h3 { color: white; font-size: 1.3em; margin-bottom: 10px; }
        .card-body p { color: #94a3b8; font-size: 0.95em; flex-grow: 1; margin-bottom: 20px; }
        .btn { display: inline-block; padding: 15px 35px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120; text-decoration: none; border-radius: 50px; font-weight: 700; font-size: 1em; transition: all 0.3s; text-align: center; border: none; cursor: pointer; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(56, 189, 248, 0.6); }

        /* FOOTER */
        footer { background: #0f172a; padding: 60px 5% 30px 5%; border-top: 1px solid #1e293b; text-align: center; }
        .copyright { color: #475569; font-size: 0.9em; margin-top: 20px; }
    </style>
</head>
<body>

    <nav>
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <div class="nav-links">
            <a href="#formations">Formations</a>
            <a href="#services">Services</a>
            <a href="#contact" class="btn-nav">Nous Contacter</a>
        </div>
    </nav>

    <!-- SLIDER -->
    <div class="slider-container">
        <div class="slide active">
            <img src="https://images.unsplash.com/photo-1611162617474-5b21e879e113?q=80&w=1920&auto=format&fit=crop" alt="Déblocage">
            <div class="slide-content">
                <h2>Maîtrisez le Déblocage Mobile</h2>
                <p>Apprenez les techniques secrètes pour débloquer tous les smartphones.</p>
                <a href="#formations" class="btn">Voir la formation</a>
            </div>
        </div>
        <div class="slide">
            <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1920&auto=format&fit=crop" alt="Système d'exploitation">
            <div class="slide-content">
                <h2>Dominez les Systèmes d'Exploitation</h2>
                <p>Windows, Linux, Mac : devenez un expert en installation et dépannage.</p>
                <a href="#formations" class="btn">Voir la formation</a>
            </div>
        </div>
        <div class="slide">
            <img src="https://images.unsplash.com/photo-1557838923-2985c318be48?q=80&w=1920&auto=format&fit=crop" alt="Marketing">
            <div class="slide-content">
                <h2>Boostez votre Business en Ligne</h2>
                <p>Les stratégies marketing les plus puissantes pour vendre dès aujourd'hui.</p>
                <a href="#formations" class="btn">Voir la formation</a>
            </div>
        </div>
        <div class="slider-dots">
            <div class="dot active" onclick="currentSlide(0)"></div>
            <div class="dot" onclick="currentSlide(1)"></div>
            <div class="dot" onclick="currentSlide(2)"></div>
        </div>
    </div>

    <!-- RUBRIQUES AVEC IMAGES -->
    <section id="services">
        <h2 class="section-titre">Nos Domaines d'Expertise</h2>
        <div class="rubriques-grid">
            <!-- Rubrique 1 -->
            <div class="rubrique-card">
                <img src="https://images.unsplash.com/photo-1592890288564-76628a30a657?q=80&w=800&auto=format&fit=crop" class="rubrique-img" alt="Déblocage Mobile">
                <div class="rubrique-content">
                    <h3>Déblocage Mobile</h3>
                    <p>Apprenez à débloquer, flasher et réparer les smartphones.</p>
                </div>
            </div>
            <!-- Rubrique 2 -->
            <div class="rubrique-card">
                <img src="https://images.unsplash.com/photo-1629654297299-c8506221ca3b?q=80&w=800&auto=format&fit=crop" class="rubrique-img" alt="Systèmes d'Exploitation">
                <div class="rubrique-content">
                    <h3>Systèmes d'Exploitation</h3>
                    <p>Formations complètes sur Windows, Linux et macOS.</p>
                </div>
            </div>
            <!-- Rubrique 3 -->
            <div class="rubrique-card">
                <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800&auto=format&fit=crop" class="rubrique-img" alt="Marketing Digital">
                <div class="rubrique-content">
                    <h3>Marketing Digital</h3>
                    <p>Stratégies avancées pour vendre en ligne et créer un business.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- CATALOGUE DYNAMIQUE -->
    <section id="formations" style="background: #0f172a;">
        <h2 class="section-titre">Nos Dernières Formations</h2>
        <div class="content-grid">
            {% for item in contenus %}
            <div class="card">
                <img src="{{ item.image_url }}" class="card-img" alt="{{ item.titre }}" onerror="this.src='https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=800'">
                <div class="card-body">
                    <h3>{{ item.titre }}</h3>
                    <p>{{ item.description }}</p>
                    {% if item.lien %}
                    <a href="{{ item.lien }}" class="btn" target="_blank">Regarder</a>
                    {% else %}
                    <a href="#" class="btn" style="background: #334155; color: #94a3b8;">Bientôt</a>
                    {% endif %}
                </div>
            </div>
            {% else %}
            <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 60px;">
                <div class="card-body" style="align-items: center;">
                    <h3 style="color: #38bdf8;">Aucune formation pour le moment</h3>
                    <p>Connectez-vous à l'espace admin pour ajouter des vidéos et leurs images !</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <footer id="contact">
        <p>Prêt à commencer votre transformation digitale ?</p>
        <div class="copyright">&copy; 2026 Jacob Tools. Tous droits réservés.</div>
    </footer>

    <script>
        let slideIndex = 0;
        const slides = document.querySelectorAll('.slide');
        const dots = document.querySelectorAll('.dot');
        let slideInterval;

        function showSlide(n) {
            slides.forEach(s => s.classList.remove('active'));
            dots.forEach(d => d.classList.remove('active'));
            slides[n].classList.add('active');
            dots[n].classList.add('active');
            slideIndex = n;
        }

        function nextSlide() {
            slideIndex = (slideIndex + 1) % slides.length;
            showSlide(slideIndex);
        }

        function currentSlide(n) {
            clearInterval(slideInterval);
            showSlide(n);
            slideInterval = setInterval(nextSlide, 5000);
        }

        slideInterval = setInterval(nextSlide, 5000);
    </script>
</body>
</html>"""

with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)
print("✅ Les rubriques ont maintenant de vraies images professionnelles !")
