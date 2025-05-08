from typing import Any, List, Optional, Union

from sqlalchemy import Engine, Row, Sequence, create_engine, inspect, text


class PostgresDBConsult:
    def __init__(
        self,
        DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5433/postgres",
    ) -> None:
        self.DATABASE_URL = DATABASE_URL

    def create_db_connection(self) -> Engine:
        """Cria conexão com o banco de dados."""
        return create_engine(self.DATABASE_URL)

    def get_interactions(
        self, limit: int = 10, tabela: str = "checkpoints"
    ) -> Optional[Union[Sequence[Row], List[Any]]]:
        """Recupera as últimas interações do banco de dados."""
        try:
            engine = self.create_db_connection()

            with engine.connect() as conn:
                query = f"""
                SELECT * FROM {tabela}
                """
                result = conn.execute(text(query), {"limit": limit})
                return result.fetchall()  # type:ignore

        except Exception as e:
            print(f"Erro ao recuperar dados: {e}")
            return []

    def drop_table(self, tabela: str = "checkpoints") -> None:
        """Apaga a tabela llm_interactions."""
        try:

            engine = self.create_db_connection()

            # Apagar a tabela
            with engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {tabela}"))
                conn.commit()
                print("Tabela apagada com sucesso!")

        except Exception as e:
            print(f"Erro ao apagar tabela: {e}")

    def inspecionar_tabelas(self) -> List[str]:
        engine = self.create_db_connection()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        if len(tables) == 0:
            print("O banco de dados esta vazio!")
        return tables
