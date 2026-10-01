import json
from logs import obtenir_logger
from datetime import datetime

logger = obtenir_logger(__name__)

def enregistrer_historique():
    try:
        with open("produits.json", "r", encoding="utf-8") as f:
            livres_actuelle = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.info("creation de produit.json")
        return
    try:
      with open("historique_prix.json", "r", encoding="utf-8") as f:
          historique = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        historique = []
    session = {
        "date": datetime.now().isoformat(),
        "livres": livres_actuelle
    }
    historique.append(session)  
    with open("historique_prix.json", "w", encoding="utf-8") as f:
        json.dump(historique, f, ensure_ascii=False, indent=4)
        logger.info("historique sauvegarder")
        logger.info(f"nombre de releve : {len(historique)}")

