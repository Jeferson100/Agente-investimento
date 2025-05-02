from typing import Iterator

from pydantic import SecretStr

from ..chat_bots import ChatValuationAsync, get_secret_key
from ..tratando_dados import TratandoDadosValuation

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc


class ModeloValuationAsync:
    def __init__(
        self,
        ticker: str,
        query: str,
        anos_projecao: int = 5,
        taxa_crescimento_perpetuidade: float = 0.014,
        calculo_necessidade_capital_de_giro: bool = False,
        stream: bool = False,
        modelo_llm: str = "meta-llama/llama-4-scout-17b-16e-instruct",
        api_secret: SecretStr | None = api_secret_groq,
    ) -> None:
        self.query = query
        self.ticker = ticker
        self.anos_projecao = anos_projecao
        self.taxa_crescimento_perpetuidade = taxa_crescimento_perpetuidade
        self.calculo_necessidade_capital_de_giro = calculo_necessidade_capital_de_giro
        self.stream = stream
        self.modelo_llm = modelo_llm
        self.api_secret = api_secret

    def tratando_ticker(self) -> str:
        if ".SA" in self.ticker:
            acao = self.ticker
        else:
            acao = f"{self.ticker}.SA"
        return acao

    def dados_valuation(self) -> tuple[str, str, str, str]:
        dados_valu = TratandoDadosValuation(
            ticker=self.tratando_ticker(),
            anos_projecao=5,
            taxa_crescimento_perpetuidade=self.taxa_crescimento_perpetuidade,
            calculo_necessidade_capital_de_giro=self.calculo_necessidade_capital_de_giro,
        )
        markdow_gordon, markdow_fluxo, markdow_preco, markdow_indicadores = (
            dados_valu.dados_valuation()
        )
        return markdow_gordon, markdow_fluxo, markdow_preco, markdow_indicadores

    async def chat_valuation(self) -> str | Iterator[str]:
        markdow_gordon, markdow_fluxo, markdow_preco, markdow_indicadores = (
            self.dados_valuation()
        )

        response = await ChatValuationAsync(
            query=self.query,
            precos_atual_valuations=markdow_preco,
            indicadores_valuation_fluxo=markdow_indicadores,
            valuation_metodo_gordon=markdow_gordon,
            valuation_fluxo_caixa=markdow_fluxo,
            api_secret=self.api_secret,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        if "</think>" in response:
            response = response.split("</think>")[1]  # type: ignore

        return response
