import unittest
from unittest.mock import MagicMock, patch, mock_open
import pandas as pd
from langgraph.types import Command
from typing import Dict, Any

from agente_investimento.langgraph_construcao.verifica_tick import verificacao_tickets


class TestVerificaTick(unittest.TestCase):
    def setUp(self) -> None:
        """Configuração inicial para os testes."""
        self.mock_empresas_df = pd.DataFrame({
            'tic': ['PETR4', 'VALE3', 'ITUB4', 'BBDC4'],
            'nome': ['Petrobras', 'Vale', 'Itau', 'Bradesco']
        })

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_valid_ticker_list(self, mock_read_csv: MagicMock) -> None:
        """Testa verificação com lista de tickers válidos."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "ticker": ["PETR4", "VALE3"],
            "messages": ["Analise PETR4 e VALE3"],
            "interacao_procura_ticker": 0
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "supervisor")

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_valid_single_ticker(self, mock_read_csv: MagicMock) -> None:
        """Testa verificação com ticker único válido."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "ticker": "PETR4",
            "messages": ["Analise PETR4"],
            "interacao_procura_ticker": 0
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "supervisor")

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_invalid_ticker_list(self, mock_read_csv: MagicMock) -> None:
        """Testa verificação com lista de tickers inválidos."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "ticker": ["INVALID1", "INVALID2"],
            "messages": ["Analise INVALID1 e INVALID2"],
            "interacao_procura_ticker": 0
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertIn("interacao_procura_ticker", result.update)
        self.assertEqual(result.update["interacao_procura_ticker"], 1)

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_invalid_single_ticker(self, mock_read_csv: MagicMock) -> None:
        """Testa verificação com ticker único inválido."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "ticker": "INVALID",
            "messages": ["Analise INVALID"],
            "interacao_procura_ticker": 0
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertIn("interacao_procura_ticker", result.update)
        self.assertEqual(result.update["interacao_procura_ticker"], 1)

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_mixed_valid_invalid(self, mock_read_csv: MagicMock) -> None:
        """Testa verificação com tickers mistos (válidos e inválidos)."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "ticker": ["PETR4", "INVALID"],
            "messages": ["Analise PETR4 e INVALID"],
            "interacao_procura_ticker": 0
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "supervisor")

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_max_attempts_reached(self, mock_read_csv: MagicMock) -> None:
        """Testa quando o número máximo de tentativas é atingido."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "ticker": ["INVALID"],
            "messages": ["Analise INVALID"],
            "interacao_procura_ticker": 2
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "chatbot_padrao")
        self.assertIsNotNone(result.update)
        self.assertIn("mensagem_sistema", result.update)
        self.assertIn("interacao_procura_ticker", result.update)
        self.assertEqual(result.update["interacao_procura_ticker"], 0)

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_empty_ticker(self, mock_read_csv: MagicMock) -> None:
        """Testa verificação com ticker vazio."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "ticker": "",
            "messages": ["Analise"],
            "interacao_procura_ticker": 0
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "identifica_ticks")

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_none_ticker(self, mock_read_csv: MagicMock) -> None:
        """Testa verificação com ticker None."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "ticker": None,
            "messages": ["Analise"],
            "interacao_procura_ticker": 0
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "identifica_ticks")

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_missing_ticker_key(self, mock_read_csv: MagicMock) -> None:
        """Testa verificação quando a chave ticker não existe no state."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "messages": ["Analise"],
            "interacao_procura_ticker": 0
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "identifica_ticks")

    @patch('agente_investimento.langgraph_construcao.verifica_tick.pd.read_csv')
    def test_verificacao_tickets_missing_interacao_key(self, mock_read_csv: MagicMock) -> None:
        """Testa verificação quando a chave interacao_procura_ticker não existe no state."""
        mock_read_csv.return_value = self.mock_empresas_df
        
        state: Dict[str, Any] = {
            "ticker": ["INVALID"],
            "messages": ["Analise INVALID"]
        }
        
        result = verificacao_tickets(state)
        
        self.assertIsInstance(result, Command)
        self.assertEqual(result.goto, "identifica_ticks")
        self.assertIsNotNone(result.update)
        self.assertIn("interacao_procura_ticker", result.update)
        self.assertEqual(result.update["interacao_procura_ticker"], 1)


if __name__ == '__main__':
    unittest.main() 