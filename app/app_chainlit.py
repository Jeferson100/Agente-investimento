import os
import sys

import chainlit as cl
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agente_investimento import langgraph_main

load_dotenv()

graph_builder = langgraph_main()
memory = MemorySaver()
# graph = graph_builder.compile(checkpointer=memory)# Use checkpointer=memory
graph = graph_builder.compile()


@cl.on_message
async def main(message: cl.Message):

    response = await graph.ainvoke(
        {"messages": [HumanMessage(content=message.content)]},
        config=RunnableConfig(
            callbacks=[
                cl.LangchainCallbackHandler(
                    to_ignore=[
                        "ChannelRead",
                        "RunnableLambda",
                        "ChannelWrite",
                        "__start__",
                        "_execute",
                    ]
                    # can add more into the to_ignore: "agent:edges", "call_model"
                    # to_keep=
                )
            ]
        ),
    )

    # Debug: verificar o que está sendo retornado
    print(f"Response type: {type(response)}")
    print(f"Response content: {response}")

    # Verificar se response["messages"] existe e é uma lista
    if (
        "messages" in response
        and isinstance(response["messages"], list)
        and len(response["messages"]) > 0
    ):
        await cl.Message(content=response["messages"][-1].content).send()
    else:
        await cl.Message(content="Erro: Resposta inválida recebida").send()
