import asyncio
from collections.abc import Iterator
from typing import Literal

from langchain.schema import HumanMessage
from langgraph.types import Command

from ..juncao_modelos_dados import (
    ModeloAnaliseTecnicaComparacao,
    ModeloFundamentosComparacaoAsync,
    ModeloSentimentoComparacao,
    ModeloValuationComparacao,
)
from ..langgraph_construcao.type_state import State


async def process_fundamental(state: State) -> Command[Literal["supervisor"]]:
    """
    Executa a comparação de análise fundamentalista para os tickers especificados no estado.

    Recupera o ticker e a última mensagem do usuário do estado.
    Instancia e chama o modelo de análise fundamentalista assíncrono.
    Adiciona a resposta do modelo à lista 'dados_input' no estado.

    Args:
        state (State): O dicionário de estado atual, contendo 'ticker',
                       'messages' e 'dados_input'.

    Returns:
        Optional[State]: O estado atualizado com a resposta da análise fundamentalista
                         adicionada a 'dados_input', ou None se ocorrer um erro.
    """
    print("Entrei nos fundamentos comparacao")

    tickers = state["ticker"]
    query = state["messages"][-1]
    modelo = ModeloFundamentosComparacaoAsync(tickers=tickers, query=query)
    response = await modelo.chat_fundamentalistas_comparacao()
    dados_input = state.get("dados_input", "")
    if dados_input:
        response = f"{dados_input}\n{response}"
    return Command(
        update={"dados_input": [HumanMessage(content=response, name="fundamental")]},
        goto="supervisor",
    )


async def process_technical(state: State) -> Command[Literal["supervisor"]]:
    """
    Executa a comparação de análise tecnica para os tickers especificados no estado.

    Recupera o ticker e a última mensagem do usuário do estado.
    Instancia e chama o modelo de análise fundamentalista assíncrono.
    Adiciona a resposta do modelo à lista 'dados_input' no estado.

    Args:
        state (State): O dicionário de estado atual, contendo 'ticker',
                       'messages' e 'dados_input'.

    Returns:
        Optional[State]: O estado atualizado com a resposta da análise fundamentalista
                         adicionada a 'dados_input', ou None se ocorrer um erro.
    """
    print("Entrei nos tecnica comparacao")

    tickers = state["ticker"]
    query = state["messages"][-1]
    modelo = ModeloAnaliseTecnicaComparacao(
        tickers=tickers,
        query=query,
        periodo="3Y",
        intervalo="1mo",
    )
    response = await modelo.chat_analise_tecnica_comparacao()
    dados_input = state.get("dados_input", "")
    if dados_input:
        response = f"{dados_input}\n{response}"
    return Command(
        update={"dados_input": [HumanMessage(content=response, name="technical")]},
        goto="supervisor",
    )


async def process_valuation(state: State) -> Command[Literal["supervisor"]]:
    """
    Executa a comparação de análise valuation para os tickers especificados no estado.

    Recupera o ticker e a última mensagem do usuário do estado.
    Instancia e chama o modelo de análise fundamentalista assíncrono.
    Adiciona a resposta do modelo à lista 'dados_input' no estado.

    Args:
        state (State): O dicionário de estado atual, contendo 'ticker',
                       'messages' e 'dados_input'.

    Returns:
        Optional[State]: O estado atualizado com a resposta da análise fundamentalista
                         adicionada a 'dados_input', ou None se ocorrer um erro.
    """
    print("Entrei nos fundamentos comparacao")

    tickers = state["ticker"]
    query = state["messages"][-1]

    modelo = ModeloValuationComparacao(query=query, tickers=tickers)

    response = await modelo.chat_valuation()
    dados_input = state.get("dados_input", "")
    if dados_input:
        response = f"{dados_input}\n{response}"

    return Command(
        update={"dados_input": [HumanMessage(content=response, name="valuation")]},
        goto="supervisor",
    )


async def process_sentimento(state: State) -> Command[Literal["supervisor"]]:
    """
    Executa a comparação de análise de sentimento para os tickers especificados no estado.

    Recupera o ticker e a última mensagem do usuário do estado.
    Instancia e chama o modelo de análise fundamentalista assíncrono.
    Adiciona a resposta do modelo à lista 'dados_input' no estado.

    Args:
        state (State): O dicionário de estado atual, contendo 'ticker',
                       'messages' e 'dados_input'.

    Returns:
        Optional[State]: O estado atualizado com a resposta da análise fundamentalista
                         adicionada a 'dados_input', ou None se ocorrer um erro.
    """
    print("Entrei nos sentimentos comparacao")

    tickers = state["ticker"]
    query = state["messages"][-1]
    modelo = ModeloSentimentoComparacao(tickers=tickers, query=query)
    response = await modelo.chat_sentimento()
    dados_input = state.get("dados_input", "")
    if dados_input:
        response = f"{dados_input}\n{response}"
    return Command(
        update={"dados_input": [HumanMessage(content=response, name="sentimento")]},
        goto="supervisor",
    )


async def analise_investimento(state: State) -> Command[Literal["supervisor"]]:
    """
    Executes fundamental analysis, valuation analysis, technical analysis and sentiment analysis for the specified ticker in the state.

    Retrieves the ticker and the user's last message from the state.
    Instantiates and calls the asynchronous fundamental analysis model.
    Adds the model's response to the 'dados_input' list in the state.

    Args:
        state (State): The current state dictionary, containing 'ticker',
                       'messages', and 'dados_input'.

    Returns:
        Optional[State]: The updated state with the fundamental analysis response
                         added to 'dados_input', or None if an error occurs.
    """

    print("Entrei em analise investimento comparacao")
    tickers = state["ticker"]

    query = state["messages"][-1]

    dados_input = state.get("dados_input", "")

    tecnica = ModeloAnaliseTecnicaComparacao(
        query=query,
        tickers=tickers,
    )
    fundamentos = ModeloFundamentosComparacaoAsync(
        query=query,
        tickers=tickers,
    )
    valuation = ModeloValuationComparacao(
        query=query,
        tickers=tickers,
    )
    sentimento = ModeloSentimentoComparacao(
        query=query,
        tickers=tickers,
    )

    response = await asyncio.gather(
        tecnica.chat_analise_tecnica_comparacao(),
        fundamentos.chat_fundamentalistas_comparacao(),
        valuation.chat_valuation(),
        sentimento.chat_sentimento(),
    )

    try:
        if isinstance(dados_input, list):  # type: ignore
            dados_input = "\n".join(dados_input) if dados_input else ""
    except TypeError:
        if isinstance(dados_input, list):

            dados_input = (
                "\n".join(
                    m.content if hasattr(m, "content") else str(m) for m in dados_input
                )
                if dados_input
                else ""
            )

    response = "\n".join(response)  # type: ignore

    response = f"{dados_input}\n{response}" if dados_input else response  # type: ignore

    return Command(
        update={
            "dados_input": [HumanMessage(content=response, name="analise_investimento")]
        },
        goto="supervisor",
    )
