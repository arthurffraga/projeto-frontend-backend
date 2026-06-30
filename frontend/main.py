import streamlit as st

if "token" not in st.session_state:
    pg = st.navigation([
        st.Page("pages/Login.py", title="Login", url_path="login"),
        st.Page("pages/Cadastro_Usuario.py", title="Cadastro", url_path="cadastro"),
    ])
else:
    pg = st.navigation({
        "Medicamentos": [
            st.Page("pages/Medicamentos.py", title="Listar"),
            st.Page("pages/Cadastro_Medicamento.py", title="Novo Medicamento"),
        ],
        "Categorias": [
            st.Page("pages/Categorias.py", title="Listar"),
            st.Page("pages/Nova_Categoria.py", title="Nova Categoria"),
        ],
        "Vendas": [
            st.Page("pages/Vendas.py", title="Historico"),
            st.Page("pages/Nova_Venda.py", title="Nova Venda"),
        ],
    })

pg.run()