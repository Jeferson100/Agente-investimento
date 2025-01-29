from coleta_dados import DadosNoticiasBuscadorYahoo, LinksExtractorHtml, DadosNoticiasGoogle
from selenium import webdriver
from typing import List, Dict
from chat_bots import ChatLimpaResposta


class TratarDadosNoticias:

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
    
    def get_news_google(self) -> List:
        clas_noticias_google = DadosNoticiasGoogle(self.acao)
        dados_noticias_google = clas_noticias_google.get_news()
    
        data_links_google = [links.get('link') for links in dados_noticias_google['news'] if isinstance(links, dict)]
        
        return data_links_google

    def clean_chat_html(self) -> str:
        text_html = LinksExtractorHtml()
        links = self.get_news_yahoo()["links"]
        links = links[: self.numero_noticias]
        dados_news = ""
        for link in links:
            dados_mark = text_html.clean_text_html(link)

            if len(dados_mark) >= 7000:
                dados_mark = dados_mark[:6500]

            dados_limpo = ChatLimpaResposta(dados_mark, self.acao)

            dados_news = dados_news + "\n New notice\n" + dados_limpo

        return dados_news
