from coleta_dados import DadosNoticiasBuscadorYahoo
from selenium import webdriver


def options_headless() -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    return options

def test_get_news() -> None:
    result = DadosNoticiasBuscadorYahoo("PETR4", options_headless()).get_news(number_paginas=1)
    assert isinstance(result, dict)
    assert "links" in result
    assert "titulos" in result
    assert "fontes" in result
    assert "datas" in result
    assert len(result["links"]) > 0
    assert len(result["titulos"]) > 0
    assert len(result["fontes"]) > 0
    assert len(result["datas"]) > 0
