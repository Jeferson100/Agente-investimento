import json

import pandas as pd
from langchain_core.messages import HumanMessage
from ..chat_bots import get_llm

from .state import State


async def chat_input(state: State) -> State:
    """
    Processes the user's last message to identify a stock ticker and the requested analysis method.

    This function reads a list of companies and their tickers from an external source.
    It builds a prompt for a large language model (LLM) instructing it to extract
    the stock ticker and the type of analysis (fundamentals, valuation, sentimental, technical, analise_investimento, chatbot)
    from the user's last message in the provided state.

    The function sends the prompt and the user's message to the LLM, parses the response
    to extract the ticker and method. It performs a basic check to ensure
    the extracted ticker is valid or finds a similar one if necessary.
    Finally, it updates the state dictionary with the identified ticker and analysis method,
    and returns the updated state.

    Args:
        state (State): A dictionary representing the current conversation state,
                       expected to contain a "messages" key with a list
                       of messages, where the last one is from the user.

    Returns:
        State: The updated state dictionary with the 'ticker' and
               'method_analysis' keys filled in with the values extracted from
               the LLM response. The ticker may be an empty string if none
               was identified. The analysis method will be one of the following:
               fundamentals, valuation, sentimental, technical, analise_investimento, chatbot.
    """

    empresas_df = pd.read_csv(
        "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv",
        encoding="utf-8",
    )

    prompt = """
    Você é um assistente especializado em investimentos do mercado brasileiro. Extraia precisamente as seguintes informações:
    
    1. O ticker (código) da ação mencionada na mensagem do usuário. Se houver múltiplos tickers, identifique qual está sendo solicitado para análise.
    2. O método de análise desejado (fundamentals, valuation, sentimental, technical). 
    3. Se for dado exemplos parecido com "Analise essa petrobras" ou "Vale apena investir na vale" responda (analise_investimento).
    4. Se o usuário apenas mencionar uma empresa sem pedir análise específica, ainda extraia o ticker e defina o método como .
    5. Se não houver menção a nenhuma empresa ou ticker, retorne o método como "chatbot".
    
    Regras para identificação de tickers:
    - Tickers brasileiros geralmente terminam com números (ex: PETR4, VALE3)
    - Se o usuário mencionar apenas o nome da empresa (ex: "Petrobras"), identifique o ticker correto ({empresas_tickers})
    - Se houver ambiguidade, prefira o ticker mais líquido (geralmente terminados em 3 ou 4)
    - Se o usuário mencionar apenas o setor (ex: "bancos"), não retorne ticker específico
    
    Formato de resposta (apenas):
    <FORMATO RESPOSTAS>
    TICKER: [ticker em letras maiúsculas ou vazio se não identificado]
    MÉTODO: [Deve retornar strings, Caso haja mais de um método, separe-as strings por vírgula, ex: ["technical", "valuation"]]
    <FORMATO RESPOSTAS>
    """

    empresas_tickers = "\n".join(
        [
            f"{empresa} ({ticker})"
            for empresa, ticker in zip(empresas_df["Empresa"], empresas_df["tic"])
        ]
    )
    prompt = prompt.format(empresas_tickers=empresas_tickers)

    last_message = state["messages"][-1]

    llm = get_llm()

    response = await llm.ainvoke(
        [HumanMessage(content=prompt), HumanMessage(content=last_message.content)]
    )

    response_text = response.content

    ticker = ""
    metodo_analise = "chatbot"

    # Extração mais robusta
    for line in response_text.split("\n"):  # type: ignore[union-attr]
        if line.startswith("TICKER:"):
            ticker = line.split(":")[1].strip()
        elif line.startswith("MÉTODO:"):
            metodo_analise = line.split(":")[1].strip()

    if isinstance(metodo_analise, str) and metodo_analise.startswith("["):
        metodo_analise = json.loads(metodo_analise)
    else:
        metodo_analise = [m.strip() for m in metodo_analise.split(",") if m.strip()]  # type: ignore
    if ticker:
        if ticker not in empresas_df["tic"].values:
            similar_tickers = empresas_df[empresas_df["tic"].str.contains(ticker[:2])][
                "tic"
            ].tolist()
            if similar_tickers:
                ticker = similar_tickers[0]

    state["ticker"] = ticker
    state["method_analysis"] = metodo_analise  # type: ignore

    return state
