from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages]  # type: ignore
    ticker: str
    method_analysis: list[str]
    dados_input: str
    next: str
