import streamlit as st
import requests
import pandas as pd
import time

BASE_URL = "http://127.0.0.1:8000"

def renderizarTela(acao):
    if acao == "Listar":
        st.header("Lista de Categorias")
        try:
            response = requests.get(f"{BASE_URL}/categoria")
            if response.status_code == 200:
                categorias = response.json()
                if categorias:
                    tabela = pd.DataFrame(categorias)
                    estilo = tabela.style.set_table_styles([{'selector': 'th', 'props': [('background-color', '#ffffff !important')]}])
                    st.dataframe(estilo, use_container_width=True, hide_index=True)

                    st.divider()
                    st.subheader("Excluir Categoria")
                    id_delete = st.number_input("ID da categoria para excluir", min_value=1, step=1)
                    if st.button("Excluir Categoria"):
                        delete = requests.delete(f"{BASE_URL}/categoria/{id_delete}")
                        if delete.status_code == 204:
                            st.success("Categoria excluída com sucesso!")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error("Erro ao excluir. Verifique se o ID existe.")
                else:
                    st.info("Nenhuma categoria cadastrada.")
            else:
                st.error("Erro ao carregar categorias.")
        except:
            st.error("API não está rodando")

    elif acao == "Criar":
        st.header("Nova Categoria")
        with st.form("form_criar_cat", clear_on_submit=True):
            nome = st.text_input("Nome da Categoria")

            if st.form_submit_button("Salvar Categoria"):
                categoria = {"nome": nome}
                try:
                    response = requests.post(f"{BASE_URL}/categoria", json=categoria)
                    if response.status_code == 201:
                        st.success("Categoria criada com sucesso!")
                    else:
                        st.error("Erro ao criar categoria.")
                except:
                    st.error("API não está rodando.")

    elif acao == "Editar":
        st.header("Editar Categoria")
        id_editar = st.number_input("Digite o ID da Categoria", min_value=1, step=1)

        if st.button("Buscar Categoria"):
            response = requests.get(f"{BASE_URL}/categoria/{id_editar}")
            if response.status_code == 200:
                st.session_state["categoria"] = response.json()
            else:
                st.error("Categoria não encontrada.")

        if "categoria" in st.session_state:
            cat = st.session_state["categoria"]
            with st.form("form_editar_cat"):
                nome = st.text_input("Nome", value=cat["nome"])

                if st.form_submit_button("Atualizar Categoria"):
                    dados = {"nome": nome}
                    response = requests.put(f"{BASE_URL}/categoria/{id_editar}", json=dados)
                    if response.status_code == 200:
                        st.success("Categoria atualizada com sucesso!")
                        del st.session_state["categoria"]
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("Erro ao atualizar categoria.")