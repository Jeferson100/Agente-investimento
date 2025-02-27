import streamlit as st
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from juncao_modelos_dados import ModeloFundamentos

# CSS para customização

st.title("Agentes de Inteligência Artificial para Análise de Investimentos")
st.markdown("""
No mundo dos investimentos, a tomada de decisões embasadas é fundamental para minimizar riscos e maximizar retornos. Para isso, quatro agentes de inteligência artificial foram desenvolvidos, cada um focado em uma abordagem específica de análise:

### 📊 Análise Fundamentalista  
Examina balanços patrimoniais, demonstrativos financeiros e indicadores-chave como **P/L, ROE e EBITDA** para avaliar a saúde financeira e o potencial de crescimento de uma empresa.  

### 📉 Análise Técnica  
Interpreta padrões gráficos, médias móveis e indicadores como **RSI** para prever movimentos de preços e auxiliar no **timing** de compra e venda.  

### 📰 Análise de Sentimento  
Coleta e processa **notícias** para identificar o sentimento do mercado em relação a uma ação, classificando-o como **positivo, neutro ou negativo**.  

### 💰 Valuation  
Utiliza modelos como **Fluxo de Caixa Descontado (DCF)** e o **Modelo de Gordon** para estimar o valor intrínseco de uma empresa, ajudando investidores a entenderem se uma ação está **sobre ou subavaliada**.  

Juntos, esses agentes formam um **ecossistema para análise de investimentos**.  
""")

with st.sidebar:
    st.markdown("# Login APIS:")
    st.write(
        """Para utilizar o Bot, primeiro faça um cadastro gratuito nos sites abaixo e depois gere as chaves APIs necessárias:"""
    )

    st.markdown(
        """
    [![Groq API](https://img.shields.io/badge/Create%20Groq%20API%20Key-black?style=flat&logo=groq)](https://console.groq.com/keys)
    [![Create SEARCHAPI API Key](https://img.shields.io/badge/Create%20SEARCHAPI%20API%20Key-green?style=flat&logo=key)](https://www.searchapi.io/)
    """,
        unsafe_allow_html=True,
    )
    
    if 'groq_api' not in st.session_state:
        st.session_state['groq_api'] = ''
    try:
        if os.getenv("GROQ_API_KEY") is not None:
            groq_api = os.getenv("GROQ_API_KEY")
            st.success("API key GROQ ja existe!", icon="✅")
        else:
            groq_api = st.text_input("Enter GROQ API token:", type="password")
            st.session_state['groq_api'] = groq_api
            
    except ValueError as e:
        st.error(f"Erro ao utilizar a API: {e}")
        st.stop()
        
    st.markdown("---")
    
    st.sidebar.markdown("Observação")

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
                <img src="https://img.shields.io/badge/linkedin-0077b5?style=for-the-badge&logo=linkedin&logocolor=white">
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )
              






