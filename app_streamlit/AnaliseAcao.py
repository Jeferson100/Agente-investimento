import sys
import os
import streamlit as st
# Obtém o diretório pai do diretório atual (app_streamlit)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Adiciona o diretório pai ao sys.path
sys.path.append(parent_dir)

from juncao_modelos_dados import ModeloFundamentos, ModeloValuation, ModeloSentimento, ModeloAnaliseTecnica

st.set_page_config(
    page_title="Analise Ações",
    page_icon="https://s3-symbol-logo.tradingview.com/b3-on-nm--big.svg",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Analise Ações",
    },
)

st.title("Análise Fundamentalista")


st.image("https://s3-symbol-logo.tradingview.com/b3-on-nm--big.svg", width=200, )





