import os
import psycopg
from dotenv import load_dotenv

# ==========================================
# 1. CREATION DE LA TABLE DES PARAMETRES DANS NEON
# ==========================================
load_dotenv()
db_url = os.getenv('DATABASE_URL')

if db_url:
    try:
        conn = psycopg.connect(db_url)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS parametres (
                    cle VARCHAR(50) PRIMARY KEY,
                    valeur TEXT
                );
            """)
            # On insère les valeurs par défaut si elles n'existent pas
            cur.execute("INSERT INTO parametres (cle, valeur) VALUES ('whatsapp', '243977982648') ON CONFLICT DO NOTHING;")
            cur.execute("INSERT INTO parametres (cle, valeur) VALUES ('email', 'ton.email@exemple.com') ON CONFLICT DO NOTHING;")
            cur.execute("INSERT INTO parametres (cle, valeur) VALUES ('facebook', 'https://facebook.com/jacobtools') ON CONFLICT DO NOTHING;")
        conn.commit()
        conn.close()
        print("✅ Table 'parametres' creee dans Neon !")
    except Exception as e:
        print(f"⚠️ Erreur Neon: {e}")
else:
    print("⚠️ DATABASE_URL introuvable dans le .env local.")

# ==========================================
# 2. MISE A JOUR DE APP.PY
# ==========================================
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# On ajoute une fonction pour récupérer les paramètres
ancien_get_db = "def init_db():"
nouveau_get_db = """
def get_parametres():
    params = {'whatsapp': '243977982648', 'email': 'contact@jacobtools.com', 'facebook': '#'}
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT cle, valeur FROM parametres;")
                rows = cur.fetchall()
                for r in rows:
                    params[r[0]] = r[1]
        except Exception as e:
            print(f"Erreur params: {e}")
        finally:
            conn.close()
    return params

def init_db():"""
code = code.replace(ancien_get_db, nouveau_get_db)

# On met à jour la route /admin/parametres pour sauvegarder
ancienne_route_param = """@app.route(ADMIN_URL + '/parametres')
def admin_parametres():
    if not session.get('logged_in'): return redirect(url_for('admin'))
    # Pour l'instant, on renvoie une page vide qu'on remplira plus tard
    return render_template('dashboard.html', contenus=[], modifier=None, page='parametres')"""

nouvelle_route_param = """@app.route(ADMIN_URL + '/parametres', methods=['GET', 'POST'])
def admin_parametres():
    if not session.get('logged_in'): return redirect(url_for('admin'))
    
    if request.method == 'POST':
        whatsapp = request.form.get('whatsapp')
        email = request.form.get('email')
        facebook = request.form.get('facebook')
        conn = get_db()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("UPDATE parametres SET valeur = %s WHERE cle = 'whatsapp';", (whatsapp,))
                    cur.execute("UPDATE parametres SET valeur = %s WHERE cle = 'email';", (email,))
                    cur.execute("UPDATE parametres SET valeur = %s WHERE cle = 'facebook';", (facebook,))
                conn.commit()
            except Exception as e:
                print(f"Erreur sauvegarde params: {e}")
            finally:
                conn.close()
        return redirect(url_for('admin_parametres'))
        
    params = get_parametres()
    return render_template('dashboard.html', contenus=[], modifier=None, page='parametres', params=params)"""

code = code.replace(ancienne_route_param, nouvelle_route_param)

# On met à jour la route d'accueil pour envoyer les params au site
code = code.replace("return render_template('index.html', contenus=contenus)", "return render_template('index.html', contenus=contenus, params=get_parametres())")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ app.py mis a jour pour les parametres.")

# ==========================================
# 3. MISE A JOUR DU DASHBOARD (Formulaire Paramètres)
# ==========================================
with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

ancienne_section_param = """<div id="tab-parametres" class="tab-content {% if page == 'parametres' %}active{% endif %}">
            <div class="card">
                <h2>Paramètres du site</h2>
                <p style="color: #94a3b8; text-align: center; padding: 40px;">Les paramètres seront bientôt disponibles.</p>
            </div>
        </div>"""

nouvelle_section_param = """<div id="tab-parametres" class="tab-content {% if page == 'parametres' %}active{% endif %}">
            <div class="card">
                <h2>Paramètres du site</h2>
                <form method="POST" action="/admin/parametres">
                    <div class="form-group">
                        <label>Numéro WhatsApp (ex: 243977982648)</label>
                        <input type="text" name="whatsapp" value="{{ params.whatsapp if params else '' }}" required>
                    </div>
                    <div class="form-group">
                        <label>Adresse Email de contact</label>
                        <input type="email" name="email" value="{{ params.email if params else '' }}" required>
                    </div>
                    <div class="form-group">
                        <label>Lien Facebook (optionnel)</label>
                        <input type="url" name="facebook" value="{{ params.facebook if params else '' }}">
                    </div>
                    <button type="submit" class="btn-submit">Enregistrer les paramètres</button>
                </form>
            </div>
        </div>"""

dash = dash.replace(ancienne_section_param, nouvelle_section_param)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash)
print("✅ dashboard.html mis a jour avec le formulaire de parametres.")

# ==========================================
# 4. MISE A JOUR DE L'ACCUEIL (Utilisation des paramètres)
# ==========================================
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# On remplace le numéro de WhatsApp en dur par la variable
html = html.replace('https://wa.me/243977982648?text=', 'https://wa.me/{{ params.whatsapp }}?text=')

# On remplace l'email en dur par la variable
html = html.replace('mailto:ton.email@exemple.com?subject=', 'mailto:{{ params.email }}?subject=')

# On ajoute le lien Facebook dans le footer s'il existe
ancien_footer = """<a href="#services">Services</a>
            </div>"""
nouveau_footer = """<a href="#services">Services</a>
                {% if params.facebook and params.facebook != '#' %}
                <a href="{{ params.facebook }}" target="_blank">Facebook</a>
                {% endif %}
            </div>"""
html = html.replace(ancien_footer, nouveau_footer)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✅ index.html mis a jour pour utiliser les parametres.")

# ==========================================
# 5. ENVOI AUTOMATIQUE SUR GITHUB
# ==========================================
print("Envoi sur GitHub en cours...")
os.system('git add .')
os.system('git commit -m "Ajout de la gestion des parametres du site"')
os.system('git push')
print("✅ Termine ! Attends 2 minutes que Render redemarre.")
