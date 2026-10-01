import json


def sauvegarder_produits(livres):
    with open("produits.json", "w", encoding="utf-8") as f:
        json.dump(livres, f, ensure_ascii=False, indent=4)

