import streamlit as st
import requests
import pandas as pd
import time

BASE_URL = "http://127.0.0.1:8000"

def renderizarTela(acao):
    if acao == "Listar":
        st.header("Lista de Medicamentos")
        try:
            response = requests.get(f"{BASE_URL}/medicamento")
            if response.status_code == 200:
                medicamentos = response.json()
                if medicamentos:
                    tabela = pd.DataFrame(medicamentos)
                    estilo = tabela.style.set_table_styles([{'selector': 'th', 'props': [('background-color', '#ffffff !important')]}])
                    st.dataframe(estilo, use_container_width=True, hide_index=True)
                    st.divider()
                    st.subheader("Excluir Medicamento")
                    id_delete = st.number_input("ID do medicamento para excluir", min_value=1, step=1)
                    if st.button("Excluir Medicamento"):
                        delete = requests.delete(f"{BASE_URL}/medicamento/{id_delete}")
                        if delete.status_code == 204:
                            st.success("Medicamento excluído com sucesso!")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error("Erro ao excluir. Verifique se o ID existe.")
                else:
                    st.info("Nenhum medicamento cadastrado.")
            else:
                st.error("Erro ao carregar medicamentos.")
        except Exception as e:
            st.error(f"Erro de conexão com a API: {e}")

    elif acao == "Criar":
        st.header("Novo Medicamento")
        with st.form("form_criar_med", clear_on_submit=True):
            nome = st.text_input("Nome")
            preco = st.number_input("Preço", min_value=0.0, step=0.1)
            unidade = st.selectbox("Unidade", ["mg", "ml", "g"])
            categoriaId = st.number_input("ID da Categoria", min_value=1, step=1)
            quantidade = st.number_input("Quantidade", min_value=0, step=1)

            if st.form_submit_button("Salvar"):
                medicamento = {
                    "nome": nome,
                    "preco": float(preco),
                    "quantidade": int(quantidade),
                    "unidade": unidade,
                    "categoria_id": int(categoriaId)
                }
                try:
                    response = requests.post(f"{BASE_URL}/medicamento", json=medicamento)
                    if response.status_code == 201:
                        st.success("Medicamento criado com sucesso!")
                    else:
                        st.error(f"Erro ao criar: {response.text}")
                except:
                    st.error("A API não está rodando.")

    elif acao == "Editar":
        st.header("Editar Medicamento")
        id_editar = st.number_input("Digite o ID do Medicamento", min_value=1, step=1)

        if st.button("Buscar Medicamento"):
            response = requests.get(f"{BASE_URL}/medicamento/{id_editar}")
            if response.status_code == 200:
                st.session_state["medicamento"] = response.json()
            else:
                st.error("Medicamento não encontrado.")

        if "medicamento" in st.session_state:
            med = st.session_state["medicamento"]
            with st.form("form_editar_med"):
                nome = st.text_input("Nome", value=med["nome"])
                preco = st.number_input("Preço", value=float(med["preco"]), step=0.1)

                opcoes_unidade = ["mg", "ml", "g"]
                index_unidade = opcoes_unidade.index(med["unidade"]) if med["unidade"] in opcoes_unidade else 0
                unidade = st.selectbox("Unidade", opcoes_unidade, index=index_unidade)

                categoriaId = st.number_input("ID da Categoria", value=int(med["categoria_id"]), step=1)
                quantidade = st.number_input("Quantidade", value=int(med["quantidade"]), step=1)

                if st.form_submit_button("Atualizar Medicamento"):
                    dados = {
                        "nome": nome,
                        "preco": float(preco),
                        "quantidade": int(quantidade),
                        "unidade": unidade,
                        "categoria_id": int(categoriaId)
                    }
                    response = requests.put(f"{BASE_URL}/medicamento/{id_editar}", json=dados)
                    if response.status_code == 200:
                        st.success("Medicamento atualizado com sucesso!")
                        del st.session_state["medicamento"]
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("Erro ao atualizar.")