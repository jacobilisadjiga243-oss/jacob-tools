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
HASHED_PASSWORD = generate_password_hash("jacob123")
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
        return render_template('dashboard.html', contenus=contenus, modifier=None)
    
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
