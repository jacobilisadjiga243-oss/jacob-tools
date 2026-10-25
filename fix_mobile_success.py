import os

# ==========================================
# 1. MISE A JOUR DE APP.PY (Message de succès)
# ==========================================
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# On modifie la route inscription pour rediriger avec un succès
ancien_inscription = """                conn.commit()
                return redirect(url_for('connexion'))
            except Exception:
                return render_template('inscription.html', erreur="Cet email est deja utilise.")"""

nouveau_inscription = """                conn.commit()
                return redirect(url_for('connexion', succes='1'))
            except Exception:
                return render_template('inscription.html', erreur="Cet email est deja utilise.")"""

code = code.replace(ancien_inscription, nouveau_inscription)

# On modifie la route connexion pour accepter le paramètre succes
ancien_connexion = """    return render_template('connexion.html', erreur="")

@app.route('/deconnexion')"""
nouveau_connexion = """    succes = request.args.get('succes')
    return render_template('connexion.html', erreur="", succes=succes)

@app.route('/deconnexion')"""
code = code.replace(ancien_connexion, nouveau_connexion)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ app.py mis a jour (Message de succes).")

# ==========================================
# 2. AMELIORATION DU DESIGN MOBILE (Inscription et Connexion)
# ==========================================
# On ajoute du CSS pour que les champs soient plus grands sur mobile (min-height: 48px, font-size: 16px)
css_mobile = """
        @media (max-width: 768px) {
            .box { padding: 25px 20px; margin: 15px; }
            input { padding: 18px; font-size: 16px; margin: 12px 0; }
            button { padding: 18px; font-size: 1.2em; }
            h2 { font-size: 1.8em; }
        }
"""

# --- Fichier INSCRIPTION ---
with open('templates/inscription.html', 'r', encoding='utf-8') as f:
    html_insc = f.read()

# On injecte le CSS avant la fermeture de la balise </style>
if "@media (max-width: 768px)" not in html_insc:
    html_insc = html_insc.replace("</style>", css_mobile + "\n</style>")

# On ajoute un message de succès si l'URL contient succes=1 (au cas où)
with open('templates/inscription.html', 'w', encoding='utf-8') as f:
    f.write(html_insc)

# --- Fichier CONNEXION ---
with open('templates/connexion.html', 'r', encoding='utf-8') as f:
    html_conn = f.read()

# On injecte le CSS mobile
if "@media (max-width: 768px)" not in html_conn:
    html_conn = html_conn.replace("</style>", css_mobile + "\n</style>")

# On affiche un message de succès si succes=1
ancien_msg = """<p class="error">{{ erreur }}</p>"""
nouveau_msg = """<p class="error">{{ erreur }}</p>
        {% if succes %}
            <p style="color: #10b981; margin-top: 15px; font-weight: 600;">✅ Compte créé avec succès ! Connectez-vous.</p>
        {% endif %}"""
html_conn = html_conn.replace(ancien_msg, nouveau_msg)

with open('templates/connexion.html', 'w', encoding='utf-8') as f:
    f.write(html_conn)
print("✅ Pages Inscription et Connexion mises a jour pour mobile.")

# ==========================================
# 3. ENVOI AUTOMATIQUE SUR GITHUB
# ==========================================
print("Envoi sur GitHub en cours...")
os.system('git add .')
os.system('git commit -m "Amelioration mobile et message de succes inscription"')
os.system('git push')
print("✅ Termine ! Attends 2 minutes que Render redemarre.")
