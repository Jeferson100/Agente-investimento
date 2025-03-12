from streamlit.testing.v1 import AppTest


def test_no_interaction_1_AnaliseAcao() -> None:
    at = AppTest.from_file("app_streamlit/1_AnaliseAcao.py")
    at.secrets["password"] = "streamlit"
    at.run()
    assert len(at.title) == 1
    assert len(at.markdown) >= 2
    assert len(at.sidebar) == 10


def test_no_interaction_2_AnaliseFundamentalista() -> None:
    at = AppTest.from_file("app_streamlit/pages/2_AnaliseFundamentalista.py")
    at.secrets["password"] = "streamlit"
    at.run()
    assert len(at.title) == 1
    assert len(at.markdown) >= 2
    assert len(at.sidebar) == 8
    assert len(at.chat_input) == 1


def test_no_interaction_3_AnaliseTecnica() -> None:
    at = AppTest.from_file("app_streamlit/pages/3_AnaliseTecnica.py")
    at.secrets["password"] = "streamlit"
    at.run()
    assert len(at.title) == 1
    assert len(at.markdown) >= 2
    assert len(at.sidebar) == 8
    assert len(at.chat_input) == 1


def test_no_interaction_4_AnaliseSentimento() -> None:
    at = AppTest.from_file("app_streamlit/pages/4_AnaliseSentimento.py")
    at.secrets["password"] = "streamlit"
    at.run()
    assert len(at.title) == 1
    assert len(at.markdown) >= 2
    assert len(at.sidebar) == 13
    assert len(at.chat_input) == 1


def test_no_interaction_5_AnaliseValuation() -> None:
    at = AppTest.from_file("app_streamlit/pages/5_AnaliseValuation.py")
    at.secrets["password"] = "streamlit"
    at.run()
    assert len(at.title) == 1
    assert len(at.markdown) >= 2
    assert len(at.sidebar) == 8
    assert len(at.chat_input) == 1
