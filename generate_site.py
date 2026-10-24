import os

# Création du dossier templates s'il n'existe pas
os.makedirs('templates', exist_ok=True)

# ==========================================
# 1. PAGE D'ACCUEIL (INDEX.HTML)
# ==========================================
index_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jacob Tools - Solutions Digitales</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background-color: #0b1120; color: #e2e8f0; line-height: 1.6; }
        nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 50px; background: rgba(15, 23, 42, 0.9); position: sticky; top: 0; z-index: 100; border-bottom: 1px solid #1e293b; backdrop-filter: blur(10px); }
        .logo { font-size: 1.8em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; }
        .logo span { color: #38bdf8; }
        .nav-links a { color: #cbd5e1; text-decoration: none; margin-left: 30px; font-weight: 400; transition: color 0.3s; }
        .nav-links a:hover { color: #38bdf8; }
        .btn-nav { background: #38bdf8; color: #0f172a !important; padding: 10px 20px; border-radius: 8px; font-weight: 600 !important; }
        .hero { text-align: center; padding: 120px 20px; background: radial-gradient(circle at top, #1e293b 0%, #0b1120 100%); }
        .hero h1 { font-size: 4em; font-weight: 800; margin-bottom: 20px; color: white; line-height: 1.2; }
        .hero h1 span { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 1.2em; color: #94a3b8; max-width: 700px; margin: 0 auto 40px auto; }
        .btn { display: inline-block; padding: 15px 35px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0f172a; text-decoration: none; border-radius: 50px; font-weight: 600; font-size: 1.1em; transition: transform 0.2s, box-shadow 0.2s; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4); }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(56, 189, 248, 0.6); }
        .section-titre { text-align: center; font-size: 2.5em; margin: 60px 0 40px 0; color: white; font-weight: 800; }
        .content-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; max-width: 1200px; margin: 0 auto; padding: 0 20px 100px 20px; }
        .card { background: #1e293b; padding: 30px; border-radius: 16px; border: 1px solid #334155; transition: transform 0.3s, border-color 0.3s; display: flex; flex-direction: column; }
        .card:hover { transform: translateY(-5px); border-color: #38bdf8; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .card h3 { color: #38bdf8; font-size: 1.5em; margin-bottom: 15px; font-weight: 600; }
        .card p { color: #cbd5e1; flex-grow: 1; margin-bottom: 25px; }
        .card .btn { padding: 12px 20px; font-size: 1em; text-align: center; border-radius: 8px; }
        footer { text-align: center; padding: 40px; border-top: 1px solid #1e293b; color: #64748b; }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <div class="nav-links">
            <a href="/">Accueil</a>
            <a href="#services">Services</a>
            <a href="#cours">Cours</a>
            <a href="/admin" class="btn-nav">Admin</a>
        </div>
    </nav>
    <header class="hero">
        <h1>Propulsez vos projets avec <span>Jacob Tools</span></h1>
        <p>La plateforme ultime pour les applications de déblocage, les cours en ligne exclusifs et les solutions marketing digitales.</p>
        <a href="#services" class="btn">Découvrir nos offres</a>
    </header>
    <h2 class="section-titre" id="services">Nos Dernières Offres</h2>
    <div class="content-grid">
        {% for item in contenus %}
        <div class="card">
            <h3>{{ item.titre }}</h3>
            <p>{{ item.description }}</p>
            {% if item.lien %}
            <a href="{{ item.lien }}" class="btn" target="_blank">Accéder</a>
            {% endif %}
        </div>
        {% else %}
        <div class="card" style="grid-column: 1 / -1; text-align: center;">
            <p>Aucune offre disponible pour le moment. Revenez bientôt !</p>
        </div>
        {% endfor %}
    </div>
    <footer>
        &copy; 2026 Jacob Tools. Tous droits réservés.
    </footer>
</body>
</html>"""

# ==========================================
# 2. PAGE DE CONNEXION (LOGIN.HTML)
# ==========================================
login_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Connexion Admin - Jacob Tools</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background-color: #0b1120; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: radial-gradient(circle at center, #1e293b 0%, #0b1120 100%); }
        .login-box { background: #1e293b; padding: 50px 40px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; width: 100%; max-width: 400px; border: 1px solid #334155; }
        h2 { color: #38bdf8; margin-bottom: 30px; font-weight: 800; letter-spacing: 1px; }
        input { width: 100%; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 1em; }
        input:focus { outline: none; border-color: #38bdf8; }
        button { width: 100%; padding: 15px; background: #38bdf8; color: #0f172a; border: none; border-radius: 8px; font-weight: 600; font-size: 1.1em; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        button:hover { background: #0ea5e9; }
        p { color: #f87171; margin-top: 15px; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Espace Admin</h2>
        <form method="POST" action="/admin">
            <input type="password" name="password" placeholder="Mot de passe" required>
            <button type="submit">Se connecter</button>
        </form>
        <p>{{ erreur }}</p>
    </div>
</body>
</html>"""

# ==========================================
# 3. TABLEAU DE BORD (DASHBOARD.HTML)
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
        .danger:hover { text-decoration: underline; }
        .nav-links { text-align: center; margin-top: 30px; }
        .nav-links a { margin: 0 15px; font-weight: 600; }
    </style>
</head>
<body>
    <h1 style="text-align: center; margin-bottom: 30px;">Tableau de bord Admin</h1>
    <div class="card">
        <h2>Ajouter un contenu</h2>
        <form method="POST" action="/admin/ajouter">
            <input type="text" name="titre" placeholder="Titre (ex: Déblocage iPhone)" required>
            <textarea name="description" placeholder="Description courte" required rows="3"></textarea>
            <input type="text" name="lien" placeholder="Lien (URL de la vidéo ou du cours) - Optionnel">
            <button type="submit">Publier sur le site</button>
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
                <a href="/admin/supprimer/{{ item.id }}" class="danger">Supprimer</a>
            </li>
            {% else %}
            <li style="justify-content: center; border-left: none; color: #64748b;">Aucun contenu enregistré.</li>
            {% endfor %}
        </ul>
    </div>
    <div class="nav-links">
        <a href="/">← Retour au site</a>
        <a href="/admin/logout">Se déconnecter</a>
    </div>
</body>
</html>"""

# Sauvegarde des fichiers
with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)
with open('templates/login.html', 'w', encoding='utf-8') as f: f.write(login_html)
with open('templates/dashboard.html', 'w', encoding='utf-8') as f: f.write(dashboard_html)

print("✅ Tous les fichiers HTML ont ete crees avec succes !")
