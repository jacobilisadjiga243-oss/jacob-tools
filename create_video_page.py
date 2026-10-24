html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ video.titre }} - Jacob Tools</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }
        body { background-color: #0b1120; color: #e2e8f0; overflow-x: hidden; }
        
        nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 5%; background: rgba(11, 17, 32, 0.95); position: fixed; width: 100%; top: 0; z-index: 1000; border-bottom: 1px solid #1e293b; backdrop-filter: blur(10px); }
        .logo { font-size: 1.6em; font-weight: 800; color: white; text-decoration: none; letter-spacing: 1px; }
        .logo span { color: #38bdf8; }
        .nav-links { display: flex; gap: 30px; align-items: center; }
        .nav-links a { color: #cbd5e1; text-decoration: none; font-weight: 500; transition: 0.3s; }
        .nav-links a:hover { color: #38bdf8; }
        .btn-nav { background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120 !important; padding: 10px 25px; border-radius: 50px; font-weight: 700; }

        .video-container-page { max-width: 1000px; margin: 120px auto 60px; padding: 0 20px; }
        
        .video-header { margin-bottom: 30px; }
        .video-header h1 { font-size: 2.5em; color: white; margin-bottom: 10px; }
        .badge { display: inline-block; padding: 6px 15px; border-radius: 50px; font-size: 0.8em; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
        .bg-deblocage { background: #38bdf8; color: #0b1120; }
        .bg-hardreset { background: #f59e0b; color: #0b1120; }
        .bg-frp { background: #ef4444; color: white; }
        .bg-marketing { background: #f472b6; color: white; }

        .video-player { width: 100%; aspect-ratio: 16/9; background: #000; border-radius: 16px; overflow: hidden; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .video-player iframe { width: 100%; height: 100%; border: none; }
        .video-player img { width: 100%; height: 100%; object-fit: cover; }

        .video-description { background: #1e293b; padding: 30px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 30px; }
        .video-description h2 { color: #38bdf8; margin-bottom: 15px; }
        .video-description p { color: #cbd5e1; line-height: 1.8; font-size: 1.1em; }

        .action-buttons { display: flex; gap: 20px; flex-wrap: wrap; }
        .btn { display: inline-block; padding: 15px 30px; background: linear-gradient(90deg, #38bdf8, #0ea5e9); color: #0b1120; text-decoration: none; border-radius: 50px; font-weight: 700; transition: 0.3s; text-align: center; flex: 1; min-width: 200px; }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(56,189,248,0.4); }
        .btn-secondary { background: #334155; color: white; border: 1px solid #475569; }
        .btn-secondary:hover { background: #475569; box-shadow: none; }

        footer { background: #0f172a; padding: 40px 5%; text-align: center; border-top: 1px solid #1e293b; margin-top: 60px; }
        .copyright { color: #475569; font-size: 0.9em; }

        @media (max-width: 768px) {
            .video-header h1 { font-size: 1.8em; }
            .nav-links { display: none; }
        }
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">JACOB<span>TOOLS</span></a>
        <div class="nav-links">
            <a href="/">Accueil</a>
            <a href="/#formations">Formations</a>
            <a href="/apropos">À propos</a>
        </div>
    </nav>

    <div class="video-container-page">
        <div class="video-header">
            {% if video.categorie == 'Déblocage' %}<span class="badge bg-deblocage">{{ video.categorie }}</span>
            {% elif video.categorie == 'Hard Reset' %}<span class="badge bg-hardreset">{{ video.categorie }}</span>
            {% elif video.categorie == 'FRP' %}<span class="badge bg-frp">{{ video.categorie }}</span>
            {% else %}<span class="badge bg-marketing">{{ video.categorie }}</span>{% endif %}
            
            <h1>{{ video.titre }}</h1>
        </div>

        <div class="video-player">
            {% if video.lien and ('youtube.com' in video.lien or 'youtu.be' in video.lien) %}
                {% set video_id = video.lien.split('v=')[1].split('&')[0] if 'v=' in video.lien else video.lien.split('/')[-1] %}
                <iframe src="https://www.youtube.com/embed/{{ video_id }}?rel=0&autoplay=0" allowfullscreen></iframe>
            {% else %}
                <img src="{{ video.image_url }}" alt="{{ video.titre }}" onerror="this.src='https://i.postimg.cc/6pQ2y5Gj/placeholder.jpg'">
            {% endif %}
        </div>

        <div class="video-description">
            <h2>Description de la formation</h2>
            <p>{{ video.description }}</p>
        </div>

        <div class="action-buttons">
            <a href="/" class="btn btn-secondary">← Retour à l'accueil</a>
            {% if video.lien %}
                <a href="{{ video.lien }}" class="btn" target="_blank">▶ Ouvrir sur YouTube</a>
            {% endif %}
        </div>
    </div>

    <footer>
        <div class="copyright">&copy; 2026 Jacob Tools. Tous droits réservés.</div>
    </footer>
</body>
</html>"""

with open('templates/video.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Page video.html creee !")
