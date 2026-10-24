import os
import json

# S'assurer que le fichier de données existe
if not os.path.exists('data.json'):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump([], f)

# ==========================================
# 1. MISE A JOUR DE APP.PY (On garde ce qui marche)
# ==========================================
app_py = """from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os, json, time

app = Flask(__name__)
app.secret_key = "jacob_tools_2026_secret"
ADMIN_URL = "/gestion-jacob-2026"
HASHED_PASSWORD = generate_password_hash("jacob123")
DATA_FILE = "data.json"

def lire_donnees():
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return []

def sauvegarder_donnees(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def accueil():
    return render_template('index.html', contenus=lire_donnees())

@app.route(ADMIN_URL, methods=['GET', 'POST'])
def admin():
    if session.get('logged_in'):
        return render_template('dashboard.html', contenus=lire_donnees(), modifier=None)
    if request.method == 'POST':
        if check_password_hash(HASHED_PASSWORD, request.form.get('password')):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', erreur="Mot de passe incorrect.")
    return render_template('login.html', erreur="")

@app.route(ADMIN_URL + '/ajouter', methods=['POST'])
def ajouter():
    if not session.get('logged_in'): return redirect(url_for('admin'))
    contenus = lire_donnees()
    contenus.append({
        'id': int(time.time() * 1000), 'titre': request.form.get('titre'),
        'image_url': request.form.get('image_url'), 'description': request.form.get('description'),
        'lien': request.form.get('lien'), 'categorie': request.form.get('categorie')
    })
    sauvegarder_donnees(contenus)
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/supprimer/<int:id>')
def supprimer(id):
    if not session.get('logged_in'): return redirect(url_for('admin'))
    sauvegarder_donnees([c for c in lire_donnees() if c.get('id') != id])
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    if not session.get('logged_in'): return redirect(url_for('admin'))
    contenus = lire_donnees()
    if request.method == 'POST':
        for c in contenus:
            if c.get('id') == id:
                c.update({'titre': request.form.get('titre'), 'image_url': request.form.get('image_url'),
                          'description': request.form.get('description'), 'lien': request.form.get('lien'),
                          'categorie': request.form.get('categorie')})
        sauvegarder_donnees(contenus)
        return redirect(url_for('admin'))
    contenu = next((c for c in contenus if c.get('id') == id), None)
    return render_template('dashboard.html', contenus=contenus, modifier=contenu)

@app.route(ADMIN_URL + '/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('accueil'))

if __name__ == '__main__':
    app.run(debug=True)
"""
with open('app.py', 'w', encoding='utf-8') as f: f.write(app_py)

# ==========================================
# 2. RECREATION DE L'ACCUEIL AVEC LE SLIDER ANIMÉ
# ==========================================
index_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jacob Tools - Formations</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background-color: #0b1120; color: #e2e8f0; overflow-x: hidden; }
        
        /* NAVIGATION */
        nav { display: flex; justify-content: space-between; align-items: center; padding: 15px 5%; background: rgba(11, 17, 32, 0.95); position: fixed; width: 100%; top: 0; z-index: 1000; border-bottom: 1px solid #1e293b; backdrop-filter: blur(10px); }
        .logo { font-size: 1.5em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; }
        .logo span { color: #38bdf8; }
        .nav-links a { color: #cbd5e1; text-decoration: none; margin-left: 25px; font-size: 0.95em; font-weight: 500; transition: 0.3s; }
        .nav-links a:hover { color: #38bdf8; }
        .btn-nav { background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120 !important; padding: 10px 25px; border-radius: 50px; font-weight: 700; }
        
        /* SLIDER (CARROUSEL) */
        .slider-container { position: relative; width: 100%; height: 70vh; overflow: hidden; background: #0f172a; margin-top: 60px; }
        .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; display: flex; align-items: center; justify-content: center; }
        .slide.active { opacity: 1; z-index: 1; }
        .slide img { width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0; opacity: 0.4; }
        .slide-content { position: relative; z-index: 2; text-align: center; max-width: 800px; padding: 30px; background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(8px); border-radius: 20px; border: 1px solid #334155; margin: 0 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        .slide-content h2 { font-size: 3em; color: white; margin-bottom: 15px; }
        .slide-content p { font-size: 1.1em; color: #cbd5e1; margin-bottom: 25px; }
        .slider-dots { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 10; display: flex; gap: 12px; }
        .dot { width: 12px; height: 12px; border-radius: 50%; background: #475569; cursor: pointer; transition: 0.3s; }
        .dot.active { background: #38bdf8; transform: scale(1.3); }

        /* BOUTONS ET SECTIONS */
        .btn { display: inline-block; padding: 14px 35px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120; text-decoration: none; border-radius: 50px; font-weight: 700; transition: 0.3s; border: none; cursor: pointer; }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(56, 189, 248, 0.4); }
        section { padding: 80px 5%; }
        .section-titre { text-align: center; font-size: 2.5em; color: white; margin-bottom: 50px; font-weight: 800; }
        
        /* GRILLE DE CONTENUS */
        .content-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; overflow: hidden; transition: 0.3s; display: flex; flex-direction: column; }
        .card:hover { transform: translateY(-8px); border-color: #38bdf8; box-shadow: 0 15px 30px rgba(0,0,0,0.4); }
        .card-img { height: 200px; width: 100%; object-fit: cover; }
        .card-body { padding: 25px; flex-grow: 1; display: flex; flex-direction: column; position: relative; }
        .card-body h3 { color: white; margin-bottom: 10px; font-size: 1.3em; }
        .card-body p { color: #94a3b8; font-size: 0.95em; margin-bottom: 25px; flex-grow: 1; }
        .badge { position: absolute; top: 15px; right: 15px; padding: 6px 15px; border-radius: 50px; font-size: 0.75em; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
        .bg-deblocage { background: #38bdf8; color: #0b1120; }
        .bg-systeme { background: #818cf8; color: white; }
        .bg-marketing { background: #f472b6; color: white; }
        
        footer { text-align: center; padding: 40px; border-top: 1px solid #1e293b; color: #64748b; font-size: 0.9em; }
        
        @media (max-width: 768px) {
            .nav-links { display: none; }
            .slide-content h2 { font-size: 2em; }
            .slider-container { height: 50vh; }
        }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <div class="nav-links">
            <a href="#formations">Formations</a>
            <a href="#services">Services</a>
            <a href="#contact" class="btn-nav">Contact</a>
        </div>
    </nav>

    <!-- SLIDER ANIMÉ -->
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
            <img src="https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1920&auto=format&fit=crop" alt="Système">
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

    <!-- FORMATIONS -->
    <section id="formations" style="background: #0f172a;">
        <h2 class="section-titre">Nos Dernières Formations</h2>
        <div class="content-grid">
            {% for item in contenus %}
            <div class="card">
                {% if item.categorie == 'Déblocage' %}<span class="badge bg-deblocage">{{ item.categorie }}</span>
                {% elif item.categorie == 'Système' %}<span class="badge bg-systeme">{{ item.categorie }}</span>
                {% else %}<span class="badge bg-marketing">{{ item.categorie }}</span>{% endif %}
                <img src="{{ item.image_url }}" class="card-img" alt="{{ item.titre }}" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">
                <div class="card-body">
                    <h3>{{ item.titre }}</h3>
                    <p>{{ item.description }}</p>
                    {% if item.lien %}<a href="{{ item.lien }}" class="btn" target="_blank">Regarder</a>
                    {% else %}<a href="#" class="btn" style="background: #334155; color: #94a3b8;">Bientôt disponible</a>{% endif %}
                </div>
            </div>
            {% else %}
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px; background: #1e293b; border-radius: 16px; border: 1px dashed #475569;">
                <h3 style="color: #38bdf8; margin-bottom: 10px;">Aucune formation pour le moment</h3>
                <p style="color: #94a3b8;">Connectez-vous à l'espace admin pour ajouter vos vidéos.</p>
            </div>
            {% endfor %}
        </div>
    </section>

    <footer id="contact">
        <p>Prêt à commencer votre transformation digitale ?</p>
        <div style="margin-top: 10px;">&copy; 2026 Jacob Tools. Tous droits réservés.</div>
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
        function nextSlide() { slideIndex = (slideIndex + 1) % slides.length; showSlide(slideIndex); }
        function currentSlide(n) { clearInterval(slideInterval); showSlide(n); slideInterval = setInterval(nextSlide, 5000); }
        slideInterval = setInterval(nextSlide, 5000);
    </script>
</body>
</html>"""
with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)

print("✅ Le Carrousel a ete remis en place sur l'accueil !")
