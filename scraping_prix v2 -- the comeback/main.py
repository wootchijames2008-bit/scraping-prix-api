from scraper import lancer_scraping
from price_change import trouver_changement
from price_checker import trouver_bonne_affaire
from price_history import enregistrer_historique
from logs import obtenir_logger
from config import FICHIER_URL

logger = obtenir_logger(__name__)

def main():
    logger.info("=== Demarage du scri  pt global de scraping===")
    #etape 1 : Recuperation des donnee actuelle
    logger.info("etape 1/4 : lancement du scraping...")
    produits = lancer_scraping(url=FICHIER_URL)
    if not produits:
        logger.error("arret du scraping : aucun produit recuperer")
        return
    #etape 2 : enregistrement dans l'historique
    logger.info("etape 2/4 : enregistrement de l'historique des prix...")
    enregistrer_historique()
    #etape 3 : analyse des changement et alertes
    logger.info("etape 3/4 : analyse des variation des prix...")
    changement = trouver_changement()
    if not changement:
        logger.info("aucun changement detecter dans les produit recuperer")
    # etpe 4 : filtrage des produits pour trouver un prix optimal
    logger.info("etape 4: Filtrage des bonne affaires")
    trouver_bonne_affaire()
    logger.info("===cycle de scraping terminer avec succes===")

if __name__ == "__main__":
    main()