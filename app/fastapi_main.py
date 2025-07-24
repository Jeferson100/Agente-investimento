import sys

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langchain.schema import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
sys.path.append("..")
from agente_investimento import langgraph_main

app = FastAPI(
    title="Agente de Investimento API",
    description="API para análise de investimentos usando LangGraph",
    version="1.0.0",
)


@app.get("/")
async def root():
    """
    Rota raiz que retorna informações básicas sobre a API
    """
    return JSONResponse(
        {
            "message": "Bem-vindo à API do Agente de Investimento",
            "endpoints": {
                "docs": "/docs",
                "chatbot": "/chatbot/{message}",
            },
            "exemplo": '/chatbot/ "Devo investir na pretrobras"4',
        }
    )


@app.get("/chatbot/{message}")
async def chatbot(message: str):
    """
    Endpoint do chatbot que recebe uma mensagem e retorna a resposta do LangGraph.
    """
    graph_builder = langgraph_main()
    memory = MemorySaver()
    # Compila o grafo com o memory saver
    graph = graph_builder.compile(checkpointer=memory)  # Use checkpointer=memory

    # Configuração para a thread específica (pode ser dinâmica se necessário)
    config = {"configurable": {"thread_id": "1"}}

    # Estado inicial para a invocação do grafo
    initial_state = {
        "messages": [HumanMessage(content=message)],
        "ticker": "",
        "method_analysis": "",
        "dados_input": "",
        "next": "",
    }

    # Invoca o grafo de forma assíncrona
    response = await graph.ainvoke(
        initial_state,
        config=config,
        # stream_mode="values", # O stream_mode pode precisar de tratamento especial em FastAPI
        # dependendo de como você quer lidar com o stream.
        # Para um retorno simples, pode remover ou ajustar.
        # Se precisar de streaming, use StreamingResponse do FastAPI.
    )

    # FastAPI lida automaticamente com a serialização de dicionários/listas para JSON
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fastapi_main:app", host="0.0.0.0", port=3000, reload=True)
