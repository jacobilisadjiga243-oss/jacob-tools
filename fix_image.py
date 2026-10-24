# On lit le fichier actuel
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# On remplace l'ancien lien cassé par une magnifique image de système d'exploitation
ancien_lien = 'https://images.unsplash.com/photo-1629654297299-c8506221ca3b?q=80&w=800&auto=format&fit=crop'
nouveau_lien = 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=800&auto=format&fit=crop'

# On fait le remplacement
content = content.replace(ancien_lien, nouveau_lien)

# On sauvegarde le fichier
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ L'image pour les Systemes d'Exploitation a ete reparee !")
