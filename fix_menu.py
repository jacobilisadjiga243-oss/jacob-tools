import os

# On lit le fichier index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# On vérifie si le lien est déjà là
if 'À propos' not in html:
    # On cherche le lien Services et on ajoute À propos juste après
    ancien_lien = '<a href="#services">Services</a>'
    nouveau_lien = '<a href="#services">Services</a>\n            <a href="/apropos">À propos</a>'
    
    if ancien_lien in html:
        html = html.replace(ancien_lien, nouveau_lien)
        with open('templates/index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✅ Le lien À propos a ete ajoute avec succes !")
    else:
        print("⚠️ Je n'ai pas trouve le lien Services. Verifie le fichier.")
else:
    print("ℹ️ Le lien À propos est deja present.")
