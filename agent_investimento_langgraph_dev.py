from langgraph.graph import END, StateGraph

from agente_investimento import (
    analise_investimento,
    process_fundamental,
    process_sentimento,
    process_technical,
    process_valuation,
)
from agente_investimento import chatbot_investimento
from agente_investimento import chatbot_padrao
from agente_investimento import State
from agente_investimento import supervisor_node
from agente_investimento import verificacao_tickets
from agente_investimento import identifica_metodo_analise
from agente_investimento import identifica_ticks



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


graph_buider = graph.compile()