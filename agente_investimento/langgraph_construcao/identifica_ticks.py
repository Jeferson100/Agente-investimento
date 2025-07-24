import pandas as pd
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from .type_state import State
from ..chat_bots import get_llm
from typing import Final

from dotenv import load_dotenv
import os

load_dotenv()

DEFAULT_MODEL: Final = "llama3-70b-8192"

MODEL_ID_IDENTIFICA_TICKER: str = os.getenv("MODEL_ID_IDENTIFICA_TICKER", DEFAULT_MODEL)

llm = get_llm(
    model=MODEL_ID_IDENTIFICA_TICKER,
)

# 2. Carregamento dos dados das empresas
empresas_df = pd.read_csv(
    "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv",
    encoding="utf-8",
)

# 3. Criação da lista de tickers para o prompt
empresas_tickers = "\n".join(
    [f"{empresa} ({ticker})" for empresa, ticker in zip(empresas_df['Empresa'], empresas_df['tic'])]
)

# 4. Template de Prompt Aprimorado
template = """
You are an expert investment analysis agent. Your task is to identify all relevant stock tickers from the user's query.

Here is a list of available Brazilian companies and their corresponding tickers:
---
{empresas_tickers}
---

Based on the list above, identify ALL stock tickers mentioned in the user's query below.

Rules for ticker identification:
- Brazilian tickers usually end with a number (e.g., 3, 4, 11).
- If the user mentions only the company name (e.g., "Petrobras"), find the correct ticker from the list.
- If a company has multiple tickers, prefer the most liquid one, which typically ends in 3 (common stock) or 4 (preferred stock).
- You must return every ticker you identify. For example, if the user asks about "Petrobras e Vale", you must return both 'PETR4' and 'VALE3'.
- If no relevant tickers are found in the query, return an empty list.

User Query: "{messages}"
"""

prompt = ChatPromptTemplate.from_template(template)

# 5. Modelo Pydantic mais claro e específico
class Tickers(BaseModel):
    """A list of identified stock tickers."""
    tickers: List[str] = Field(
        ...,
        description="A list of stock tickers identified from the user's message. For example: ['PETR4', 'VALE3']"
    )

# 6. Chain com o LLM e o output estruturado
llm_identifica_ticker = prompt | llm.with_structured_output(Tickers)

# 7. Função para o nó do grafo, agora mais robusta
def identifica_ticks(state: State): #Command[Literal["chatinput", "roteador_analise"]]:
    """
    Identifies stock tickers from the last message in the state and updates the 'ticker' key.
    """
    print('Entrei identificacao ticks')
    messages = state.get('messages', [])

    if not messages:
        return {"ticker": []}  # Retorna lista vazia se não houver mensagens
    

    # Invoca a chain para identificar os tickers
    resposta_ticker = llm_identifica_ticker.invoke({
        "messages": messages,
        "empresas_tickers": empresas_tickers
    })
    return {'ticker': resposta_ticker.tickers} 

