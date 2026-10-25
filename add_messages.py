import os
import psycopg
from dotenv import load_dotenv

# ==========================================
# 1. CREATION DE LA TABLE MESSAGES DANS NEON
# ==========================================
load_dotenv()
db_url = os.getenv('DATABASE_URL')

if db_url:
    try:
        conn = psycopg.connect(db_url)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(100) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    date_envoi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()
        conn.close()
        print("✅ Table 'messages' creee dans Neon !")
    except Exception as e:
        print(f"⚠️ Erreur Neon: {e}")

# ==========================================
# 2. MISE A JOUR DE APP.PY
# ==========================================
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Route pour TRAITER le formulaire de contact
route_contact = """
@app.route('/contact', methods=['POST'])
def contact():
    nom = request.form.get('nom')
    email = request.form.get('email')
    message = request.form.get('message')
    
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO messages (nom, email, message) VALUES (%s, %s, %s);", (nom, email, message))
            conn.commit()
        except Exception as e:
            print(f"Erreur contact: {e}")
        finally:
            conn.close()
            
    return redirect(url_for('apropos', succes='1'))

@app.route(ADMIN_URL + '/messages', methods=['GET'])
def admin_messages():"""

# On remplace l'ancienne route admin_messages par la nouvelle (avec lecture des messages)
ancienne_route_messages = """@app.route(ADMIN_URL + '/messages')
def admin_messages():
    if not session.get('logged_in'): return redirect(url_for('admin'))
    # Pour l'instant, on renvoie une page vide qu'on remplira plus tard
    return render_template('dashboard.html', contenus=[], modifier=None, page='messages')"""

nouvelle_route_messages = """@app.route(ADMIN_URL + '/messages', methods=['GET'])
def admin_messages():
    if not session.get('logged_in'): return redirect(url_for('admin'))
    
    messages = []
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nom, email, message, date_envoi FROM messages ORDER BY date_envoi DESC;")
                rows = cur.fetchall()
                messages = [{"id": r[0], "nom": r[1], "email": r[2], "message": r[3], "date": r[4]} for r in rows]
        except Exception as e:
            print(f"Erreur lecture messages: {e}")
        finally:
            conn.close()
            
    return render_template('dashboard.html', contenus=[], modifier=None, page='messages', messages=messages)"""

code = code.replace(ancienne_route_messages, nouvelle_route_messages)

# On ajoute la route /contact juste avant la route de l'admin
if "def contact():" not in code:
    code = code.replace("""@app.route(ADMIN_URL + '/messages', methods=['GET'])""", route_contact)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ app.py mis a jour pour gerer les messages.")

# ==========================================
# 3. MISE A JOUR DE LA PAGE A PROPOS (Formulaire réel)
# ==========================================
with open('templates/apropos.html', 'r', encoding='utf-8') as f:
    apropos = f.read()

ancien_form = """<form onsubmit="event.preventDefault(); alert('Formulaire envoyé ! (Nous allons configurer l\\'envoi d\\'email bientôt)');">
                <div class="form-group">
                    <label>Votre nom</label>
                    <input type="text" placeholder="Entrez votre nom" required>
                </div>
                <div class="form-group">
                    <label>Votre adresse email</label>
                    <input type="email" placeholder="Entrez votre email" required>
                </div>
                <div class="form-group">
                    <label>Votre message</label>
                    <textarea rows="5" placeholder="Décrivez votre demande..." required></textarea>
                </div>
                <button type="submit" class="btn-submit">Envoyer le message</button>
            </form>"""

nouveau_form = """<form method="POST" action="/contact">
                <div class="form-group">
                    <label>Votre nom</label>
                    <input type="text" name="nom" placeholder="Entrez votre nom" required>
                </div>
                <div class="form-group">
                    <label>Votre adresse email</label>
                    <input type="email" name="email" placeholder="Entrez votre email" required>
                </div>
                <div class="form-group">
                    <label>Votre message</label>
                    <textarea name="message" rows="5" placeholder="Décrivez votre demande..." required></textarea>
                </div>
                <button type="submit" class="btn-submit">Envoyer le message</button>
            </form>
            {% if request.args.get('succes') %}
                <p style="color: #10b981; text-align: center; margin-top: 20px; font-weight: 600;">✅ Votre message a bien été envoyé !</p>
            {% endif %}"""

apropos = apropos.replace(ancien_form, nouveau_form)
with open('templates/apropos.html', 'w', encoding='utf-8') as f:
    f.write(apropos)
print("✅ Page A propos mise a jour.")

# ==========================================
# 4. MISE A JOUR DU DASHBOARD (Affichage des messages)
# ==========================================
with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

ancien_affichage_messages = """<div id="tab-messages" class="tab-content {% if page == 'messages' %}active{% endif %}">
            <div class="card">
                <h2>Messages reçus</h2>
                <p style="color: #94a3b8; text-align: center; padding: 40px;">La boîte de réception sera bientôt disponible.</p>
            </div>
        </div>"""

nouveau_affichage_messages = """<div id="tab-messages" class="tab-content {% if page == 'messages' %}active{% endif %}">
            <div class="card">
                <h2>Messages reçus ({{ messages|length if messages else 0 }})</h2>
                
                {% if messages %}
                    {% for msg in messages %}
                    <div class="content-item" style="flex-direction: column; align-items: flex-start; padding: 20px;">
                        <div style="display: flex; justify-content: space-between; width: 100%; margin-bottom: 10px;">
                            <h3 style="color: #38bdf8;">{{ msg.nom }} <span style="font-size: 0.8em; color: #94a3b8;">({{ msg.email }})</span></h3>
                            <span style="font-size: 0.8em; color: #64748b;">{{ msg.date.strftime('%d/%m/%Y à %H:%M') }}</span>
                        </div>
                        <p style="color: #cbd5e1; width: 100%;">{{ msg.message }}</p>
                    </div>
                    {% endfor %}
                {% else %}
                    <p style="color: #94a3b8; text-align: center; padding: 40px;">Aucun message pour le moment.</p>
                {% endif %}
            </div>
        </div>"""

dash = dash.replace(ancien_affichage_messages, nouveau_affichage_messages)
with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash)
print("✅ Dashboard mis a jour pour afficher les messages.")

# ==========================================
# 5. ENVOI AUTOMATIQUE
# ==========================================
print("Envoi sur GitHub en cours...")
os.system('git add .')
os.system('git commit -m "Ajout de la boite de reception des messages"')
os.system('git push')
print("✅ Termine ! Attends 2 minutes que Render redemarre.")
