import streamlit as st
import sys
import os
import requests
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from juncao_modelos_dados import ModeloValuation
from utils import PegandoLogotipo, generator_to_string, string_to_generator, configurar_mensagem
from chat_bots import ChatTradutor
import yfinance as yf
from typing import Generator

st.set_page_config(
    page_title="Analise Ações",
    page_icon="https://s3-symbol-logo.tradingview.com/b3-on-nm--big.svg",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Analise Ações",
    },
)

if "chat_history_valuation" not in st.session_state:
    st.session_state.chat_history_valuation = []
    
if "codigos" not in st.session_state:
    url = "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/codigos_rodando/codigos_ibovespa.txt"
    codigos = requests.get(url)
    st.session_state.codigos =  sorted(set(filter(None, codigos.text.split('\r\n'))))


codigos = st.session_state.codigos
messages = st.session_state.chat_history_valuation


st.title("Modelo de LLM para Análise de Valuation de Ações")

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


ticker = st.chat_input('Digite o código de negociação da ação (ex: BBDC4):')


with st.sidebar:
    if not ticker:
        st.image("https://s3-symbol-logo.tradingview.com/b3-on-nm--big.svg", use_column_width=True)
    else:
        pegar_logotipo = PegandoLogotipo(ticker=ticker)
        logo_url = pegar_logotipo.pegar_logotipo()
        if logo_url:
            st.image(logo_url, use_column_width=True)
        else:
            st.image("https://s3-symbol-logo.tradingview.com/b3-on-nm--big.svg", use_column_width=True)
        try:
            acao = yf.Ticker(f'{ticker}.SA')
            info = acao.info
            resposta_tradutor = ChatTradutor(info['longBusinessSummary'])
            if resposta_tradutor:
                #st.sidebar.markdown(resposta_tradutor.split('\n\n')[-1])  # Exibe a resposta no sidebar
                st.sidebar.markdown(
                f"<div style='text-align: justify; color: #708090;'><strong>{resposta_tradutor.split('\n\n')[-1]}</strong></div>",
        unsafe_allow_html=True
    )
        except Exception as e:
            pass
 
    st.sidebar.markdown("---")

    # Controle da visibilidade dos códigos
    if 'show_codes' not in st.session_state:
        st.session_state.show_codes = False
    
    # Botão para alternar a visibilidade dos códigos
    if st.sidebar.button("Códigos de Negociação"):
        st.session_state.show_codes = not st.session_state.show_codes
    
    if st.session_state.show_codes:
        st.sidebar.markdown(
            "<div style='max-height: 300px; overflow-y: auto;color: #8B4513;'><strong>"
            + "\n".join(f"- {codigo}" for codigo in codigos)
            + "</strong></div>",
            unsafe_allow_html=True
        )    

if ticker:
    messages.append({"role": "user", "content": ticker})
    with st.chat_message("user"):
        st.markdown(ticker)
    fundamentos = ModeloValuation(query=f'O que voce pode me dizer sobre os fundamentos da acao {ticker}', ticker=ticker)
    response = fundamentos.chat_valuation()
    if response and isinstance(response, Generator):
        response_text, chunks = generator_to_string(response)
        response_generator = string_to_generator(chunks)
        with st.chat_message("assistant"):
            st.write_stream(response_generator)
        messages.append({"role": "assistant", "content": configurar_mensagem(response_text)})
    else:
        with st.chat_message("assistant"):
            st.write(response)
        messages.append({"role": "assistant", "content": response}) 