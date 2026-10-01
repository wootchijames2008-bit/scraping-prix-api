from database import Base
from sqlalchemy import Column,Float, Integer, String

class LivreModel(Base):
    __tablename__ = "livre"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String,unique=True, index=True, nullable=False)
    price = Column(Float,nullable=False)
    rating = Column(Integer)
    stock = Column(Integer,default=0)