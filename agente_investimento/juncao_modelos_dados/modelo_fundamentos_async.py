from typing import Any, Iterator, List

from pydantic import SecretStr

from ..chat_bots import ChatFundamentalistasAsync, get_secret_key
from ..tratando_dados import tratando_dados_fundamentalistas
import os

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc

MODEL_FUNDAMENTAL = os.getenv("MODEL_ID_FUNDAMENTAL")

if MODEL_FUNDAMENTAL is None:
    print("Modelo fundamental nao definido no .env!")


class ModeloFundamentosAsync:
    def __init__(
        self,
        ticker: str,
        query: str,
        stream: bool = False,
        modelo_llm: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        dados_inicio: str = "2022-06-01",
        api_secret: SecretStr | None = api_secret_groq,
    ) -> None:
        self.query = query
        self.ticker = ticker
        self.stream = stream
        self.modelo_llm = modelo_llm if MODEL_FUNDAMENTAL is not None else modelo_llm
        self.dados_inicio = dados_inicio
        self.api_secret = api_secret

    async def dados_fundamentalistas(self) -> List[Any]:
        return await tratando_dados_fundamentalistas(self.ticker, self.dados_inicio)

    async def chat_fundamentalistas(self) -> str | Iterator[str]:
        dados_fundamentalistas = await self.dados_fundamentalistas()
        response = await ChatFundamentalistasAsync(
            query=self.query,
            dados=dados_fundamentalistas,
            api_secret=self.api_secret,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        if "</think>" in response:
            response = response.split("</think>")[1]  # type: ignore
        return response
