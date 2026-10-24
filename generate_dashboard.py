import os

# --- 1. CREATION DU FICHIER DASHBOARD.HTML ---
dashboard_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Tableau de bord - Jacob Tools</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background-color: #0b1120; color: #e2e8f0; padding: 30px; }
        h1, h2 { color: #38bdf8; }
        .card { background-color: #1e293b; padding: 25px; border-radius: 12px; margin-bottom: 20px; max-width: 800px; margin-left: auto; margin-right: auto; border: 1px solid #334155; }
        input, textarea { width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; font-family: inherit; }
        input:focus, textarea:focus { outline: none; border-color: #38bdf8; }
        button { padding: 12px 24px; background-color: #38bdf8; color: #0f172a; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: 0.3s; }
        button:hover { background-color: #0ea5e9; }
        a { color: #38bdf8; text-decoration: none; }
        ul { list-style-type: none; padding: 0; }
        li { background-color: #0f172a; padding: 15px; margin-bottom: 10px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #38bdf8; }
        .danger { color: #f87171; cursor: pointer; font-weight: 600; font-size: 0.9em; }
        .danger:hover { text-decoration: underline; }
        .nav-links { text-align: center; margin-top: 20px; }
        .nav-links a { margin: 0 15px; font-weight: 600; }
    </style>
</head>
<body>
    <h1 style="text-align: center;">Tableau de bord Admin</h1>
    <div class="card">
        <h2>Ajouter un contenu</h2>
        <form method="POST" action="/admin/ajouter">
            <input type="text" name="titre" placeholder="Titre (ex: Déblocage iPhone)" required>
            <textarea name="description" placeholder="Description courte" required rows="3"></textarea>
            <input type="text" name="lien" placeholder="Lien (URL de la vidéo ou du cours) - Optionnel">
            <button type="submit">Ajouter au site</button>
        </form>
    </div>
    <div class="card">
        <h2>Vos contenus actuels</h2>
        <ul>
            {% for item in contenus %}
            <li>
                <div>
                    <strong style="color: #38bdf8;">{{ item.titre }}</strong><br>
                    <span style="font-size: 0.9em; color: #94a3b8;">{{ item.description }}</span>
                </div>
                <a href="/admin/supprimer/{{ item.id }}" class="danger">Supprimer</a>
            </li>
            {% else %}
            <li style="justify-content: center; border-left: none; color: #64748b;">Aucun contenu enregistré sur Neon.</li>
            {% endfor %}
        </ul>
    </div>
    <div class="nav-links">
        <a href="/">← Retour au site</a>
        <a href="/admin/logout">Se déconnecter</a>
    </div>
</body>
</html>"""

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_html)

print("✅ Fichier dashboard.html créé avec succes !")
