import os
import json

# ==========================================
# 1. NETTOYAGE DU FICHIER DE DONNEES
# ==========================================
# On remet le fichier data.json à zéro pour effacer les bugs
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump([], f)

# ==========================================
# 2. MISE A JOUR DE APP.PY (Ajout de la modification)
# ==========================================
app_py = """from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import time

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
        return render_template('dashboard.html', contenus=contenus, modifier=None)
    
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
    categorie = request.form.get('categorie')
    
    contenus = lire_donnees()
    nouvel_id = int(time.time() * 1000) # ID unique infaillible
    
    contenus.append({
        'id': nouvel_id, 'titre': titre, 'image_url': image_url,
        'description': description, 'lien': lien, 'categorie': categorie
    })
    sauvegarder_donnees(contenus)
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/supprimer/<int:id>')
def supprimer(id):
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    contenus = lire_donnees()
    # On garde tous les contenus SAUF celui avec l'ID
    contenus = [c for c in contenus if c.get('id') != id]
    sauvegarder_donnees(contenus)
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    contenus = lire_donnees()
    
    if request.method == 'POST':
        titre = request.form.get('titre')
        image_url = request.form.get('image_url')
        description = request.form.get('description')
        lien = request.form.get('lien')
        categorie = request.form.get('categorie')
        
        for c in contenus:
            if c.get('id') == id:
                c['titre'] = titre
                c['image_url'] = image_url
                c['description'] = description
                c['lien'] = lien
                c['categorie'] = categorie
                break
                
        sauvegarder_donnees(contenus)
        return redirect(url_for('admin'))
        
    # Si c'est un GET, on trouve le contenu à modifier et on l'envoie au template
    contenu_a_modifier = next((c for c in contenus if c.get('id') == id), None)
    return render_template('dashboard.html', contenus=contenus, modifier=contenu_a_modifier)

@app.route(ADMIN_URL + '/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('accueil'))

if __name__ == '__main__':
    app.run(debug=True)
"""
with open('app.py', 'w', encoding='utf-8') as f: f.write(app_py)


# ==========================================
# 3. NOUVEAU TABLEAU DE BORD (Bouton Modifier + Responsive)
# ==========================================
dashboard_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin - Jacob Tools</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; margin: 0; padding: 0; }
        body { background-color: #0b1120; color: #e2e8f0; display: flex; min-height: 100vh; }
        
        /* SIDEBAR */
        .sidebar { width: 260px; background-color: #0f172a; border-right: 1px solid #1e293b; padding: 30px 20px; display: flex; flex-direction: column; flex-shrink: 0; }
        .logo { font-size: 1.5em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; margin-bottom: 40px; text-align: center; }
        .logo span { color: #38bdf8; }
        .nav-item { display: block; padding: 12px 20px; color: #94a3b8; text-decoration: none; border-radius: 8px; margin-bottom: 10px; transition: 0.3s; font-weight: 500; background: transparent; border: none; width: 100%; text-align: left; cursor: pointer; font-size: 1em; }
        .nav-item:hover, .nav-item.active { background-color: #1e293b; color: #38bdf8; }
        .logout-btn { margin-top: auto; color: #f87171 !important; }
        .logout-btn:hover { background-color: rgba(248, 113, 113, 0.1) !important; }

        /* MAIN CONTENT */
        .main-content { flex: 1; padding: 40px; overflow-y: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .header h1 { color: white; font-size: 2em; }
        
        /* TABS */
        .tabs { display: flex; gap: 10px; margin-bottom: 30px; background: #0f172a; padding: 5px; border-radius: 10px; border: 1px solid #1e293b; display: inline-flex; }
        .tab-btn { padding: 12px 25px; background: transparent; border: none; color: #94a3b8; font-weight: 600; font-size: 1em; cursor: pointer; border-radius: 8px; transition: 0.3s; }
        .tab-btn.active { background: #1e293b; color: #38bdf8; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }

        /* SECTIONS */
        .tab-content { display: none; animation: fadeIn 0.4s; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* CARDS & FORMULAIRE */
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .card h2 { color: #38bdf8; font-size: 1.3em; margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 15px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #cbd5e1; font-size: 0.9em; font-weight: 500; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 14px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; font-family: inherit; font-size: 1em; }
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus { outline: none; border-color: #38bdf8; box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.1); }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        button.btn-submit { width: 100%; padding: 16px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120; border: none; border-radius: 8px; font-weight: 700; font-size: 1.1em; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        button.btn-submit:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(56, 189, 248, 0.4); }

        /* LISTE DES CONTENUS */
        .content-list { display: flex; flex-direction: column; gap: 15px; }
        .content-item { display: flex; align-items: center; background: #0f172a; padding: 15px; border-radius: 12px; border: 1px solid #1e293b; flex-wrap: wrap; gap: 15px; }
        .content-item img { width: 100px; height: 70px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }
        .content-info { flex: 1; min-width: 200px; }
        .content-info h3 { color: white; font-size: 1.1em; margin-bottom: 5px; }
        .content-info p { color: #94a3b8; font-size: 0.85em; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 50px; font-size: 0.75em; font-weight: 600; margin-top: 8px; }
        .badge-deblocage { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
        .badge-systeme { background: rgba(129, 140, 248, 0.2); color: #818cf8; }
        .badge-marketing { background: rgba(244, 114, 182, 0.2); color: #f472b6; }
        
        .actions { display: flex; gap: 10px; }
        .btn-edit { background: rgba(56, 189, 248, 0.1); color: #38bdf8; padding: 10px 15px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9em; transition: 0.3s; }
        .btn-edit:hover { background: rgba(56, 189, 248, 0.2); }
        .btn-delete { background: rgba(248, 113, 113, 0.1); color: #f87171; padding: 10px 15px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9em; transition: 0.3s; }
        .btn-delete:hover { background: rgba(248, 113, 113, 0.2); }

        /* RESPONSIVE ADMIN */
        @media (max-width: 768px) {
            body { flex-direction: column; }
            .sidebar { width: 100%; padding: 20px; flex-direction: row; flex-wrap: wrap; justify-content: center; gap: 10px; }
            .logo { width: 100%; margin-bottom: 10px; }
            .nav-item { width: auto; padding: 10px; font-size: 0.9em; }
            .logout-btn { margin-top: 0; }
            .main-content { padding: 20px; }
            .form-row { grid-template-columns: 1fr; }
            .content-item { flex-direction: column; align-items: flex-start; }
            .content-item img { width: 100%; height: 150px; }
        }
    </style>
</head>
<body>

    <!-- SIDEBAR -->
    <div class="sidebar">
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <button class="nav-item active" onclick="openTab('list')">📋 Gestion</button>
        <button class="nav-item" onclick="openTab('add')">➕ Ajouter</button>
        <a href="/" class="nav-item" target="_blank">🌐 Voir le site</a>
        <a href="/gestion-jacob-2026/logout" class="nav-item logout-btn">🚪 Déconnexion</a>
    </div>

    <!-- MAIN CONTENT -->
    <div class="main-content">
        <div class="header">
            <h1 id="page-title">Liste des contenus</h1>
        </div>

        <!-- ONGLET 1 : LISTE -->
        <div id="tab-list" class="tab-content active">
            <div class="card">
                <h2>Toutes vos vidéos ({{ contenus|length }})</h2>
                <div class="content-list">
                    {% for item in contenus %}
                    <div class="content-item">
                        <img src="{{ item.image_url }}" alt="{{ item.titre }}" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">
                        <div class="content-info">
                            <h3>{{ item.titre }}</h3>
                            <p>{{ item.description[:80] }}...</p>
                            {% if item.categorie == 'Déblocage' %}
                            <span class="badge badge-deblocage">{{ item.categorie }}</span>
                            {% elif item.categorie == 'Système' %}
                            <span class="badge badge-systeme">{{ item.categorie }}</span>
                            {% else %}
                            <span class="badge badge-marketing">{{ item.categorie }}</span>
                            {% endif %}
                        </div>
                        <div class="actions">
                            <a href="/gestion-jacob-2026/modifier/{{ item.id }}" class="btn-edit">Modifier</a>
                            <a href="/gestion-jacob-2026/supprimer/{{ item.id }}" class="btn-delete" onclick="return confirm('Supprimer ce contenu ?')">Supprimer</a>
                        </div>
                    </div>
                    {% else %}
                    <p style="text-align: center; color: #64748b; padding: 20px;">Aucun contenu.</p>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- ONGLET 2 : AJOUTER / MODIFIER -->
        <div id="tab-add" class="tab-content {% if modifier %}active{% endif %}">
            <div class="card">
                {% if modifier %}
                <h2>Modifier la formation</h2>
                <form method="POST" action="/gestion-jacob-2026/modifier/{{ modifier.id }}">
                {% else %}
                <h2>Publier une nouvelle formation</h2>
                <form method="POST" action="/gestion-jacob-2026/ajouter">
                {% endif %}
                    <div class="form-row">
                        <div class="form-group">
                            <label>Titre</label>
                            <input type="text" name="titre" value="{{ modifier.titre if modifier else '' }}" required>
                        </div>
                        <div class="form-group">
                            <label>Catégorie</label>
                            <select name="categorie" required>
                                <option value="Déblocage" {% if modifier and modifier.categorie == 'Déblocage' %}selected{% endif %}>Déblocage Mobile</option>
                                <option value="Système" {% if modifier and modifier.categorie == 'Système' %}selected{% endif %}>Systèmes d'Exploitation</option>
                                <option value="Marketing" {% if modifier and modifier.categorie == 'Marketing' %}selected{% endif %}>Marketing Digital</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Lien de l'image</label>
                        <input type="url" name="image_url" value="{{ modifier.image_url if modifier else '' }}" required>
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <textarea name="description" required rows="3">{{ modifier.description if modifier else '' }}</textarea>
                    </div>
                    <div class="form-group">
                        <label>Lien vidéo</label>
                        <input type="url" name="lien" value="{{ modifier.lien if modifier else '' }}">
                    </div>
                    <button type="submit" class="btn-submit">{% if modifier %}Mettre à jour{% else %}Publier{% endif %}</button>
                </form>
            </div>
        </div>
    </div>

    <script>
        function openTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));
            document.getElementById('tab-' + tabName).classList.add('active');
            
            if(tabName === 'list') {
                document.querySelectorAll('.nav-item')[0].classList.add('active');
                document.getElementById('page-title').innerText = "Liste des contenus";
            } else {
                document.querySelectorAll('.nav-item')[1].classList.add('active');
                document.getElementById('page-title').innerText = "Ajouter un contenu";
            }
        }
    </script>
</body>
</html>"""
with open('templates/dashboard.html', 'w', encoding='utf-8') as f: f.write(dashboard_html)


# ==========================================
# 4. MISE A JOUR DE L'ACCUEIL (100% RESPONSIVE POUR MOBILE)
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
        
        /* NAVIGATION (Responsive) */
        nav { display: flex; justify-content: space-between; align-items: center; padding: 15px 5%; background: rgba(11, 17, 32, 0.95); position: fixed; width: 100%; top: 0; z-index: 1000; border-bottom: 1px solid #1e293b; backdrop-filter: blur(10px); }
        .logo { font-size: 1.5em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; }
        .logo span { color: #38bdf8; }
        .nav-links { display: flex; gap: 20px; align-items: center; }
        .nav-links a { color: #cbd5e1; text-decoration: none; font-weight: 500; transition: color 0.3s; font-size: 0.9em; }
        .nav-links a:hover { color: #38bdf8; }
        .btn-nav { background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120 !important; padding: 8px 20px; border-radius: 50px; font-weight: 700 !important; }

        /* SLIDER (Responsive) */
        .slider-container { position: relative; width: 100%; height: 60vh; overflow: hidden; background: #0f172a; margin-top: 60px; }
        .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out; display: flex; align-items: center; justify-content: center; }
        .slide.active { opacity: 1; z-index: 1; }
        .slide img { width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0; opacity: 0.4; }
        .slide-content { position: relative; z-index: 2; text-align: center; max-width: 800px; padding: 20px; background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(5px); border-radius: 20px; border: 1px solid #334155; margin: 0 20px; }
        .slide-content h2 { font-size: 2.5em; color: white; margin-bottom: 15px; line-height: 1.2; }
        .slide-content p { font-size: 1em; color: #cbd5e1; margin-bottom: 20px; }
        .btn { display: inline-block; padding: 12px 25px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120; text-decoration: none; border-radius: 50px; font-weight: 700; font-size: 0.9em; transition: all 0.3s; text-align: center; border: none; cursor: pointer; }
        
        .slider-dots { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); z-index: 10; display: flex; gap: 10px; }
        .dot { width: 10px; height: 10px; border-radius: 50%; background: #475569; cursor: pointer; transition: 0.3s; }
        .dot.active { background: #38bdf8; transform: scale(1.2); }

        section { padding: 60px 5%; }
        .section-titre { text-align: center; font-size: 2em; margin-bottom: 30px; color: white; font-weight: 800; }

        /* RUBRIQUES (Responsive) */
        .rubriques-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .rubrique-card { background: #1e293b; border-radius: 20px; overflow: hidden; border: 1px solid #334155; transition: all 0.4s; }
        .rubrique-card:hover { transform: translateY(-5px); border-color: #38bdf8; }
        .rubrique-img { width: 100%; height: 180px; object-fit: cover; }
        .rubrique-content { padding: 20px; text-align: center; }
        .rubrique-content h3 { color: #38bdf8; font-size: 1.3em; margin-bottom: 10px; }
        .rubrique-content p { color: #94a3b8; font-size: 0.9em; }

        /* CATALOGUE (Responsive) */
        .content-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; max-width: 1200px; margin: 0 auto; }
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; overflow: hidden; transition: transform 0.3s, border-color 0.3s; display: flex; flex-direction: column; }
        .card:hover { transform: translateY(-5px); border-color: #38bdf8; }
        .card-img { height: 180px; width: 100%; object-fit: cover; border-bottom: 1px solid #334155; }
        .card-body { padding: 20px; display: flex; flex-direction: column; flex-grow: 1; position: relative; }
        .card-body h3 { color: white; font-size: 1.2em; margin-bottom: 10px; }
        .card-body p { color: #94a3b8; font-size: 0.9em; flex-grow: 1; margin-bottom: 15px; }

        .badge-cat { position: absolute; top: 15px; right: 15px; padding: 5px 12px; border-radius: 50px; font-size: 0.7em; font-weight: 700; text-transform: uppercase; }
        .bg-deblocage { background: #38bdf8; color: #0b1120; }
        .bg-systeme { background: #818cf8; color: white; }
        .bg-marketing { background: #f472b6; color: white; }

        footer { background: #0f172a; padding: 40px 5%; border-top: 1px solid #1e293b; text-align: center; }
        .copyright { color: #475569; font-size: 0.85em; }

        /* MEDIA QUERIES POUR MOBILE */
        @media (max-width: 768px) {
            .nav-links { display: none; } /* On cache le menu sur petit écran (on fera un menu burger plus tard) */
            .slider-container { height: 50vh; }
            .slide-content h2 { font-size: 1.8em; }
            .section-titre { font-size: 1.5em; }
            .content-grid { grid-template-columns: 1fr; }
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

    <section id="services">
        <h2 class="section-titre">Nos Domaines d'Expertise</h2>
        <div class="rubriques-grid">
            <div class="rubrique-card">
                <img src="https://images.unsplash.com/photo-1592890288564-76628a30a657?q=80&w=800&auto=format&fit=crop" class="rubrique-img" alt="Déblocage Mobile">
                <div class="rubrique-content">
                    <h3>Déblocage Mobile</h3>
                    <p>Apprenez à débloquer, flasher et réparer les smartphones.</p>
                </div>
            </div>
            <div class="rubrique-card">
                <img src="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=800&auto=format&fit=crop" class="rubrique-img" alt="Systèmes d'Exploitation">
                <div class="rubrique-content">
                    <h3>Systèmes d'Exploitation</h3>
                    <p>Formations complètes sur Windows, Linux et macOS.</p>
                </div>
            </div>
            <div class="rubrique-card">
                <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=800&auto=format&fit=crop" class="rubrique-img" alt="Marketing Digital">
                <div class="rubrique-content">
                    <h3>Marketing Digital</h3>
                    <p>Stratégies avancées pour vendre en ligne et créer un business.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="formations" style="background: #0f172a;">
        <h2 class="section-titre">Nos Dernières Formations</h2>
        <div class="content-grid">
            {% for item in contenus %}
            <div class="card">
                {% if item.categorie == 'Déblocage' %}
                <span class="badge-cat bg-deblocage">{{ item.categorie }}</span>
                {% elif item.categorie == 'Système' %}
                <span class="badge-cat bg-systeme">{{ item.categorie }}</span>
                {% else %}
                <span class="badge-cat bg-marketing">{{ item.categorie }}</span>
                {% endif %}
                
                <img src="{{ item.image_url }}" class="card-img" alt="{{ item.titre }}" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">
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
            <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                <div class="card-body" style="align-items: center;">
                    <h3 style="color: #38bdf8;">Aucune formation pour le moment</h3>
                    <p>Ajoutez vos vidéos depuis l'espace admin.</p>
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

        function nextSlide() { slideIndex = (slideIndex + 1) % slides.length; showSlide(slideIndex); }
        function currentSlide(n) { clearInterval(slideInterval); showSlide(n); slideInterval = setInterval(nextSlide, 5000); }
        slideInterval = setInterval(nextSlide, 5000);
    </script>
</body>
</html>"""

with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)

print("✅ Mise a jour reussie : Nettoyage, bouton Modifier, et Responsive Mobile ajoutes !")
