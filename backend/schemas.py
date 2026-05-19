from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum

class Unidade(str, Enum):
    ml = "ml"
    mg = "mg"
    g = "g"
class CategoriaCreate(BaseModel):
    nome: str

class CategoriaUpdate(BaseModel):
    nome: str

class CategoriaResponse(BaseModel):
    id: int
    nome: str

class MedicamentoCreate(BaseModel):
    nome: str
    preco: float
    quantidade: int
    unidade: Unidade
    categoria_id: int

class MedicamentoUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    quantidade: Optional[int] = None
    unidade: Optional[Unidade] = None
    categoria_id: Optional[int] = None

class MedicamentoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    quantidade: int
    unidade: Unidade
    categoria_id: int
