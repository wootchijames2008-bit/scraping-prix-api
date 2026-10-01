from pydantic import BaseModel, Field

class LivreCreate(BaseModel):
    title : str = Field(min_length=2)
    price : float = Field(gt=0)
    rating: int = Field(ge=1, le=5)
    stock: bool

class LivreResponse(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    stock: bool

class LivreUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2)
    price: float | None = Field(default=None, gt=0)
    rating: int | None = Field(default=None, ge=1, le=5)
    stock: bool | None = None

