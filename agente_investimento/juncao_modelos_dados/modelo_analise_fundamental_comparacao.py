import os
from typing import Any, Iterator, List

from pydantic import SecretStr  # pylint: disable=import-error

from ..chat_bots import ChatFundamentalistasComparacaoAsync, get_secret_key
from ..tratando_dados import TratatandoDadosFundamentalistasComparacao

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


MODEL_FUNDAMENTAL = os.getenv("MODEL_ID_FUNDAMENTAL")

if MODEL_FUNDAMENTAL is None:
    print("Modelo fundamental nao definido no .env!")


class ModeloFundamentosComparacaoAsync:
    def __init__(
        self,
        tickers: List[str],
        query: str,
        modelo_llm: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        stream: bool = False,
        api_secret: SecretStr | None = api_secret_groq,
    ) -> None:
        self.query = query
        self.tickers = tickers
        self.stream = stream
        self.modelo_llm = modelo_llm if MODEL_FUNDAMENTAL is not None else modelo_llm
        self.api_secret = api_secret

    async def dados_fundamentalistas_comparacao(self) -> List[Any]:
        fudamentos_comparacao = TratatandoDadosFundamentalistasComparacao(
            self.tickers,
        )
        fudamentos_comparacao = await fudamentos_comparacao.coletando_dados_tickers()
        return fudamentos_comparacao  # type: ignore

    async def chat_fundamentalistas_comparacao(self) -> str | Iterator[str]:
        print("O modelo usado e o:", self.modelo_llm)
        dados_fundamentalistas = await self.dados_fundamentalistas_comparacao()
        response = await ChatFundamentalistasComparacaoAsync(
            query=self.query,
            dados=dados_fundamentalistas,
            api_secret=self.api_secret,
            modelo_llm=self.modelo_llm,  # type: ignore
            stream=self.stream,
        )
        if "</think>" in response:
            response = response.split("</think>")[1]  # type: ignore
        return response
