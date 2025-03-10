from tratando_dados import TratarDadosNoticias
from selenium import webdriver
from chat_bots import ChatSentimento
from typing import Iterator
from chat_bots import get_secret_key
from pydantic import SecretStr

try:
    api_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


class ModeloSentimento:
    def __init__(
        self,
        query: str,
        acao: str,
        modelo_llm: str = "deepseek-r1-distill-llama-70b",
        stream: bool = True,
        api_secret_groq: SecretStr | None = api_groq,
        api_secret_serper: SecretStr | None = None,
    ) -> None:
        self.acao = acao
        self.modelo_llm = modelo_llm
        self.query = query
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

    def dados_sentimento(self) -> str:
        dados_noticias = TratarDadosNoticias(
            acao=self.acao,
            options=self.option(),
            api_secret_groq=self.api_secret_groq,
            api_secret_serper=self.api_secret_serper,
        )
        dados_new = dados_noticias.clean_chat_html_bs4()
        return dados_new

    def chat_sentimento(self) -> tuple[str | Iterator[str], str]:
        dados_new = self.dados_sentimento()
        response = ChatSentimento(
            query=self.query,
            noticia=dados_new,
            api_secret=self.api_secret_groq,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        return response, dados_new
