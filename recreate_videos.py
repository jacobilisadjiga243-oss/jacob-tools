import json

# On prépare les 4 vidéos avec les nouvelles catégories
videos = [
    {
        "id": 1,
        "titre": "DEBLOCAGE SAMSUNG",
        "image_url": "https://images.unsplash.com/photo-1592890288564-76628a30a657?q=80&w=800",
        "description": "Courte video sur le deblocage.",
        "lien": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "categorie": "Déblocage"
    },
    {
        "id": 2,
        "titre": "HARD RESET IPHONE",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=800",
        "description": "Methode complete pour le hard reset.",
        "lien": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "categorie": "Hard Reset"
    },
    {
        "id": 3,
        "titre": "CONTOURNER LE FRP",
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=800",
        "description": "Solution FRP 100% gratuite.",
        "lien": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "categorie": "FRP"
    },
    {
        "id": 4,
        "titre": "MARKETING DIGITAL",
        "image_url": "https://images.unsplash.com/photo-1557838923-2985c318be48?q=80&w=800",
        "description": "Apprenez a vendre en ligne.",
        "lien": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "categorie": "Marketing"
    }
]

# On sauvegarde dans data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(videos, f, ensure_ascii=False, indent=4)

print("✅ Tes 4 videos ont ete recreees avec succes !")
