from tratando_dados import (
    TratandoDadosIndicadores,
    TratandoDadosValuation,
    TratarDadosNoticias,
    tratando_dados_fundamentalistas,
)
import pytest
from pydantic import SecretStr
from selenium import webdriver
import pandas as pd
import os

api_key_serper = os.getenv("API_KEY_SERPER")
api_secret_groq = os.getenv("API_SECRET_GROQ")


## testes tratando dados fundamentalistas
def test_tratando_dados_fundamentalistas() -> None:
    dados_fund = tratando_dados_fundamentalistas("BBDC3")
    assert isinstance(dados_fund, list)


## testes tratando dados indicadores


def test_tratando_dados_indicadores_coleta() -> None:
    dados_indicadores = TratandoDadosIndicadores("PETR4")
    df = dados_indicadores.coletando_indicadores()
    assert isinstance(df, pd.DataFrame)


def test_tratando_dados_indicadores_tratando_indicadores() -> None:
    dados_indicadores = TratandoDadosIndicadores("PETR4")
    df = dados_indicadores.tratando_indicadores()
    assert isinstance(df, pd.DataFrame)


def test_tratando_dados_indicadores_indicadores_data_loader() -> None:
    dados_indicadores = TratandoDadosIndicadores("PETR4")
    df = dados_indicadores.indicadores_data_loader()
    assert isinstance(df, list)


## testes tratando_valuations


@pytest.fixture
def tratando_dados_valuation() -> TratandoDadosValuation:
    return TratandoDadosValuation("PETR4")


def tratando_dados_valuations_preco_atual() -> None:
    df = tratando_dados_valuation().preco_atual()
    assert isinstance(df, float)


def tratando_dados_valuation_indicadores_financeiros() -> None:
    df = tratando_dados_valuation().indicadores_financeiros()
    assert isinstance(df, pd.DataFrame)


def tratando_dados_valuation_fluxo_caixa_descontado() -> None:
    fluxo_caixa, valuation_preco = (
        tratando_dados_valuation().valuation_fluxo_caixa_descontado()
    )
    assert isinstance(fluxo_caixa, pd.DataFrame)
    assert isinstance(valuation_preco, dict)


def tratando_dados_valuation_metodo_gordon() -> None:
    df = tratando_dados_valuation().valuation_metodo_gordon()
    assert isinstance(df, pd.DataFrame)


def tratando_dados_markdow_metodo_gordon() -> None:
    markdow_gordon, valuation_acao_gordon = (
        tratando_dados_valuation().markdow_metodo_gordon()
    )
    assert isinstance(markdow_gordon, str)
    assert isinstance(valuation_acao_gordon, str)


def tratando_dados_markdow_fluxo_caixa_descontado() -> None:
    markdow_fluxo, valuation_acao_fluxo = (
        tratando_dados_valuation().markdow_fluxo_caixa_descontado()
    )
    assert isinstance(markdow_fluxo, str)
    assert isinstance(valuation_acao_fluxo, str)


def tratando_dados_valuation_markdow_indicadores_financeiros() -> None:
    markdow_indicadores = tratando_dados_valuation().markdow_indicadores_financeiros()
    assert isinstance(markdow_indicadores, str)


def tratando_dados_valuation_dados_valuation() -> None:
    markdow_gordon, markdow_fluxo, markdow_preco, markdow_indicadores = (
        tratando_dados_valuation().dados_valuation()
    )
    assert isinstance(markdow_gordon, str)
    assert isinstance(markdow_fluxo, str)
    assert isinstance(markdow_preco, str)
    assert isinstance(markdow_indicadores, str)


## testes tratando dados noticias


def options_headless() -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    return options


def tratando_dados_noticias_clean_chat_html_bs4() -> None:
    if api_key_serper is None:
        raise ValueError("API key serper inválida ou não definida")
    if api_secret_groq is None:
        raise ValueError("API secret groq inválida ou não definida")
    trat_noticias = TratarDadosNoticias(
        acao="PETR4",
        options=options_headless(),
        api_secret_groq=SecretStr(api_secret_groq),
        api_secret_serper=SecretStr(api_key_serper),
    )
    df = trat_noticias.clean_chat_html_bs4()
    assert isinstance(df, str)
