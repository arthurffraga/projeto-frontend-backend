import streamlit as st

API_URL = "http://localhost:8000"

def verificar_login():
    if "token" not in st.session_state:
        st.switch_page("main.py")

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def sidebar_usuario():    
    with st.sidebar:
        st.markdown("---")
        st.caption(f" {st.session_state.get('nome', '')}")
        if st.button("Sair", use_container_width=True):
            del st.session_state["token"]
            del st.session_state["nome"]
            st.switch_page("main.py")