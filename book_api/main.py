from pathlib import Path
from fastapi import FastAPI,APIRouter
from routers import livres
from database import Base,engine
from model import LivreModel

Base.metadata.create_all(bind=engine)
router = APIRouter(prefix="/livres", tags=["livres"])
app = FastAPI()
app.include_router(livres.router)

@app.get("/")
def acceuil():
    return {"message": "bienvenue sur mon api de livres !"}