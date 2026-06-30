import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from utils.auth import verificar_login, sidebar_usuario, get_headers, API_URL

st.set_page_config(page_title="Medicamentos", layout="wide")
verificar_login()
sidebar_usuario()

if "toast_msg" in st.session_state:
    st.toast(st.session_state.pop("toast_msg"), icon=st.session_state.pop("toast_icon", None))

if "confirmar_del_med" not in st.session_state:
    st.session_state.confirmar_del_med = None

@st.dialog("Confirmar exclusao")
def dialog_excluir_med(med):
    st.write(f"Tem certeza que deseja excluir **{med['nome']}**?")
    st.write("Esta acao nao pode ser desfeita.")
    col_sim, col_nao = st.columns(2)
    with col_sim:
        if st.button("Sim, excluir", use_container_width=True):
            del_resp = requests.delete(
                f"{API_URL}/medicamento/{med['id']}",
                headers=get_headers()
            )
            st.session_state.confirmar_del_med = None
            if del_resp.status_code == 204:
                st.session_state["toast_msg"] = "Medicamento excluido com sucesso."
                st.session_state["toast_icon"] = None
            else:
                st.session_state["toast_msg"] = "Erro ao excluir medicamento."
                st.session_state["toast_icon"] = None
            st.rerun()
    with col_nao:
        if st.button("Cancelar", use_container_width=True):
            st.session_state.confirmar_del_med = None
            st.rerun()

st.title("Medicamentos")

busca = st.text_input("Buscar por nome", placeholder="Ex: Dipirona")

if "busca_med" not in st.session_state:
    st.session_state.busca_med = ""
if busca != st.session_state.busca_med:
    st.session_state.pagina_med = 1
    st.session_state.busca_med = busca

if "pagina_med" not in st.session_state:
    st.session_state.pagina_med = 1

LIMITE = 5

resp = requests.get(
    f"{API_URL}/medicamento",
    params={"nome": busca, "page": st.session_state.pagina_med, "limit": LIMITE},
)

if resp.status_code != 200:
    st.toast("Erro ao carregar medicamentos.")
    st.stop()

dados = resp.json()

if st.session_state.confirmar_del_med:
    dialog_excluir_med(st.session_state.confirmar_del_med)

if not dados["data"]:
    st.info("Nenhum medicamento encontrado.")
else:
    col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 1, 1, 2, 1, 1])
    col1.markdown("**Nome**")
    col2.markdown("**Categoria**")
    col3.markdown("**Preco**")
    col4.markdown("**Qtd**")
    col5.markdown("**Unidade**")
    col6.markdown("**Editar**")
    col7.markdown("**Excluir**")
    st.divider()

    for med in dados["data"]:
        col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 2, 1, 1, 2, 1, 1])
        col1.write(med["nome"])
        col2.write(med["categoria"]["nome"])
        col3.write(f"R$ {med['preco']:.2f}")
        col4.write(str(med["quantidade"]))
        col5.write(med["unidade"])
        with col6:
            if st.button("Editar", key=f"edit_{med['id']}", use_container_width=True):
                st.session_state["editar_med_id"] = med["id"]
                st.switch_page("pages/Cadastro_Medicamento.py")
        with col7:
            if st.button("Excluir", key=f"del_{med['id']}", use_container_width=True):
                st.session_state.confirmar_del_med = {"id": med["id"], "nome": med["nome"]}
                st.rerun()

st.divider()
col_ant, col_info, col_prox = st.columns([1, 2, 1])

with col_ant:
    if st.button("Anterior", disabled=st.session_state.pagina_med <= 1, use_container_width=True):
        st.session_state.pagina_med -= 1
        st.rerun()

with col_info:
    st.markdown(
        f"<p style='text-align:center; margin-top:8px'>Pagina {dados['page']} de {dados['pages']} "
        f"&nbsp;·&nbsp; {dados['total']} resultado(s)</p>",
        unsafe_allow_html=True,
    )

with col_prox:
    if st.button("Proximo", disabled=st.session_state.pagina_med >= dados["pages"], use_container_width=True):
        st.session_state.pagina_med += 1
        st.rerun()