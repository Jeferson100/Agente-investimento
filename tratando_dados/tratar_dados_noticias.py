from coleta_dados import (
    DadosNoticiasBuscadorYahoo,
    LinksExtractorHtml,
    DadosNoticiasGoogle,
    LinksExtractorBS4,
)
from selenium import webdriver
from typing import List, Dict, Optional
from chat_bots import ChatLimpaResposta
from pydantic import SecretStr
from selenium.common.exceptions import SessionNotCreatedException
import httpx


class TratarDadosNoticias:
    MAX_HTML_LENGTH = 7000
    TRUNCATE_LENGTH = 6500

    def __init__(
        self,
        acao: str,
        options: webdriver.ChromeOptions,
        api_secret_groq: SecretStr | None,
        api_secret_serper: SecretStr | None,
        number_paginas: int = 1,
        numero_noticias: int = 10,
    ):
        self.acao = acao
        self.options = options
        self.number_paginas = number_paginas
        self.numero_noticias = numero_noticias
        self.api_secret_groq = api_secret_groq
        self.api_secret_serper = api_secret_serper

    def get_news_yahoo(self) -> Dict[str, List[str]]:
        dados_noticias = DadosNoticiasBuscadorYahoo(self.acao, self.options)
        return dados_noticias.get_news(self.number_paginas)

    def get_news_google(self) -> List[Optional[str]]:
        clas_noticias_google = DadosNoticiasGoogle(
            acao=self.acao, api_serper=self.api_secret_serper
        )
        dados_noticias_google = clas_noticias_google.get_news()
        data_links_google: List[Optional[str]] = []
        for links in dados_noticias_google.get("news", []):
            if isinstance(links, dict) and "link" in links:
                data_links_google.append(links.get("link"))
            else:
                data_links_google.append(None)
        data_links_google = [link for link in data_links_google if link is not None]

        return data_links_google

    def _process_news_content(self, link: Optional[str]) -> str:
        """Processa o conteúdo HTML de uma notícia."""
        if link is None:
            return ""

        text_html = LinksExtractorHtml()

        dados_mark = text_html.clean_text_html(link)

        if len(dados_mark) >= self.MAX_HTML_LENGTH:
            dados_mark = dados_mark[: self.TRUNCATE_LENGTH]

        return ChatLimpaResposta(dados_mark, self.acao, self.api_secret_groq)

    def clean_chat_html(self) -> str:
        try:
            links = self.get_news_yahoo()["links"]
        except KeyError:
            links_optional = self.get_news_google()
            links = [link for link in links_optional if link is not None]
        except SessionNotCreatedException:
            links_optional = self.get_news_google()
            links = [link for link in links_optional if link is not None]

        if len(links) <= 5:
            print(
                f"Poucas noticias encontrada para o ticker {self.acao} no Yahoo Finance. Buscando noticias no Google"
            )
            links_optional = self.get_news_google()
            links = [link for link in links_optional if link is not None]

        links = [link for link in links if link is not None][: self.numero_noticias]

        dados_news = ""

        for link in links:
            if link:
                dados_limpo = self._process_news_content(link)

                dados_news = dados_news + "\n New notice\n" + dados_limpo

        return dados_news

    def clean_chat_html_bs4(self) -> str:
        try:
            links = self.get_news_yahoo()["links"]
        except KeyError:
            links_optional = self.get_news_google()
            links = [link for link in links_optional if link is not None]
        except SessionNotCreatedException:
            links_optional = self.get_news_google()
            links = [link for link in links_optional if link is not None]

        if len(links) <= 5:
            print(
                f"Poucas noticias encontrada para o ticker {self.acao} no Yahoo Finance. Buscando noticias no Google"
            )
            links_optional = self.get_news_google()
            links = [link for link in links_optional if link is not None]

        links = [link for link in links if link is not None][:10]
        dados_news = ""
        text_bs4 = LinksExtractorBS4()
        for link in links:
            try:
                text = text_bs4.clean_text_bs4(url=link)
                if isinstance(text, str):
                    if len(text) >= 900:
                        text = text[150:900]
                    dados_news = (
                        dados_news + "\nNew notice\n" + "\n".join(text.split("\n"))
                    )
            except httpx.HTTPError:
                pass

        return dados_news
