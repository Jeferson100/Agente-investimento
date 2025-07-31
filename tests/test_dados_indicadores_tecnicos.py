import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
from finta import TA

from agente_investimento.coleta_dados.dados_indicadores_tecnicos import DadosIndicadoresTecnicos


class TestDadosIndicadoresTecnicos(unittest.TestCase):
    def setUp(self) -> None:
        """Configuração inicial para os testes."""
        self.ticker = "PETR4"
        self.periodo = "5Y"
        self.intervalo = "1wk"
        self.dados_indicadores = DadosIndicadoresTecnicos(
            self.ticker, self.periodo, self.intervalo
        )

    def test_init(self) -> None:
        """Testa a inicialização da classe."""
        self.assertEqual(self.dados_indicadores.ticker, "PETR4")
        self.assertEqual(self.dados_indicadores.periodo, "5Y")
        self.assertEqual(self.dados_indicadores.intervalo, "1wk")

    def test_tratando_ticker(self) -> None:
        """Testa o tratamento do ticker."""
        result = self.dados_indicadores.tratando_ticker()
        self.assertEqual(result, "PETR4.SA")

    def test_tratando_ticker_lowercase(self) -> None:
        """Testa o tratamento do ticker em minúsculas."""
        dados_indicadores = DadosIndicadoresTecnicos("petr4")
        result = dados_indicadores.tratando_ticker()
        self.assertEqual(result, "PETR4.SA")

    @patch('agente_investimento.coleta_dados.dados_indicadores_tecnicos.yf.Ticker')
    def test_cotacoes_ticker_success(self, mock_ticker: MagicMock) -> None:
        """Testa a obtenção de cotações com sucesso."""
        # Mock do histórico
        mock_historico = pd.DataFrame({
            'Open': [10.0, 11.0, 12.0],
            'High': [11.0, 12.0, 13.0],
            'Low': [9.0, 10.0, 11.0],
            'Close': [10.5, 11.5, 12.5],
            'Volume': [1000, 1100, 1200]
        })
        
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = mock_historico
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.dados_indicadores.cotacoes_ticker()
        
        mock_ticker.assert_called_once_with("PETR4.SA")
        mock_ticker_instance.history.assert_called_once_with(
            period="5Y", interval="1wk"
        )
        pd.testing.assert_frame_equal(result, mock_historico)

    @patch('agente_investimento.coleta_dados.dados_indicadores_tecnicos.yf.Ticker')
    def test_cotacoes_ticker_exception(self, mock_ticker: MagicMock) -> None:
        """Testa o comportamento quando ocorre uma exceção."""
        mock_ticker.side_effect = Exception("API error")
        
        with self.assertRaises(Exception):
            self.dados_indicadores.cotacoes_ticker()

    def test_indicadores_tecnicos(self) -> None:
        """Testa o cálculo de indicadores técnicos."""
        # Criar DataFrame de teste com dados mínimos necessários
        historico = pd.DataFrame({
            'Open': [10.0, 11.0, 12.0, 13.0, 14.0],
            'High': [11.0, 12.0, 13.0, 14.0, 15.0],
            'Low': [9.0, 10.0, 11.0, 12.0, 13.0],
            'Close': [10.5, 11.5, 12.5, 13.5, 14.5],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = self.dados_indicadores.indicadores_tecnicos(historico)
        
        # Verificar se é um dicionário
        self.assertIsInstance(result, dict)
        
        # Verificar se contém as chaves esperadas
        expected_keys = [
            "media_20", "media_100", "rsi", "macd", "bands", 
            "pivots", "vwap", "adx", "sar"
        ]
        for key in expected_keys:
            self.assertIn(key, result)

    def test_indicadores_tecnicos_empty_dataframe(self) -> None:
        """Testa o cálculo de indicadores com DataFrame vazio."""
        # Criar DataFrame vazio mas com as colunas necessárias
        historico = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])
        
        # Deve capturar a exceção LookupError
        with self.assertRaises(LookupError):
            self.dados_indicadores.indicadores_tecnicos(historico)

    @patch('agente_investimento.coleta_dados.dados_indicadores_tecnicos.yf.Ticker')
    def test_pegando_indicadores_tecnicos_success(self, mock_ticker: MagicMock) -> None:
        """Testa a obtenção completa de indicadores técnicos."""
        # Mock do histórico
        mock_historico = pd.DataFrame({
            'Open': [10.0] * 50,
            'High': [11.0] * 50,
            'Low': [9.0] * 50,
            'Close': [10.5] * 50,
            'Volume': [1000] * 50
        })
        
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = mock_historico
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.dados_indicadores.pegando_indicadores_tecnicos()
        
        # Verificar se é um DataFrame
        self.assertIsInstance(result, pd.DataFrame)
        
        # Verificar se não está vazio
        self.assertGreater(len(result), 0)

    @patch('agente_investimento.coleta_dados.dados_indicadores_tecnicos.yf.Ticker')
    def test_pegando_indicadores_tecnicos_less_than_30_rows(self, mock_ticker: MagicMock) -> None:
        """Testa quando há menos de 30 linhas de dados."""
        # Mock do histórico com poucos dados
        mock_historico = pd.DataFrame({
            'Open': [10.0] * 10,
            'High': [11.0] * 10,
            'Low': [9.0] * 10,
            'Close': [10.5] * 10,
            'Volume': [1000] * 10
        })
        
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = mock_historico
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.dados_indicadores.pegando_indicadores_tecnicos()
        
        # Deve retornar todos os dados disponíveis
        self.assertIsInstance(result, pd.DataFrame)
        self.assertLessEqual(len(result), 10)

    @patch('agente_investimento.coleta_dados.dados_indicadores_tecnicos.yf.Ticker')
    def test_pegando_indicadores_tecnicos_more_than_30_rows(self, mock_ticker: MagicMock) -> None:
        """Testa quando há mais de 30 linhas de dados."""
        # Mock do histórico com muitos dados
        mock_historico = pd.DataFrame({
            'Open': [10.0] * 100,
            'High': [11.0] * 100,
            'Low': [9.0] * 100,
            'Close': [10.5] * 100,
            'Volume': [1000] * 100
        })
        
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.return_value = mock_historico
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.dados_indicadores.pegando_indicadores_tecnicos()
        
        # Deve retornar apenas as últimas 30 linhas ou menos (dependendo dos dados válidos)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertLessEqual(len(result), 30)

    @patch('agente_investimento.coleta_dados.dados_indicadores_tecnicos.yf.Ticker')
    def test_pegando_indicadores_tecnicos_exception(self, mock_ticker: MagicMock) -> None:
        """Testa o comportamento quando ocorre uma exceção."""
        mock_ticker.side_effect = Exception("API error")
        
        with self.assertRaises(Exception):
            self.dados_indicadores.pegando_indicadores_tecnicos()

    def test_different_periods_and_intervals(self) -> None:
        """Testa diferentes períodos e intervalos."""
        dados_indicadores = DadosIndicadoresTecnicos("VALE3", "1Y", "1d")
        
        self.assertEqual(dados_indicadores.ticker, "VALE3")
        self.assertEqual(dados_indicadores.periodo, "1Y")
        self.assertEqual(dados_indicadores.intervalo, "1d")
        self.assertEqual(dados_indicadores.tratando_ticker(), "VALE3.SA")

    def test_indicadores_tecnicos_with_nan_values(self) -> None:
        """Testa o cálculo de indicadores com valores NaN."""
        historico = pd.DataFrame({
            'Open': [10.0, np.nan, 12.0, 13.0, 14.0],
            'High': [11.0, 12.0, np.nan, 14.0, 15.0],
            'Low': [9.0, 10.0, 11.0, np.nan, 13.0],
            'Close': [10.5, 11.5, 12.5, 13.5, np.nan],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        result = self.dados_indicadores.indicadores_tecnicos(historico)
        
        self.assertIsInstance(result, dict)
        # Deve conter as chaves mesmo com NaN
        expected_keys = [
            "media_20", "media_100", "rsi", "macd", "bands", 
            "pivots", "vwap", "adx", "sar"
        ]
        for key in expected_keys:
            self.assertIn(key, result)


if __name__ == '__main__':
    unittest.main() 