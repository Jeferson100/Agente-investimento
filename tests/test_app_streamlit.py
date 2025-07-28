from streamlit.testing.v1 import AppTest


def test_no_interaction_1_AnaliseAcao() -> None:
    at = AppTest.from_file("app/app_streamlit.py")
    at.secrets["password"] = "streamlit"
    at.run()
    assert len(at.title) == 1
    assert len(at.markdown) >= 2
    assert len(at.sidebar) == 10
