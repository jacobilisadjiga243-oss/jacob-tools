with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# La nouvelle route à insérer
nouvelle_route = """
@app.route('/video/<int:id>')
def video_detail(id):
    conn = get_db()
    video = None
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('SELECT id, titre, image_url, description, lien, categorie FROM contenus WHERE id = %s;', (id,))
                row = cur.fetchone()
                if row:
                    video = {"id": row[0], "titre": row[1], "image_url": row[2], "description": row[3], "lien": row[4], "categorie": row[5]}
        except Exception as e:
            print(f'Erreur lecture video: {e}')
        finally:
            conn.close()
    
    if not video:
        return 'Vidéo introuvable', 404
        
    return render_template('video.html', video=video)

@app.route(ADMIN_URL, methods=['GET', 'POST'])
def admin():"""

# On cherche l'ancienne route admin et on la remplace par la nouvelle + l'ancienne
ancienne_route = """@app.route(ADMIN_URL, methods=['GET', 'POST'])
def admin():"""

if "def video_detail(id):" not in code:
    code = code.replace(ancienne_route, nouvelle_route)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ Route /video/<id> ajoutee dans app.py !")
else:
    print("ℹ️ La route /video/<id> existe deja.")
