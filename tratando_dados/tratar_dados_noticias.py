from coleta_dados import (
    DadosNoticiasBuscadorYahoo,
    LinksExtractorHtml,
    DadosNoticiasGoogle,
)
from selenium import webdriver
from typing import List, Dict, Any
from chat_bots import ChatLimpaResposta


class TratarDadosNoticias:
    MAX_HTML_LENGTH = 7000
    TRUNCATE_LENGTH = 6500

    def __init__(
        self,
        acao: str,
        options: webdriver.ChromeOptions,
        number_paginas: int = 1,
        numero_noticias: int = 10,
    ) -> None:
        self.acao = acao
        self.options = options
        self.number_paginas = number_paginas
        self.numero_noticias = numero_noticias

    def get_news_yahoo(self) -> Dict[str, List[str]]:
        dados_noticias = DadosNoticiasBuscadorYahoo(self.acao, self.options)
        return dados_noticias.get_news(self.number_paginas)

    def get_news_google(self) -> List[Any]:
        clas_noticias_google = DadosNoticiasGoogle(self.acao)
        dados_noticias_google = clas_noticias_google.get_news()

        if isinstance(dados_noticias_google, str):
            data_links_google = [
                links.get("link")
                for links in dados_noticias_google["news"]
                if isinstance(links, dict)
            ]
            return data_links_google
        else:
            return []

    def _process_news_content(self, link: str) -> str:
        """Processa o conteúdo HTML de uma notícia."""
        text_html = LinksExtractorHtml()

        dados_mark = text_html.clean_text_html(link)

        if len(dados_mark) >= self.MAX_HTML_LENGTH:
            dados_mark = dados_mark[: self.TRUNCATE_LENGTH]

        return ChatLimpaResposta(dados_mark, self.acao)

    def clean_chat_html(self) -> str:
        try:
            links = self.get_news_yahoo()["links"]
        except KeyError:
            links = self.get_news_google()

        if len(links) <= 5:
            print(
                f"Poucas noticias encontrada para o ticker {self.acao} no Yahoo Finance. Buscando noticias no Google"
            )
            links = self.get_news_google()

        links = links[: self.numero_noticias]

        dados_news = ""

        for link in links:
            dados_limpo = self._process_news_content(link)

            dados_news = dados_news + "\n New notice\n" + dados_limpo

        return dados_news
