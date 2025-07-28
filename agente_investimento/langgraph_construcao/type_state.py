from typing import Annotated
from typing import List
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages]
    ticker: List[str]
    method_analysis: List[str]
    interacao_procura_ticker: int
    next_method: str
    mensagem_sistema: str
    dados_input: str
