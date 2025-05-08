from typing import Any, Iterator, List, Optional

from pydantic import SecretStr
from ..chat_bots import ChatFundamentalistasComparacaoAsync, get_secret_key
from ..tratando_dados import TratatandoDadosFundamentalistasComparacao

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


class ModeloFundamentosComparacaoAsync:
    def __init__(
        self,
        tickers: List[str],
        query: str,
        stream: bool = False,
        modelo_llm: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        api_secret: SecretStr | None = api_secret_groq,
    ) -> None:
        self.query = query
        self.tickers = tickers
        self.stream = stream
        self.modelo_llm = modelo_llm
        self.api_secret = api_secret
    
    async def dados_fundamentalistas_comparacao(self) -> List[Any]:
        fudamentos_comparacao = TratatandoDadosFundamentalistasComparacao(
        self.tickers,
        )
        fudamentos_comparacao = await fudamentos_comparacao.coletando_dados_tickers()
        return fudamentos_comparacao
    
    async def chat_fundamentalistas_comparacao(self) -> str | Iterator[str]:
        dados_fundamentalistas = await self.dados_fundamentalistas_comparacao()
        response = await ChatFundamentalistasComparacaoAsync(
            query=self.query,
            dados=dados_fundamentalistas,
            api_secret=self.api_secret,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        if "</think>" in response:
            response = response.split("</think>")[1]  # type: ignore
        return response


