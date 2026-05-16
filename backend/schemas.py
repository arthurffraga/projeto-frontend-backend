from typing import Optional
from pydantic import BaseModel, ConfigDict

class CategoriaCreate(BaseModel):
    nome: str

class CategoriaUpdate(BaseModel):
    nome: str

class CategoriaResponse(BaseModel):
    id: int
    nome: str