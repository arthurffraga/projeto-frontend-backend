from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
from database import Base, engine, get_db
from schemas import MedicamentoCreate, MedicamentoResponse, MedicamentoUpdate, CategoriaCreate, CategoriaResponse, CategoriaUpdate

Base.metadata.create_all(bind=engine)
app = FastAPI(title= "API da Farmacia")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/categoria", response_model=list[CategoriaResponse])
def readCategoria(db: Session = Depends(get_db)):
    return crud.readCategoria(db)

@app.get("/categoria/{categoria_id}", response_model=CategoriaResponse)
def getCategoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.getCategoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@app.get("/medicamento", response_model=list[MedicamentoResponse])
def readMedicamento(db: Session = Depends(get_db)):
    return crud.readMedicamento(db)

@app.get("/medicamento/{medicamento_id}", response_model=MedicamentoResponse)
def getMedicamento(medicamento_id: int, db: Session = Depends(get_db)):
    medicamento = crud.getMedicamento(db, medicamento_id)
    return medicamento

@app.post("/categoria",response_model=CategoriaResponse, status_code=201)
def postCategoria(dados: CategoriaCreate, db: Session = Depends(get_db)):
    return crud.createCategoria(db, dados)

@app.post("/medicamento", response_model=MedicamentoResponse, status_code=201)
def postMedicamento(dados: MedicamentoCreate, db: Session = Depends(get_db)):
    return crud.createMedicamento(db, dados)

@app.put("/categoria/{categoria_id}", response_model=CategoriaResponse)
def putCategoria(categoria_id: int, dados: CategoriaCreate, db: Session = Depends(get_db)):
    categoria = crud.replaceCategoria(db, categoria_id, dados)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@app.put("/medicamento/{medicamento_id}", response_model=MedicamentoResponse)
def putMedicamento(medicamento_id: int, dados: MedicamentoCreate, db: Session = Depends(get_db)):
    medicamento = crud.replaceMedicamento(db, medicamento_id, dados)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrada")
    return medicamento

@app.patch("/categoria/{categoria_id}", response_model= CategoriaResponse)
def patchCategoria(categoria_id: int, dados: CategoriaUpdate, db: Session = Depends(get_db)):
    categoria = crud.updateCategoria(db, categoria_id, dados)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@app.patch("/medicamento/{medicamento_id}", response_model= MedicamentoResponse)
def patchMedicamento(medicamento_id: int, dados: MedicamentoUpdate, db: Session = Depends(get_db)):
    medicamento = crud.updateMedicamento(db, medicamento_id, dados)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrada")
    return medicamento

@app.delete("/categoria/{categoria_id}", status_code=204)
def deleteCategoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.getCategoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    crud.deleteCategoria(db, categoria_id)

@app.delete("/medicamento/{medicamento_id}", status_code=204)
def deleteMedicamento(medicamento_id: int, db: Session = Depends(get_db)):
    medicamento = crud.getMedicamento(db, medicamento_id)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrada")
    crud.deleteMedicamento(db, medicamento_id)