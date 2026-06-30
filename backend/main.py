from fastapi import Depends, FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud
import auth
import servicoEmail
import os
from database import Base, engine, get_db
from schemas import MedicamentoCreate, MedicamentoResponse, MedicamentoUpdate, CategoriaCreate, CategoriaResponse, CategoriaUpdate, PaginatedMedicamento, PaginatedCategoria, PaginatedVenda, VendaResponse, VendaCreate, UsuarioCreate, UsuarioResponse, PaginatedUsuario
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
load_dotenv()
Base.metadata.create_all(bind=engine)
app = FastAPI(title= "API da Farmacia")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/categoria", response_model=PaginatedCategoria)
def readCategoria(nome: Optional[str] = None, page: int = Query(default=1, ge=1),limit: int = Query(default=5, ge=1), db: Session = Depends(get_db)):
    return crud.readCategoria(db, nome=nome, page=page, limit=limit)

@app.get("/categoria/{categoria_id}", response_model=CategoriaResponse)
def getCategoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.getCategoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@app.get("/medicamento", response_model=PaginatedMedicamento)
def readMedicamento(nome: Optional[str] = None, page: int = Query(default=1, ge=1),limit: int = Query(default=5, ge=1), db: Session = Depends(get_db)):
    return crud.readMedicamento(db, nome=nome, page=page, limit=limit)

@app.get("/medicamento/{medicamento_id}", response_model=MedicamentoResponse)
def getMedicamento(medicamento_id: int, db: Session = Depends(get_db)):
    medicamento = crud.getMedicamento(db, medicamento_id)
    return medicamento

@app.get("/venda", response_model= PaginatedVenda)
def readVendas(nomeRemedio: Optional[str] = None, page: int = Query(default=1, ge=1), limit: int = Query(default=5, ge=1), db: Session = Depends(get_db)):
    return crud.readVenda(db, nomeRemedio=nomeRemedio, page = page, limit=limit)

@app.get("/venda/{venda_id}", response_model=VendaResponse)
def getVenda(venda_id: int, db: Session = Depends(get_db)):
    venda = crud.getVenda(db, venda_id=venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@app.get("/usuario", response_model=PaginatedUsuario)
def getUsuarios(page: int = Query(default=1, ge=1), limit: int = Query(default=5, ge=1), db: Session = Depends(get_db), usuarioLogado: str = Depends(auth.verificarToken)):
    return crud.readUsuario(db, page=page, limit=limit)

@app.post("/venda", response_model=VendaResponse, status_code=201)
def postVenda(dados: VendaCreate, db: Session = Depends(get_db), usuarioLogado: str = Depends(auth.verificarToken)):
    venda = crud.createVenda(db, dados = dados)
    if not venda:
        raise HTTPException(status_code=404, detail="Não foi possivel concluir a venda")
    return venda
@app.post("/categoria",response_model=CategoriaResponse, status_code=201)
def postCategoria(dados: CategoriaCreate, db: Session = Depends(get_db), usuarioLogado: str = Depends(auth.verificarToken)):
    return crud.createCategoria(db, dados)

@app.post("/medicamento", response_model=MedicamentoResponse, status_code=201)
def postMedicamento(dados: MedicamentoCreate, db: Session = Depends(get_db), usuarioLogado: str = Depends(auth.verificarToken)):
    medicamento = crud.createMedicamento(db, dados)
    if not medicamento:
        raise HTTPException(status_code=404, detail="Categoria não encontrada. Impossível criar o medicamento.")
    return medicamento
@app.post("/usuario", response_model=UsuarioResponse, status_code=201)
def postUsuario(dados: UsuarioCreate, tarefasFundo: BackgroundTasks ,db: Session = Depends(get_db),):
    usuario = crud.createUsuario(db, dados = dados)
    if usuario == "email_duplicado":
        raise HTTPException(status_code=409, detail="Este email ja esta em uso.")
    if not usuario:
        raise HTTPException(status_code=400, detail="Este nome de utilizador já está registado.")
    
    tarefasFundo.add_task(servicoEmail.enviarEmailBoasVindas, usuario.email, usuario.username)

    return usuario

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud.getUsuario(db, username=form_data.username)
    if not usuario or not auth.verificarSenha(form_data.password, usuario.senha):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos", headers={"WWW-Authenticate": "Bearer"})
    
    token_acesso = auth.criarTokenAcesso(dados={"sub": usuario.username})
    
    return {
        "access_token": token_acesso, 
        "token_type": "bearer"
    }
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