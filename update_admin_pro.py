import os

# ==========================================
# 1. MISE A JOUR DE APP.PY (Gestion des catégories)
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
    contenus.append({
        'id': len(contenus) + 1, 
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
# 2. NOUVEAU TABLEAU DE BORD ULTRA PRO (SIDEBAR)
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
        .nav-item { display: block; padding: 12px 20px; color: #94a3b8; text-decoration: none; border-radius: 8px; margin-bottom: 10px; transition: 0.3s; font-weight: 500; }
        .nav-item:hover, .nav-item.active { background-color: #1e293b; color: #38bdf8; }
        .logout-btn { margin-top: auto; color: #f87171 !important; }
        .logout-btn:hover { background-color: rgba(248, 113, 113, 0.1) !important; }

        /* MAIN CONTENT */
        .main-content { flex: 1; padding: 40px; overflow-y: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
        .header h1 { color: white; font-size: 2em; }
        
        /* CARDS */
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .card h2 { color: #38bdf8; font-size: 1.3em; margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 15px; }
        
        /* FORMULAIRE */
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
        .content-item img { width: 80px; height: 60px; object-fit: cover; border-radius: 8px; margin-right: 20px; }
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
        <a href="/gestion-jacob-2026" class="nav-item active">📊 Tableau de bord</a>
        <a href="/" class="nav-item" target="_blank">🌐 Voir le site</a>
        <a href="/gestion-jacob-2026/logout" class="nav-item logout-btn">🚪 Déconnexion</a>
    </div>

    <!-- MAIN CONTENT -->
    <div class="main-content">
        <div class="header">
            <h1>Gestion des contenus</h1>
        </div>

        <!-- FORMULAIRE D'AJOUT -->
        <div class="card">
            <h2>Ajouter une nouvelle formation / vidéo</h2>
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
                    <textarea name="description" placeholder="Décrivez brièvement le contenu de la formation..." required rows="3"></textarea>
                </div>

                <div class="form-group">
                    <label>Lien de la vidéo (YouTube, Google Drive, etc.)</label>
                    <input type="url" name="lien" placeholder="https://youtube.com/watch?v=...">
                </div>

                <button type="submit" class="btn-submit">Publier la formation</button>
            </form>
        </div>

        <!-- LISTE DES CONTENUS -->
        <div class="card">
            <h2>Vos contenus en ligne ({{ contenus|length }})</h2>
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
                <p style="text-align: center; color: #64748b; padding: 20px;">Aucun contenu pour le moment. Utilisez le formulaire ci-dessus.</p>
                {% endfor %}
            </div>
        </div>
    </div>

</body>
</html>"""
with open('templates/dashboard.html', 'w', encoding='utf-8') as f: f.write(dashboard_html)


# ==========================================
# 3. MISE A JOUR DE L'ACCUEIL (Affichage des catégories)
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
        
        nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 5%; background: rgba(11, 17, 32, 0.95); position: fixed; width: 100%; top: 0; z-index: 1000; border-bottom: 1px solid #1e293b; backdrop-filter: blur(10px); }
        .logo { font-size: 1.8em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; }
        .logo span { color: #38bdf8; }
        .nav-links { display: flex; gap: 30px; align-items: center; }
        .nav-links a { color: #cbd5e1; text-decoration: none; font-weight: 500; transition: color 0.3s; font-size: 0.95em; }
        .nav-links a:hover { color: #38bdf8; }
        .btn-nav { background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120 !important; padding: 10px 25px; border-radius: 50px; font-weight: 700 !important; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3); }
        
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

        section { padding: 100px 5%; }
        .section-titre { text-align: center; font-size: 2.8em; margin-bottom: 15px; color: white; font-weight: 800; }
        .section-sous-titre { text-align: center; color: #94a3b8; font-size: 1.1em; max-width: 600px; margin: 0 auto 60px auto; }

        .rubriques-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .rubrique-card { background: #1e293b; border-radius: 20px; overflow: hidden; border: 1px solid #334155; transition: all 0.4s; display: flex; flex-direction: column; }
        .rubrique-card:hover { transform: translateY(-10px); border-color: #38bdf8; box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
        .rubrique-img { width: 100%; height: 200px; object-fit: cover; border-bottom: 1px solid #334155; }
        .rubrique-content { padding: 30px; text-align: center; flex-grow: 1; }
        .rubrique-content h3 { color: #38bdf8; font-size: 1.5em; margin-bottom: 15px; }
        .rubrique-content p { color: #94a3b8; font-size: 0.95em; }

        .content-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .card { background: #1e293b; border-radius: 16px; border: 1px solid #334155; overflow: hidden; transition: transform 0.3s, border-color 0.3s; display: flex; flex-direction: column; }
        .card:hover { transform: translateY(-5px); border-color: #38bdf8; box-shadow: 0 15px 30px rgba(0,0,0,0.5); }
        .card-img { height: 200px; width: 100%; object-fit: cover; border-bottom: 1px solid #334155; }
        .card-body { padding: 25px; display: flex; flex-direction: column; flex-grow: 1; position: relative; }
        .card-body h3 { color: white; font-size: 1.3em; margin-bottom: 10px; }
        .card-body p { color: #94a3b8; font-size: 0.95em; flex-grow: 1; margin-bottom: 20px; }
        .btn { display: inline-block; padding: 15px 35px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120; text-decoration: none; border-radius: 50px; font-weight: 700; font-size: 1em; transition: all 0.3s; text-align: center; border: none; cursor: pointer; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(56, 189, 248, 0.6); }

        .badge-cat { position: absolute; top: 15px; right: 15px; padding: 5px 15px; border-radius: 50px; font-size: 0.75em; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
        .bg-deblocage { background: #38bdf8; color: #0b1120; }
        .bg-systeme { background: #818cf8; color: white; }
        .bg-marketing { background: #f472b6; color: white; }

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
            <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 60px;">
                <div class="card-body" style="align-items: center;">
                    <h3 style="color: #38bdf8;">Aucune formation pour le moment</h3>
                    <p>Connectez-vous à l'espace admin pour ajouter vos vidéos.</p>
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

print("✅ Espace Admin Ultra Pro et site mis a jour avec succes !")
