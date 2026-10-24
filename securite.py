# On lit le fichier app.py actuel
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# On ajoute le module de sauvegarde
import_code = "import os, json, time, shutil, datetime\n"
code = code.replace("import os, json, time\n", import_code)

# On modifie la fonction sauvegarder_donnees pour faire des backups
ancienne_fonction = """def sauvegarder_donnees(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)"""

nouvelle_fonction = """def sauvegarder_donnees(data):
    # 1. Créer une sauvegarde horodatée avant d'écraser
    if os.path.exists(DATA_FILE):
        os.makedirs('backups', exist_ok=True)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        shutil.copy(DATA_FILE, f"backups/data_{date_str}.json")
    
    # 2. Écrire les nouvelles données
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)"""

code = code.replace(ancienne_fonction, nouvelle_fonction)

# On sauvegarde le fichier modifié
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("✅ Sécurité activée : Une sauvegarde sera créée à chaque modification.")
