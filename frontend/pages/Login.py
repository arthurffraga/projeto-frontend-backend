import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from utils.auth import API_URL

st.title("Farmacia")
st.subheader("Acesse sua conta")

if st.session_state.pop("cadastro_sucesso", False):
    st.toast("Conta criada com sucesso! Faca login.")

email = st.text_input("Email")
senha = st.text_input("Senha", type="password")

if st.button("Entrar", use_container_width=True):
    if not email or not senha:
        st.toast("Preencha email e senha.")
    else:
        try:
            resposta = requests.post(
                f"{API_URL}/login",
                data={"username": email, "password": senha}
            )
            if resposta.status_code == 200:
                dados = resposta.json()
                st.session_state["token"] = dados["access_token"]
                st.session_state["email"] = email
                st.rerun()
            else:
                st.toast("Email ou senha invalidos.")
        except requests.exceptions.ConnectionError:
            st.toast("Nao foi possivel conectar ao servidor.")

st.markdown("---")
st.page_link("pages/Cadastro_Usuario.py", label="Nao tem conta? Cadastre-se")