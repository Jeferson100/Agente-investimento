import streamlit as st
from juncao_modelos_dados import ModeloFundamentos, ModeloValuation, ModeloSentimento, ModeloAnaliseTecnica

st.set_page_config(
    page_title="Análise de Ações",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)
