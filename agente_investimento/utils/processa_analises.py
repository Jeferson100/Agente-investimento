import asyncio
from collections.abc import Iterator
from typing import Literal

from langchain.schema import HumanMessage
from langgraph.types import Command

from ..juncao_modelos_dados import (
    ModeloAnaliseTecnicaAsync,
    ModeloFundamentosAsync,
    ModeloSentimentoAsync,
    ModeloValuationAsync,
)
from ..langgraph_construcao.type_state import State


async def process_technical(state: State) -> Command[Literal["supervisor"]]:
    """
    Executes technical analysis for the specified ticker in the state.

        Retrieves the ticker and the user's last message from the state.
        Instantiates and calls the asynchronous technical analysis model.
        Adds the model's response to the 'dados_input' list in the state.

        Args:
            state (State): The current state dictionary, containing 'ticker',
                        'messages', and 'dados_input'.

        Returns:
            Optional[State]: The updated state with the technical analysis response
                            added to 'dados_input', or None if an error occurs.
    """
    print("Entrei nos techincal")

    ticker = state["ticker"]
    query = state["messages"][-1]
    modelo = ModeloAnaliseTecnicaAsync(ticker=ticker, query=query)
    response = await modelo.chat_analise_tecnica()

    dados_input = state["dados_input"]

    if isinstance(dados_input, list):
        dados_input = dados_input[0].content  # type: ignore

    response = dados_input + "\n" + response  # type: ignore

    return Command(
        update={"dados_input": [HumanMessage(content=response, name="tecnica")]},
        goto="supervisor",
    )


async def process_valuation(state: State) -> Command[Literal["supervisor"]]:
    """
    Executes valuation analysis for the specified ticker in the state.

    Retrieves the ticker and the user's last message from the state.
    Instantiates and calls the asynchronous valuation model.
    Adds the model's response to the 'dados_input' list in the state.

    Args:
        state (State): The current state dictionary, containing 'ticker',
                    'messages', and 'dados_input'.

    Returns:
        Optional[State]: The updated state with the valuation analysis response
                        added to 'dados_input', or None if an error occurs.
    """
    print("Entrei nos valuation")

    ticker = state["ticker"]
    query = state["messages"][-1]
    modelo = ModeloValuationAsync(ticker=ticker, query=query)
    response = await modelo.chat_valuation()
    dados_input = state["dados_input"]

    if isinstance(dados_input, list):
        dados_input = dados_input[0].content  # type: ignore

    response = dados_input + "\n" + response  # type: ignore
    return Command(
        update={"dados_input": [HumanMessage(content=response, name="valuation")]},
        goto="supervisor",
    )


async def process_sentimetal(state: State) -> Command[Literal["supervisor"]]:
    """
    Executes sentiment analysis for the specified ticker in the state.

    Retrieves the ticker and the user's last message from the state.
    Instantiates and calls the asynchronous sentiment analysis model.
    Adds the model's response to the 'dados_input' list in the state.

    Args:
        state (State): The current state dictionary, containing 'ticker',
                       'messages', and 'dados_input'.

    Returns:
        Optional[State]: The updated state with the sentiment analysis response
                         added to 'dados_input', or None if an error occurs.
    """
    print("Entrei nos sentimental")

    ticker = state["ticker"]
    query = state["messages"][-1]
    modelo = ModeloSentimentoAsync(ticker=ticker, query=query)
    response = await modelo.chat_sentimento()
    dados_input = state["dados_input"]

    if isinstance(dados_input, list):
        dados_input = dados_input[0].content  # type: ignore

    response = dados_input + "\n" + response  # type: ignore

    return Command(
        update={"dados_input": [HumanMessage(content=response, name="valuation")]},
        goto="supervisor",
    )


async def process_fundamental(state: State) -> Command[Literal["supervisor"]]:
    """
    Executes fundamental analysis for the specified ticker in the state.

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
    print("Entrei nos fundamentos")

    ticker = state["ticker"]
    query = state["messages"][-1]
    modelo = ModeloFundamentosAsync(ticker=ticker, query=query)
    response = await modelo.chat_fundamentalistas()
    dados_input = state["dados_input"]

    if isinstance(dados_input, list):
        dados_input = dados_input[0].content  # type: ignore

    response = dados_input + "\n" + response  # type: ignore

    return Command(
        update={"dados_input": [HumanMessage(content=response, name="valuation")]},
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
    ticker = state["ticker"]
    dados_input = state.get("dados_input", "")

    tecnica = ModeloAnaliseTecnicaAsync(
        query=f"Qual a analise tecnica da {ticker}",
        ticker=ticker,
    )
    fundamentos = ModeloFundamentosAsync(
        query=f"Qual o fundamentos da {ticker}",
        ticker=ticker,
    )
    valuation = ModeloValuationAsync(
        query=f"Qual o valuation da {ticker}",
        ticker=ticker,
    )
    sentimento = ModeloSentimentoAsync(
        query=f"Qual o sentimento da {ticker}",
        ticker=ticker,
    )

    response = await asyncio.gather(
        tecnica.chat_analise_tecnica(),
        fundamentos.chat_fundamentalistas(),
        valuation.chat_valuation(),
        sentimento.chat_sentimento(),
    )

    # Se dados_input é uma lista, converta para string antes de concatenar
    if isinstance(dados_input, list):  # type: ignore
        dados_input = "\n".join(dados_input) if dados_input else ""

    response = "\n".join(response)  # type: ignore

    # Agora concatena as strings
    response = f"{dados_input}\n{response}" if dados_input else response  # type: ignore

    return Command(
        update={"dados_input": [HumanMessage(content=response)]},  # type: ignore
        goto="supervisor",
    )
