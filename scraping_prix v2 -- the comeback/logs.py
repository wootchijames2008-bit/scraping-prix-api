import logging

#configuration de base du systeme de logging
logging.basicConfig(filename="app.log",
                    level= logging.INFO,
                    format="%(asctime)s -%(levelname)s -%(message)s",
                    encoding="utf-8")
def obtenir_logger(nom):
    """renvoie un logger configurer pour le module qui l'appelle."""
    return logging.getLogger(nom)