import json

# 1. On met à jour le fichier index.html pour intégrer le lecteur
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# On crée un "filtre" pour transformer le lien YouTube en lecteur
macro = """{% macro youtube_embed(url) %}
    {% if url and ('youtube.com' in url or 'youtu.be' in url) %}
        {% set video_id = url.split('v=')[1].split('&')[0] if 'v=' in url else url.split('/')[-1] %}
        <iframe width="100%" height="200" src="https://www.youtube.com/embed/{{ video_id }}" frameborder="0" allowfullscreen style="border-radius: 16px 16px 0 0;"></iframe>
    {% else %}
        <img src="{{ url }}" class="card-img" alt="Image" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">
    {% endif %}
{% endmacro %}
"""

# On ajoute ce filtre tout en haut du fichier HTML
if "{% macro youtube_embed" not in html:
    html = html.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n" + macro)

# On remplace l'image par le lecteur (ou l'image si ce n'est pas youtube)
ancien_code = """<img src="{{ item.image_url }}" class="card-img" alt="{{ item.titre }}" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">"""
nouveau_code = """{{ youtube_embed(item.image_url) }}"""

html = html.replace(ancien_code, nouveau_code)

# On sauvegarde le fichier
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Le lecteur video est pret !")
