import logging
import os
import sys
import uvicorn
import psycopg2
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from langchain.schema import HumanMessage
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

config_env = Config(".env") if os.path.exists(".env") else Config()

CHECKPOINT_URL = config_env(
    "DB_URI",
    cast=str,
    default="postgresql://postgres:postgres@localhost:5433/postgres",
)

logger.info(
    f"DB_URI: {CHECKPOINT_URL}"
)  # pylint: disable=logging-fstring-interpolation

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

        config = {"configurable": {"thread_id": "1"}}  # pylint: disable=unused-variable

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
    except Exception as e:  # pylint: disable=broad-exception-caught
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
            config = {
                "configurable": {"thread_id": thread_id}
            }  # pylint: disable=unused-variable
            checkpoint = await checkpointer.aget(config)  # type:ignore
            if checkpoint is None:
                return {"status": "Vazio", "message": "O banco de dados está vazio."}
            return checkpoint
    except Exception as e:  # pylint: disable=broad-exception-caught
        import traceback

        return {
            "status": "error",
            "message": f"Erro ao verificar a conexão: {str(e)}",
            "details": traceback.format_exc(),
        }


@app.get("/quantidade_linhas/{thread_id}")
async def quantidade_linhas(thread_id: str = "1"):
    """
    Endpoint para retornar a quantidade de linhas do thread_id informado.
    """

    try:
        # Conexão
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="langgraph-postgres",
            port=5432,
        )
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM checkpoints WHERE thread_id = '{thread_id}';")
        rows = cur.fetchall()
        number_linhas_restante = len(rows)

        return {
            "status": "success",
            "message": f"""Quantidade"" de linhas para o thread_id {thread_id}: 
                        {number_linhas_restante}""",
        }
    except Exception as e:  # pylint: disable=broad-exception-caught
        import traceback

        return {
            "status": "error",
            "message": f"Erro ao contar linhas: {str(e)}",
            "details": traceback.format_exc(),
        }


@app.delete("/delete_linhas/{thread_id}/{num_linhas}")
async def limpar_memoria(thread_id: str = "2", num_linhas: str = "3"):
    """
    Endpoint para limpar a memória (checkpoint) do thread_id informado.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="langgraph-postgres",
            port=5432,
        )
        cur = conn.cursor()

        cur.execute(
            f"""
        DELETE FROM checkpoints
        WHERE ctid IN (
            SELECT ctid FROM checkpoints
            WHERE thread_id = '{thread_id}'
            ORDER BY checkpoint ASC
            LIMIT {num_linhas if num_linhas.isdigit() else 3}
        );
        """
        )
        conn.commit()
        cur.execute(f"SELECT * FROM checkpoints WHERE thread_id = '{thread_id}';")
        rows = cur.fetchall()
        number_linhas_restante = len(rows)
        cur.close()
        return {
            "status": "success",
            "thread_id": thread_id,
            "message": f"{num_linhas} linhas deletadas com sucesso.",
            "remaining_rows": number_linhas_restante,
        }

    except Exception as e:  # pylint: disable=broad-exception-caught
        import traceback

        return {
            "status": "error",
            "message": f"Erro ao limpar memória: {str(e)}",
            "details": traceback.format_exc(),
        }


if __name__ == "__main__":

    uvicorn.run("fastapi_postgree_main:app", host="0.0.0.0", port=3000, reload=True)
