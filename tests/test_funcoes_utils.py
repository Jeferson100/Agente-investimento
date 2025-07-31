import unittest
from unittest.mock import MagicMock
import pandas as pd
from langchain.schema import Document

from agente_investimento.utils.funcoes_utils import (
    generator_to_string,
    string_to_generator,
    configurar_mensagem,
    retransfromando_pandas
)


class TestFuncoesUtils(unittest.TestCase):
    def setUp(self) -> None:
        """Configuração inicial para os testes."""
        pass

    def test_generator_to_string_with_content_attribute(self) -> None:
        """Testa conversão de generator com atributo content."""
        # Criar objetos simples com atributo content
        class MockChunk:
            def __init__(self, content):
                self.content = content
        
        def mock_generator():
            yield MockChunk("chunk1")
            yield MockChunk("chunk2")
        
        result_string, result_chunks = generator_to_string(mock_generator())
        
        self.assertEqual(result_string, "chunk1chunk2")
        self.assertEqual(result_chunks, ["chunk1", "chunk2"])

    def test_generator_to_string_with_text_attribute(self) -> None:
        """Testa conversão de generator com atributo text."""
        # Criar objetos simples com atributo text
        class MockChunk:
            def __init__(self, text):
                self.text = text
        
        def mock_generator():
            yield MockChunk("text1")
            yield MockChunk("text2")
        
        result_string, result_chunks = generator_to_string(mock_generator())
        
        self.assertEqual(result_string, "text1text2")
        self.assertEqual(result_chunks, ["text1", "text2"])

    def test_generator_to_string_with_string_objects(self) -> None:
        """Testa conversão de generator com objetos string."""
        def mock_generator():
            yield "string1"
            yield "string2"
        
        result_string, result_chunks = generator_to_string(mock_generator())
        
        self.assertEqual(result_string, "string1string2")
        self.assertEqual(result_chunks, ["string1", "string2"])

    def test_string_to_generator_with_string(self) -> None:
        """Testa conversão de string para generator."""
        test_string = "test string"
        
        generator = string_to_generator(test_string)
        result = list(generator)
        
        self.assertEqual(result, ["test string"])

    def test_string_to_generator_with_list(self) -> None:
        """Testa conversão de lista para generator."""
        test_list = ["chunk1", "chunk2", "chunk3"]
        
        generator = string_to_generator(test_list)
        result = list(generator)
        
        self.assertEqual(result, ["chunk1", "chunk2", "chunk3"])

    def test_configurar_mensagem_with_think_tag(self) -> None:
        """Testa configuração de mensagem com tag </think>."""
        test_response = "some text</think>actual message"
        
        result = configurar_mensagem(test_response)
        
        self.assertEqual(result, "actual message")

    def test_configurar_mensagem_without_think_tag(self) -> None:
        """Testa configuração de mensagem sem tag </think>."""
        test_response = "simple message without think tag"
        
        result = configurar_mensagem(test_response)
        
        self.assertEqual(result, "simple message without think tag")

    def test_configurar_mensagem_with_multiple_think_tags(self) -> None:
        """Testa configuração de mensagem com múltiplas tags </think>."""
        test_response = "text1</think>text2</think>final message"
        
        result = configurar_mensagem(test_response)
        
        # A função retorna apenas a primeira parte após </think>
        self.assertEqual(result, "text2")

    def test_retransfromando_pandas(self) -> None:
        """Testa transformação de documentos para DataFrame."""
        # Criar documentos de teste
        doc1 = Document(
            page_content="content1",
            metadata={"field1": "value1", "field2": 100}
        )
        doc2 = Document(
            page_content="content2",
            metadata={"field1": "value2", "field2": 200}
        )
        
        documents = [doc1, doc2]
        
        result_df = retransfromando_pandas(documents)
        
        # Verificar se é um DataFrame
        self.assertIsInstance(result_df, pd.DataFrame)
        
        # Verificar colunas
        expected_columns = ["field1", "field2", "data"]
        self.assertEqual(list(result_df.columns), expected_columns)
        
        # Verificar dados
        self.assertEqual(result_df.iloc[0]["field1"], "value1")
        self.assertEqual(result_df.iloc[0]["field2"], 100)
        self.assertEqual(result_df.iloc[0]["data"], "content1")
        self.assertEqual(result_df.iloc[1]["field1"], "value2")
        self.assertEqual(result_df.iloc[1]["field2"], 200)
        self.assertEqual(result_df.iloc[1]["data"], "content2")

    def test_retransfromando_pandas_empty_list(self) -> None:
        """Testa transformação com lista vazia."""
        result_df = retransfromando_pandas([])
        
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(len(result_df), 0)
        self.assertIn("data", result_df.columns)


if __name__ == '__main__':
    unittest.main() 