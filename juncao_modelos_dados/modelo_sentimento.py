from tratando_dados import TratarDadosNoticias
from selenium import webdriver
from chat_bots import ChatSentimento
from typing import Iterator


class ModeloSentimento:
    def __init__(
        self,
        query: str,
        acao: str,
        modelo_llm: str = "deepseek-r1-distill-llama-70b",
        stream: bool = True,
    ) -> None:
        self.acao = acao
        self.modelo_llm = modelo_llm
        self.query = query
        self.stream = stream

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
        dados_noticias = TratarDadosNoticias(self.acao, self.option())
        dados_new = dados_noticias.clean_chat_html()
        return dados_new

    def chat_sentimento(self) -> str | Iterator[str]:
        response = ChatSentimento(
            query=self.query,
            noticia=self.dados_sentimento(),
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        return response
