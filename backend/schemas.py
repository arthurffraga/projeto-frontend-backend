from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum

class Unidade(str, Enum):
    ml = "ml"
    mg = "mg"
    g = "g"

class FormaPagamento(str, Enum):
    pix = "Pix"
    credito = "Crédito"
    debito = "débito"
    dinheiro = "Dinheiro"
class CategoriaCreate(BaseModel):
    nome: str

class CategoriaUpdate(BaseModel):
    nome: str

class CategoriaResponse(BaseModel):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)

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
    categoria: CategoriaResponse
    model_config = ConfigDict(from_attributes=True)

class PaginatedMedicamento(BaseModel):
    data: list[MedicamentoResponse]
    total: int
    page: int
    limit: int
    pages: int

class PaginatedCategoria(BaseModel):
    data: list[CategoriaResponse]
    total: int
    page: int
    limit: int
    pages: int

