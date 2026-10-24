# 1. On recrée un app.py propre pour le mode local
app_local = """from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os, json, time

app = Flask(__name__)
app.secret_key = "jacob_tools_secret_2026"
ADMIN_URL = "/gestion-jacob-2026"
HASHED_PASSWORD = generate_password_hash("jacob123")
DATA_FILE = "data.json"

def lire_donnees():
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return []

def sauvegarder_donnees(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def accueil():
    return render_template('index.html', contenus=lire_donnees())

@app.route(ADMIN_URL, methods=['GET', 'POST'])
def admin():
    if session.get('logged_in'):
        return render_template('dashboard.html', contenus=lire_donnees(), modifier=None)
    if request.method == 'POST':
        if check_password_hash(HASHED_PASSWORD, request.form.get('password')):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', erreur="Mot de passe incorrect.")
    return render_template('login.html', erreur="")

@app.route(ADMIN_URL + '/ajouter', methods=['POST'])
def ajouter():
    if not session.get('logged_in'): return redirect(url_for('admin'))
    contenus = lire_donnees()
    contenus.append({
        'id': int(time.time() * 1000), 'titre': request.form.get('titre'),
        'image_url': request.form.get('image_url'), 'description': request.form.get('description'),
        'lien': request.form.get('lien'), 'categorie': request.form.get('categorie')
    })
    sauvegarder_donnees(contenus)
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/supprimer/<int:id>')
def supprimer(id):
    if not session.get('logged_in'): return redirect(url_for('admin'))
    sauvegarder_donnees([c for c in lire_donnees() if c.get('id') != id])
    return redirect(url_for('admin'))

@app.route(ADMIN_URL + '/modifier/<int:id>', methods=['GET', 'POST'])
def modifier(id):
    if not session.get('logged_in'): return redirect(url_for('admin'))
    contenus = lire_donnees()
    if request.method == 'POST':
        for c in contenus:
            if c.get('id') == id:
                c.update({'titre': request.form.get('titre'), 'image_url': request.form.get('image_url'),
                          'description': request.form.get('description'), 'lien': request.form.get('lien'),
                          'categorie': request.form.get('categorie')})
        sauvegarder_donnees(contenus)
        return redirect(url_for('admin'))
    contenu = next((c for c in contenus if c.get('id') == id), None)
    return render_template('dashboard.html', contenus=contenus, modifier=contenu)

@app.route(ADMIN_URL + '/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('accueil'))

if __name__ == '__main__':
    app.run(debug=True)
"""
with open('app.py', 'w', encoding='utf-8') as f: f.write(app_local)

# 2. On s'assure que le fichier de données existe et est vide
if not os.path.exists('data.json'):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump([], f)

print("✅ app.py est repare pour le mode local !")
