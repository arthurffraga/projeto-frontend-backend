from sqlalchemy.orm import Session
from models import Medicamento, Categoria
from schemas import MedicamentoCreate, MedicamentoUpdate, CategoriaCreate, CategoriaUpdate

def readMedicamento(db: Session):
    return db.query(Medicamento).all()

def getMedicamento(db: Session, medicamento_id: int):
    return db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()

def createMedicamento(db: Session, dados: MedicamentoCreate):
    medicamento = Medicamento(**dados.model_dump())
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
def readCategoria(db: Session):
    return db.query(Categoria).all()

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