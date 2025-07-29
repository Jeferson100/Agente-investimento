import os
import sys

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import asyncio

import pandas as pd
from langchain.schema import HumanMessage
from langgraph.checkpoint.memory import MemorySaver


from agente_investimento import (
    
    langgraph_main,
   
)

st.set_page_config(
    page_title="Analise Ações",
    page_icon="imagem/logo_robo.png",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Analise Ações",
    },
)


if 'groq_api' in st.session_state and st.session_state.groq_api or os.getenv("GROQ_API_KEY"):
    pass
else:
    st.warning("Por favor, defina a chave API do GROQ.")

if 'serper_api' in st.session_state and st.session_state.serper_api or os.getenv("API_KEY_SERPER"):
    pass
else:
    st.warning("Por favor, defina a chave API do Serper.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "codigos" not in st.session_state:
    codigos = pd.read_csv(
        "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv",
    )["tic"].to_list()
    st.session_state.codigos = sorted(set(filter(None, codigos)))

codigos = st.session_state.codigos
messages = st.session_state.chat_history


def clear_messages():
    if "chat_history_valuation" in st.session_state:
        del st.session_state["chat_history_valuation"]
    st.rerun()


st.title("Agente de Inteligência Artificial para Análise de Investimentos")

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

mensagem_usuario = st.chat_input("Faça sua pergunta:")

with st.sidebar:
    st.image("imagem/logo_robo.png", width=400)

    st.markdown(
        """
    No mundo dos investimentos, a tomada de decisões embasadas é fundamental para 
    minimizar 
    riscos e maximizar retornos. Para isso, quatro agentes de inteligência artificial 
    foram desenvolvidos, 
    cada um focado em uma abordagem específica de análise:

    ### 📊 Análise Fundamentalista  
    Examina balanços patrimoniais, demonstrativos financeiros e indicadores-chave como 
    **P/L, ROE e EBITDA** para avaliar a saúde financeira e o potencial de crescimento 
    de uma empresa.  

    ### 📉 Análise Técnica  
    Interpreta padrões gráficos, médias móveis e indicadores como **RSI** para prever 
    movimentos de preços e auxiliar no **timing** de compra e venda.  

    ### 📰 Análise de Sentimento  
    Coleta e processa **notícias** para identificar o sentimento do mercado 
    em relação a uma ação, classificando-o como **positivo, neutro ou negativo**.  

    ### 💰 Valuation  
    Utiliza modelos como **Fluxo de Caixa Descontado (DCF)** e o **Modelo de Gordon** 
    para 
    estimar o valor intrínseco de uma empresa, ajudando investidores a entenderem se 
    uma ação está **sobre ou subavaliada**.  

    Juntos, esses agentes formam um **ecossistema para análise de investimentos**.  
    """
    )
    st.markdown("# Login APIS:")
    st.write(
        """Para utilizar o Bot, primeiro faça o cadastro gratuito nos site abaixo e 
        depois gere as chaves API necessária:"""
    )

    st.markdown(
        """
    [![Groq API](https://img.shields.io/badge/Create%20Groq%20API%20Key-black?style=flat&logo=groq)](https://console.groq.com/keys)
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    [![Serper](https://img.shields.io/badge/Create%20Serper%20API%20Key-blue?style=flat&logo=groq)](https://serper.dev/api-key)
    """,
        unsafe_allow_html=True,
    )

    if "groq_api" not in st.session_state:
        st.session_state["groq_api"] = None

    if "serper_api" not in st.session_state:
        st.session_state["serper_api"] = None

    try:
        if os.getenv("GROQ_API_KEY") is not None:
            groq_api = os.getenv("GROQ_API_KEY")
            st.success("API key GROQ ja existe!", icon="✅")
        else:
            # Pede a chave apenas se ainda não estiver salva
            api_key = st.text_input(
                "Enter GROQ API token:",
                value=st.session_state.groq_api,
                type="password",
            )

            if api_key:
                os.environ["GROQ_API_KEY"] = api_key

            if api_key:
                st.session_state.groq_api = api_key
                st.success("API key GROQ configurada com sucesso!", icon="✅")

        if os.getenv("API_KEY_SERPER") is not None:
            serper_api = os.getenv("API_KEY_SERPER")
            st.success("API key Serper ja existe!", icon="✅")

        else:
            # Pede a chave apenas se ainda não estiver salva
            serper_api = st.text_input(
                "Enter Serper API token:",
                value=st.session_state.serper_api,
                type="password",
            )

            if serper_api:
                os.environ["API_KEY_SERPER"] = serper_api

            if serper_api:
                st.session_state.serper_api = serper_api
                st.success("API key Serper configurada com sucesso!", icon="✅")

    except ValueError as e:
        st.error(f"Erro ao utilizar a API: {e}")
        st.stop()

    st.markdown("---")

    col1, col2, col3 = st.sidebar.columns(3)

    with col1:
        # Controle da visibilidade dos códigos
        if "show_codes" not in st.session_state:
            st.session_state.show_codes = False

        # Botão para alternar a visibilidade dos códigos
        if st.button("Códigos de Negociação", help="Mostra os códigos de negociação"):
            st.session_state.show_codes = not st.session_state.show_codes

    with col2:
        if st.button(
            "Limpar Mémoria",
            help="Limpa o histórico de mensagens",
            key="limpar_memoria_tecnica",
        ):
            clear_messages()

    with col3:
        data_string = "\n".join(codigos)
        st.download_button(
            label="Download dados",
            data=data_string,
            file_name="dados_llm.md",
            mime="text/markdown",
            help="Esses dados são os que foram processados pela LLM",
        )

    if st.session_state.show_codes:
        st.sidebar.markdown(
            "<div style='max-height: 300px; overflow-y: auto;color: #8B4513;'><strong>"
            + "\n".join(f"- {codigo}" for codigo in codigos)
            + "</strong></div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.sidebar.markdown("Observação")

    st.sidebar.markdown(
        """
        <div style="background-color:#FF6347; padding: 10px; border-radius: 5px;">
            <p style="color: #000000;">🚨 Aviso Importante:</p>
            <p style="color: #000000;">Os resultados fornecidos por este sistema 
            são meramente informativos e não devem ser considerados como 
            recomendações de investimento.</p>
            <p style="color: #000000;">Sempre realize sua própria análise antes de 
            tomar qualquer decisão financeira.</p>
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

if mensagem_usuario:
    messages.append({"role": "user", "content": mensagem_usuario})
    with st.chat_message("user"):
        st.markdown(mensagem_usuario)
    graph_builder = langgraph_main()
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)  # Use checkpointer=memory
    config = {"configurable": {"thread_id": "1"}}
    # Estado inicial para a invocação do grafo
    initial_state = {
        "messages": [HumanMessage(content=mensagem_usuario)],
        "ticker": "",
        "method_analysis": "",
        "dados_input": "",
        "next": "",
    }
    response = asyncio.run(
        graph.ainvoke(
            initial_state,
            config=config,
        )
    )

    response_text = response["messages"][1].content

    with st.chat_message("assistant"):
        st.write(response_text)
    messages.append({"role": "assistant", "content": response_text})
