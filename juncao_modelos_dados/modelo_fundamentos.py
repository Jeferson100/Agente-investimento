from tratando_dados import tratando_dados_fundamentalistas
from chat_bots import ChatFundamentalistas
from typing import Iterator, List, Any
from chat_bots import get_secret_key
from pydantic import SecretStr

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


class ModeloFundamentos:
    def __init__(
        self,
        query: str,
        ticker: str,
        stream: bool = True,
        modelo_llm: str = "deepseek-r1-distill-llama-70b",
        dados_inicio: str = "2021-01-01",
        api_secret: SecretStr | None = api_secret_groq,
    ) -> None:
        self.ticker = ticker
        self.query = query
        self.stream = stream
        self.modelo_llm = modelo_llm
        self.dados_inicio = dados_inicio
        self.api_secret = api_secret

    def dados_fundamentalistas(self) -> List[Any]:
        return tratando_dados_fundamentalistas(self.ticker, self.dados_inicio)

    def chat_fundamentalistas(self) -> tuple[str | Iterator[str], List[Any]]:
        dados_fundamentalistas = self.dados_fundamentalistas()
        response = ChatFundamentalistas(
            query=self.query,
            dados=dados_fundamentalistas,
            api_secret=self.api_secret,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        return response, dados_fundamentalistas
