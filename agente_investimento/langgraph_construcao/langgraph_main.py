from langgraph.graph import END, StateGraph

from ..utils import (
    analise_investimento,
    process_fundamental,
    process_sentimetal,
    process_technical,
    process_valuation,
)

from .chat_bot_response import chatbot
from .chat_input_langgraph import chat_input
from .state import State
from .supervisor_node import supervisor_node
from .verifica_tick import verificacao_tickets


def langgraph_main() -> StateGraph:
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatinput", chat_input)
    graph_builder.add_node("verificacao_tickets", verificacao_tickets)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("analise_investimento", analise_investimento)
    graph_builder.add_node("fundamentals", process_fundamental)
    graph_builder.add_node("sentimental", process_sentimetal)
    graph_builder.add_node("valuation", process_valuation)
    graph_builder.add_node("technical", process_technical)
    graph_builder.add_node("supervisor", supervisor_node)
    graph_builder.add_edge("chatinput", "verificacao_tickets")
    graph_builder.set_entry_point("chatinput")
    graph_builder.add_edge("chatbot", END)

    return graph_builder
