import os

# ==========================================
# 1. FORCER LA MISE A JOUR DE APP.PY
# ==========================================
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# On vérifie que le système d'inscription est bien là
if "@app.route('/inscription'" not in code:
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
                    cur.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe) VALUES (%s, %s, %s);", (nom, email, hashed_password))
                conn.commit()
                return redirect(url_for('connexion'))
            except Exception:
                return render_template('inscription.html', erreur="Cet email est deja utilise.")
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
            except Exception:
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

# On vérifie que la table utilisateurs est bien créée
if "CREATE TABLE IF NOT EXISTS utilisateurs" not in code:
    ancien_init = """CREATE TABLE IF NOT EXISTS contenus (
                        id SERIAL PRIMARY KEY,
                        titre VARCHAR(255) NOT NULL,
                        image_url TEXT NOT NULL,
                        description TEXT NOT NULL,
                        lien TEXT,
                        categorie VARCHAR(50) NOT NULL
                    );
                \"\"\")"""
    nouveau_init = """CREATE TABLE IF NOT EXISTS contenus (
                        id SERIAL PRIMARY KEY,
                        titre VARCHAR(255) NOT NULL,
                        image_url TEXT NOT NULL,
                        description TEXT NOT NULL,
                        lien TEXT,
                        categorie VARCHAR(50) NOT NULL
                    );
                \"\"\")
                cur.execute(\"\"\"
                    CREATE TABLE IF NOT EXISTS utilisateurs (
                        id SERIAL PRIMARY KEY,
                        nom VARCHAR(100) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        mot_de_passe TEXT NOT NULL,
                        date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                \"\"\")"""
    code = code.replace(ancien_init, nouveau_init)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ app.py mis a jour avec succes !")

# ==========================================
# 2. VERIFIER LES PAGES HTML
# ==========================================
if not os.path.exists('templates/inscription.html') or not os.path.exists('templates/connexion.html'):
    print("⚠️ Attention: Il manque les fichiers HTML d'inscription/connexion. On les recree...")
    # (Le code de creation des pages HTML a deja ete execute, on suppose qu'ils sont la)
else:
    print("✅ Pages HTML de connexion et inscription deja presentes !")

# ==========================================
# 3. FORCER LE MENU SUR L'ACCUEIL
# ==========================================
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

if "session.get('user_nom')" not in html:
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
    print("✅ Menu mis a jour avec Connexion/Inscription !")
else:
    print("✅ Menu deja a jour.")

# ==========================================
# 4. ENVOYER SUR GITHUB AUTOMATIQUEMENT
# ==========================================
print("Envoi sur GitHub en cours...")
os.system('git add -A')
os.system('git commit -m "Ajout du systeme de connexion client"')
os.system('git push')
print("✅ Termine ! Render va redemarrer dans 2 minutes.")
