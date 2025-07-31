import os
import asyncio
import pandas as pd
import pytest
from pydantic import SecretStr
from agente_investimento import (
    TratatandoDadosFundamentalistasComparacao,
    TratarDadosNoticiasComparacao,
    TratandoDadosValuationComparacao,
    TratandoDadosIndicadoresComparacao
)
import asyncio

# Constants for tests
TICKERS = ["PETR4", "VALE3"]
API_KEY_SERPER = os.getenv("API_KEY_SERPER")
API_SECRET_GROQ = os.getenv("GROQ_API_KEY")

def test_tratando_dados_fundamentalistas() -> None:

    fund = TratatandoDadosFundamentalistasComparacao(TICKERS)
    dados_fund = asyncio.run(fund.coletando_dados_tickers()) 

    assert isinstance(dados_fund, list)

def test_tratando_dados_sent() -> None:
    if not API_KEY_SERPER or not API_SECRET_GROQ:
        pytest.skip("API keys (SERPER ou GROQ) não definidas. Pulando teste de sentimento.")

    dados_sent = TratarDadosNoticiasComparacao(tickers=TICKERS, 
                                                    api_secret_groq = SecretStr(API_SECRET_GROQ), 
                                                    api_secret_serper = SecretStr(API_KEY_SERPER),
                                                    options=None)
    df = asyncio.run(dados_sent.tickes_news())
    assert isinstance(df, str)
        
def test_tratando_dados_valuation() -> None:


    fund = TratandoDadosValuationComparacao(TICKERS)
    dados_fund = asyncio.run(fund.dados_valuation())

    assert isinstance(dados_fund, dict)

def test_tratando_dados_indicadores() -> None:


    fund = TratandoDadosIndicadoresComparacao(TICKERS)
    dados_fund = asyncio.run(fund.pegando_indicadores_comparacao())

    assert isinstance(dados_fund, list)

    