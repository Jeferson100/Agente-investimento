from coleta_dados import LinksExtractorBS4


def test_text_bs4() -> None:
    extractor = LinksExtractorBS4()
    url = "https://www.infomoney.com.br/mercados/petrobras-o-alerta-acionado-sobre-investimentos-apesar-da-visao-positiva-para-petr4/"
    text = extractor.clean_text_bs4(url)
    assert text
    assert isinstance(text, str)
    assert len(text) > 0
