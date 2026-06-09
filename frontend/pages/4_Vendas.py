import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from utils.auth import verificar_login, sidebar_usuario, get_headers, API_URL

st.set_page_config(page_title="Vendas", page_icon="", layout="wide")
verificar_login()
sidebar_usuario()

st.title(" Vendas")

tab_historico, tab_nova = st.tabs(["Histórico", " Nova Venda"])

with tab_historico:
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
        st.error("Erro ao carregar vendas.")
        st.stop()

    dados = resp.json()

    if not dados["data"]:
        st.info("Nenhuma venda encontrada.")
    else:
        for venda in dados["data"]:
            data_fmt = venda["dataVenda"][:10] if venda["dataVenda"] else "—"
            with st.expander(
                f"Venda #{venda['id']}  ·  {data_fmt}  ·  "
                f"R$ {venda['total']:.2f}  ·  {venda['formaPagamento']}"
            ):
                for item in venda["itens"]:
                    st.write(
                        f"• **{item['medicamento']['nome']}** — "
                        f"{item['quantidade']} x R$ {item['precoUnitario']:.2f}"
                    )

    st.divider()
    col_ant, col_info, col_prox = st.columns([1, 2, 1])
    with col_ant:
        if st.button("Anterior", key="ant_v", disabled=st.session_state.pagina_venda <= 1, use_container_width=True):
            st.session_state.pagina_venda -= 1
            st.rerun()
    with col_info:
        st.markdown(
            f"<p style='text-align:center; margin-top:8px'>Página {dados['page']} de {dados['pages']} "
            f"&nbsp;·&nbsp; {dados['total']} venda(s)</p>",
            unsafe_allow_html=True,
        )
    with col_prox:
        if st.button("Próximo", key="prox_v", disabled=st.session_state.pagina_venda >= dados["pages"], use_container_width=True):
            st.session_state.pagina_venda += 1
            st.rerun()

with tab_nova:
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    resp_meds = requests.get(f"{API_URL}/medicamento", params={"limit": 100})
    if resp_meds.status_code != 200:
        st.error("Erro ao carregar medicamentos.")
        st.stop()

    meds = resp_meds.json()["data"]
    if not meds:
        st.warning("Nenhum medicamento cadastrado.")
        st.stop()

    opcoes_med = {f"{m['nome']} — R$ {m['preco']:.2f} ({m['unidade']})": m for m in meds}

    st.subheader("Adicionar item")
    col_med, col_qtd, col_add = st.columns([4, 1, 1])

    with col_med:
        med_selecionado_key = st.selectbox("Medicamento", options=list(opcoes_med.keys()))
    with col_qtd:
        qtd = st.number_input("Qtd", min_value=1, step=1, value=1)
    with col_add:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("+ Adicionar", use_container_width=True):
            med_obj = opcoes_med[med_selecionado_key]
            existente = next((i for i in st.session_state.carrinho if i["id"] == med_obj["id"]), None)
            if existente:
                existente["quantidade"] += qtd
            else:
                st.session_state.carrinho.append({
                    "id": med_obj["id"],
                    "nome": med_obj["nome"],
                    "preco": med_obj["preco"],
                    "quantidade": qtd,
                })
            st.rerun()

    st.subheader("Carrinho")

    if not st.session_state.carrinho:
        st.info("Nenhum item adicionado.")
    else:
        total = 0.0
        for i, item in enumerate(st.session_state.carrinho):
            subtotal = item["preco"] * item["quantidade"]
            total += subtotal
            col_nome, col_qtd2, col_sub, col_rem = st.columns([4, 1, 2, 1])
            col_nome.write(item["nome"])
            col_qtd2.write(f"x{item['quantidade']}")
            col_sub.write(f"R$ {subtotal:.2f}")
            with col_rem:
                if st.button("✖", key=f"rem_{i}", help="Remover"):
                    st.session_state.carrinho.pop(i)
                    st.rerun()

        st.markdown(f"**Total: R$ {total:.2f}**")
        st.divider()

        FORMAS = ["Pix", "Crédito", "débito", "Dinheiro"]
        forma = st.selectbox("Forma de pagamento", options=FORMAS)

        col_finalizar, col_limpar = st.columns(2)

        with col_finalizar:
            if st.button("Finalizar Venda", use_container_width=True):
                payload = {
                    "formaPagamento": forma,
                    "itens": [
                        {"medicamento_id": item["id"], "quantidade": item["quantidade"]}
                        for item in st.session_state.carrinho
                    ],
                }
                resp_venda = requests.post(
                    f"{API_URL}/venda",
                    json=payload,
                    headers=get_headers()
                )
                if resp_venda.status_code == 201:
                    st.success(f"Venda finalizada! Total: R$ {resp_venda.json()['total']:.2f}")
                    st.session_state.carrinho = []
                    st.rerun()
                elif resp_venda.status_code == 401:
                    st.error("Sessão expirada. Faça login novamente.")
                    st.switch_page("main.py")
                else:
                    st.error(f"Erro ao finalizar venda: {resp_venda.text}")

        with col_limpar:
            if st.button("Limpar carrinho", use_container_width=True):
                st.session_state.carrinho = []
                st.rerun()