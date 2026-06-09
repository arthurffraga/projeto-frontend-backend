import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import requests
from utils.auth import verificar_login, sidebar_usuario, get_headers, API_URL

st.set_page_config(page_title="Cadastro de Medicamento", layout="centered")
verificar_login()
sidebar_usuario()

editando_id = st.session_state.pop("editar_med_id", None)
modo_edicao = editando_id is not None

st.title("Editar Medicamento" if modo_edicao else "Novo Medicamento")

resp_cat = requests.get(f"{API_URL}/categoria", params={"limit": 100})
if resp_cat.status_code != 200:
    st.error("Erro ao carregar categorias.")
    st.stop()

categorias = resp_cat.json()["data"]
if not categorias:
    st.warning("Nenhuma categoria cadastrada. Cadastre uma categoria primeiro.")
    if st.button("Ir para Categorias"):
        st.switch_page("pages/3_Categorias.py")
    st.stop()

opcoes_cat = {c["nome"]: c["id"] for c in categorias}

med_atual = {}
if modo_edicao:
    resp_med = requests.get(f"{API_URL}/medicamento/{editando_id}")
    if resp_med.status_code == 200:
        med_atual = resp_med.json()
    else:
        st.error("Medicamento nao encontrado.")
        st.stop()

UNIDADES = ["mg", "ml", "g"]

nome = st.text_input("Nome do medicamento", value=med_atual.get("nome", ""))
preco = st.number_input("Preco (R$)", min_value=0.0, step=0.01, format="%.2f",
                        value=float(med_atual.get("preco", 0.0)))
quantidade = st.number_input("Quantidade em estoque", min_value=0, step=1,
                              value=int(med_atual.get("quantidade", 0)))

unidade_atual = med_atual.get("unidade", "mg")
unidade = st.selectbox("Unidade", options=UNIDADES,
                       index=UNIDADES.index(unidade_atual) if unidade_atual in UNIDADES else 0)

cat_atual_nome = med_atual.get("categoria", {}).get("nome", list(opcoes_cat.keys())[0])
idx_cat = list(opcoes_cat.keys()).index(cat_atual_nome) if cat_atual_nome in opcoes_cat else 0
categoria = st.selectbox("Categoria", options=list(opcoes_cat.keys()), index=idx_cat)

col1, col2 = st.columns(2)

with col1:
    if st.button("Salvar", use_container_width=True):
        if not nome.strip():
            st.warning("Informe o nome do medicamento.")
        elif quantidade <= 0:
            st.warning("A quantidade em estoque deve ser maior que zero.")
        else:
            payload = {
                "nome": nome,
                "preco": preco,
                "quantidade": quantidade,
                "unidade": unidade,
                "categoria_id": opcoes_cat[categoria],
            }

            if modo_edicao:
                resp = requests.put(
                    f"{API_URL}/medicamento/{editando_id}",
                    json=payload,
                    headers=get_headers()
                )
            else:
                resp = requests.post(
                    f"{API_URL}/medicamento",
                    json=payload,
                    headers=get_headers()
                )

            if resp.status_code in (200, 201):
                st.success("Medicamento salvo com sucesso!")
                st.switch_page("pages/1_Medicamentos.py")
            elif resp.status_code == 404:
                st.error("Categoria nao encontrada.")
            elif resp.status_code == 401:
                st.error("Sessao expirada. Faca login novamente.")
                st.switch_page("main.py")
            else:
                st.error(f"Erro: {resp.text}")

with col2:
    if st.button("Voltar", use_container_width=True):
        st.switch_page("pages/1_Medicamentos.py")