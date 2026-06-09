from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from datetime import datetime

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
    page: int = Field(ge=1, description= "A página deve ser 1 ou maior")
    limit: int = Field(ge=1)
    pages: int

class PaginatedCategoria(BaseModel):
    data: list[CategoriaResponse]
    total: int
    page: int = Field(ge=1, description= "A página deve ser 1 ou maior")
    limit: int = Field(ge=1)
    pages: int

class ItemVendaCreate(BaseModel):
    medicamento_id: int
    quantidade: int

class ItemVendaResponse(BaseModel):
    id: int
    quantidade: int
    precoUnitario: float
    medicamento: MedicamentoResponse
    model_config = ConfigDict(from_attributes=True)

class VendaCreate(BaseModel):
    formaPagamento: FormaPagamento
    itens: list[ItemVendaCreate]

class VendaResponse(BaseModel):
    id: int
    dataVenda: datetime
    total: float
    formaPagamento: FormaPagamento
    itens: list[ItemVendaResponse]
    model_config = ConfigDict(from_attributes=True)

class PaginatedVenda(BaseModel):
    data: list[VendaResponse]
    total: int
    page: int = Field(ge=1, description= "A página deve ser 1 ou maior")
    limit: int = Field(ge=1)
    pages: int

class UsuarioCreate(BaseModel):
    username: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

class PaginatedUsuario(BaseModel):
    data: list[UsuarioResponse] 
    total: int
    page: int = Field(ge=1, description= "A página deve ser 1 ou maior")
    limit: int = Field(ge=1)
    pages: int