from langgraph.graph import END, StateGraph

from ..utils import (
    analise_investimento,
    process_fundamental,
    process_sentimento,
    process_technical,
    process_valuation,
)
from .chat_bot_response import chatbot_investimento
from .chat_bot_padrao import chatbot_padrao
from .type_state import State
from .supervisor_node import supervisor_node
from .verifica_tick import verificacao_tickets
from .identifica_metodo_analise import identifica_metodo_analise
from .identifica_ticks import identifica_ticks


def langgraph_main() -> StateGraph:
    graph = StateGraph(State)
    graph.add_node("identifica_ticks", identifica_ticks)
    graph.add_node("verificacao_tickets", verificacao_tickets)
    graph.add_node("metodo_analise", identifica_metodo_analise)
    graph.add_node("chatbot_investimento", chatbot_investimento)
    graph.add_node("valuation", process_valuation)
    graph.add_node("analise_investimento", analise_investimento)
    graph.add_node("tecnico", process_technical)
    graph.add_node("fundamentalista", process_fundamental)
    graph.add_node("sentimento", process_sentimento)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("chatbot_padrao", chatbot_padrao)
    graph.set_entry_point("metodo_analise")
    graph.add_edge("identifica_ticks", "verificacao_tickets")
    graph.add_edge("chatbot_investimento", END)
    graph.add_edge("chatbot_padrao", END)

    return graph
