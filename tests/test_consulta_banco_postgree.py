import unittest
from unittest.mock import MagicMock, patch, mock_open
import pytest
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from agente_investimento.consulta_banco_postgree import PostgresDBConsult


class TestPostgresDBConsult(unittest.TestCase):
    def setUp(self) -> None:
        """Configuração inicial para os testes."""
        self.db_url = "postgresql://postgres:postgres@localhost:5433/postgres"
        self.postgres_consult = PostgresDBConsult(self.db_url)

    def test_init(self) -> None:
        """Testa a inicialização da classe."""
        self.assertEqual(self.postgres_consult.DATABASE_URL, self.db_url)

    @patch('agente_investimento.consulta_banco_postgree.create_engine')
    def test_create_db_connection(self, mock_create_engine: MagicMock) -> None:
        """Testa a criação da conexão com o banco de dados."""
        mock_engine = MagicMock(spec=Engine)
        mock_create_engine.return_value = mock_engine

        result = self.postgres_consult.create_db_connection()

        mock_create_engine.assert_called_once_with(self.db_url)
        self.assertEqual(result, mock_engine)

    @patch('agente_investimento.consulta_banco_postgree.create_engine')
    def test_get_interactions_success(self, mock_create_engine: MagicMock) -> None:
        """Testa a recuperação de interações com sucesso."""
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_result = MagicMock()
        
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_connection.execute.return_value = mock_result
        mock_result.fetchall.return_value = [{"id": 1, "data": "test"}]

        result = self.postgres_consult.get_interactions(limit=5, tabela="test_table")

        self.assertEqual(result, [{"id": 1, "data": "test"}])
        mock_connection.execute.assert_called_once()

    @patch('agente_investimento.consulta_banco_postgree.create_engine')
    def test_get_interactions_exception(self, mock_create_engine: MagicMock) -> None:
        """Testa o comportamento quando ocorre uma exceção."""
        mock_create_engine.side_effect = SQLAlchemyError("Connection error")

        result = self.postgres_consult.get_interactions()

        self.assertEqual(result, [])

    @patch('agente_investimento.consulta_banco_postgree.create_engine')
    def test_drop_table_success(self, mock_create_engine: MagicMock) -> None:
        """Testa a remoção de tabela com sucesso."""
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__.return_value = mock_connection

        self.postgres_consult.drop_table("test_table")

        mock_connection.execute.assert_called_once()
        mock_connection.commit.assert_called_once()

    @patch('agente_investimento.consulta_banco_postgree.create_engine')
    def test_drop_table_exception(self, mock_create_engine: MagicMock) -> None:
        """Testa o comportamento quando ocorre uma exceção ao remover tabela."""
        mock_create_engine.side_effect = SQLAlchemyError("Drop error")

        # Não deve levantar exceção
        self.postgres_consult.drop_table("test_table")

    @patch('agente_investimento.consulta_banco_postgree.create_engine')
    @patch('agente_investimento.consulta_banco_postgree.inspect')
    def test_inspecionar_tabelas_with_tables(self, mock_inspect: MagicMock, mock_create_engine: MagicMock) -> None:
        """Testa a inspeção de tabelas quando existem tabelas."""
        mock_engine = MagicMock()
        mock_inspector = MagicMock()
        
        mock_create_engine.return_value = mock_engine
        mock_inspect.return_value = mock_inspector
        mock_inspector.get_table_names.return_value = ["table1", "table2"]

        result = self.postgres_consult.inspecionar_tabelas()

        self.assertEqual(result, ["table1", "table2"])

    @patch('agente_investimento.consulta_banco_postgree.create_engine')
    @patch('agente_investimento.consulta_banco_postgree.inspect')
    def test_inspecionar_tabelas_empty(self, mock_inspect: MagicMock, mock_create_engine: MagicMock) -> None:
        """Testa a inspeção de tabelas quando o banco está vazio."""
        mock_engine = MagicMock()
        mock_inspector = MagicMock()
        
        mock_create_engine.return_value = mock_engine
        mock_inspect.return_value = mock_inspector
        mock_inspector.get_table_names.return_value = []

        result = self.postgres_consult.inspecionar_tabelas()

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main() 