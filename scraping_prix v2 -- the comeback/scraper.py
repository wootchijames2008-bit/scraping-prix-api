from config import FICHIER_URL
import requests
from bs4 import BeautifulSoup
from sauvegarde import sauvegarder_produits
from logs import obtenir_logger
import time
from notification import envoyer_alerte_telegramme

logger = obtenir_logger(__name__)

def recuperer_page(url,max_tentatives=3):
    """telecharge le contenue html d'une page avec gestion des retries et du timeout."""
    headers = {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64;x64)AppleWebkit/537.36 (KHTML,like Gecko)chrome/120.0.0.0 Safari/537.36",
        "Accept-language": "fr-FR,fr;q=0.9,en-US;q=0.7"
    }
    for tentative in range(1,max_tentatives + 1):
        try:
            response = requests.get(url,headers=headers, timeout=10)
            if response.status_code == 200:
                logger.info(f"page recuperer avec succes : {url}")
                return response.text
            elif response.status_code == 403:
                logger.error(f"acces refuser (HTTP 403) pour : {url}")
                return None
            else:
                logger.warning(f"Tentative {tentative} - code HTTP innatendue : {response.status_code}")
        except requests.RequestException as e:
            logger.warning(f"Tentative {tentative} echouer (erreur reseau) : {e}")
            if tentative < max_tentatives:
                time.sleep(2)
            logger.error(f"echec definitif pour recuperer l'URL apres {max_tentatives} tentatives : {url}")
            return None

def scraper_page(url):
    """scrape la pge extrait les donnee et netoie proprement les prix en float"""
    html_content = recuperer_page(url)
    if not html_content:
        return[]
    soup = BeautifulSoup(html_content,"html.parser")
    livres_trouves = []
    #adapte les selecteur css selon la structure de mon site cible (ex: books toscrape)
    articles = soup.select(".product_pod")
    for article in articles:
        #extraction du titre
        titre = article.select_one("h3 a") ["title"]
        #extraction du lien 
        lien = article.select_one(".image_container a").get("href")
        #extraction de la disponibilite
        disponibilite = article.select_one(".availability").text.strip()
        #extraction et nettoyage strict du prix en float
        prix_brut = article.select_one(".price_color").text.strip()
        #on retire les symbole monetaire (Â£)
        prix_nettoyee = prix_brut.replace("Â£","").strip()
        conversion_notes = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }
        tag_rating = article.select_one("p",class_="star-rating")
        note_etoiles = 1

        if tag_rating:
            classes = tag_rating.get("class")
            if len(classes) > 1:
                mot_cle = classes[1]
                note_etoiles = conversion_notes.get(mot_cle,0)
        try:
            prix_float = float(prix_nettoyee)
        except ValueError:
            prix_float = 0.0
            logger.error(f"impossible de convertire le prix, '{prix_brut}' pour le livre : {titre}")
            #ajout du dictionnaire propre
        est_disponible = (
            True if "in stock" in disponibilite.lower() else False
        )
        try:
            response = traiter_livre_scrape(titre,prix_float,est_disponible,note_etoiles)
            if response.status_code == 201:
                logger.info(f"livre ajouter avec succes en BDD via l'api : {titre} (note: {note_etoiles})")
            else:
                logger.error(f"Erreur API pour {titre}: {response.text}")
        except Exception as e:
            logger.error(f"impossible de contacter l'api : {e}")
        livres_trouves.append({
            "titre": titre,
            "prix": prix_float,
            "disponibilite": disponibilite,
            "lien": lien
        })
        logger.info(f"{len(livres_trouves)} livres trouver et nettoyer avec succes.")
        return livres_trouves
        

def lancer_scraping(url):
    livre_totals = []
    page_reussie = 0
    page_echoue = 0
    for page in range(1,51):
        url = FICHIER_URL.format(page=page)
        livres = scraper_page(url)
        if livres:
            page_reussie += 1
            livre_totals.extend(livres)
        else:
            page_echoue += 1
    sauvegarder_produits(livre_totals)
    return livre_totals

def verifier_et_mettre_a_jour_prix(livre_id_en_base, ancien_prix, nouveau_prix,titre_livre):
    if nouveau_prix != ancien_prix:
        # le prix a changer on prepare la modificatio partielle dans l'api avec patch
        url_api = f"http://127.0.0.1:8000/livres/{livre_id_en_base}"
        donnee_maj = {"price":
                      nouveau_prix}
        # requete patch vers mon api
        response = requests.patch(url_api,json=donnee_maj)
        print("STATUS PATCH:",response.status_code)
        print("RESPONSE PATCH:",response.text)
        if response.status_code == 200:
            # envoie de l'alerte telegramme
            message = (f"cahngement de prix detecter!**\n\n" f"*{titre_livre}*\n"
                       f"ancien_prix : £{ancien_prix}\n"
                       f"nouveau_prix : £{nouveau_prix}")
    envoyer_alerte_telegramme(message)
    logger.info(f"prix mise a jour et alerte envoyer pour {titre_livre}")

def traiter_livre_scrape(titre,prix_actuelle,stock,rating):
    print("TITRE REÇU :", titre)
    # on interoge l'api pour voir si le livre existe deja
    response_get = requests.get("http://127.0.0.1:8000/livres/?limit=1000")
    if response_get.status_code == 200:
        livre_en_base = response_get.json()
        # on cherche si le livre existe deja par son titre
        livre_trouve = None
        print("NOMBRE DE LIVRES DANS L'API :", len(livre_en_base))
        for livre in livre_en_base:
            if livre["title"] == titre:
                livre_trouve = livre
                break
        print("LIVRE TROUVÉ :", livre_trouve)
        print("CLÉS DU LIVRE :", livre_trouve.keys())
        if livre_trouve:
            # le livre existe deja ! on verifie si le prix a changer
            id_base = livre_trouve["id"]
            ancien_prix = livre_trouve["price"]
            print("ANCIEN PRIX :", ancien_prix)
            print("NOUVEAU PRIX :", prix_actuelle)
            #  on appelle notre fontion de verification et de patch
            verifier_et_mettre_a_jour_prix(id_base,ancien_prix,prix_actuelle,titre)
        else:
            #le livre n'existe pas du tout on fait un poste pour le creer
            nouveau_livre = {
                "title": titre,
                "price": prix_actuelle,
                "rating": rating,
                "stock": stock
            }
            requests.post("http://127.0.0.1:8000/livres/",json = nouveau_livre)