import os

# ==========================================
# 1. MISE A JOUR DE APP.PY (Routes Utilisateurs)
# ==========================================
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# On ajoute la création de la table utilisateurs au démarrage
ancien_init = """def init_db():
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(\"\"\"
                    CREATE TABLE IF NOT EXISTS contenus (
                        id SERIAL PRIMARY KEY,
                        titre VARCHAR(255) NOT NULL,
                        image_url TEXT NOT NULL,
                        description TEXT NOT NULL,
                        lien TEXT,
                        categorie VARCHAR(50) NOT NULL
                    );
                \"\"\")
            conn.commit()"""

nouveau_init = """def init_db():
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                # Table des contenus (existante)
                cur.execute(\"\"\"
                    CREATE TABLE IF NOT EXISTS contenus (
                        id SERIAL PRIMARY KEY,
                        titre VARCHAR(255) NOT NULL,
                        image_url TEXT NOT NULL,
                        description TEXT NOT NULL,
                        lien TEXT,
                        categorie VARCHAR(50) NOT NULL
                    );
                \"\"\")
                # NOUVELLE TABLE : Utilisateurs (clients)
                cur.execute(\"\"\"
                    CREATE TABLE IF NOT EXISTS utilisateurs (
                        id SERIAL PRIMARY KEY,
                        nom VARCHAR(100) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        mot_de_passe TEXT NOT NULL,
                        date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                \"\"\")
            conn.commit()"""

code = code.replace(ancien_init, nouveau_init)

# On ajoute les routes d'inscription, connexion et déconnexion client
routes_client = """
# --- ROUTES CLIENTS (INSCRIPTION / CONNEXION) ---
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')
        
        hashed_password = generate_password_hash(mot_de_passe)
        
        conn = get_db()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe) VALUES (%s, %s, %s);",
                                (nom, email, hashed_password))
                conn.commit()
                return redirect(url_for('connexion'))
            except Exception as e:
                print(f"Erreur inscription: {e}")
                return render_template('inscription.html', erreur="Cet email est déjà utilisé.")
            finally:
                conn.close()
    return render_template('inscription.html', erreur="")

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')
        
        conn = get_db()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, nom, mot_de_passe FROM utilisateurs WHERE email = %s;", (email,))
                    user = cur.fetchone()
                    
                if user and check_password_hash(user[2], mot_de_passe):
                    session['user_id'] = user[0]
                    session['user_nom'] = user[1]
                    return redirect(url_for('accueil'))
                else:
                    return render_template('connexion.html', erreur="Email ou mot de passe incorrect.")
            except Exception as e:
                print(f"Erreur connexion: {e}")
                return render_template('connexion.html', erreur="Une erreur est survenue.")
            finally:
                conn.close()
    return render_template('connexion.html', erreur="")

@app.route('/deconnexion')
def deconnexion():
    session.pop('user_id', None)
    session.pop('user_nom', None)
    return redirect(url_for('accueil'))

@app.route(ADMIN_URL, methods=['GET', 'POST'])
def admin():"""

code = code.replace("""@app.route(ADMIN_URL, methods=['GET', 'POST'])
def admin():""", routes_client)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ app.py mis a jour avec les routes clients !")

# ==========================================
# 2. CREATION DES PAGES HTML (Inscription / Connexion)
# ==========================================
page_style = """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background: radial-gradient(circle at center, #1e293b 0%, #0b1120 100%); color: white; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .box { background: #1e293b; padding: 40px; border-radius: 16px; border: 1px solid #334155; width: 100%; max-width: 400px; text-align: center; }
        h2 { color: #38bdf8; margin-bottom: 20px; }
        input { width: 100%; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; font-family: inherit; }
        input:focus { outline: none; border-color: #38bdf8; }
        button { width: 100%; padding: 15px; background: #38bdf8; color: #0b1120; border: none; border-radius: 8px; font-weight: 700; font-size: 1.1em; cursor: pointer; margin-top: 10px; }
        button:hover { background: #0ea5e9; }
        a { color: #38bdf8; text-decoration: none; display: block; margin-top: 15px; font-size: 0.9em; }
        .error { color: #f87171; margin-top: 15px; }
    </style>
"""

html_inscription = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>Inscription - Jacob Tools</title>{page_style}</head>
<body>
    <div class="box">
        <h2>Créer un compte</h2>
        <form method="POST">
            <input type="text" name="nom" placeholder="Votre nom complet" required>
            <input type="email" name="email" placeholder="Votre adresse email" required>
            <input type="password" name="mot_de_passe" placeholder="Mot de passe" required>
            <button type="submit">S'inscrire</button>
        </form>
        <a href="/connexion">Déjà un compte ? Connectez-vous</a>
        <p class="error">{{{{ erreur }}}}</p>
    </div>
</body>
</html>"""

html_connexion = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>Connexion - Jacob Tools</title>{page_style}</head>
<body>
    <div class="box">
        <h2>Connexion</h2>
        <form method="POST">
            <input type="email" name="email" placeholder="Votre adresse email" required>
            <input type="password" name="mot_de_passe" placeholder="Votre mot de passe" required>
            <button type="submit">Se connecter</button>
        </form>
        <a href="/inscription">Pas encore de compte ? Inscrivez-vous</a>
        <p class="error">{{{{ erreur }}}}</p>
    </div>
</body>
</html>"""

with open('templates/inscription.html', 'w', encoding='utf-8') as f:
    f.write(html_inscription)
with open('templates/connexion.html', 'w', encoding='utf-8') as f:
    f.write(html_connexion)
print("✅ Pages inscription.html et connexion.html creees !")

# ==========================================
# 3. MISE A JOUR DU MENU SUR L'ACCUEIL (index.html)
# ==========================================
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

ancien_menu = """<a href="/apropos">À propos</a>
            <a href="#contact" class="btn-nav">Contact</a>"""

nouveau_menu = """<a href="/apropos">À propos</a>
            {% if session.get('user_nom') %}
                <span style="color: #38bdf8; font-weight: 600;">Bonjour, {{ session['user_nom'] }}</span>
                <a href="/deconnexion" style="color: #f87171;">Déconnexion</a>
            {% else %}
                <a href="/connexion" style="color: #cbd5e1;">Connexion</a>
                <a href="/inscription" class="btn-nav" style="background: #10b981;">S'inscrire</a>
            {% endif %}"""

html = html.replace(ancien_menu, nouveau_menu)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✅ Menu de l'accueil mis a jour avec Connexion/Inscription !")
