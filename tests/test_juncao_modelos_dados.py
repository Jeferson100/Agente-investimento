import asyncio
import os
import unittest
from unittest.mock import MagicMock, patch

import pytest
from agente_investimento import (
    ModeloAnaliseTecnicaComparacao,
    ModeloFundamentosComparacaoAsync,
    ModeloSentimentoComparacao,
    ModeloValuationComparacao,
)
from pydantic import SecretStr


class TestJuncaoModelosDados(unittest.TestCase):
    def setUp(self) -> None:
        """Configuração inicial para os testes."""
        self.api_key_serper = os.getenv("API_KEY_SERPER")
        self.api_secret_groq = os.getenv("GROQ_API_KEY")

        # Verificar se as chaves de API estão disponíveis
        if not self.api_secret_groq:
            pytest.skip(
                "API secret groq não definida. Configure a variável de ambiente GROQ_API_KEY"
            )

        self.ticker = ["PETR4", "VALE3"]

    @patch("agente_investimento.ModeloValuationComparacao")
    def test_modelo_valuation(self, mock_modelo_valuation: MagicMock) -> None:
        mock_modelo_valuation.return_value = "Resposta do modelo de evaluation"

        query = f"Qual o valor de mercado da {self.ticker}"

        modelo_valuation_instance = ModeloValuationComparacao(
            query=query,
            tickers=self.ticker,
            api_secret=SecretStr(self.api_secret_groq or ""),
            stream=False,
        )

        result = asyncio.run(modelo_valuation_instance.chat_valuation())

        self.assertIsNotNone(result)

        self.assertIsInstance(result, str)

    @patch("agente_investimento.ModeloFundamentosComparacaoAsync")
    def test_modelo_fundamentos(self, mock_modelo_fundamentos: MagicMock) -> None:
        mock_modelo_fundamentos.return_value = "Resposta do modelo de fundamentos"

        query = f"Como está a saúde financeira da {self.ticker}"

        modelo_fundamentos_instance = ModeloFundamentosComparacaoAsync(
            query=query,
            tickers=self.ticker,
            api_secret=SecretStr(self.api_secret_groq or ""),
            stream=False,
        )

        response = asyncio.run(
            modelo_fundamentos_instance.chat_fundamentalistas_comparacao()
        )

        self.assertIsNotNone(response)

        self.assertIsInstance(response, str)
    

    @patch("agente_investimento.ModeloSentimentoComparacao")
    def test_modelo_sentimento(self, mock_modelo_sentimento: MagicMock) -> None:
        mock_modelo_sentimento.return_value = "Resposta do modelo de sentimento"

        query = f"Qual o sentimento das notícias sobre a {self.ticker}"

        modelo_sentimento_instance = ModeloSentimentoComparacao(
            query=query,
            tickers=self.ticker,
            api_secret_groq=SecretStr(self.api_secret_groq or ""),
            api_secret_serper=SecretStr(self.api_key_serper or ""),
            stream=False,
        )

        response = asyncio.run(modelo_sentimento_instance.chat_sentimento())

        self.assertIsNotNone(response)


        self.assertIsInstance(response, str)
      

    @patch("agente_investimento.ModeloAnaliseTecnicaComparacao")
    def test_modelo_analise_tecnica(
        self, mock_modelo_analise_tecnica: MagicMock
    ) -> None:
        mock_modelo_analise_tecnica.return_value = (
            "Resposta do modelo de análise técnica"
        )

        query = f"Faça uma análise técnica da {self.ticker}"

        modelo_analise_tecnica_instance = ModeloAnaliseTecnicaComparacao(
            query=query,
            tickers=self.ticker,
            api_secret=SecretStr(self.api_secret_groq or ""),
            stream=False,
        )

        response = asyncio.run(
            modelo_analise_tecnica_instance.chat_analise_tecnica_comparacao()
        )

        self.assertIsNotNone(response)


        self.assertIsInstance(response, str)

