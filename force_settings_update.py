import os

# 1. On force un petit changement pour être sûr que Git détecte la modification
with open('app.py', 'a', encoding='utf-8') as f:
    f.write("\n# Force update parametres")

print("Envoi sur GitHub en cours...")
os.system('git add -A')
os.system('git commit -m "Activation du formulaire de parametres"')
os.system('git push')
print("✅ Envoye ! Attends 2 minutes que Render redemarre.")
