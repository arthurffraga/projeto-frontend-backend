import streamlit as st
import telaCategoria
import telaMedicamento

st.set_page_config(page_title="Farmácia", layout="wide")

st.markdown("""
    <style>
        .stAppDeployButton {display:none;}
        div[data-baseweb="input"] > div {background-color: #ffffff !important;}
        div[data-baseweb="select"] > div {background-color: #ffffff !important;}
    </style>
""", unsafe_allow_html=True)

st.title("Sistema da Farmácia")

if 'modulo_ativo' not in st.session_state:
    st.session_state['modulo_ativo'] = 'Medicamentos'
    st.session_state['acao_ativa'] = 'Listar'
    st.session_state['radio_med'] = 'Listar'
    st.session_state['radio_cat'] = None

def updateMedicamento():
    if st.session_state['radio_med'] is not None:
        st.session_state['modulo_ativo'] = 'Medicamentos'
        st.session_state['acao_ativa'] = st.session_state['radio_med']
        st.session_state['radio_cat'] = None 

def updateCategoria():
    if st.session_state['radio_cat'] is not None:
        st.session_state['modulo_ativo'] = 'Categorias'
        st.session_state['acao_ativa'] = st.session_state['radio_cat']
        st.session_state['radio_med'] = None 

with st.sidebar.expander("Medicamentos", expanded=(st.session_state['modulo_ativo'] == 'Medicamentos')):
    st.radio("Opções", ["Listar", "Criar", "Editar"], key="radio_med", on_change=updateMedicamento, label_visibility="collapsed")

with st.sidebar.expander("Categorias", expanded=(st.session_state['modulo_ativo'] == 'Categorias')):
    st.radio("Opções", ["Listar", "Criar", "Editar"], key="radio_cat", on_change=updateCategoria, label_visibility="collapsed")

modulo = st.session_state['modulo_ativo']
acao = st.session_state['acao_ativa']

if modulo == "Medicamentos":
    telaMedicamento.renderizarTela(acao)
elif modulo == "Categorias":
    telaCategoria.renderizarTela(acao)