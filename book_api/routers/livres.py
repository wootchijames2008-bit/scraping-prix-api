from database import get_db
import model
from fastapi import APIRouter,Depends, status, HTTPException
from sqlalchemy.orm import Session
import shemas
from typing import Optional
#initialisation du router pour le module 
router = APIRouter(prefix="/livres", tags=["Livres"])

@router.get("/", response_model=list[shemas.LivreResponse])
def lister_livres(skip: int = 0, limit: int = 1000,min_rating: Optional[int] = None,
                  en_stock: Optional[bool] = None,
                  tri_prix: Optional[str] = (None),
                  db: Session= Depends(get_db),):
    query = db.query(model.LivreModel)
    #filtrage par note minimal
    if min_rating is not None:
        query = query.filter(model.LivreModel.rating >= min_rating)
    #filtrage par stock
    if en_stock is not None:
        query = query.filter(model.LivreModel.stock == en_stock)
    #tri par prix
    if tri_prix == "asc":
        query = query.order_by(model.LivreModel.price.asc())
    elif tri_prix == "desc":
        query = query.order_by(model.LivreModel.price.desc())
    livres = query.offset(skip).limit(limit).all()
    return livres

@router.post("/",response_model=shemas.LivreResponse,
             status_code=status.HTTP_201_CREATED,)
def creer_livre(payload:shemas.LivreCreate, db:
                Session = Depends(get_db)):
    #on creer une instance du modele SQLAlchemy avec les donnee valider par pydantic
    nouveau_livre = model.LivreModel(
        title=payload.title,
        price=payload.price,
        rating=payload.rating,
        stock=payload.stock
    )
    #on l'ajoute a la session active
    db.add(nouveau_livre)
    #on valide commit() pour l'ecrire dans la base de donnee SQLite
    db.commit()
    #on rafraichit l'objet pour recuperer L"ID unique gerer par la base
    db.refresh(nouveau_livre)
    return nouveau_livre

@router.patch("/{livre_id}",response_model=shemas.LivreResponse)
def modifier_livre_partielle(livre_id: int, payload:shemas.LivreUpdate, db:
                 Session = Depends(get_db)):
    #on recherche le livre existant
    livre = (
        db.query(model.LivreModel).filter(model.LivreModel.id == livre_id)
        .first()
    )
    if not livre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Le livre avec l'ID {livre_id} est introuvable.",)
    # on recupere uniquement les donne envoyer dans la requete
    donnees_fournie = payload.model_dump(exclude_unset=True)
    #on met a jour dynamiquement les attributs du model SQLAlshemy
    for cle, valeur in donnees_fournie.items():
        setattr(livre, cle, valeur)
        # on enregistre en base de donner
    db.commit()
    db.refresh(livre)
    return livre

@router.delete("/{livre_id}",status_code=status.HTTP_200_OK)
def effacer_un_livre(livre_id: int, db:
                     Session = Depends(get_db)):
    livre = (
        db.query(model.LivreModel).filter(model.LivreModel.id == livre_id)
        .first()
    )
    if not livre:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"le livre avec l'ID {livre_id} n'est pa trouver ou a deja ete effacer")
    db.delete(livre)
    db.commit()
        