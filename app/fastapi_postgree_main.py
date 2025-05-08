import logging
import os
import sys

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langchain.schema import HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from starlette.config import Config

sys.path.append("..")
from agente_investimento import langgraph_main

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Agente de Investimento API",
    description="API para análise de investimentos usando LangGraph",
    version="1.0.0",
)

config = Config(".env") if os.path.exists(".env") else Config()

CHECKPOINT_URL = config(
    "DB_URI",
    cast=str,
    default="postgresql://postgres:postgres@localhost:5433/postgres",
)

logger.info(f"DB_URI: {CHECKPOINT_URL}")

connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
    "row_factory": dict_row,
}


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

    async with AsyncConnectionPool(
        conninfo=CHECKPOINT_URL,
        max_size=20,
        kwargs=connection_kwargs,
    ) as pool:
        checkpointer = AsyncPostgresSaver(pool)  # type:ignore

        await checkpointer.setup()

        graph = graph_builder.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": "1"}}

        # Estado inicial para a invocação do grafo
        initial_state = {
            "messages": [HumanMessage(content=message)],
            "ticker": "",
            "method_analysis": "",
            "dados_input": "",
            "next": "",
        }

        response = await graph.ainvoke(
            initial_state,
            config=config,  # type:ignore
        )

    return response


@app.get("/check-db")
async def check_db():
    """
    Endpoint para verificar a conexão com o banco de dados
    """
    try:
        async with AsyncConnectionPool(
            conninfo=CHECKPOINT_URL,
            max_size=20,
            kwargs=connection_kwargs,
        ) as pool:
            checkpointer = AsyncPostgresSaver(pool)  # type:ignore
            await checkpointer.setup()
            return {
                "status": "success",
                "message": "Conexão com o banco de dados estabelecida com sucesso.",
            }
    except Exception as e:
        import traceback

        return {
            "status": "error",
            "message": f"Erro ao verificar a conexão: {str(e)}",
            "details": traceback.format_exc(),
        }


@app.get("/return-db/{thread_id}")
async def return_db(thread_id: str = "1"):
    """
    Endpoint para retornar os dados do banco de dados
    """
    try:
        async with AsyncConnectionPool(
            conninfo=CHECKPOINT_URL,
            max_size=20,
            kwargs=connection_kwargs,
        ) as pool:
            checkpointer = AsyncPostgresSaver(pool)  # type:ignore
            await checkpointer.setup()
            config = {"configurable": {"thread_id": thread_id}}
            checkpoint = await checkpointer.aget(config)  # type:ignore
            if checkpoint is None:
                return {"status": "Vazio", "message": "O banco de dados está vazio."}
            return checkpoint
    except Exception as e:
        import traceback

        return {
            "status": "error",
            "message": f"Erro ao verificar a conexão: {str(e)}",
            "details": traceback.format_exc(),
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fastapi_postgree_main:app", host="0.0.0.0", port=3000, reload=True)
