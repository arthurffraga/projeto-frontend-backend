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
streamlit run app.py