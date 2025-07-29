import asyncio
import warnings
from typing import Dict, List, Optional

import httpx
from pydantic import SecretStr
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException

from ..chat_bots import ChatLimpaResposta
from ..coleta_dados import (
    DadosNoticiasBuscadorYahoo,
    DadosNoticiasGoogle,
    LinksExtractorBS4,
    LinksExtractorHtml,
)

warnings.filterwarnings("ignore")


class TratarDadosNoticiasComparacao:
    MAX_HTML_LENGTH = 7000
    TRUNCATE_LENGTH = 6500

    def __init__(
        self,
        tickers: List[str],
        options: webdriver.ChromeOptions | None,
        api_secret_groq: SecretStr | None,
        api_secret_serper: SecretStr | None,
        number_paginas: int = 1,
        numero_noticias: int = 10,
    ):
        self.tickers = tickers
        self.options = options
        self.number_paginas = number_paginas
        self.numero_noticias = numero_noticias
        self.api_secret_groq = api_secret_groq
        self.api_secret_serper = api_secret_serper

    async def get_news_yahoo(self, ticker: str) -> Dict[str, List[str]]:
        if self.options is None:
            self.options = webdriver.ChromeOptions()
            self.options.add_argument("--headless")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-features=NetworkService")
            self.options.add_argument("--window-size=1920x1080")
            self.options.add_argument("--disable-features=VizDisplayCompositor")
        dados_noticias = DadosNoticiasBuscadorYahoo(ticker, self.options)
        return await asyncio.to_thread(dados_noticias.get_news, self.number_paginas)

    async def get_news_google(self, ticker: str) -> List[Optional[str]]:
        clas_noticias_google = DadosNoticiasGoogle(
            acao=ticker, api_serper=self.api_secret_serper
        )
        dados_noticias_google = await asyncio.to_thread(clas_noticias_google.get_news)
        data_links_google: List[Optional[str]] = []

        for links in dados_noticias_google.get("news", []):
            if isinstance(links, dict) and "link" in links:
                data_links_google.append(links.get("link"))
            else:
                data_links_google.append(None)

        data_links_google = [link for link in data_links_google if link is not None]
        return data_links_google

    async def _process_news_content(self, link: Optional[str], ticker: str) -> str:
        """Processa o conteúdo HTML de uma notícia de forma assíncrona."""
        if link is None:
            return ""

        text_html = LinksExtractorHtml()
        dados_mark = await asyncio.to_thread(text_html.clean_text_html, link)

        if len(dados_mark) >= self.MAX_HTML_LENGTH:
            dados_mark = dados_mark[: self.TRUNCATE_LENGTH]

        return await ChatLimpaResposta(dados_mark, ticker, self.api_secret_groq)

    async def clean_chat_html(self, ticker: str) -> str:
        try:
            links = (await self.get_news_yahoo(ticker=ticker))["links"]
        except KeyError:
            links_optional = await self.get_news_google(ticker=ticker)
            links = [link for link in links_optional if link is not None]
        except SessionNotCreatedException:
            links_optional = await self.get_news_google(ticker=ticker)
            links = [link for link in links_optional if link is not None]

        if len(links) <= 5:
            print(
                f"Poucas noticias encontrada para o ticker {ticker} no Yahoo Finance. Buscando noticias no Google"
            )
            links_optional = await self.get_news_google(ticker=ticker)
            links = [link for link in links_optional if link is not None]

        links = [link for link in links if link is not None][: self.numero_noticias]
        dados_news = ""

        async def process_link(link):
            if link:
                dados_limpo = await self._process_news_content(link, ticker)
                return f"\nNew notice\n{dados_limpo}"
            return ""

        results = await asyncio.gather(*[process_link(link) for link in links])
        dados_news = "".join(results)

        return dados_news

    async def clean_chat_html_bs4(self, ticker: str) -> str:
        links_optional = await self.get_news_google(ticker=ticker)
        links = [link for link in links_optional if link is not None][:10]
        text_bs4 = LinksExtractorBS4()

        async def process_link(link: str) -> str:
            try:
                text = await asyncio.to_thread(text_bs4.clean_text_bs4, url=link)
                if isinstance(text, str):
                    if len(text) >= 900:
                        text = text[150:900]
                    return f"\nNew notice\n{'\n'.join(text.split('\n'))}"
            except httpx.HTTPError:
                pass
            return ""

        results = await asyncio.gather(*[process_link(link) for link in links])
        return "".join(results)

    async def tickes_news(self) -> str:
        """
        Coleta notícias de forma assíncrona para múltiplos tickers.

        Args:
            tickers: Lista de códigos de ações para coletar notícias

        Returns:
            str: String concatenada com todas as notícias por ticker
        """

        async def process_ticker(ticker: str) -> str:
            news_ticker = f"Noticias sobre {ticker}:\n"
            dados_news = await self.clean_chat_html_bs4(ticker=ticker)
            dados_news_clean = await ChatLimpaResposta(
                dados_news, ticker, self.api_secret_groq
            )
            if "\n</think>\n\n" in dados_news_clean:
                dados_news_clean = dados_news_clean.split("\n</think>\n\n")[1]
            return news_ticker + dados_news_clean

        results = await asyncio.gather(
            *[process_ticker(ticker) for ticker in self.tickers]
        )

        return "".join(results)
