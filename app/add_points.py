import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import APIRouter, Request
from langchain.schema import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from starlette.config import Config

sys.path.append("..")
from agente_investimento import langgraph_main

logger = logging.getLogger(__name__)

router = APIRouter()

config = Config(".env") if os.path.exists(".env") else Config()

CHECKPOINT_URL = config(
    "DB_URI",
    cast=str,
    default="postgresql://postgres:postgres@localhost:5433/postgres",
)

logger.info(
    f"DB_URI: {CHECKPOINT_URL}"
)  # pylint: disable=logging-fstring-interpolation


@asynccontextmanager
async def lifespan() -> AsyncGenerator:
    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold": 0,
        "row_factory": dict_row,
    }
    async with AsyncConnectionPool(
        conninfo=CHECKPOINT_URL, max_size=20, kwargs=connection_kwargs
    ) as pool:
        await pool.wait()
        yield {"pool": pool}
        checkpointer = AsyncPostgresSaver(pool)  # type:ignore
        await checkpointer.setup()
        yield {"pool": pool, "checkpointer": checkpointer}


@router.post("/message")
async def chatbot(message: str, request: Request):
    """
    Endpoint do chatbot que recebe uma mensagem e retorna a resposta do LangGraph.
    """  # pylint: disable= logging-fstring-interpolation

    # Estado inicial para a invocação do grafo
    initial_state = {
        "messages": [HumanMessage(content=message)],
        "ticker": "",
        "method_analysis": "",
        "dados_input": "",
        "next": "",
    }

    checkpointer = request.state.checkpointer

    # Constrói e compila o grafo
    graph_builder = langgraph_main()

    graph = graph_builder.compile(checkpointer=checkpointer)

    response = await graph.ainvoke(
        initial_state,
        config=config,  # type:ignore
        stream_mode="values",  # Adicionado para corresponder ao notebook
    )

    return response
