import re

# ==========================================
# 1. MISE A JOUR DE APP.PY POUR NEON (Préparation)
# ==========================================
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# On ajoute les imports pour Neon
if "import psycopg" not in app_code:
    app_code = app_code.replace(
        "import os, json, time",
        "import os, json, time\nimport psycopg\nfrom dotenv import load_dotenv\n\nload_dotenv()\nDATABASE_URL = os.getenv('DATABASE_URL')"
    )

# On prépare la fonction pour utiliser Neon (si le lien est présent)
ancienne_fonction = """def lire_donnees():
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return []"""

nouvelle_fonction = """def lire_donnees():
    # Si on a un lien Neon, on l'utilise (plus tard)
    if DATABASE_URL:
        try:
            with psycopg.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, titre, image_url, description, lien, categorie FROM contenus ORDER BY id DESC;")
                    rows = cur.fetchall()
                    return [{"id": r[0], "titre": r[1], "image_url": r[2], "description": r[3], "lien": r[4], "categorie": r[5]} for r in rows]
        except Exception as e:
            print(f"Erreur Neon: {e}")
            return []
    # Sinon, on utilise le fichier local (pour l'instant)
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except: return []"""

app_code = app_code.replace(ancienne_fonction, nouvelle_fonction)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)


# ==========================================
# 2. MISE A JOUR DE L'ACCUEIL POUR LE LECTEUR YOUTUBE
# ==========================================
with open('templates/index.html', 'r', encoding='utf-8') as f:
    index_code = f.read()

# Fonction Jinja pour transformer un lien YouTube en iframe
# On l'ajoute tout en haut du fichier HTML
if "{% macro youtube_embed" not in index_code:
    macro_youtube = """{% macro youtube_embed(url) %}
    {% if 'youtube.com' in url or 'youtu.be' in url %}
        {% set video_id = url.split('v=')[1].split('&')[0] if 'v=' in url else url.split('/')[-1] %}
        <iframe width="100%" height="200" src="https://www.youtube.com/embed/{{ video_id }}" frameborder="0" allowfullscreen style="border-radius: 16px 16px 0 0;"></iframe>
    {% else %}
        <img src="{{ url }}" class="card-img" alt="Image" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">
    {% endif %}
{% endmacro %}"""
    index_code = index_code.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n" + macro_youtube)

# On remplace l'image de la carte par le lecteur si c'est une vidéo
ancienne_carte = """<img src="{{ item.image_url }}" class="card-img" alt="{{ item.titre }}" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">
                <div class="card-body">"""

nouvelle_carte = """{{ youtube_embed(item.image_url) }}
                <div class="card-body">"""
index_code = index_code.replace(ancienne_carte, nouvelle_carte)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_code)

print("✅ Le lecteur YouTube est pret ! Et le code est pret pour Neon.")
