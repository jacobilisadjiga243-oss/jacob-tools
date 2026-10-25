import os

with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

# 1. On s'assure que le menu "Gestion" ne s'affiche QUE si on est sur la page list
# (On utilise la variable 'page' envoyée par le serveur)
dash = dash.replace('<a href="/admin" class="nav-item {% if page == \'list\' %}active{% endif %}">', '<a href="/admin" class="nav-item {% if page == \'list\' or not page %}active{% endif %}">')

# 2. On s'assure que la section "Vos vidéos" ne s'affiche QUE si on est sur la page list
# On cherche la div id="tab-list" et on ajoute la condition Jinja
ancien_list = """<div id="tab-list" class="tab-content active">"""
nouveau_list = """<div id="tab-list" class="tab-content {% if not page or page == 'list' %}active{% endif %}">"""
dash = dash.replace(ancien_list, nouveau_list)

# 3. On s'assure que la section "Messages" s'affiche correctement
ancien_msg = """<div id="tab-messages" class="tab-content {% if page == 'messages' %}active{% endif %}">"""
nouveau_msg = """<div id="tab-messages" class="tab-content {% if page == 'messages' %}active{% endif %}">"""
# (C'était déjà bon, on ne change rien)

# 4. On s'assure que la section "Paramètres" s'affiche correctement
ancien_param = """<div id="tab-parametres" class="tab-content {% if page == 'parametres' %}active{% endif %}">"""
nouveau_param = """<div id="tab-parametres" class="tab-content {% if page == 'parametres' %}active{% endif %}">"""
# (C'était déjà bon, on ne change rien)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash)

print("✅ Correction de l'affichage des onglets admin !")

# Envoi automatique sur GitHub
os.system('git add .')
os.system('git commit -m "Correction de l affichage des onglets admin"')
os.system('git push')
print("✅ Envoye ! Attends 2 min que Render redemarre.")
