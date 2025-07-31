import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from langchain.schema import HumanMessage
from langgraph.types import Command
from typing import Dict, Any

from agente_investimento.utils.processa_analises import (
    process_fundamental,
    process_technical,
    process_valuation,
    process_sentimento,
    analise_investimento
)


class TestProcessaAnalises(unittest.TestCase):
    def setUp(self) -> None:
        """Configuração inicial para os testes."""
        self.mock_state: Dict[str, Any] = {
            "ticker": ["PETR4", "VALE3"],
            "messages": [HumanMessage(content="Analise fundamentalista")],
            "dados_input": ""
        }

    @patch('agente_investimento.utils.processa_analises.ModeloFundamentosComparacaoAsync')
    async def test_process_fundamental_success(self, mock_modelo_class: MagicMock) -> None:
        """Testa processamento de análise fundamentalista com sucesso."""
        mock_modelo = AsyncMock()
        mock_modelo.chat_fundamentalistas_comparacao.return_value = "Análise fundamentalista concluída"
        mock_modelo_class.return_value = mock_modelo

        result = await process_fundamental(self.mock_state)

        # Verificar se o modelo foi instanciado corretamente
        mock_modelo_class.assert_called_once_with(
            tickers=["PETR4", "VALE3"],
            query=HumanMessage(content="Analise fundamentalista")
        )
        
        # Verificar se o método foi chamado
        mock_modelo.chat_fundamentalistas_comparacao.assert_called_once()
        
        # Verificar o resultado
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "supervisor")
        self.assertIsNotNone(result.update)
        self.assertIn("dados_input", result.update)
        self.assertIsInstance(result.update["dados_input"], list)
        self.assertIsInstance(result.update["dados_input"][0], HumanMessage)
        self.assertEqual(result.update["dados_input"][0].content, "Análise fundamentalista concluída")
        self.assertEqual(result.update["dados_input"][0].name, "fundamental")

    @patch('agente_investimento.utils.processa_analises.ModeloFundamentosComparacaoAsync')
    async def test_process_fundamental_with_existing_data(self, mock_modelo_class: MagicMock) -> None:
        """Testa processamento com dados existentes."""
        state_with_data = self.mock_state.copy()
        state_with_data["dados_input"] = "Dados anteriores"
        
        mock_modelo = AsyncMock()
        mock_modelo.chat_fundamentalistas_comparacao.return_value = "Nova análise"
        mock_modelo_class.return_value = mock_modelo

        result = await process_fundamental(state_with_data)

        expected_content = "Dados anteriores\nNova análise"
        self.assertIsNotNone(result.update)
        self.assertEqual(result.update["dados_input"][0].content, expected_content)

    @patch('agente_investimento.utils.processa_analises.ModeloAnaliseTecnicaComparacao')
    async def test_process_technical_success(self, mock_modelo_class: MagicMock) -> None:
        """Testa processamento de análise técnica com sucesso."""
        mock_modelo = AsyncMock()
        mock_modelo.chat_analise_tecnica_comparacao.return_value = "Análise técnica concluída"
        mock_modelo_class.return_value = mock_modelo

        result = await process_technical(self.mock_state)

        # Verificar se o modelo foi instanciado corretamente
        mock_modelo_class.assert_called_once_with(
            tickers=["PETR4", "VALE3"],
            query=HumanMessage(content="Analise fundamentalista"),
            periodo="3Y",
            intervalo="1mo"
        )
        
        # Verificar se o método foi chamado
        mock_modelo.chat_analise_tecnica_comparacao.assert_called_once()
        
        # Verificar o resultado
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "supervisor")
        self.assertIsNotNone(result.update)
        self.assertIn("dados_input", result.update)
        self.assertEqual(result.update["dados_input"][0].content, "Análise técnica concluída")
        self.assertEqual(result.update["dados_input"][0].name, "technical")

    @patch('agente_investimento.utils.processa_analises.ModeloValuationComparacao')
    async def test_process_valuation_success(self, mock_modelo_class: MagicMock) -> None:
        """Testa processamento de análise de valuation com sucesso."""
        mock_modelo = AsyncMock()
        mock_modelo.chat_valuation_comparacao.return_value = "Análise de valuation concluída"
        mock_modelo_class.return_value = mock_modelo

        result = await process_valuation(self.mock_state)

        # Verificar se o modelo foi instanciado corretamente
        mock_modelo_class.assert_called_once_with(
            tickers=["PETR4", "VALE3"],
            query=HumanMessage(content="Analise fundamentalista")
        )
        
        # Verificar se o método foi chamado
        mock_modelo.chat_valuation_comparacao.assert_called_once()
        
        # Verificar o resultado
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "supervisor")
        self.assertIsNotNone(result.update)
        self.assertIn("dados_input", result.update)
        self.assertEqual(result.update["dados_input"][0].content, "Análise de valuation concluída")
        self.assertEqual(result.update["dados_input"][0].name, "valuation")

    @patch('agente_investimento.utils.processa_analises.ModeloSentimentoComparacao')
    async def test_process_sentimento_success(self, mock_modelo_class: MagicMock) -> None:
        """Testa processamento de análise de sentimento com sucesso."""
        mock_modelo = AsyncMock()
        mock_modelo.chat_sentimento_comparacao.return_value = "Análise de sentimento concluída"
        mock_modelo_class.return_value = mock_modelo

        result = await process_sentimento(self.mock_state)

        # Verificar se o modelo foi instanciado corretamente
        mock_modelo_class.assert_called_once_with(
            tickers=["PETR4", "VALE3"],
            query=HumanMessage(content="Analise fundamentalista")
        )
        
        # Verificar se o método foi chamado
        mock_modelo.chat_sentimento_comparacao.assert_called_once()
        
        # Verificar o resultado
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "supervisor")
        self.assertIsNotNone(result.update)
        self.assertIn("dados_input", result.update)
        self.assertEqual(result.update["dados_input"][0].content, "Análise de sentimento concluída")
        self.assertEqual(result.update["dados_input"][0].name, "sentimento")

    @patch('agente_investimento.utils.processa_analises.chatbot_investimento')
    async def test_analise_investimento_success(self, mock_chatbot: AsyncMock) -> None:
        """Testa análise de investimento com sucesso."""
        mock_chatbot.ainvoke.return_value = "Análise de investimento concluída"

        result = await analise_investimento(self.mock_state)

        # Verificar se o chatbot foi chamado
        mock_chatbot.ainvoke.assert_called_once()
        
        # Verificar o resultado
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "supervisor")
        self.assertIsNotNone(result.update)
        self.assertIn("dados_input", result.update)
        self.assertEqual(result.update["dados_input"][0].content, "Análise de investimento concluída")
        self.assertEqual(result.update["dados_input"][0].name, "investimento")

    @patch('agente_investimento.utils.processa_analises.ModeloFundamentosComparacaoAsync')
    async def test_process_fundamental_exception_handling(self, mock_modelo_class: MagicMock) -> None:
        """Testa tratamento de exceção no processamento fundamentalista."""
        mock_modelo = AsyncMock()
        mock_modelo.chat_fundamentalistas_comparacao.side_effect = Exception("Erro no modelo")
        mock_modelo_class.return_value = mock_modelo

        # Deve capturar a exceção e retornar um comando válido
        result = await process_fundamental(self.mock_state)

        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "supervisor")


if __name__ == '__main__':
    unittest.main() 