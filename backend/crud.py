from sqlalchemy.orm import Session
from models import Medicamento, Categoria
from schemas import MedicamentoCreate, MedicamentoUpdate, CategoriaCreate, CategoriaUpdate
import math
def readMedicamento(db: Session, nome: str = None, page: int = 1, limit: int = 10):
    query = db.query(Medicamento)
    if nome:
        query = query.filter(Medicamento.nome.ilike(f"%{nome}%"))
    
    totalQuery = query.count()
    if limit > 0:
        totalPage = math.ceil(totalQuery/limit)
    else:
        totalPage = 0
    pular = (page - 1) * limit
    dados = query.offset(pular).limit(limit).all()

    return {
        "data": dados,
        "total": totalQuery,
        "page": page,
        "limit": limit,
        "pages": totalPage
    }

def getMedicamento(db: Session, medicamento_id: int):
    return db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()

def createMedicamento(db: Session, dados: MedicamentoCreate):
    medicamento = Medicamento(**dados.model_dump())
    categoriaValidacao = getCategoria(db, dados.categoria_id)
    if not categoriaValidacao:
        return None
    db.add(medicamento)
    db.commit()
    db.refresh(medicamento)
    return medicamento

def updateMedicamento(db: Session, medicamento_id: int, dados: MedicamentoUpdate):
    medicamento = getMedicamento(db, medicamento_id)
    if not medicamento:
        return None
    update = dados.model_dump(exclude_unset=True)
    for campo, valor in update.items():
        setattr(medicamento, campo, valor)
    db.commit()
    db.refresh(medicamento)
    return medicamento

def replaceMedicamento(db: Session, medicamento_id, dados: MedicamentoCreate):
    medicamento = getMedicamento(db, medicamento_id)
    if not medicamento:
        return None
    replace = dados.model_dump()
    for campo, valor in replace.items():
        setattr(medicamento, campo, valor)
    db.commit()
    db.refresh(medicamento)
    return medicamento

def deleteMedicamento(db: Session, medicamento_id: int):
    medicamento = getMedicamento(db, medicamento_id)
    if not medicamento:
        return None
    db.delete(medicamento)
    db.commit()
def readCategoria(db: Session, nome: str = None, page: int = 1, limit: int = 10):
    query = db.query(Categoria)
    if nome:
        query = query.filter(Categoria.nome.ilike(f"%{nome}%"))
    totalQuery = query.count()
    if limit > 0:
        totalPage = math.ceil(totalQuery/limit)
    else:
        totalPage = 0

    pular = (page - 1) * limit
    dados = query.offset(pular).limit(limit).all()
    return {
        "data": dados,
        "total": totalQuery,
        "page": page,
        "limit": limit,
        "pages": totalPage,
    }

def getCategoria(db: Session, categoria_id: int):
    return db.query(Categoria).filter(categoria_id == Categoria.id).first()

def createCategoria(db: Session, dados: CategoriaCreate):
    categoria = Categoria(**dados.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

def updateCategoria(db: Session, categoria_id: int,dados: CategoriaUpdate):
    categoria = getCategoria(db, categoria_id)
    if not categoria:
        return None
    update = dados.model_dump(exclude_unset=True)
    for campo, valor in update.items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria

def replaceCategoria(db: Session, categoria_id: int, dados: CategoriaCreate):
    categoria = getCategoria(db, categoria_id)
    if not categoria:
        return None
    replace = dados.model_dump()
    for campo, valor in replace.items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria

def deleteCategoria(db: Session, categoria_id: int):
    categoria = getCategoria(db, categoria_id)
    if not categoria:
        return None
    db.delete(categoria)
    db.commit()