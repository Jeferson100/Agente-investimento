from typing import Any, Iterator, List

from pydantic import SecretStr

from ..chat_bots import ChatAnaliseTecnicaComparacao, get_secret_key
from ..tratando_dados import TratandoDadosIndicadoresComparacao

import os

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc

MODEL_ID_TECNICAL = os.getenv("MODEL_ID_TECNICAL")

if MODEL_ID_TECNICAL is None:
    print("Modelo tecnica nao definido no .env!")


class ModeloAnaliseTecnicaComparacao:
    def __init__(
        self,
        query: str,
        tickers: List[str],
        periodo: str = "18Y",
        intervalo: str = "1mo",
        modelo_llm: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        stream: bool = False,
        api_secret: SecretStr | None = api_secret_groq,
    ) -> None:
        self.query = query
        self.tickers = tickers
        self.periodo = periodo
        self.intervalo = intervalo
        self.modelo_llm = modelo_llm if MODEL_ID_TECNICAL is not None else modelo_llm
        self.stream = stream
        self.api_secret = api_secret

    async def dados_indicadores_tecnicas(self) -> List[Any]:
        ind = TratandoDadosIndicadoresComparacao(
            tickers=self.tickers, periodo=self.periodo, intervalo=self.intervalo
        )
        return await ind.pegando_indicadores_comparacao()

    async def chat_analise_tecnica_comparacao(self) -> str | Iterator[str]:
        dados_tecnicas = await self.dados_indicadores_tecnicas()
        response = await ChatAnaliseTecnicaComparacao(
            query=self.query,
            dados=dados_tecnicas,
            api_secret=self.api_secret,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        if "</think>" in response:
            response = response.split("</think>")[1]  # type: ignore
        return response