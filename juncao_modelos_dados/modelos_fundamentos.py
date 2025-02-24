from tratando_dados import tratando_dados_fundamentalistas
from chat_bots import ChatFundamentalistas
from typing import Iterator
from typing import List, Any


class ModeloFundamentos:
    def __init__(
        self,
        query: str,
        ticker: str,
        stream: bool = True,
        modelo_llm: str = "deepseek-r1-distill-llama-70b",
        dados_inicio: str = "2020-01-01",
    ) -> None:
        self.ticker = ticker
        self.query = query
        self.stream = stream
        self.modelo_llm = modelo_llm
        self.dados_inicio = dados_inicio

    def dados_fundamentalistas(self) -> List[Any]:
        return tratando_dados_fundamentalistas(self.ticker, self.dados_inicio)

    def chat_fundamentalistas(self) -> str | Iterator[str]:
        response = ChatFundamentalistas(
            query=self.query,
            dados=self.dados_fundamentalistas(),
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        return response
