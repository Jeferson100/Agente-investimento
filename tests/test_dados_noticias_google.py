from pydantic import SecretStr
from coleta_dados.dados_noticias_google import DadosNoticiasGoogle
import os


def test_get_news() -> None:
    api_key_serper = os.environ.get("API_KEY_SERPER")
    assert api_key_serper is not None, "API_KEY_SERPER environment variable is not set"
    obj = DadosNoticiasGoogle("PETR4", api_serper=SecretStr(api_key_serper))
    noticias = obj.get_news()

    assert isinstance(noticias, dict)
    assert "news" in noticias
    assert isinstance(noticias["news"], list)
    assert len(noticias["news"]) > 0
    assert all("title" in noticia and "link" in noticia for noticia in noticias["news"])
