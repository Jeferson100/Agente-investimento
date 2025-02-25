import streamlit as st
import sys
import os
import requests
import pandas as pd
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from juncao_modelos_dados import ModeloFundamentos
from utils import PegandoLogotipo
from chat_bots import ChatTradutor
import yfinance as yf

st.set_page_config(
    page_title="Analise Ações",
    page_icon="https://s3-symbol-logo.tradingview.com/b3-on-nm--big.svg",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Analise Ações",
    },
)

def configurar_mensagem(response):
    text = ''.join(response)  
    lines = text.split('\n</think>\n\n')[1]
    return lines

if "chat_history_fundamentalista" not in st.session_state:
    st.session_state.chat_history_fundamentalista = []
    
if "codigos" not in st.session_state:
    url = "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/codigos_rodando/codigos_ibovespa.txt"
    codigos = requests.get(url)
    st.session_state.codigos =  sorted(set(filter(None, codigos.text.split('\r\n'))))

codigos = st.session_state.codigos
messages = st.session_state.chat_history_fundamentalista

st.title("Modelo de LLM para Análise Fundamentalista")

for message in messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


ticker = st.chat_input('Digite o código de negociação da ação (ex: BBDC4):')
with st.sidebar:
    if not ticker:
        st.image("https://s3-symbol-logo.tradingview.com/b3-on-nm--big.svg", width=300,)
    else:
        pegar_logotipo = PegandoLogotipo(ticker=ticker)
        logo_url = pegar_logotipo.pegar_logotipo()
        if logo_url:
            st.image(logo_url, width=300,)
        else:
            st.image("https://s3-symbol-logo.tradingview.com/b3-on-nm--big.svg", width=300,)
        
        try:
            acao = yf.Ticker(f'{ticker}.SA')
            info = acao.info
            reposta_tradutor = ChatTradutor(info['longBusinessSummary'])
            st.write(reposta_tradutor)
        except:
            pass
            
    
            
    st.sidebar.markdown("---")
    
    if 'show_codes' not in st.session_state:
        st.session_state.show_codes = False
    
    # Botão para alternar a visibilidade dos códigos
    if st.sidebar.button("Códigos de Negociação"):
        st.session_state.show_codes = not st.session_state.show_codes
    
    if st.session_state.show_codes:
        st.sidebar.markdown(
            "<div style='max-height: 300px; overflow-y: auto;'>"
            + "\n".join(f"- {codigo}" for codigo in codigos)
            + "</div>",
            unsafe_allow_html=True
        )    

if ticker:
    messages.append({"role": "user", "content": ticker})
    fundamentos = ModeloFundamentos(query=f'O que voce pode me dizer sobre os fundamentos da acao {ticker}', ticker=ticker)
    response = fundamentos.chat_fundamentalistas()
    if response:
        messages.append({"role": "assistant", "content": configurar_mensagem(response)})
        with st.chat_message("assistant"):
            st.write_stream(response)