from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import psycopg
from dotenv import load_dotenv

# Charge les variables d'environnement (le lien Neon)
load_dotenv()

app = Flask(__name__)
app.secret_key = "jacob_tools_secret_2026"
ADMIN_URL = "/admin"
HASHED_PASSWORD = generate_password_hash(os.getenv("ADMIN_PASSWORD", "jacob123"))
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    if not DATABASE_URL:
        print("ATTENTION: DATABASE_URL manquant !")
        return None
    # On ajoute sslmode=require si ce n'est pas déjà dans le lien
    db_url = DATABASE_URL
    if "sslmode" not in db_url:
        db_url += "?sslmode=require" if "?" not in db_url else "&sslmode=require"
    return psycopg.connect(db_url)

def init_db():
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS contenus (
                        id SERIAL PRIMARY KEY,
                        titre VARCHAR(255) NOT NULL,
                        image_url TEXT NOT NULL,
                        description TEXT NOT NULL,
                        lien TEXT,
                        categorie VARCHAR(50) NOT NULL
                    );
                """)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS utilisateurs (
                        id SERIAL PRIMARY KEY,
                        nom VARCHAR(100) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        mot_de_passe TEXT NOT NULL,
                        date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            conn.commit()
        except Exception as e:
            print(f"Erreur init DB: {e}")
        finally:
            conn.close()

# Initialisation au démarrage
init_db()

@app.route('/')
def accueil():
    contenus = []
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, titre, image_url, description, lien, categorie FROM contenus ORDER BY id DESC;")
                rows = cur.fetchall()
                contenus = [{"id": r[0], "titre": r[1], "image_url": r[2], "description": r[3], "lien": r[4], "categorie": r[5]} for r in rows]
        except Exception as e:
            print(f"Erreur lecture: {e}")
        finally:
            conn.close()
    return render_template('index.html', contenus=contenus)


@app.route('/apropos')
def apropos():
    return render_template('apropos.html')


@app.route('/video/<int:id>')
def video_detail(id):
    conn = get_db()
    video = None
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT id, titre, image_url, description, lien, categorie FROM contenus WHERE id = %s;', (id,))
                row = cur.fetchone()
                if row:
                    video = {"id": row[0], "titre": row[1], "image_url": row[2], "description": row[3], "lien": row[4], "categorie": row[5]}
        except Exception as e:
            print(f'Erreur lecture video: {e}')
        finally:
            conn.close()
    
    if not video:
        return 'Vidéo introuvable', 404
        
    return render_template('video.html', video=video)


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
    succes = request.args.get('succes')
    return render_template('connexion.html', erreur="", succes=succes)

@app.route('/deconnexion')
def deconnexion():
    session.pop('user_id', None)
    session.pop('user_nom', None)
    return redirect(url_for('accueil'))


@app.route(ADMIN_URL + '/messages')
def admin_messages():
    if not session.get('logged_in'): return redirect(url_for('admin'))
    # Pour l'instant, on renvoie une page vide qu'on remplira plus tard
    return render_template('dashboard.html', contenus=[], modifier=None, page='messages')

@app.route(ADMIN_URL + '/parametres')
def admin_parametres():
    if not session.get('logged_in'): return redirect(url_for('admin'))
    # Pour l'instant, on renvoie une page vide qu'on remplira plus tard
    return render_template('dashboard.html', contenus=[], modifier=None, page='parametres')

@app.route(ADMIN_URL, methods=['GET', 'POST'])
def admin():
    if session.get('logged_in'):
        contenus = []
        conn = get_db()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, titre, image_url, description, lien, categorie FROM contenus ORDER BY id DESC;")
                    rows = cur.fetchall()
                    contenus = [{"id": r[0], "titre": r[1], "image_url": r[2], "description": r[3], "lien": r[4], "categorie": r[5]} for r in rows]
            except Exception as e:
                print(f"Erreur admin: {e}")
            finally:
                conn.close()
        return render_template('dashboard.html', contenus=contenus, modifier=None, page='list')
    
    if request.method == 'POST':
        if check_password_hash(HASHED_PASSWORD, request.form.get('password')):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', erreur="Mot de passe incorrect.")
    return render_template('login.html', erreur="")

@app.route(ADMIN_URL + '/ajouter', methods=['POST'])
def ajouter():
    if not session.get('logged_in'): return redirect(url_for('admin'))
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO contenus (titre, image_url, description, lien, categorie) VALUES (%s, %s, %s, %s, %s);",
                    (request.form.get('titre'), request.form.get('image_url'),
                     request.form.get('description'), request.form.get('lien'),
                     request.form.get('categorie'))
                )
            conn.commit()
        except Exception as e:
            print(f"Erreur ajout: {e}")
        finally:
            conn.close()
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/supprimer/<int:id>')
def supprimer(id):
    if not session.get('logged_in'): return redirect(url_for('admin'))
    conn = get_db()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM contenus WHERE id = %s;", (id,))
            conn.commit()
        except Exception as e:
            print(f"Erreur suppression: {e}")
        finally:
            conn.close()
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    if not session.get('logged_in'): return redirect(url_for('admin'))
    conn = get_db()
    
    if request.method == 'POST' and conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE contenus SET titre=%s, image_url=%s, description=%s, lien=%s, categorie=%s WHERE id=%s;",
                    (request.form.get('titre'), request.form.get('image_url'),
                     request.form.get('description'), request.form.get('lien'),
                     request.form.get('categorie'), id)
                )
            conn.commit()
        except Exception as e:
            print(f"Erreur modification: {e}")
        finally:
            conn.close()
        return redirect(url_for('admin'))
    
    contenu = None
    contenus = []
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, titre, image_url, description, lien, categorie FROM contenus WHERE id = %s;", (id,))
                row = cur.fetchone()
                if row:
                    contenu = {"id": row[0], "titre": row[1], "image_url": row[2], "description": row[3], "lien": row[4], "categorie": row[5]}
                
                cur.execute("SELECT id, titre, image_url, description, lien, categorie FROM contenus ORDER BY id DESC;")
                rows = cur.fetchall()
                contenus = [{"id": r[0], "titre": r[1], "image_url": r[2], "description": r[3], "lien": r[4], "categorie": r[5]} for r in rows]
        except Exception as e:
            print(f"Erreur: {e}")
        finally:
            conn.close()
    
    return render_template('dashboard.html', contenus=contenus, modifier=contenu)

@app.route(ADMIN_URL + '/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('accueil'))

if __name__ == '__main__':
    app.run(debug=True)
# Mise a jour

# Force update parametres