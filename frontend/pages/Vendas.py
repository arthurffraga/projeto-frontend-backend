import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from utils.auth import verificar_login, sidebar_usuario, API_URL

st.set_page_config(page_title="Historico de Vendas", layout="wide")
verificar_login()
sidebar_usuario()

if "toast_msg" in st.session_state:
    st.toast(st.session_state.pop("toast_msg"), icon=st.session_state.pop("toast_icon", "✅"))

st.title("Historico de Vendas")

busca = st.text_input("Buscar por nome do medicamento", placeholder="Ex: Dipirona")

if "busca_venda" not in st.session_state:
    st.session_state.busca_venda = ""
if busca != st.session_state.busca_venda:
    st.session_state.pagina_venda = 1
    st.session_state.busca_venda = busca

if "pagina_venda" not in st.session_state:
    st.session_state.pagina_venda = 1

LIMITE = 5

resp = requests.get(
    f"{API_URL}/venda",
    params={"nomeRemedio": busca, "page": st.session_state.pagina_venda, "limit": LIMITE},
)

if resp.status_code != 200:
    st.toast("Erro ao carregar vendas.", icon="❌")
    st.stop()

dados = resp.json()

if not dados["data"]:
    st.info("Nenhuma venda encontrada.")
else:
    for venda in dados["data"]:
        data_fmt = venda["dataVenda"][:10] if venda["dataVenda"] else "-"
        with st.expander(
            f"Venda #{venda['id']}  |  {data_fmt}  |  "
            f"R$ {venda['total']:.2f}  |  {venda['formaPagamento']}"
        ):
            for item in venda["itens"]:
                st.write(
                    f"{item['medicamento']['nome']} - "
                    f"{item['quantidade']} x R$ {item['precoUnitario']:.2f}"
                )

st.divider()
col_ant, col_info, col_prox = st.columns([1, 2, 1])

with col_ant:
    if st.button("Anterior", disabled=st.session_state.pagina_venda <= 1, use_container_width=True):
        st.session_state.pagina_venda -= 1
        st.rerun()

with col_info:
    st.markdown(
        f"<p style='text-align:center; margin-top:8px'>Pagina {dados['page']} de {dados['pages']} "
        f"&nbsp;·&nbsp; {dados['total']} venda(s)</p>",
        unsafe_allow_html=True,
    )

with col_prox:
    if st.button("Proximo", disabled=st.session_state.pagina_venda >= dados["pages"], use_container_width=True):
        st.session_state.pagina_venda += 1
        st.rerun()