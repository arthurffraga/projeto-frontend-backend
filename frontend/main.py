import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Farmácia — Login", page_icon="", layout="centered")

if "token" in st.session_state:
    st.switch_page("pages/1_Medicamentos.py")

st.title("Farmácia")
st.subheader("Acesse sua conta")

nome = st.text_input("Nome")
senha = st.text_input("Senha", type="password")

if st.button("Entrar", use_container_width=True):
    if not nome or not senha:
        st.warning("Preencha nome e senha.")
    else:
        try:
            resposta = requests.post(
                f"{API_URL}/login",
                data={"username": nome, "password": senha}
            )
            if resposta.status_code == 200:
                dados = resposta.json()
                st.session_state["token"] = dados["access_token"]
                st.session_state["email"] = nome
                st.switch_page("pages/1_Medicamentos.py")
            else:
                st.error("Nome ou senha inválidos.")
        except requests.exceptions.ConnectionError:
            st.error("Não foi possível conectar ao servidor. Verifique se o backend está rodando.")