import streamlit as st
import sys
import os
import requests
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from juncao_modelos_dados import ModeloFundamentos
from utils import PegandoLogotipo, generator_to_string, string_to_generator, configurar_mensagem, retransfromando_pandas
from chat_bots import ChatTradutor
import yfinance as yf
from typing import Generator
import pandas as pd
from typing import List, Any
import io



st.set_page_config(
    page_title="Analise Ações",
    page_icon="imagem/analise_fundamentalista.webp",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Analise Ações",
    },
)

if 'groq_api' in st.session_state and st.session_state.groq_api or os.getenv("GROQ_API_KEY"):
    pass
else:
    st.warning("Por favor, retorne à página principal para inserir sua chave de API GROQ.")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #D3D3D3;  /* Cor de fundo */
    }
    .css-1d391kg {  /* A classe pode mudar com atualizações do Streamlit! */
        color: #6A5ACD;  /* Cor do texto */
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "chat_history_fundamentalista" not in st.session_state:
    st.session_state.chat_history_fundamentalista = []
    
if "codigos" not in st.session_state:
    codigos = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv",
            
        )['tic'].to_list()

    st.session_state.codigos =  sorted(set(filter(None, codigos)))

if "dados_fundamentalistas" not in st.session_state:
    st.session_state.dados_fundamentalistas = None

codigos = st.session_state.codigos
messages = st.session_state.chat_history_fundamentalista

def clear_messages():
    if "chat_history_fundamentalista" in st.session_state:
        del st.session_state["chat_history_fundamentalista"]
    st.rerun()


st.title("Modelo de LLM para Análise Fundamentalista")


for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


ticker = st.chat_input('Digite o código de negociação da ação (ex: BBDC4):')

with st.sidebar:
    if not ticker:
        st.image("imagem/analise_fundamentalista.webp", use_column_width=True)
    else:
        pegar_logotipo = PegandoLogotipo(ticker=ticker)
        logo_url = pegar_logotipo.pegar_logotipo()
        if logo_url:
            st.image(logo_url, use_column_width=True)
        else:
            st.image("imagem/analise_fundamentalista.webp", use_column_width=True)
        try:
            acao = yf.Ticker(f'{ticker}.SA')
            info = acao.info
            resposta_tradutor = ChatTradutor(info['longBusinessSummary'],api_secret=st.session_state.groq_api)
            if resposta_tradutor:
                #st.sidebar.markdown(resposta_tradutor.split('\n\n')[-1])  # Exibe a resposta no sidebar
                st.sidebar.markdown(
                f"<div style='text-align: justify; color: #000000;'><strong>{resposta_tradutor.split('\n\n')[-1]}</strong></div>",
        unsafe_allow_html=True
    )
        except Exception as e:
            pass
 

if ticker:
    messages.append({"role": "user", "content": ticker})
    with st.chat_message("user"):
        st.markdown(ticker)
    fundamentos = ModeloFundamentos(query=f'O que voce pode me dizer sobre os fundamentos da acao {ticker}', ticker=ticker,api_secret=st.session_state.groq_api)
    response, dados_fundamentalistas = fundamentos.chat_fundamentalistas()
    st.session_state.dados_fundamentalistas = dados_fundamentalistas
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
    
    
with st.sidebar:
    
    st.sidebar.markdown("---")
        
    col1, col2,  col3 = st.sidebar.columns(3)
    
    with col1:
        # Controle da visibilidade dos códigos
        if 'show_codes' not in st.session_state:
            st.session_state.show_codes = False
        
        # Botão para alternar a visibilidade dos códigos
        if st.button("Códigos de Negociação", help="Mostra os códigos de negociação"):
            st.session_state.show_codes = not st.session_state.show_codes
        
    with col2:
        if st.button("Limpar Mémoria", help="Limpa o histórico de mensagens", key="limpar_memoria_tecnica"):
            clear_messages()
    
            
    with col3:
        if 'download_dados_fundamentalista' not in st.session_state:
            st.session_state.download_dados_fundamentalista = False

        # Botão para alternar a exibição dos dados
        if st.button("Visualizar dados", help="Visualizar os dados processados pela LLM"):
            st.session_state.download_dados_fundamentalista = not st.session_state.download_dados_fundamentalista

    if st.session_state.show_codes:
        st.sidebar.markdown("---")
        st.sidebar.markdown(
                "<div style='max-height: 300px; overflow-y: auto;color: #8B4513;'><strong>"
                + "\n".join(f"- {codigo}" for codigo in codigos)
                + "</strong></div>",
                unsafe_allow_html=True
            )  
             
    if st.session_state.download_dados_fundamentalista and st.session_state.dados_fundamentalistas:
        st.sidebar.markdown("---")
        dados_fundamentalistas_df = retransfromando_pandas(st.session_state.dados_fundamentalistas)
        
        st.dataframe(dados_fundamentalistas_df)
        
        st.download_button(
                label="Download dados",
                data=dados_fundamentalistas_df.to_csv(index=False),
                file_name=f"dados_fundamentalistas.csv",
                mime="text/csv",
                help="Esses dados são os que foram processados pela LLM",
            )
    else:
        pass
    
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

