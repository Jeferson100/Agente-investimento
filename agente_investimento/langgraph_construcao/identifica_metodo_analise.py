
from typing import List, Literal, TypedDict
from pydantic import BaseModel, Field
from langchain.prompts.chat import ChatPromptTemplate
from .type_state import State
from langgraph.types import Command
from ..chat_bots import get_llm
from typing import Final

from dotenv import load_dotenv
import os

load_dotenv()

DEFAULT_MODEL: Final = "llama-3.1-8b-instant"

MODEL_ID_IDENTIFICA_METODO_ANALISE = os.getenv("MODEL_ID_IDENTIFICA_METODO_ANALISE", DEFAULT_MODEL)

llm = get_llm(
    model=MODEL_ID_IDENTIFICA_METODO_ANALISE,
)


class MetodoAnalise(BaseModel):
    """A list of stock Analysis methods."""
    method_analysis: List[Literal['fundamentalista', 'tecnico', 'sentimento', 'valuation', 'sem_analise', 'analise_investimento']] = Field(
        ...,
        description="A list of method analysis identified from the user's message. For example: ['fundamentalista', 'valuation']"
    )

prompt_metodo_analise = """
You are an expert investment analysis agent. Your task is to identify the analysis method from the user's query.

Available analysis methods:
- fundamentalista
- tecnico
- sentimento
- valuation
- analise_investimento - This method includes all methods: fundamentalista, tecnico, sentimento, valuation.
- sem_analise - If the user's query is a saudation or does not match any of the available methods, return 'sem_analise'.
If the user's query does not match any of the available methods, return 'sem_analise'.
If the user's query make questions about multiple methods, return analise_investimento method that includes all methods.

User Query: "{messages}"
"""
prompt_metodo_analise = ChatPromptTemplate.from_template(prompt_metodo_analise)

llm_identifica_metodo_analise = prompt_metodo_analise | llm.with_structured_output(MetodoAnalise)

def identifica_metodo_analise(state: State) -> Command[Literal["identifica_ticks", "chatbot_padrao"]]:
    """
    Identifies stock tickers from the last message in the state and updates the 'ticker' key.
    """
    print('Entrei no identifica_metodo_analise')
    messages = state.get('messages', [])
    if not messages:
        return {"method_analysis": []}  # Retorna lista vazia se não houver mensagens
    # Invoca a chain para identificar os tickers
    resposta_metodo_analise = llm_identifica_metodo_analise.invoke({"messages": messages})
    
    
    
    if 'sem_analise' in resposta_metodo_analise.method_analysis :
        return Command(
        goto="chatbot_padrao",
        update={"mensagem_sistema": "Essa foi a pergunta feita pelo usuario:{messages}"}
    ) 
    return Command(
        goto="identifica_ticks",
        update={'method_analysis': resposta_metodo_analise.method_analysis})