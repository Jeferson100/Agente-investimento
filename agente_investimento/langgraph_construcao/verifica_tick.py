import pandas as pd
from langgraph.types import Command
from typing_extensions import Literal

from .type_state import State


def verificacao_tickets(state: State) -> Command[Literal["chatinput", "supervisor"]]:
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
    ticker = state.get("ticker", "")
    metodo_analise = state.get("method_analysis", [])
    empresas_df = pd.read_csv(
        "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv",
        encoding="utf-8",
    )
    # ticks_ok = [tick for tick in ticker if tick in empresas_df['tic'].values]
    if ticker in empresas_df["tic"].values or any(
        metodo == "chatbot" for metodo in metodo_analise
    ):
        return Command(
            goto="supervisor",
        )
    return Command(
        goto="chat_input",
    )
