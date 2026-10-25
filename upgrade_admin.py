import os

# ==========================================
# 1. MISE A JOUR DE APP.PY (Ajout des routes admin)
# ==========================================
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# On ajoute la route /admin/messages
route_messages = """
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
def admin():"""

if "def admin_messages():" not in code:
    code = code.replace("""@app.route(ADMIN_URL, methods=['GET', 'POST'])
def admin():""", route_messages)

# On s'assure que la route admin passe la variable 'page' au template
code = code.replace("return render_template('dashboard.html', contenus=contenus, modifier=None)", "return render_template('dashboard.html', contenus=contenus, modifier=None, page='list')")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("✅ app.py mis a jour avec les nouvelles routes admin.")

# ==========================================
# 2. MISE A JOUR DU DASHBOARD.HTML (Nouveaux onglets)
# ==========================================
with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

# On ajoute les boutons dans le menu de gauche
ancien_menu = """<button class="nav-item active" onclick="openTab('list')">📋 Gestion</button>
        <button class="nav-item" onclick="openTab('add')">➕ Ajouter</button>
        <a href="/" class="nav-item" target="_blank">🌐 Voir le site</a>"""

nouveau_menu = """<a href="/admin" class="nav-item {% if page == 'list' %}active{% endif %}">📋 Gestion</a>
        <button class="nav-item" onclick="openTab('add')">➕ Ajouter</button>
        <a href="/admin/messages" class="nav-item {% if page == 'messages' %}active{% endif %}">✉️ Messages</a>
        <a href="/admin/parametres" class="nav-item {% if page == 'parametres' %}active{% endif %}">⚙️ Paramètres</a>
        <a href="/" class="nav-item" target="_blank">🌐 Voir le site</a>"""

dash = dash.replace(ancien_menu, nouveau_menu)

# On ajoute une section vide pour les messages et paramètres
ancien_fin = """</div>
    <script>
        function openTab(tabName) {"""

nouveau_fin = """</div>
        
        <!-- SECTION MESSAGES (Vide pour l'instant) -->
        <div id="tab-messages" class="tab-content {% if page == 'messages' %}active{% endif %}">
            <div class="card">
                <h2>Messages reçus</h2>
                <p style="color: #94a3b8; text-align: center; padding: 40px;">La boîte de réception sera bientôt disponible.</p>
            </div>
        </div>

        <!-- SECTION PARAMETRES (Vide pour l'instant) -->
        <div id="tab-parametres" class="tab-content {% if page == 'parametres' %}active{% endif %}">
            <div class="card">
                <h2>Paramètres du site</h2>
                <p style="color: #94a3b8; text-align: center; padding: 40px;">Les paramètres seront bientôt disponibles.</p>
            </div>
        </div>

    </div>
    <script>
        function openTab(tabName) {"""

dash = dash.replace(ancien_fin, nouveau_fin)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash)
print("✅ dashboard.html mis a jour avec les nouveaux menus.")

# ==========================================
# 3. ENVOI AUTOMATIQUE SUR GITHUB
# ==========================================
print("Envoi sur GitHub en cours...")
os.system('git add .')
os.system('git commit -m "Ajout des onglets Messages et Parametres dans l admin"')
os.system('git push')
print("✅ Termine ! Attends 2 minutes que Render redemarre.")
