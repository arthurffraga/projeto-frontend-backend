import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from utils.auth import verificar_login, sidebar_usuario, get_headers, API_URL

st.set_page_config(page_title="Categorias", layout="centered")
verificar_login()
sidebar_usuario()

st.title("Categorias")

if "confirmar_del_cat" not in st.session_state:
    st.session_state.confirmar_del_cat = None

busca = st.text_input("Buscar categoria", placeholder="Ex: Analgesico")

if "busca_cat" not in st.session_state:
    st.session_state.busca_cat = ""
if busca != st.session_state.busca_cat:
    st.session_state.pagina_cat = 1
    st.session_state.busca_cat = busca

if "pagina_cat" not in st.session_state:
    st.session_state.pagina_cat = 1

LIMITE = 5

resp = requests.get(
    f"{API_URL}/categoria",
    params={"nome": busca, "page": st.session_state.pagina_cat, "limit": LIMITE},
)

if resp.status_code != 200:
    st.error("Erro ao carregar categorias.")
    st.stop()

dados = resp.json()

if not dados["data"]:
    st.info("Nenhuma categoria encontrada.")
else:
    for cat in dados["data"]:
        col1, col2, col3 = st.columns([5, 1, 1])
        col1.write(cat["nome"])

        with col2:
            if st.button("Editar", key=f"ecat_{cat['id']}", use_container_width=True):
                st.session_state["editar_cat"] = cat
                st.session_state.confirmar_del_cat = None
                st.rerun()

        with col3:
            if st.button("Excluir", key=f"dcat_{cat['id']}", use_container_width=True):
                st.session_state.confirmar_del_cat = {"id": cat["id"], "nome": cat["nome"]}
                st.rerun()

        if st.session_state.confirmar_del_cat and st.session_state.confirmar_del_cat["id"] == cat["id"]:
            st.warning(f"Tem certeza que deseja excluir **{cat['nome']}**?")
            col_sim, col_nao = st.columns(2)
            with col_sim:
                if st.button("Sim, excluir", key=f"sim_cat_{cat['id']}", use_container_width=True):
                    del_resp = requests.delete(
                        f"{API_URL}/categoria/{cat['id']}",
                        headers=get_headers()
                    )
                    st.session_state.confirmar_del_cat = None
                    if del_resp.status_code == 204:
                        st.success("Categoria excluida.")
                    else:
                        st.error("Erro ao excluir. Pode haver medicamentos vinculados.")
                    st.rerun()
            with col_nao:
                if st.button("Cancelar", key=f"nao_cat_{cat['id']}", use_container_width=True):
                    st.session_state.confirmar_del_cat = None
                    st.rerun()

st.divider()
col_ant, col_info, col_prox = st.columns([1, 2, 1])

with col_ant:
    if st.button("Anterior", disabled=st.session_state.pagina_cat <= 1, use_container_width=True):
        st.session_state.pagina_cat -= 1
        st.rerun()

with col_info:
    st.markdown(
        f"<p style='text-align:center; margin-top:8px'>Pagina {dados['page']} de {dados['pages']} "
        f"&nbsp;·&nbsp; {dados['total']} resultado(s)</p>",
        unsafe_allow_html=True,
    )

with col_prox:
    if st.button("Proximo", disabled=st.session_state.pagina_cat >= dados["pages"], use_container_width=True):
        st.session_state.pagina_cat += 1
        st.rerun()

st.divider()
cat_editando = st.session_state.get("editar_cat", None)
st.subheader("Editar categoria" if cat_editando else "Nova categoria")

nome_input = st.text_input(
    "Nome da categoria",
    value=cat_editando["nome"] if cat_editando else "",
    key="input_cat_nome"
)

col_salvar, col_cancelar = st.columns(2)

with col_salvar:
    if st.button("Salvar", use_container_width=True):
        if not nome_input.strip():
            st.warning("Informe um nome.")
        else:
            if cat_editando:
                resp_save = requests.put(
                    f"{API_URL}/categoria/{cat_editando['id']}",
                    json={"nome": nome_input},
                    headers=get_headers()
                )
            else:
                resp_save = requests.post(
                    f"{API_URL}/categoria",
                    json={"nome": nome_input},
                    headers=get_headers()
                )

            if resp_save.status_code in (200, 201):
                st.success("Categoria salva!")
                st.session_state.pop("editar_cat", None)
                st.rerun()
            elif resp_save.status_code == 401:
                st.error("Sessao expirada.")
                st.switch_page("main.py")
            else:
                st.error(f"Erro: {resp_save.text}")

with col_cancelar:
    if cat_editando:
        if st.button("Cancelar edicao", use_container_width=True):
            st.session_state.pop("editar_cat", None)
            st.rerun()