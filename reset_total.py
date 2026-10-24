import os
import json

# ==========================================
# 1. RECREATION DE APP.PY (Le cerveau du site)
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
# 2. RECREATION DE L'ACCUEIL (Design Pro + Mobile)
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
        nav { display: flex; justify-content: space-between; align-items: center; padding: 15px 5%; background: rgba(11, 17, 32, 0.95); position: fixed; width: 100%; top: 0; z-index: 1000; border-bottom: 1px solid #1e293b; }
        .logo { font-size: 1.5em; font-weight: 800; color: white; text-decoration: none; }
        .logo span { color: #38bdf8; }
        .nav-links a { color: #cbd5e1; text-decoration: none; margin-left: 20px; font-size: 0.9em; }
        .btn-nav { background: #38bdf8; color: #0b1120 !important; padding: 8px 20px; border-radius: 50px; font-weight: 700; }
        
        .hero { padding: 150px 20px 80px; text-align: center; background: radial-gradient(circle at top, #1e293b, #0b1120); }
        .hero h1 { font-size: 3em; color: white; margin-bottom: 20px; }
        .hero h1 span { color: #38bdf8; }
        .hero p { font-size: 1.1em; color: #94a3b8; margin-bottom: 30px; max-width: 600px; margin-left: auto; margin-right: auto; }
        .btn { display: inline-block; padding: 12px 30px; background: #38bdf8; color: #0b1120; text-decoration: none; border-radius: 50px; font-weight: 700; transition: 0.3s; }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(56, 189, 248, 0.3); }

        section { padding: 60px 5%; }
        .section-titre { text-align: center; font-size: 2em; color: white; margin-bottom: 40px; }
        
        .content-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; max-width: 1200px; margin: 0 auto; }
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; overflow: hidden; transition: 0.3s; display: flex; flex-direction: column; }
        .card:hover { transform: translateY(-5px); border-color: #38bdf8; }
        .card-img { height: 180px; width: 100%; object-fit: cover; }
        .card-body { padding: 20px; flex-grow: 1; display: flex; flex-direction: column; position: relative; }
        .card-body h3 { color: white; margin-bottom: 10px; font-size: 1.2em; }
        .card-body p { color: #94a3b8; font-size: 0.9em; margin-bottom: 20px; flex-grow: 1; }
        .badge { position: absolute; top: 15px; right: 15px; padding: 5px 12px; border-radius: 50px; font-size: 0.7em; font-weight: 700; text-transform: uppercase; }
        .bg-deblocage { background: #38bdf8; color: #0b1120; }
        .bg-systeme { background: #818cf8; color: white; }
        .bg-marketing { background: #f472b6; color: white; }
        
        footer { text-align: center; padding: 40px; border-top: 1px solid #1e293b; color: #64748b; font-size: 0.9em; }
        
        @media (max-width: 768px) {
            .nav-links { display: none; }
            .hero h1 { font-size: 2em; }
        }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <div class="nav-links">
            <a href="#formations">Formations</a>
            <a href="#contact" class="btn-nav">Contact</a>
        </div>
    </nav>

    <header class="hero">
        <h1>Bienvenue sur <span>Jacob Tools</span></h1>
        <p>Apprenez le déblocage, les systèmes d'exploitation et le marketing digital avec des experts.</p>
        <a href="#formations" class="btn">Découvrir les cours</a>
    </header>

    <section id="formations" style="background: #0f172a;">
        <h2 class="section-titre">Nos Formations</h2>
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
                    {% else %}<a href="#" class="btn" style="background: #334155; color: #94a3b8;">Bientôt</a>{% endif %}
                </div>
            </div>
            {% else %}
            <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
                <h3 style="color: #38bdf8;">Aucune formation</h3>
                <p>Ajoutez vos vidéos depuis l'espace admin.</p>
            </div>
            {% endfor %}
        </div>
    </section>
    <footer id="contact">&copy; 2026 Jacob Tools. Tous droits réservés.</footer>
</body>
</html>"""
with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)

# ==========================================
# 3. RECREATION DU TABLEAU DE BORD (Admin Pro)
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
        .sidebar { width: 260px; background-color: #0f172a; border-right: 1px solid #1e293b; padding: 30px 20px; display: flex; flex-direction: column; }
        .logo { font-size: 1.5em; font-weight: 800; color: white; text-decoration: none; margin-bottom: 40px; text-align: center; }
        .logo span { color: #38bdf8; }
        .nav-item { display: block; padding: 12px 20px; color: #94a3b8; text-decoration: none; border-radius: 8px; margin-bottom: 10px; transition: 0.3s; background: transparent; border: none; width: 100%; text-align: left; cursor: pointer; font-size: 1em; font-weight: 500; }
        .nav-item:hover, .nav-item.active { background-color: #1e293b; color: #38bdf8; }
        .logout-btn { margin-top: auto; color: #f87171 !important; }
        .main-content { flex: 1; padding: 40px; overflow-y: auto; }
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; padding: 30px; margin-bottom: 30px; }
        .card h2 { color: #38bdf8; font-size: 1.3em; margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 15px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #cbd5e1; font-size: 0.9em; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 14px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; font-family: inherit; }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        button.btn-submit { width: 100%; padding: 16px; background: #38bdf8; color: #0b1120; border: none; border-radius: 8px; font-weight: 700; cursor: pointer; transition: 0.3s; }
        button.btn-submit:hover { background: #0ea5e9; }
        .content-item { display: flex; align-items: center; background: #0f172a; padding: 15px; border-radius: 12px; border: 1px solid #1e293b; flex-wrap: wrap; gap: 15px; margin-bottom: 10px; }
        .content-item img { width: 100px; height: 70px; object-fit: cover; border-radius: 8px; }
        .content-info { flex: 1; min-width: 200px; }
        .content-info h3 { color: white; font-size: 1.1em; }
        .content-info p { color: #94a3b8; font-size: 0.85em; }
        .actions { display: flex; gap: 10px; }
        .btn-edit { background: rgba(56, 189, 248, 0.1); color: #38bdf8; padding: 10px 15px; border-radius: 8px; text-decoration: none; font-weight: 600; }
        .btn-delete { background: rgba(248, 113, 113, 0.1); color: #f87171; padding: 10px 15px; border-radius: 8px; text-decoration: none; font-weight: 600; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        @media (max-width: 768px) { body { flex-direction: column; } .sidebar { width: 100%; flex-direction: row; flex-wrap: wrap; } .form-row { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="sidebar">
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <button class="nav-item active" onclick="openTab('list')">📋 Gestion</button>
        <button class="nav-item" onclick="openTab('add')">➕ Ajouter</button>
        <a href="/" class="nav-item" target="_blank">🌐 Voir le site</a>
        <a href="/gestion-jacob-2026/logout" class="nav-item logout-btn">🚪 Déconnexion</a>
    </div>
    <div class="main-content">
        <div id="tab-list" class="tab-content active">
            <div class="card">
                <h2>Vos vidéos ({{ contenus|length }})</h2>
                {% for item in contenus %}
                <div class="content-item">
                    <img src="{{ item.image_url }}" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">
                    <div class="content-info">
                        <h3>{{ item.titre }}</h3>
                        <p>{{ item.description[:50] }}...</p>
                    </div>
                    <div class="actions">
                        <a href="/gestion-jacob-2026/modifier/{{ item.id }}" class="btn-edit">Modifier</a>
                        <a href="/gestion-jacob-2026/supprimer/{{ item.id }}" class="btn-delete" onclick="return confirm('Supprimer ?')">Supprimer</a>
                    </div>
                </div>
                {% else %}
                <p style="text-align:center; color:#64748b;">Aucun contenu.</p>
                {% endfor %}
            </div>
        </div>
        <div id="tab-add" class="tab-content {% if modifier %}active{% endif %}">
            <div class="card">
                {% if modifier %}<h2>Modifier</h2><form method="POST" action="/gestion-jacob-2026/modifier/{{ modifier.id }}">
                {% else %}<h2>Ajouter</h2><form method="POST" action="/gestion-jacob-2026/ajouter">{% endif %}
                    <div class="form-row">
                        <div class="form-group"><label>Titre</label><input type="text" name="titre" value="{{ modifier.titre if modifier else '' }}" required></div>
                        <div class="form-group"><label>Catégorie</label>
                            <select name="categorie">
                                <option value="Déblocage" {% if modifier and modifier.categorie == 'Déblocage' %}selected{% endif %}>Déblocage</option>
                                <option value="Système" {% if modifier and modifier.categorie == 'Système' %}selected{% endif %}>Système</option>
                                <option value="Marketing" {% if modifier and modifier.categorie == 'Marketing' %}selected{% endif %}>Marketing</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group"><label>Lien Image</label><input type="url" name="image_url" value="{{ modifier.image_url if modifier else '' }}" required></div>
                    <div class="form-group"><label>Description</label><textarea name="description" rows="3" required>{{ modifier.description if modifier else '' }}</textarea></div>
                    <div class="form-group"><label>Lien Vidéo</label><input type="url" name="lien" value="{{ modifier.lien if modifier else '' }}"></div>
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
            if(tabName === 'list') document.querySelectorAll('.nav-item')[0].classList.add('active');
            else document.querySelectorAll('.nav-item')[1].classList.add('active');
        }
    </script>
</body>
</html>"""
with open('templates/dashboard.html', 'w', encoding='utf-8') as f: f.write(dashboard_html)

# ==========================================
# 4. RECREATION DE LOGIN.HTML
# ==========================================
login_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion Admin</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { background-color: #0b1120; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'Poppins', sans-serif; }
        .login-box { background: #1e293b; padding: 40px; border-radius: 16px; text-align: center; width: 100%; max-width: 400px; border: 1px solid #334155; }
        h2 { color: #38bdf8; margin-bottom: 20px; }
        input { width: 100%; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; box-sizing: border-box; font-family: inherit; }
        button { width: 100%; padding: 15px; background: #38bdf8; color: #0b1720; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; margin-top: 10px; font-family: inherit; }
        button:hover { background: #0ea5e9; }
        p { color: #f87171; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Espace Admin</h2>
        <form method="POST" action="/gestion-jacob-2026">
            <input type="password" name="password" placeholder="Mot de passe" required>
            <button type="submit">Se connecter</button>
        </form>
        <p>{{ erreur }}</p>
    </div>
</body>
</html>"""
with open('templates/login.html', 'w', encoding='utf-8') as f: f.write(login_html)

print("✅ TOUT EST RECREE A NEUF ET PRET A FONCTIONNER !")
