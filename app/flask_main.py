import sys

from flask import Flask

sys.path.append("..")
from langchain.schema import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from agente_investimento import langgraph_main

app = Flask(__name__)


@app.route("/chatbot/<message>", methods=["GET"])
async def chatbot(message: str):
    graph_builder = langgraph_main()
    memory = MemorySaver()
    graph = graph_builder.compile(memory)
    config = {"configurable": {"thread_id": "1"}}
    initial_state = {
        "messages": [HumanMessage(content=message)],
        "ticker": "",
        "method_analysis": "",
        "dados_input": "",
        "next": "",
    }

    response = await graph.ainvoke(
        initial_state,
        config=config,
        stream_mode="values",
    )

    return response


if __name__ == "__main__":
    app.run(debug=True)
