import os

# ==========================================
# 1. CORRECTION DE APP.PY (Suppression par ID robuste)
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
    categorie = request.form.get('categorie')
    
    contenus = lire_donnees()
    # On utilise un identifiant unique basé sur le temps pour éviter les doublons
    import time
    nouvel_id = int(time.time())
    
    contenus.append({
        'id': nouvel_id, 
        'titre': titre, 
        'image_url': image_url,
        'description': description, 
        'lien': lien,
        'categorie': categorie
    })
    sauvegarder_donnees(contenus)
    
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/supprimer/<int:id>')
def supprimer(id):
    if not session.get('logged_in'):
        return redirect(url_for('admin'))
    
    contenus = lire_donnees()
    # On garde tous les contenus SAUF celui qui a l'ID à supprimer
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
# 2. NOUVEAU TABLEAU DE BORD AVEC ONGLETS
# ==========================================
dashboard_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Admin - Jacob Tools</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; margin: 0; padding: 0; }
        body { background-color: #0b1120; color: #e2e8f0; display: flex; height: 100vh; overflow: hidden; }
        
        /* SIDEBAR */
        .sidebar { width: 260px; background-color: #0f172a; border-right: 1px solid #1e293b; padding: 30px 20px; display: flex; flex-direction: column; }
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

        /* SECTIONS (Cachées par défaut) */
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
        .content-item { display: flex; align-items: center; background: #0f172a; padding: 15px; border-radius: 12px; border: 1px solid #1e293b; }
        .content-item img { width: 100px; height: 70px; object-fit: cover; border-radius: 8px; margin-right: 20px; }
        .content-info { flex: 1; }
        .content-info h3 { color: white; font-size: 1.1em; margin-bottom: 5px; }
        .content-info p { color: #94a3b8; font-size: 0.85em; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 50px; font-size: 0.75em; font-weight: 600; margin-top: 8px; }
        .badge-deblocage { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
        .badge-systeme { background: rgba(129, 140, 248, 0.2); color: #818cf8; }
        .badge-marketing { background: rgba(244, 114, 182, 0.2); color: #f472b6; }
        .btn-delete { background: rgba(248, 113, 113, 0.1); color: #f87171; padding: 10px 15px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9em; transition: 0.3s; }
        .btn-delete:hover { background: rgba(248, 113, 113, 0.2); }
    </style>
</head>
<body>

    <!-- SIDEBAR -->
    <div class="sidebar">
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <button class="nav-item active" onclick="openTab('list')">📋 Gestion des contenus</button>
        <button class="nav-item" onclick="openTab('add')">➕ Ajouter un contenu</button>
        <a href="/" class="nav-item" target="_blank">🌐 Voir le site</a>
        <a href="/gestion-jacob-2026/logout" class="nav-item logout-btn">🚪 Déconnexion</a>
    </div>

    <!-- MAIN CONTENT -->
    <div class="main-content">
        <div class="header">
            <h1 id="page-title">Liste des contenus</h1>
        </div>

        <!-- ONGLET 1 : LISTE DES CONTENUS -->
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
                        <a href="/gestion-jacob-2026/supprimer/{{ item.id }}" class="btn-delete" onclick="return confirm('Supprimer ce contenu ?')">Supprimer</a>
                    </div>
                    {% else %}
                    <p style="text-align: center; color: #64748b; padding: 20px;">Aucun contenu. Cliquez sur "Ajouter un contenu".</p>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- ONGLET 2 : AJOUTER UN CONTENU -->
        <div id="tab-add" class="tab-content">
            <div class="card">
                <h2>Publier une nouvelle formation</h2>
                <form method="POST" action="/gestion-jacob-2026/ajouter">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Titre de la vidéo</label>
                            <input type="text" name="titre" placeholder="Ex: Déblocage iPhone 13 Pro" required>
                        </div>
                        <div class="form-group">
                            <label>Catégorie</label>
                            <select name="categorie" required>
                                <option value="Déblocage">Déblocage Mobile</option>
                                <option value="Système">Systèmes d'Exploitation</option>
                                <option value="Marketing">Marketing Digital</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Lien de l'image (Postimages, Unsplash, etc.)</label>
                        <input type="url" name="image_url" placeholder="https://i.postimg.cc/..." required>
                    </div>

                    <div class="form-group">
                        <label>Description</label>
                        <textarea name="description" placeholder="Décrivez brièvement le contenu..." required rows="3"></textarea>
                    </div>

                    <div class="form-group">
                        <label>Lien de la vidéo (YouTube, Drive, etc.)</label>
                        <input type="url" name="lien" placeholder="https://youtube.com/watch?v=...">
                    </div>

                    <button type="submit" class="btn-submit">Publier sur le site</button>
                </form>
            </div>
        </div>

    </div>

    <!-- SCRIPT POUR LES ONGLETS -->
    <script>
        function openTab(tabName) {
            // Cacher tous les onglets
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            // Désactiver tous les boutons
            document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));
            
            // Afficher le bon onglet
            document.getElementById('tab-' + tabName).classList.add('active');
            
            // Activer le bon bouton et changer le titre
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

print("✅ Admin mis a jour avec succes : Onglets ajoutes et bug de suppression corrige !")
