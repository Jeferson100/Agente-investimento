from juncao_modelos_dados import (
    ModeloValuation,
    ModeloFundamentos,
    ModeloSentimento,
    ModeloAnaliseTecnica,
)
import unittest
from unittest.mock import patch, MagicMock
import pytest
import os
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

        self.ticker = "PETR4"

    @patch("juncao_modelos_dados.ModeloValuation")
    def test_modelo_valuation(self, mock_modelo_valuation: MagicMock) -> None:
        mock_modelo_valuation.return_value = "Resposta do modelo de evaluation"

        query = f"Qual o valor de mercado da {self.ticker}"

        modelo_valuation_instance = ModeloValuation(
            query=query,
            ticker=self.ticker,
            api_secret=SecretStr(self.api_secret_groq or ""),
            stream=False,
        )

        result = modelo_valuation_instance.chat_valuation()

        self.assertIsNotNone(result)

        self.assertIsInstance(result, str)

    @patch("juncao_modelos_dados.ModeloFundamentos")
    def test_modelo_fundamentos(self, mock_modelo_fundamentos: MagicMock) -> None:
        mock_modelo_fundamentos.return_value = "Resposta do modelo de fundamentos"

        query = f"Como está a saúde financeira da {self.ticker}"

        modelo_fundamentos_instance = ModeloFundamentos(
            query=query,
            ticker=self.ticker,
            api_secret=SecretStr(self.api_secret_groq or ""),
            stream=False,
        )

        response, dados_fundamentalistas = (
            modelo_fundamentos_instance.chat_fundamentalistas()
        )

        self.assertIsNotNone(response)
        self.assertIsNotNone(dados_fundamentalistas)

        self.assertIsInstance(response, str)
        self.assertIsInstance(dados_fundamentalistas, list)

    @patch("juncao_modelos_dados.ModeloSentimento")
    def test_modelo_sentimento(self, mock_modelo_sentimento: MagicMock) -> None:
        mock_modelo_sentimento.return_value = "Resposta do modelo de sentimento"

        query = f"Qual o sentimento das notícias sobre a {self.ticker}"

        modelo_sentimento_instance = ModeloSentimento(
            query=query,
            acao=self.ticker,
            api_secret_groq=SecretStr(self.api_secret_groq or ""),
            api_secret_serper=SecretStr(self.api_key_serper or ""),
            stream=False,
        )

        response, dados_new = modelo_sentimento_instance.chat_sentimento()

        self.assertIsNotNone(response)
        self.assertIsNotNone(dados_new)

        self.assertIsInstance(response, str)
        self.assertIsInstance(dados_new, str)

    @patch("juncao_modelos_dados.ModeloAnaliseTecnica")
    def test_modelo_analise_tecnica(
        self, mock_modelo_analise_tecnica: MagicMock
    ) -> None:
        mock_modelo_analise_tecnica.return_value = (
            "Resposta do modelo de análise técnica"
        )

        query = f"Faça uma análise técnica da {self.ticker}"

        modelo_analise_tecnica_instance = ModeloAnaliseTecnica(
            query=query,
            ticker=self.ticker,
            api_secret=SecretStr(self.api_secret_groq or ""),
            stream=False,
        )

        response, dados_tecnicas = (
            modelo_analise_tecnica_instance.chat_analise_tecnica()
        )

        self.assertIsNotNone(response)
        self.assertIsNotNone(dados_tecnicas)

        self.assertIsInstance(response, str)
        self.assertIsInstance(dados_tecnicas, list)
