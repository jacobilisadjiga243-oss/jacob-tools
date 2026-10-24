# Lire le fichier
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# On corrige la ligne qui a été mal remplacée
mauvaise_ligne = "DATABASE_URL = os.getenv('DATABASE_URL'), shutil, datetime"
bonne_ligne = "DATABASE_URL = os.getenv('DATABASE_URL')"

code = code.replace(mauvaise_ligne, bonne_ligne)

# On s'assure que tous les imports sont bien là en haut
if "import shutil" not in code:
    code = code.replace("import os, json, time", "import os, json, time, shutil, datetime")

# On sauvegarde
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Erreur corrigée ! Tu peux relancer le site.")
