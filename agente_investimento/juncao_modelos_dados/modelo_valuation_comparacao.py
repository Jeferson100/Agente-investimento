import os
from typing import Dict, Iterator, List

from pydantic import SecretStr

from ..chat_bots import ChatValuationComparacao, get_secret_key
from ..tratando_dados import TratandoDadosValuationComparacao

try:
    api_secret_groq = get_secret_key("GROQ_API_KEY")
except KeyError as exc:
    raise ValueError("API key inválida ou não definida") from exc

MODEL_ID_VALUATION = os.getenv("MODEL_ID_VALUATION")

if MODEL_ID_VALUATION is None:
    print("Modelo valuation nao definido no .env!")


class ModeloValuationComparacao:
    def __init__(
        self,
        tickers: List[str],
        query: str,
        anos_projecao: int = 5,
        taxa_crescimento_perpetuidade: float = 0.014,
        calculo_necessidade_capital_de_giro: bool = False,
        stream: bool = False,
        modelo_llm: str = "deepseek-r1-distill-llama-70b",
        api_secret: SecretStr | None = api_secret_groq,
    ) -> None:
        self.query = query
        self.tickers = tickers
        self.anos_projecao = anos_projecao
        self.taxa_crescimento_perpetuidade = taxa_crescimento_perpetuidade
        self.calculo_necessidade_capital_de_giro = calculo_necessidade_capital_de_giro
        self.stream = stream
        self.modelo_llm = modelo_llm if MODEL_ID_VALUATION is not None else modelo_llm
        self.api_secret = api_secret

    def tratando_ticker(self) -> List[str]:
        acao = [f + ".SA" if not f.endswith(".SA") else f for f in self.tickers]
        return acao

    async def dados_valuation(self) -> Dict[str, str]:
        dados_valu = TratandoDadosValuationComparacao(
            tickers=self.tratando_ticker(),
            anos_projecao=5,
            taxa_crescimento_perpetuidade=self.taxa_crescimento_perpetuidade,
            calculo_necessidade_capital_de_giro=self.calculo_necessidade_capital_de_giro,
        )
        valuation_resposta = await dados_valu.dados_valuation()
        return valuation_resposta

    async def tratando_dados_valuation(self) -> tuple[Dict[str, str], Dict[str, str]]:
        dados_valuation = await self.dados_valuation()

        metodo_gordon = {}
        metodo_fluxo_caixa = {}

        for ticker, valores in dados_valuation.items():
            metodo_gordon[ticker] = valores[0]
            metodo_fluxo_caixa[ticker] = valores[1]

        return metodo_gordon, metodo_fluxo_caixa

    async def chat_valuation(self) -> str | Iterator[str]:
        metodo_gordon, metodo_fluxo_caixa = await self.tratando_dados_valuation()

        response = await ChatValuationComparacao(
            query=self.query,
            valuation_metodo_gordon=metodo_gordon,
            valuation_fluxo_caixa=metodo_fluxo_caixa,
            api_secret=self.api_secret,
            modelo_llm=self.modelo_llm,
            stream=self.stream,
        )
        if "</think>" in response:
            response = response.split("</think>")[1]  # type: ignore

        return response
