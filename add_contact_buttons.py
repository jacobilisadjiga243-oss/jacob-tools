import re

# On lit le fichier index.html actuel
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. On remplace le numéro de téléphone de test par TON vrai numéro
html = html.replace('243000000000', '243977982648')

# 2. On ajoute un bouton Email flottant juste au-dessus du bouton WhatsApp
ancien_bouton_whatsapp = """<a href="https://wa.me/243977982648?text=Bonjour%20Jacob%20Tools,%20je%20suis%20int%C3%A9ress%C3%A9%20par%20vos%20formations." class="whatsapp-float" target="_blank" rel="noopener noreferrer">"""

nouveau_bouton = """<!-- BOUTON FLOTTANT EMAIL -->
    <!-- REMPLACE 'ton.email@exemple.com' PAR TON VRAIE ADRESSE EMAIL -->
    <a href="mailto:ton.email@exemple.com?subject=Contact%20Jacob%20Tools" class="email-float" target="_blank" rel="noopener noreferrer">
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" fill="white"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
    </a>

    <!-- BOUTON FLOTTANT WHATSAPP -->
    """ + ancien_bouton_whatsapp

html = html.replace(ancien_bouton_whatsapp, nouveau_bouton)

# 3. On ajoute le style CSS pour le bouton Email
ancien_css = """.whatsapp-float:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(37, 211, 102, 0.6);
        }"""

nouveau_css = """.whatsapp-float:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(37, 211, 102, 0.6);
        }
        
        .email-float {
            position: fixed;
            width: 60px;
            height: 60px;
            bottom: 110px;
            right: 40px;
            background-color: #38bdf8;
            color: #FFF;
            border-radius: 50px;
            text-align: center;
            font-size: 30px;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.3s;
            text-decoration: none;
        }
        .email-float:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(56, 189, 248, 0.6);
        }"""

html = html.replace(ancien_css, nouveau_css)

# 4. Ajustement pour le mobile (pour que les boutons ne se chevauchent pas)
html = html.replace(
    ".whatsapp-float { bottom: 20px; right: 20px; width: 50px; height: 50px; font-size: 25px; }",
    ".whatsapp-float { bottom: 20px; right: 20px; width: 50px; height: 50px; font-size: 25px; }\n            .email-float { bottom: 85px; right: 20px; width: 50px; height: 50px; font-size: 25px; }"
)

# On sauvegarde
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Numero WhatsApp mis a jour et bouton Email ajoute !")
