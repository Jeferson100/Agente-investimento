import unittest
from unittest.mock import MagicMock, patch
from langgraph.types import Command
from pydantic import BaseModel
from typing import Dict, Any, List, Literal

from agente_investimento.langgraph_construcao.identifica_metodo_analise import (
    identifica_metodo_analise,
    MetodoAnalise
)


class TestIdentificaMetodoAnalise(unittest.TestCase):
    def setUp(self) -> None:
        """Configuração inicial para os testes."""
        pass

    @patch('agente_investimento.langgraph_construcao.identifica_metodo_analise.llm_identifica_metodo_analise')
    def test_identifica_metodo_analise_fundamentalista(self, mock_llm: MagicMock) -> None:
        """Testa identificação de método fundamentalista."""
        mock_response = MagicMock()
        mock_response.method_analysis = ["fundamentalista"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Analise fundamentalista da Petrobras"]
        }
        
        result = identifica_metodo_analise(state)
        
        # Verificar se o LLM foi chamado
        mock_llm.invoke.assert_called_once_with({"messages": "Analise fundamentalista da Petrobras"})
        
        # Verificar o resultado
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertIn("method_analysis", result.update)
        self.assertEqual(result.update["method_analysis"], ["fundamentalista"])

    @patch('agente_investimento.langgraph_construcao.identifica_metodo_analise.llm_identifica_metodo_analise')
    def test_identifica_metodo_analise_tecnico(self, mock_llm: MagicMock) -> None:
        """Testa identificação de método técnico."""
        mock_response = MagicMock()
        mock_response.method_analysis = ["tecnico"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Analise técnica do gráfico"]
        }
        
        result = identifica_metodo_analise(state)
        
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertEqual(result.update["method_analysis"], ["tecnico"])

    @patch('agente_investimento.langgraph_construcao.identifica_metodo_analise.llm_identifica_metodo_analise')
    def test_identifica_metodo_analise_sentimento(self, mock_llm: MagicMock) -> None:
        """Testa identificação de método de sentimento."""
        mock_response = MagicMock()
        mock_response.method_analysis = ["sentimento"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Analise o sentimento do mercado"]
        }
        
        result = identifica_metodo_analise(state)
        
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertEqual(result.update["method_analysis"], ["sentimento"])

    @patch('agente_investimento.langgraph_construcao.identifica_metodo_analise.llm_identifica_metodo_analise')
    def test_identifica_metodo_analise_valuation(self, mock_llm: MagicMock) -> None:
        """Testa identificação de método de valuation."""
        mock_response = MagicMock()
        mock_response.method_analysis = ["valuation"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Faça uma análise de valuation"]
        }
        
        result = identifica_metodo_analise(state)
        
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertEqual(result.update["method_analysis"], ["valuation"])

    @patch('agente_investimento.langgraph_construcao.identifica_metodo_analise.llm_identifica_metodo_analise')
    def test_identifica_metodo_analise_multiple_methods(self, mock_llm: MagicMock) -> None:
        """Testa identificação de múltiplos métodos."""
        mock_response = MagicMock()
        mock_response.method_analysis = ["fundamentalista", "tecnico"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Analise fundamentalista e técnica"]
        }
        
        result = identifica_metodo_analise(state)
        
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertEqual(result.update["method_analysis"], ["fundamentalista", "tecnico"])

    @patch('agente_investimento.langgraph_construcao.identifica_metodo_analise.llm_identifica_metodo_analise')
    def test_identifica_metodo_analise_analise_investimento(self, mock_llm: MagicMock) -> None:
        """Testa identificação de análise de investimento completa."""
        mock_response = MagicMock()
        mock_response.method_analysis = ["analise_investimento"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Faça uma análise completa de investimento"]
        }
        
        result = identifica_metodo_analise(state)
        
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertEqual(result.update["method_analysis"], ["analise_investimento"])

    @patch('agente_investimento.langgraph_construcao.identifica_metodo_analise.llm_identifica_metodo_analise')
    def test_identifica_metodo_analise_sem_analise(self, mock_llm: MagicMock) -> None:
        """Testa identificação quando não há análise específica."""
        mock_response = MagicMock()
        mock_response.method_analysis = ["sem_analise"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Olá, como você está?"]
        }
        
        result = identifica_metodo_analise(state)
        
        self.assertEqual(result.goto, "chatbot_padrao")
        self.assertIsNotNone(result.update)
        self.assertIn("mensagem_sistema", result.update)
        self.assertIn("Essa foi a pergunta feita pelo usuario:", result.update["mensagem_sistema"])


    def test_metodo_analise_model(self) -> None:
        """Testa o modelo Pydantic MetodoAnalise."""
        metodo_data = {
            "method_analysis": ["fundamentalista", "tecnico"]
        }
        
        metodo = MetodoAnalise(**metodo_data)
        
        self.assertEqual(metodo.method_analysis, ["fundamentalista", "tecnico"])
        self.assertIsInstance(metodo, BaseModel)

    def test_metodo_analise_model_single_method(self) -> None:
        """Testa o modelo Pydantic MetodoAnalise com método único."""
        metodo_data = {
            "method_analysis": ["valuation"]
        }
        
        metodo = MetodoAnalise(**metodo_data)
        
        self.assertEqual(metodo.method_analysis, ["valuation"])

    def test_metodo_analise_model_sem_analise(self) -> None:
        """Testa o modelo Pydantic MetodoAnalise com sem_analise."""
        metodo_data = {
            "method_analysis": ["sem_analise"]
        }
        
        metodo = MetodoAnalise(**metodo_data)
        
        self.assertEqual(metodo.method_analysis, ["sem_analise"])

    @patch('agente_investimento.langgraph_construcao.identifica_metodo_analise.llm_identifica_metodo_analise')
    def test_identifica_metodo_analise_mixed_methods(self, mock_llm: MagicMock) -> None:
        """Testa identificação com métodos mistos."""
        mock_response = MagicMock()
        mock_response.method_analysis = ["fundamentalista", "sentimento", "valuation"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Analise fundamentalista, sentimento e valuation"]
        }
        
        result = identifica_metodo_analise(state)
        
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertEqual(result.update["method_analysis"], ["fundamentalista", "sentimento", "valuation"])


if __name__ == '__main__':
    unittest.main() 