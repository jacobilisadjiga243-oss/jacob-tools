import os

with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# --- 1. CORRECTION DU MOT DE PASSE ADMIN ---
# On s'assure que le mot de passe admin utilise bien la variable d'environnement
if 'os.getenv("ADMIN_PASSWORD"' not in code:
    # On remplace l'ancienne ligne par la nouvelle
    code = code.replace('HASHED_PASSWORD = generate_password_hash("jacob123")', 'HASHED_PASSWORD = generate_password_hash(os.getenv("ADMIN_PASSWORD", "jacob123"))')
    print("✅ Sécurité du mot de passe admin configurée.")

# --- 2. CORRECTION DU SYSTEME DE CONNEXION (Routes) ---
# On vérifie si les routes existent. Si ce n'est pas le cas, on les ajoute.
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
    print("✅ Routes de connexion et inscription ajoutées.")

# --- 3. VERIFICATION DE LA TABLE UTILISATEURS ---
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
    print("✅ Table utilisateurs vérifiée.")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("🎉 Réparation terminée ! Tu peux envoyer sur GitHub.")
