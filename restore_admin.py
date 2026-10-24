import os
import json

# 1. On s'assure que le fichier data.json existe et est propre
if not os.path.exists('data.json'):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump([], f)

# 2. Mise à jour de app.py avec un système de sauvegarde automatique
app_py = """from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
import time
import shutil

app = Flask(__name__)
app.secret_key = "jacob_tools_ultra_secret_2026_x89f"

ADMIN_URL = "/gestion-jacob-2026"
HASHED_PASSWORD = generate_password_hash("jacob123")
DATA_FILE = "data.json"
BACKUP_FILE = "data_backup.json"

def lire_donnees():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def sauvegarder_donnees(data):
    # Créer une copie de secours avant d'écraser
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, BACKUP_FILE)
        
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
    # On utilise un identifiant basé sur le temps pour être sûr qu'il soit unique
    nouvel_id = int(time.time() * 1000)
    
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

# 3. On remet le tableau de bord avec le design propre (Onglets + Modifier)
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
        
        .sidebar { width: 260px; background-color: #0f172a; border-right: 1px solid #1e293b; padding: 30px 20px; display: flex; flex-direction: column; flex-shrink: 0; }
        .logo { font-size: 1.5em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; margin-bottom: 40px; text-align: center; }
        .logo span { color: #38bdf8; }
        .nav-item { display: block; padding: 12px 20px; color: #94a3b8; text-decoration: none; border-radius: 8px; margin-bottom: 10px; transition: 0.3s; font-weight: 500; background: transparent; border: none; width: 100%; text-align: left; cursor: pointer; font-size: 1em; }
        .nav-item:hover, .nav-item.active { background-color: #1e293b; color: #38bdf8; }
        .logout-btn { margin-top: auto; color: #f87171 !important; }
        .logout-btn:hover { background-color: rgba(248, 113, 113, 0.1) !important; }

        .main-content { flex: 1; padding: 40px; overflow-y: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .header h1 { color: white; font-size: 2em; }
        
        .tab-content { display: none; animation: fadeIn 0.4s; }
        .tab-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .card h2 { color: #38bdf8; font-size: 1.3em; margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 15px; }
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; color: #cbd5e1; font-size: 0.9em; font-weight: 500; }
        .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 14px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; font-family: inherit; font-size: 1em; }
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus { outline: none; border-color: #38bdf8; box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.1); }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        button.btn-submit { width: 100%; padding: 16px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120; border: none; border-radius: 8px; font-weight: 700; font-size: 1.1em; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        button.btn-submit:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(56, 189, 248, 0.4); }

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

    <div class="sidebar">
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <button class="nav-item active" onclick="openTab('list')">📋 Gestion</button>
        <button class="nav-item" onclick="openTab('add')">➕ Ajouter</button>
        <a href="/" class="nav-item" target="_blank">🌐 Voir le site</a>
        <a href="/gestion-jacob-2026/logout" class="nav-item logout-btn">🚪 Déconnexion</a>
    </div>

    <div class="main-content">
        <div class="header">
            <h1 id="page-title">Liste des contenus</h1>
        </div>

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
                    <p style="text-align: center; color: #64748b; padding: 20px;">Aucun contenu pour l'instant.</p>
                    {% endfor %}
                </div>
            </div>
        </div>

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

print("✅ Admin restaure et securise (sauvegarde automatique activee) !")
