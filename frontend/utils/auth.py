import streamlit as st

API_URL = "https://projeto-frontend-backend-production.up.railway.app"

def verificar_login():
    if "token" not in st.session_state:
        st.rerun()

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}

def sidebar_usuario():
    with st.sidebar:
        st.markdown("---")
        st.caption(f"Usuario: {st.session_state.get('email', '')}")
        if st.button("Sair", use_container_width=True):
            del st.session_state["token"]
            del st.session_state["email"]
            st.rerun()