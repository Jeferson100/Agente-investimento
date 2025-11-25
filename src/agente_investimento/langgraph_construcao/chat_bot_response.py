import os
from typing import Any, Dict, Final

from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from ..chat_bots import get_llm
from .type_state import State

load_dotenv()

DEFAULT_MODEL: Final = "meta-llama/llama-4-scout-17b-16e-instruct"

MODEL_ID_CHAT_RESPONSE: str = os.getenv("MODEL_ID_CHAT_RESPONSE", DEFAULT_MODEL)


async def chatbot_investimento(state: State) -> Dict[str, Any]:
    """
    Generates a consolidated investment analysis response using an LLM.

    This function builds a detailed prompt for an LLM (ChatGroq),
    providing it with the results of previous analyses (technical, fundamental,
    sentiment, valuation) stored in `state['dados_input']` and the user's latest
    message from `state['messages']`.

    The LLM is instructed to act as an investment assistant, summarize
    each type of analysis, provide an overall commentary on the asset,
    indicate a confidence level, and give final considerations (including risks),
    formatting the output in Markdown.

    Args:
        state (State): The current state dictionary, which must include:
            - 'dados_input': A list of strings, each representing the result
                             of a previous analysis, separated by specific markers
                             (e.g., '###Technical Analysis###').
            - 'messages': A list of conversation messages, where the last
                          one is the most recent user query.
            - 'ticker': (Optional) The stock ticker being analyzed.
            - 'method_analysis': (Optional) The identified analysis method.

    Returns:
        Dict[str, Any]: A dictionary containing the new AI message ('messages'),
                        and preserving 'ticker', 'method_analysis', and 'dados_input'
                        from the original state. In case of processing errors,
                        the AI message will include an error description.
    """

    try:
        system_message = """
        You are an investment analysis agent with over 10 years of experience. You receive the following data.        
        <INPUT DATA>
        {dados_input}.
        </INPUT DATA>
        Your task is to analyze the data and answer the user's question {messages}.

        Guidelines:
        - Be concise and direct
        - Use professional but accessible language  
        - Acknowledge limitations when uncertain
        - Always mention investment risks
        - Avoid direct buy/sell recommendations

        ## Investment Analysis
        - Comment on why you think the stock is good

        *Note:*  
        If there is insufficient data about the company, respond normally based on a generic conversation.
        IMPORTANT: ALWAYS PROVIDE THE RESPONSE IN PORTUGUESE (BRAZILIAN PORTUGUESE).
        
        """

        last_message = state["messages"][-1]
        dados_input = state.get("dados_input", "")

        chat_prompt: ChatPromptTemplate = ChatPromptTemplate.from_template(
            system_message
        )

        llm: ChatGroq = get_llm(model=MODEL_ID_CHAT_RESPONSE)

        llm_chain = chat_prompt | llm | StrOutputParser()

        response = await llm_chain.ainvoke(
            {"messages": last_message, "dados_input": dados_input}
        )

        return {
            "messages": [AIMessage(content=response)],
            "ticker": state.get("ticker", ""),
            "method_analysis": state.get("method_analysis", ""),
            "dados_input": state.get("dados_input", ""),
        }

    except Exception as e:  # pylint: disable=W0718
        return {
            "messages": [AIMessage(content=f"Erro no processamento: {str(e)}")],
            "ticker": state.get("ticker", ""),
            "method_analysis": state.get("method_analysis", ""),
            "dados_input": "",
        }
