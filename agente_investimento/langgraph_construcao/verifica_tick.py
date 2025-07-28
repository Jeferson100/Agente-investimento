import pandas as pd
from langgraph.types import Command
from typing_extensions import Literal

from .type_state import State
from pandas import DataFrame
from typing_extensions import Literal
from langgraph.types import Command


def verificacao_tickets(
    state: State,
) -> Command[Literal["identifica_ticks", "chatbot_padrao", "supervisor"]]:
    """
    Checks whether the extracted ticker is valid or if the analysis method corresponds to the chatbot.

    This function performs a check on the current state to determine whether the provided ticker
    is present in the list of valid companies (loaded from an external source) or if the analysis
    method includes 'chatbot'. Based on this, it decides whether the flow should proceed
    to the supervisor node or return to the user input node.

    Args:
        state (State): The current state dictionary, containing at least the keys
                       'ticker' (str) and 'method_analysis' (list).

    Returns:
        Command[Literal["chatinput", "supervisor"]]: A command indicating the next node
            to be executed in the flow:
            - "supervisor" if the ticker is valid or the analysis method is 'chatbot'.
            - "chat_input" otherwise, indicating that the user input should be revised.
    """
    print("Entrei verificacao tickets")

    ticker = state.get("ticker", "")

    mensagem = state.get("messages")

    last_messagem = mensagem[-1]

    procura_interacao_ticker: int = state.get("interacao_procura_ticker", 0)

    empresas_df: DataFrame = pd.read_csv(
        "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv",
        encoding="utf-8",
    )

    if isinstance(ticker, list):
        ticker = [tick for tick in ticker if tick in empresas_df["tic"].values]
    if isinstance(ticker, str):
        ticker = ticker in empresas_df["tic"].values
    if ticker:
        return Command(
            goto="supervisor",
        )

    if procura_interacao_ticker >= 2:
        print(f"As ações nao foram encontrados!")
        return Command(
            goto="chatbot_padrao",
            update={
                "mensagem_sistema": f"The tickers provided by the user were not found!## Inform that the tickers mentioned in this message: {last_messagem} were not found!",
                "interacao_procura_ticker": 0,
            },
        )

    procura_interacao_ticker += 1

    return Command(
        goto="identifica_ticks",
        update={"interacao_procura_ticker": procura_interacao_ticker},
    )
