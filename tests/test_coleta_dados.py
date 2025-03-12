import pandas as pd
from coleta_dados import (
    DadosFundamentalistas,
    DadosIndicadoresTecnicos,
    DadosNoticiasGoogle,
    DadosNoticiasBuscadorYahoo,
    LinksExtractorBS4,
)
from pydantic import SecretStr
from selenium import webdriver
import os

api_key_serper = os.getenv("API_KEY_SERPER")


# Test indicadores
def test_tratando_ticker() -> None:
    obj = DadosIndicadoresTecnicos("PETR4")
    assert obj.tratando_ticker() == "PETR4.SA"


def test_cotacoes_ticker() -> None:
    obj = DadosIndicadoresTecnicos("PETR4")
    df = obj.cotacoes_ticker()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert set(["Open", "High", "Low", "Close", "Volume"]).issubset(df.columns)


def test_indicadores_tecnicos() -> None:
    obj = DadosIndicadoresTecnicos("PETR4")
    df = obj.cotacoes_ticker()
    indicadores = obj.indicadores_tecnicos(df)
    assert isinstance(indicadores, dict)
    assert all(
        isinstance(indicadores[key], pd.Series)
        or isinstance(indicadores[key], pd.DataFrame)
        for key in indicadores
    )


def test_pegando_indicadores_tecnicos() -> None:
    obj = DadosIndicadoresTecnicos("PETR4")
    df = obj.pegando_indicadores_tecnicos()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] <= 30


# Test fundamentais
def test_dados_dre() -> None:
    df = DadosFundamentalistas("PETR4").dados_dre()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_capex() -> None:
    df = DadosFundamentalistas("PETR4").dados_capex()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_fluxo_caixa() -> None:
    df = DadosFundamentalistas("PETR4").dados_fluxo_caixa()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_precos_relativos() -> None:
    df = DadosFundamentalistas("PETR4").dados_precos_relativos()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_resumo_balanco() -> None:
    df = DadosFundamentalistas("PETR4").dados_resumo_balanco()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_retornos_margens() -> None:
    df = DadosFundamentalistas("PETR4").dados_retornos_margens()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


# teste coleta notcias google


def test_get_news_google() -> None:
    if api_key_serper is None:
        raise ValueError("API key serper inválida ou não definida")

    obj = DadosNoticiasGoogle("PETR4", api_serper=SecretStr(api_key_serper))
    noticias = obj.get_news()

    assert isinstance(noticias, dict)
    assert "news" in noticias
    assert isinstance(noticias["news"], list)
    assert len(noticias["news"]) > 0
    assert all("title" in noticia and "link" in noticia for noticia in noticias["news"])


# teste dados noticias yahoo


def options_headless() -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    return options


def test_get_news_yahoo() -> None:
    result = DadosNoticiasBuscadorYahoo("PETR4", options_headless()).get_news(
        number_paginas=2
    )
    assert isinstance(result, dict)
    assert "links" in result
    assert "titulos" in result
    assert "fontes" in result
    assert "datas" in result
    assert len(result["links"]) > 0
    assert len(result["titulos"]) > 0
    assert len(result["fontes"]) > 0
    assert len(result["datas"]) > 0


def test_text_bs4() -> None:
    extractor = LinksExtractorBS4()
    url = "https://www.infomoney.com.br/mercados/petrobras-o-alerta-acionado-sobre-investimentos-apesar-da-visao-positiva-para-petr4/"
    text = extractor.clean_text_bs4(url)
    assert text
    assert isinstance(text, str)
    assert len(text) > 0
