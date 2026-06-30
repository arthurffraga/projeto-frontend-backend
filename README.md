##  Como Rodar o Projeto Localmente

### 1. Preparar o Ambiente Virtual (.venv)
Abra o seu terminal na pasta raiz do projeto e crie o ambiente virtual:

python -m venv .venv

No Windows:
.venv\Scripts\activate

No Linux/Mac:
source .venv/bin/activate

### 2. Instalar as Dependências

pip install -r requirements.txt

### 3. Executar o Back-end

cd backend
uvicorn main:app --reload

### 4. Executar o Front-end

.venv\Scripts\activate
cd frontend
streamlit run main.py  

## 5. Links de Produção

Aqui estão os endereços das aplicações rodando na nuvem:

- Frontend (Streamlit): https://projeto-frontend-backend-alilsdffqv3q7f66lhtlx4.streamlit.app
- Backend (API FastAPI): https://projeto-frontend-backend-production.up.railway.app
- Documentação da API (Swagger): https://projeto-frontend-backend-production.up.railway.app/docs
