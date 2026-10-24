import re

# 1. Mise à jour de app.py pour accepter la nouvelle catégorie
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# On ne touche pas au code, la catégorie est déjà dynamique dans les formulaires
print("app.py est prêt.")

# 2. Mise à jour du dashboard pour les 4 catégories
with open('templates/dashboard.html', 'r', encoding='utf-8') as f:
    dash_code = f.read()

ancien_select = """<option value="Déblocage" {% if modifier and modifier.categorie == 'Déblocage' %}selected{% endif %}>Déblocage</option>
                                <option value="Système" {% if modifier and modifier.categorie == 'Système' %}selected{% endif %}>Système</option>
                                <option value="Marketing" {% if modifier and modifier.categorie == 'Marketing' %}selected{% endif %}>Marketing</option>"""

nouveau_select = """<option value="Déblocage" {% if modifier and modifier.categorie == 'Déblocage' %}selected{% endif %}>Déblocage</option>
                                <option value="Hard Reset" {% if modifier and modifier.categorie == 'Hard Reset' %}selected{% endif %}>Hard Reset</option>
                                <option value="FRP" {% if modifier and modifier.categorie == 'FRP' %}selected{% endif %}>FRP</option>
                                <option value="Marketing" {% if modifier and modifier.categorie == 'Marketing' %}selected{% endif %}>Marketing</option>"""

dash_code = dash_code.replace(ancien_select, nouveau_select)

# On change aussi la couleur des badges sur l'accueil pour ces nouvelles catégories
with open('templates/index.html', 'r', encoding='utf-8') as f:
    index_code = f.read()

# On ajoute des classes CSS pour les nouveaux badges
ancien_badge_css = """.bg-deblocage { background: #38bdf8; color: #0b1120; }
        .bg-systeme { background: #818cf8; color: white; }
        .bg-marketing { background: #f472b6; color: white; }"""

nouveau_badge_css = """.bg-deblocage { background: #38bdf8; color: #0b1120; }
        .bg-hardreset { background: #f59e0b; color: #0b1120; }
        .bg-frp { background: #ef4444; color: white; }
        .bg-marketing { background: #f472b6; color: white; }"""
index_code = index_code.replace(ancien_badge_css, nouveau_badge_css)

# On met à jour les conditions dans la boucle Jinja
ancien_badge_html = """{% if item.categorie == 'Déblocage' %}<span class="badge bg-deblocage">{{ item.categorie }}</span>
                {% elif item.categorie == 'Système' %}<span class="badge bg-systeme">{{ item.categorie }}</span>
                {% else %}<span class="badge bg-marketing">{{ item.categorie }}</span>{% endif %}"""

nouveau_badge_html = """{% if item.categorie == 'Déblocage' %}<span class="badge bg-deblocage">{{ item.categorie }}</span>
                {% elif item.categorie == 'Hard Reset' %}<span class="badge bg-hardreset">{{ item.categorie }}</span>
                {% elif item.categorie == 'FRP' %}<span class="badge bg-frp">{{ item.categorie }}</span>
                {% else %}<span class="badge bg-marketing">{{ item.categorie }}</span>{% endif %}"""
index_code = index_code.replace(ancien_badge_html, nouveau_badge_html)

with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash_code)
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_code)

print("✅ Catégories mises à jour : Déblocage, Hard Reset, FRP, Marketing.")
