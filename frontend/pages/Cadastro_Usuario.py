import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from utils.auth import API_URL

if "token" in st.session_state:
    st.switch_page("pages/Login.py")

st.title("Criar conta")

username = st.text_input("Nome")
email = st.text_input("Email")
senha = st.text_input("Senha", type="password")
confirmar_senha = st.text_input("Confirmar senha", type="password")

col1, col2 = st.columns(2)

with col1:
    if st.button("Cadastrar", use_container_width=True):
        if not username.strip() or not email.strip() or not senha or not confirmar_senha:
            st.toast("Preencha todos os campos.")
        elif senha != confirmar_senha:
            st.toast("As senhas nao coincidem.")
        else:
            try:
                resp = requests.post(
                    f"{API_URL}/usuario",
                    json={"username": username, "email": email, "senha": senha}
                )
                if resp.status_code in (200, 201):
                    st.session_state["cadastro_sucesso"] = True
                    st.switch_page("pages/Login.py")
                elif resp.status_code == 409:
                    st.toast("Este email ja esta em uso.")
                else:
                    st.toast(f"Erro ao cadastrar: {resp.text}")
            except requests.exceptions.ConnectionError:
                st.toast("Nao foi possivel conectar ao servidor.")

with col2:
    if st.button("Voltar para login", use_container_width=True):
        st.switch_page("pages/Login.py")