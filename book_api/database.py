from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#L'URL de connexion vers mon fichier SQLITE local
SQLALCHEMY_DATABASE_URL = "sqlite:///./livre.db"

#le moteur engine gere la connexion physique avec la base de donnee
#note:check_same_thread=False est indispensable pour SQLITE avec fastapi
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
#la session: c'est l'outil qui permetra d'ouvrir et de fermer la transactions(ajoueter,lire,modifier)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)
#la classe de base dont mon model dans (model.py) va heriter 
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()