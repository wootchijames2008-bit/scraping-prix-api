import json
from config import PRIX_MAX
from logs import obtenir_logger

logger = obtenir_logger(__name__)

def trouver_bonne_affaire(fichier_produits = "produits.json", fichier_bonne_affaire = "bonne_affaire.json"):
    with open(fichier_produits, "r", encoding="utf-8") as f:
        livres = json.load(f)
        bonne_affaire = []
        for livre in livres:
            if livre["prix"] < PRIX_MAX:
                bonne_affaire.append(f"{livre["titre"]}, {livre["prix"]},{livre["disponibilite"]}, {livre["lien"]}")
    with open(fichier_bonne_affaire, "w", encoding="utf-8") as f:
        json.dump(bonne_affaire, f, ensure_ascii=False, indent=4)
        logger.info(f"nombre de bonne affaire : {len(bonne_affaire)}")
        return bonne_affaire