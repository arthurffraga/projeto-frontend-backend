import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from utils.auth import verificar_login, sidebar_usuario, get_headers, API_URL

st.set_page_config(page_title="Nova Venda", layout="wide")
verificar_login()
sidebar_usuario()

st.title("Nova Venda")

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

resp_meds = requests.get(f"{API_URL}/medicamento", params={"limit": 100})
if resp_meds.status_code != 200:
    st.toast("Erro ao carregar medicamentos.", icon="❌")
    st.stop()

meds = resp_meds.json()["data"]
if not meds:
    st.toast("Nenhum medicamento cadastrado.", icon="⚠️")
    st.stop()

opcoes_med = {f"{m['nome']} - R$ {m['preco']:.2f} ({m['unidade']})": m for m in meds}

st.subheader("Adicionar item")
col_med, col_qtd, col_add = st.columns([4, 1, 1])

with col_med:
    med_selecionado_key = st.selectbox("Medicamento", options=list(opcoes_med.keys()))
with col_qtd:
    qtd = st.number_input("Qtd", min_value=1, step=1, value=1)
with col_add:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Adicionar", use_container_width=True):
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
        st.toast(f"{med_obj['nome']} adicionado ao carrinho.", icon="✅")
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
            if st.button("Remover", key=f"rem_{i}", use_container_width=True):
                nome_removido = item["nome"]
                st.session_state.carrinho.pop(i)
                st.toast(f"{nome_removido} removido.", icon="⚠️")
                st.rerun()

    st.markdown(f"**Total: R$ {total:.2f}**")
    st.divider()

    FORMAS = ["Pix", "Credito", "Debito", "Dinheiro"]
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
                total_final = resp_venda.json()["total"]
                st.session_state.carrinho = []
                st.session_state["toast_msg"] = f"Venda finalizada! Total: R$ {total_final:.2f}"
                st.session_state["toast_icon"] = "✅"
                st.switch_page("pages/Vendas.py")
            elif resp_venda.status_code == 401:
                st.toast("Sessao expirada.", icon="⚠️")
                st.rerun()
            else:
                st.toast("Erro ao finalizar venda.", icon="❌")

    with col_limpar:
        if st.button("Limpar carrinho", use_container_width=True):
            st.session_state.carrinho = []
            st.toast("Carrinho limpo.", icon="⚠️")
            st.rerun()