from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True)
    nome = Column(String)

class Medicamento(Base):
    __tablename__ = "medicamento"
    id = Column(Integer, primary_key= True)
    nome = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
    unidade = Column(String)
    categoria_id = Column(Integer, ForeignKey("categoria.id"))
