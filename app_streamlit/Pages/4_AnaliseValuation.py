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
    page_icon="imagem/analise_valuation.webp",
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
        st.image("imagem/analise_valuation.webp", use_column_width=True)
    else:
        pegar_logotipo = PegandoLogotipo(ticker=ticker)
        logo_url = pegar_logotipo.pegar_logotipo()
        if logo_url:
            st.image(logo_url, use_column_width=True)
        else:
            st.image("imagem/analise_valuation.webp", use_column_width=True)
        try:
            acao = yf.Ticker(f'{ticker}.SA')
            info = acao.info
            resposta_tradutor = ChatTradutor(info['longBusinessSummary'])
            if resposta_tradutor:
                #st.sidebar.markdown(resposta_tradutor.split('\n\n')[-1])  # Exibe a resposta no sidebar
                st.sidebar.markdown(
                f"<div style='text-align: justify; color: #000000;'><strong>{resposta_tradutor.split('\n\n')[-1]}</strong></div>",
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
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown(
        """
        <div style="background-color:#FF6347; padding: 10px; border-radius: 5px;">
            <p style="color: #000000;">🚨 Aviso Importante:</p>
            <p style="color: #000000;">Os resultados fornecidos por este sistema são meramente informativos e não devem ser considerados como recomendações de investimento.</p>
            <p style="color: #000000;">Sempre realize sua própria análise antes de tomar qualquer decisão financeira.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )  
    
    st.sidebar.markdown("---")
    
    st.markdown("# Contatos")
    
    st.sidebar.markdown(
        """
        <div style="display: inline-block; margin-right: 10px;">
            <a href="https://github.com/Jeferson100/Agente-investimento">
                <img src="https://img.shields.io/badge/github-100000?style=for-the-badge&logo=github">
            </a>
        </div>
        <div style="display: inline-block;">
            <a href="https://www.linkedin.com/in/jefersonsehnem/">
                <img src="https://img.shields.io/badge/linkedin-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
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