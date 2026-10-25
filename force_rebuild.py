import os

# On ajoute un commentaire à la fin de index.html pour forcer la mise à jour
with open('templates/index.html', 'a', encoding='utf-8') as f:
    f.write("\n<!-- Force update -->")

# On force l'ajout sur Git
print("Envoi sur GitHub en cours...")
os.system('git add -A')
os.system('git commit -m "Force rebuild du site"')
os.system('git push')
print("✅ Envoye ! Attends 2 minutes que Render redemarre.")
