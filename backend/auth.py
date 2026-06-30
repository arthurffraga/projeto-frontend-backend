from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
SECRET_KEY = "minha_chave_farmacia"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obterHashSenha(senha: str):
    return pwd_context.hash(senha)

def verificarSenha(senha_plana: str, senha_hash: str):
    return pwd_context.verify(senha_plana, senha_hash)


def criarTokenAcesso(dados: dict):
    dadosCopia = dados.copy()
    tempoExpiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    dadosCopia.update({"exp": tempoExpiracao})
    
    token_jwt = jwt.encode(dadosCopia, SECRET_KEY, algorithm=ALGORITHM)
    
    return token_jwt

def verificarToken(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")       
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
            
        return username
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="O tempo do seu token acabou. Faça login novamente.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token falso ou inválido.")