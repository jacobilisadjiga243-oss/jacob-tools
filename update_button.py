with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

ancien_bouton = '<a href="{{ item.lien }}" class="btn" target="_blank" style="text-align: center; padding: 12px 20px;">▶ Regarder la vidéo</a>'
nouveau_bouton = '<a href="/video/{{ item.id }}" class="btn" style="text-align: center; padding: 12px 20px;">▶ Voir la formation</a>'

if ancien_bouton in html:
    html = html.replace(ancien_bouton, nouveau_bouton)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✅ Lien vers la page video ajoute sur l'accueil !")
else:
    print("⚠️ Je n'ai pas trouve le bouton exact. Verification manuelle requise.")
