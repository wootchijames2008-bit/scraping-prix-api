import requests
from config import FICHIER_TOKEN,ID
from logs import obtenir_logger

logger = obtenir_logger(__name__)

def envoyer_alerte_telegramme(message):
    url = f"https://api.telegram.org/bot{FICHIER_TOKEN}/sendMessage"

    payload = {
        "chat_id": ID,
        "text": message,
    }

    try:
        response = requests.post(url,json=payload)
        if response.status_code != 200:
            logger.error(f"Erreur d'envoie telegram: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f" Erreur reseau lors de l'alerte telegram: {e}")