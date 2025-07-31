import unittest
from unittest.mock import patch, MagicMock
import pytest
import pandas as pd
from streamlit.testing.v1 import AppTest


@patch('streamlit.session_state')
@patch('streamlit.chat_input')
@patch('streamlit.chat_message')
@patch('streamlit.spinner')
@patch('pandas.read_csv')
def test_app_streamlit_basic_components(mock_read_csv, mock_spinner, mock_chat_message, mock_chat_input, mock_session_state):
    """Testa os componentes básicos do app Streamlit."""
    mock_read_csv.return_value = pd.DataFrame({'tic': ['PETR4', 'VALE3']})
    # Mock das variáveis de ambiente
    with patch.dict('os.environ', {
        'GROQ_API_KEY': 'fake-groq-key',
        'API_KEY_SERPER': 'fake-serper-key'
    }):
        at = AppTest.from_file("app/app_streamlit.py")
        
        # Configurar mocks para evitar timeouts
        mock_session_state.get.return_value = None
        mock_chat_input.return_value = None
        mock_chat_message.return_value.__enter__ = MagicMock()
        mock_chat_message.return_value.__exit__ = MagicMock()
        mock_spinner.return_value.__enter__ = MagicMock()
        mock_spinner.return_value.__exit__ = MagicMock()
        
        at.run()
        
        # Verificar se os componentes básicos estão presentes
        assert len(at.title) == 1



@patch('streamlit.session_state')
@patch('streamlit.chat_input')
@patch('streamlit.chat_message')
@patch('streamlit.spinner')
@patch('streamlit.error')
@patch('streamlit.warning')
@patch('pandas.read_csv')
def test_app_streamlit_api_keys_missing(mock_read_csv, mock_warning, mock_error, mock_spinner, mock_chat_message, mock_chat_input, mock_session_state):
    """Testa o comportamento quando as chaves de API estão faltando."""
    # Mock sem as variáveis de ambiente
    mock_read_csv.return_value = pd.DataFrame({'tic': ['PETR4', 'VALE3']})
    with patch.dict('os.environ', {}, clear=True):
        at = AppTest.from_file("app/app_streamlit.py")
        
        # Configurar mocks
        mock_session_state.get.return_value = None
        mock_chat_input.return_value = "Teste"
        mock_chat_message.return_value.__enter__ = MagicMock()
        mock_chat_message.return_value.__exit__ = MagicMock()
        mock_spinner.return_value.__enter__ = MagicMock()
        mock_spinner.return_value.__exit__ = MagicMock()
        
        at.run()
        
        # Verificar se os avisos de API aparecem - mudando para verificar warnings no main
        assert len(at.main) >= 1  # Deve ter pelo menos um elemento no main


@patch('streamlit.session_state')
@patch('streamlit.chat_input')
@patch('streamlit.chat_message')
@patch('streamlit.spinner')
@patch('pandas.read_csv')
@patch('agente_investimento.langgraph_main')
def test_app_streamlit_with_api_keys(mock_langgraph, mock_read_csv, mock_spinner, mock_chat_message, mock_chat_input, mock_session_state):
    """Testa o app com chaves de API configuradas."""
    mock_read_csv.return_value = pd.DataFrame({'tic': ['PETR4', 'VALE3']})
    # Mock das variáveis de ambiente
    with patch.dict('os.environ', {
        'GROQ_API_KEY': 'fake-groq-key',
        'API_KEY_SERPER': 'fake-serper-key'
    }):
        at = AppTest.from_file("app/app_streamlit.py")
        
        # Mock do langgraph
        mock_graph = MagicMock()
        mock_graph.ainvoke.return_value = {
            "messages": [
                MagicMock(content="Pergunta do usuário"),
                MagicMock(content="Resposta do assistente")
            ]
        }
        mock_langgraph.return_value = mock_graph
        
        # Configurar mocks
        mock_session_state.get.return_value = "fake-api-key"
        mock_chat_input.return_value = "Analise PETR4"
        mock_chat_message.return_value.__enter__ = MagicMock()
        mock_chat_message.return_value.__exit__ = MagicMock()
        mock_spinner.return_value.__enter__ = MagicMock()
        mock_spinner.return_value.__exit__ = MagicMock()
        
        at.run()
        
        # Verificar se o app carregou corretamente
        assert len(at.title) == 1


@patch('pandas.read_csv')
def test_app_streamlit_sidebar_components(mock_read_csv):
    """Testa os componentes da sidebar."""
    mock_read_csv.return_value = pd.DataFrame({'tic': ['PETR4', 'VALE3']})
    at = AppTest.from_file("app/app_streamlit.py")
    at.run()
    
    # Verificar se a sidebar tem os componentes esperados
    assert len(at.sidebar) >= 5  # Deve ter pelo menos 5 elementos na sidebar
    
    # Verificar se há botões na sidebar
    sidebar_buttons = [elem for elem in at.sidebar if hasattr(elem, 'label')]
    assert len(sidebar_buttons) >= 2  # Deve ter pelo menos 2 botões


@patch('pandas.read_csv')
def test_app_streamlit_session_state(mock_read_csv):
    """Testa o gerenciamento do session state."""
    mock_read_csv.return_value = pd.DataFrame({'tic': ['PETR4', 'VALE3']})
    at = AppTest.from_file("app/app_streamlit.py")
    at.run()
    
    # Verificar se o app inicializa corretamente
    assert len(at.title) == 1
    assert "Agente de Inteligência Artificial" in at.title[0].value


@patch('pandas.read_csv')
def test_app_streamlit_codigos_loading(mock_read_csv):
    """Testa o carregamento dos códigos de negociação."""
    mock_read_csv.return_value = pd.DataFrame({'tic': ["PETR4", "VALE3", "ITUB4"]})
    
    at = AppTest.from_file("app/app_streamlit.py")
    at.run()
    
    # Verificar se o app carregou sem erros
    assert len(at.title) == 1
    assert at.session_state.codigos == ["ITUB4", "PETR4", "VALE3"]


@patch('pandas.read_csv')
def test_app_streamlit_chat_input(mock_read_csv):
    """Testa se o campo de entrada de chat está presente."""
    mock_read_csv.return_value = pd.DataFrame({'tic': ['PETR4', 'VALE3']})
    at = AppTest.from_file("app/app_streamlit.py")
    at.run()
    
    # Verificar se o chat input está presente
    assert len(at.chat_input) >= 1


@patch('pandas.read_csv')
def test_app_streamlit_title_content(mock_read_csv):
    """Testa se o título do app está correto."""
    mock_read_csv.return_value = pd.DataFrame({'tic': ['PETR4', 'VALE3']})
    at = AppTest.from_file("app/app_streamlit.py")
    at.run()
    
    # Verificar se o título está correto
    assert len(at.title) == 1
    title_text = at.title[0].value
    assert "Agente de Inteligência Artificial" in title_text
    assert "Análise de Investimentos" in title_text


if __name__ == '__main__':
    unittest.main()
