from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ..chat_bots import get_llm
from .type_state import State

from typing import Final

from dotenv import load_dotenv
import os

load_dotenv()

DEFAULT_MODEL: Final = "meta-llama/llama-4-scout-17b-16e-instruct"

MODEL_ID_CHAT_RESPONSE: str = os.getenv("MODEL_ID_CHAT_RESPONSE", DEFAULT_MODEL)


async def chatbot(state: State) -> Dict[str, Any]:
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
        system_message = SystemMessage(
            content=f"""
       Você é um assistente especializado em análise de investimentos no mercado brasileiro.
        
        Voce recebe os seguintes dados 
        <DADOS INPUT>
        {state["dados_input"]}.
        <DADOS INPUT>
        Nesses dados voce recebe informacao de analise técnica, analise fundamentalista, analise de sentimento e analise de valuation de acoes expecificado pelos usuarios.
        As analises nesses dados estao divididos pelo seguinte caracteres:
        - #########Technical Analysis#######  = Dentro dessa analise tem analise tecnica da acao.
        - ##########Fundamental Analysis######## = Dentro dessa analise tem a analise dos balancos da acao.
        - ############Valuation Analysis############ = Dentro dessa te a estimativa do valuation da acao.
        - #########Sentiment Analysis##### =  Dentro dessa temos a analise de noticias sobre a acao.
        
        Diretrizes:
        - Seja conciso e direto nas respostas
        - Use linguagem acessível, mas profissional
        - Quando não tiver certeza, admita as limitações
        - Sempre mencione os riscos envolvidos em investimentos
        - Evite recomendações diretas de compra/venda
        
        Voce deve dar o nivel de confianca da analise.
        Indique se analisando as entradas do agentes, a recomendacao e de compra, venda ou manter a acao.
    
        
        """
        )

        last_message = state["messages"][-1]

        messages = [system_message, HumanMessage(content=f"{last_message.content}")]

        llm = get_llm(model=MODEL_ID_CHAT_RESPONSE)

        response = await llm.ainvoke(messages)

        return {
            "messages": [AIMessage(content=response.content)],
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
