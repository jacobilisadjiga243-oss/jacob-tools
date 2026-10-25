import os

# 1. Vérification locale
with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

if 'name="whatsapp"' not in dash:
    print("⚠️ Le formulaire de paramètres n'est PAS dans le fichier local. Correction...")
    # On ajoute le formulaire à la place du texte "bientôt disponible"
    ancien_texte = """<div id="tab-parametres" class="tab-content {% if page == 'parametres' %}active{% endif %}">
            <div class="card">
                <h2>Paramètres du site</h2>
                <p style="color: #94a3b8; text-align: center; padding: 40px;">Les paramètres seront bientôt disponibles.</p>
            </div>
        </div>"""
    
    nouveau_texte = """<div id="tab-parametres" class="tab-content {% if page == 'parametres' %}active{% endif %}">
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
    
    dash = dash.replace(ancien_texte, nouveau_texte)
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dash)
    print("✅ Formulaire ajouté localement.")
else:
    print("✅ Le formulaire est déjà dans le fichier local.")

# 2. Envoi forcé sur GitHub
print("Envoi forcé sur GitHub...")
os.system('git add -f templates/dashboard.html')
os.system('git commit -m "Force mise a jour du formulaire parametres"')
os.system('git push')
print("✅ Terminé. Attends 2 minutes que Render redémarre, puis fais Ctrl+F5.")
