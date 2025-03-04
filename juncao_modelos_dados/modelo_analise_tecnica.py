from tratando_dados import TratandoDadosIndicadores
from chat_bots import ChatAnaliseTecnica
from typing import List, Any, Iterator
from chat_bots import get_secret_key
from pydantic import SecretStr

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


class ModeloAnaliseTecnica:
    def __init__(
        self,
        query: str,
        ticker: str,
        periodo: str = "18Y",
        intervalo: str = "1mo",
        modelo_llm: str = "deepseek-r1-distill-llama-70b",
        stream: bool = True,
        api_secret: SecretStr | None = api_secret_groq,
    ) -> None:
        self.query = query
        self.ticker = ticker
        self.periodo = periodo
        self.intervalo = intervalo
        self.modelo_llm = modelo_llm
        self.stream = stream
        self.api_secret = api_secret

    def dados_indicadores_tecnicas(self) -> List[Any]:
        ind = TratandoDadosIndicadores(
            ticker=self.ticker, periodo=self.periodo, intervalo=self.intervalo
        )
        return ind.indicadores_data_loader()

    def chat_analise_tecnica(self) -> tuple[str | Iterator[str], List[Any]]:
        dados_tecnicas = self.dados_indicadores_tecnicas()
        response = ChatAnaliseTecnica(
            query=self.query,
            dados=dados_tecnicas,
            api_secret=self.api_secret,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        return response, dados_tecnicas
