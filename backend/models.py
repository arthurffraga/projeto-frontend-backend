from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    medicamentos = relationship("Medicamento", back_populates="categoria")
    
class Medicamento(Base):
    __tablename__ = "medicamento"
    id = Column(Integer, primary_key= True)
    nome = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
    unidade = Column(String)
    categoria_id = Column(Integer, ForeignKey("categoria.id"))
    categoria = relationship("Categoria", back_populates="medicamentos")

class Venda(Base):
    __tablename__ = "venda"
    id = Column(Integer, primary_key=True)
    dataVenda = Column(DateTime, default=func.now())
    formaPagamento = Column(String)
    total = Column(Float)
    itens = relationship("ItemVenda", back_populates="venda")

class ItemVenda(Base):
    __tablename__ = "item_venda"
    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer)
    precoUnidade = Column(Float)
    venda_id = Column(Integer, ForeignKey("venda.id"))
    medicamento_id = Column(Integer, ForeignKey("medicamento.id"))
    venda = relationship("Venda", back_populates="itens")
    medicamento = relationship("Medicamento")