import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import pandas as pd
from pydantic import BaseModel
from typing import Dict, Any

from agente_investimento.langgraph_construcao.identifica_ticks import identifica_ticks, Tickers


class TestIdentificaTicks(unittest.TestCase):
    def setUp(self) -> None:
        """Configuração inicial para os testes."""
        self.mock_empresas_df = pd.DataFrame({
            'Empresa': ['Petrobras', 'Vale', 'Itau', 'Bradesco'],
            'tic': ['PETR4', 'VALE3', 'ITUB4', 'BBDC4']
        })

    @patch('agente_investimento.langgraph_construcao.identifica_ticks.llm_identifica_ticker')
    def test_identifica_ticks_success(self, mock_llm: MagicMock) -> None:
        """Testa identificação de ticks com sucesso."""
        # Mock da resposta do LLM
        mock_response = MagicMock()
        mock_response.tickers = ["PETR4", "VALE3"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Analise Petrobras e Vale"]
        }
        
        result = identifica_ticks(state)
        
        # Verificar se o LLM foi chamado
        mock_llm.invoke.assert_called_once()
        
        # Verificar o resultado
        self.assertIn("ticker", result)
        self.assertEqual(result["ticker"], ["PETR4", "VALE3"])

    @patch('agente_investimento.langgraph_construcao.identifica_ticks.llm_identifica_ticker')
    def test_identifica_ticks_single_ticker(self, mock_llm: MagicMock) -> None:
        """Testa identificação de um único ticker."""
        mock_response = MagicMock()
        mock_response.tickers = ["PETR4"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Analise Petrobras"]
        }
        
        result = identifica_ticks(state)
        
        self.assertEqual(result["ticker"], ["PETR4"])

    @patch('agente_investimento.langgraph_construcao.identifica_ticks.llm_identifica_ticker')
    def test_identifica_ticks_no_tickers_found(self, mock_llm: MagicMock) -> None:
        """Testa identificação quando nenhum ticker é encontrado."""
        mock_response = MagicMock()
        mock_response.tickers = []
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Analise mercado brasileiro"]
        }
        
        result = identifica_ticks(state)
        
        self.assertEqual(result["ticker"], [])


    def test_tickers_model(self) -> None:
        """Testa o modelo Pydantic Tickers."""
        tickers_data = {
            "tickers": ["PETR4", "VALE3", "ITUB4"]
        }
        
        tickers = Tickers(**tickers_data)
        
        self.assertEqual(tickers.tickers, ["PETR4", "VALE3", "ITUB4"])
        self.assertIsInstance(tickers, BaseModel)

    def test_tickers_model_empty_list(self) -> None:
        """Testa o modelo Pydantic Tickers com lista vazia."""
        tickers_data = {
            "tickers": []
        }
        
        tickers = Tickers(**tickers_data)
        
        self.assertEqual(tickers.tickers, [])

    @patch('agente_investimento.langgraph_construcao.identifica_ticks.llm_identifica_ticker')
    def test_identifica_ticks_multiple_companies(self, mock_llm: MagicMock) -> None:
        """Testa identificação de múltiplas empresas."""
        mock_response = MagicMock()
        mock_response.tickers = ["PETR4", "VALE3", "ITUB4"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Compare Petrobras, Vale e Itau"]
        }
        
        result = identifica_ticks(state)
        
        self.assertEqual(result["ticker"], ["PETR4", "VALE3", "ITUB4"])

    @patch('agente_investimento.langgraph_construcao.identifica_ticks.llm_identifica_ticker')
    def test_identifica_ticks_with_company_names_only(self, mock_llm: MagicMock) -> None:
        """Testa identificação quando apenas nomes de empresas são mencionados."""
        mock_response = MagicMock()
        mock_response.tickers = ["PETR4"]
        mock_llm.invoke.return_value = mock_response
        
        state: Dict[str, Any] = {
            "messages": ["Quero analisar a Petrobras"]
        }
        
        result = identifica_ticks(state)
        
        self.assertEqual(result["ticker"], ["PETR4"])


if __name__ == '__main__':
    unittest.main() 