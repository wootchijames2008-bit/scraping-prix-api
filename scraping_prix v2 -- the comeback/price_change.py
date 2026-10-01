import json
from config import FICHIER_PRODUIT, FICHIER_HISTORIQUE
from logs import obtenir_logger
from notification import envoyer_alerte_telegramme

logger = obtenir_logger(__name__)

def trouver_changement(fichier_produit = "produits.json", fichier_historique = "historique_prix.json"):
    try:
        with open(fichier_produit, "r", encoding="utf-8") as f:
            fichier_produit = json.load(f)
    except FileNotFoundError:
        logger.error("liste de livre non trouver")
    try:
        with open(fichier_historique, "r", encoding="utf-8") as f:
            fichier_historique = json.load(f)
    except FileNotFoundError:
        logger.error("fichier_historique non trouver")
    if len(fichier_historique) <= 2:
        logger.info("il n'yas pas asser de relever")
        return
    ancien = fichier_historique[-2]
    nouveau = fichier_historique[-1]
    ancien_livres = ancien["livres"]
    nouveau_livres = nouveau["livres"]

    anciens = {livre["lien"]: livre for livre in ancien_livres}
    nouveaux = {livre["lien"]: livre for livre in nouveau_livres}

    for lien, nouveau_livres in nouveaux.items():
        ancien_livres = anciens.get(lien)

        if ancien_livres is None:
            continue
        difference_prix = nouveau_livres["prix"] - ancien_livres["prix"]

        if difference_prix < 0:
            message = (f"le prix du livre : {nouveau_livres['titre']}"
                f" a diminuer de {abs(difference_prix):.2f}£")
            logger.info(message)
            envoyer_alerte_telegramme(message)
        elif difference_prix > 0:
            message = (f"le prix du livre: {nouveau_livres['titre']}"
                f"a augmenter de {difference_prix:.2f}£")
            logger.info(message)
            envoyer_alerte_telegramme(message)
        else:
             logger.info("le prix d'aucun livre n'as changer")