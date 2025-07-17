from typing import Iterator

from pydantic import SecretStr
from selenium import webdriver

from ..chat_bots import ChatSentimentoComparacao, get_secret_key
from ..tratando_dados import TratarDadosNoticiasComparacao

from agente_investimento.chat_bots import ChatSentimentoAsync, get_secret_key
from agente_investimento.tratando_dados import TratarDadosNoticiasComparacao

import os
from typing import List

import warnings

warnings.filterwarnings("ignore")


try:
    api_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc

MODEL_ID_SENTIMENTO = os.getenv("MODEL_ID_SENTIMENTO")

if MODEL_ID_SENTIMENTO is None:
    print("Modelo sentimento nao definido no .env!")


class ModeloSentimentoComparacao:
    def __init__(
        self,
        tickers: List[str],
        query: str,
        modelo_llm: str = "deepseek-r1-distill-llama-70b",
        stream: bool = False,
        api_secret_groq: SecretStr | None = api_groq,
        api_secret_serper: SecretStr | None = None,
    ) -> None:
        self.tickers = tickers
        self.query = query
        self.modelo_llm = modelo_llm if MODEL_ID_SENTIMENTO is not None else modelo_llm
        self.stream = stream
        self.api_secret_groq = api_secret_groq
        self.api_secret_serper = api_secret_serper

    def option(self) -> webdriver.ChromeOptions:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-features=NetworkService")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        return chrome_options

    async def dados_sentimento(self) -> str:
        
        dados_noticias = TratarDadosNoticiasComparacao(
            tickers=self.tickers,
            options=self.option(),
            api_secret_groq=self.api_secret_groq,
            api_secret_serper=self.api_secret_serper,
        )
        dados_new = await dados_noticias.tickes_news()
        return dados_new

    async def chat_sentimento(self) -> str | Iterator[str]:
        dados_new = await self.dados_sentimento()
        response = await ChatSentimentoComparacao(
            query=self.query,
            noticia=dados_new,
            api_secret=self.api_secret_groq,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        if "</think>" in response:
            response = response.split("</think>")[1]  # type: ignore
        return response