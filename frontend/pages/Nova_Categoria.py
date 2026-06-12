import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from utils.auth import verificar_login, sidebar_usuario, get_headers, API_URL

st.set_page_config(page_title="Nova Categoria", layout="centered")
verificar_login()
sidebar_usuario()

st.title("Nova Categoria")

nome = st.text_input("Nome da categoria")

if st.button("Salvar", use_container_width=True):
    if not nome.strip():
        st.toast("Informe um nome.", icon="⚠️")
    else:
        resp = requests.post(
            f"{API_URL}/categoria",
            json={"nome": nome},
            headers=get_headers()
        )
        if resp.status_code in (200, 201):
            st.session_state["toast_msg"] = "Categoria criada com sucesso!"
            st.session_state["toast_icon"] = "✅"
            st.switch_page("pages/Categorias.py")
        elif resp.status_code == 401:
            st.toast("Sessao expirada.", icon="⚠️")
            st.rerun()
        else:
            st.toast("Erro ao criar categoria.", icon="❌")