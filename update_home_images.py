import os

# ==========================================
# 1. MISE A JOUR DU TABLEAU DE BORD (DASHBOARD.HTML)
# ==========================================
dashboard_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Tableau de bord - Jacob Tools</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background-color: #0b1120; color: #e2e8f0; padding: 30px; }
        h1, h2 { color: #38bdf8; }
        .card { background-color: #1e293b; padding: 30px; border-radius: 12px; margin-bottom: 20px; max-width: 800px; margin-left: auto; margin-right: auto; border: 1px solid #334155; box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        input, textarea { width: 100%; padding: 14px; margin: 10px 0; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; font-family: inherit; }
        input:focus, textarea:focus { outline: none; border-color: #38bdf8; }
        button { padding: 14px 30px; background-color: #38bdf8; color: #0f172a; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.3s; font-size: 1em; }
        button:hover { background-color: #0ea5e9; }
        a { color: #38bdf8; text-decoration: none; transition: 0.3s; }
        a:hover { color: #0ea5e9; }
        ul { list-style-type: none; padding: 0; }
        li { background-color: #0f172a; padding: 20px; margin-bottom: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #38bdf8; }
        .danger { color: #f87171; cursor: pointer; font-weight: 600; font-size: 0.9em; }
        .nav-links { text-align: center; margin-top: 30px; }
        .nav-links a { margin: 0 15px; font-weight: 600; }
    </style>
</head>
<body>
    <h1 style="text-align: center; margin-bottom: 30px;">Tableau de bord Admin</h1>
    <div class="card">
        <h2>Ajouter une vidéo / formation</h2>
        <form method="POST" action="/gestion-jacob-2026/ajouter">
            <input type="text" name="titre" placeholder="Titre (ex: Déblocage iPhone)" required>
            <input type="text" name="image_url" placeholder="Lien de l'image (ex: https://exemple.com/image.jpg)" required>
            <textarea name="description" placeholder="Description courte" required rows="3"></textarea>
            <input type="text" name="lien" placeholder="Lien de la vidéo (YouTube, etc.)">
            <button type="submit">Publier</button>
        </form>
    </div>
    <div class="card">
        <h2>Vos contenus actuels</h2>
        <ul>
            {% for item in contenus %}
            <li>
                <div>
                    <strong style="color: #38bdf8; font-size: 1.1em;">{{ item.titre }}</strong><br>
                    <span style="font-size: 0.9em; color: #94a3b8;">{{ item.description }}</span>
                </div>
                <a href="/gestion-jacob-2026/supprimer/{{ item.id }}" class="danger">Supprimer</a>
            </li>
            {% else %}
            <li style="justify-content: center; border-left: none; color: #64748b;">Aucun contenu enregistré.</li>
            {% endfor %}
        </ul>
    </div>
    <div class="nav-links">
        <a href="/">← Retour au site</a>
        <a href="/gestion-jacob-2026/logout">Se déconnecter</a>
    </div>
</body>
</html>"""

with open('templates/dashboard.html', 'w', encoding='utf-8') as f: f.write(dashboard_html)

# ==========================================
# 2. MISE A JOUR DE APP.PY (Ajout de la gestion d'image)
# ==========================================
app_py = """from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__)
app.secret_key = "jacob_tools_ultra_secret_2026_x89f"

ADMIN_URL = "/gestion-jacob-2026"
HASHED_PASSWORD = generate_password_hash("jacob123")
DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def lire_donnees():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def sauvegarder_donnees(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def accueil():
    contenus = lire_donnees()
    return render_template('index.html', contenus=contenus)

@app.route(ADMIN_URL, methods=['GET', 'POST'])
def admin():
    if session.get('logged_in'):
        contenus = lire_donnees()
        return render_template('dashboard.html', contenus=contenus)
    
    if request.method == 'POST':
        mot_de_passe = request.form.get('password')
        if check_password_hash(HASHED_PASSWORD, mot_de_passe):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', erreur="Mot de passe incorrect.")
            
    return render_template('login.html', erreur="")

@app.route(ADMIN_URL + '/ajouter', methods=['POST'])
def ajouter():
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    titre = request.form.get('titre')
    image_url = request.form.get('image_url')
    description = request.form.get('description')
    lien = request.form.get('lien')
    
    contenus = lire_donnees()
    contenus.append({
        'id': len(contenus) + 1, 
        'titre': titre, 
        'image_url': image_url,
        'description': description, 
        'lien': lien
    })
    sauvegarder_donnees(contenus)
    
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/supprimer/<int:id>')
def supprimer(id):
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    contenus = lire_donnees()
    contenus = [c for c in contenus if c.get('id') != id]
    sauvegarder_donnees(contenus)
        
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('accueil'))

if __name__ == '__main__':
    app.run(debug=True)
"""
with open('app.py', 'w', encoding='utf-8') as f: f.write(app_py)

# ==========================================
# 3. MISE A JOUR DE LA PAGE D'ACCUEIL (SLIDER + IMAGES)
# ==========================================
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
        
        /* SLIDER ANIMÉ (VIDEOS EN VEDETTE) */
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

        /* RUBRIQUES */
        .rubriques-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .rubrique-card { background: #1e293b; padding: 40px 30px; border-radius: 20px; text-align: center; border: 1px solid #334155; transition: all 0.4s; }
        .rubrique-card:hover { transform: translateY(-10px); border-color: #38bdf8; box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
        .rubrique-icon { font-size: 3em; margin-bottom: 20px; }
        .rubrique-card h3 { color: #38bdf8; font-size: 1.4em; margin-bottom: 10px; }

        /* CATALOGUE (IMAGES REELLES) */
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

    <!-- SLIDER (3 VIDEOS EN VEDETTE) -->
    <div class="slider-container">
        <!-- Slide 1 -->
        <div class="slide active">
            <img src="https://images.unsplash.com/photo-1611162617474-5b21e879e113?q=80&w=1920&auto=format&fit=crop" alt="Déblocage">
            <div class="slide-content">
                <h2>Maîtrisez le Déblocage Mobile</h2>
                <p>Apprenez les techniques secrètes pour débloquer tous les smartphones.</p>
                <a href="#formations" class="btn">Voir la formation</a>
            </div>
        </div>
        <!-- Slide 2 -->
        <div class="slide">
            <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1920&auto=format&fit=crop" alt="Système d'exploitation">
            <div class="slide-content">
                <h2>Dominez les Systèmes d'Exploitation</h2>
                <p>Windows, Linux, Mac : devenez un expert en installation et dépannage.</p>
                <a href="#formations" class="btn">Voir la formation</a>
            </div>
        </div>
        <!-- Slide 3 -->
        <div class="slide">
            <img src="https://images.unsplash.com/photo-1557838923-2985c318be48?q=80&w=1920&auto=format&fit=crop" alt="Marketing">
            <div class="slide-content">
                <h2>Boostez votre Business en Ligne</h2>
                <p>Les stratégies marketing les plus puissantes pour vendre dès aujourd'hui.</p>
                <a href="#formations" class="btn">Voir la formation</a>
            </div>
        </div>
        <!-- Points de navigation -->
        <div class="slider-dots">
            <div class="dot active" onclick="currentSlide(0)"></div>
            <div class="dot" onclick="currentSlide(1)"></div>
            <div class="dot" onclick="currentSlide(2)"></div>
        </div>
    </div>

    <!-- RUBRIQUES -->
    <section id="services">
        <h2 class="section-titre">Nos Domaines d'Expertise</h2>
        <div class="rubriques-grid">
            <div class="rubrique-card">
                <div class="rubrique-icon">📱</div>
                <h3>Déblocage Mobile</h3>
                <p>Apprenez à débloquer, flasher et réparer les smartphones.</p>
            </div>
            <div class="rubrique-card">
                <div class="rubrique-icon">💻</div>
                <h3>Systèmes d'Exploitation</h3>
                <p>Formations complètes sur Windows, Linux et macOS.</p>
            </div>
            <div class="rubrique-card">
                <div class="rubrique-icon">📈</div>
                <h3>Marketing Digital</h3>
                <p>Stratégies avancées pour vendre en ligne et créer un business.</p>
            </div>
        </div>
    </section>

    <!-- CATALOGUE DYNAMIQUE -->
    <section id="formations" style="background: #0f172a;">
        <h2 class="section-titre">Nos Dernières Formations</h2>
        <div class="content-grid">
            {% for item in contenus %}
            <div class="card">
                <!-- L'image de la vidéo apparaît ici -->
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

    <!-- SCRIPT POUR LE SLIDER -->
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

        // Lancer le défilement automatique
        slideInterval = setInterval(nextSlide, 5000);
    </script>
</body>
</html>"""

with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)

print("✅ Slider, images reelles et espace admin mis a jour avec succes !")
