from pydantic import SecretStr
from coleta_dados.dados_noticias_google import DadosNoticiasGoogle
import os
from unittest.mock import patch
from typing import Dict, List

api_key_serper = os.getenv("API_KEY_SERPER")


def test_get_news() -> None:
    api_key_serper = os.getenv("API_KEY_SERPER")
    
    if api_key_serper is None:
        raise ValueError("API key serper inválida ou não definida")

    obj = DadosNoticiasGoogle("PETR4", api_serper=SecretStr(api_key_serper))
    noticias = obj.get_news()

    assert isinstance(noticias, dict)
    assert "news" in noticias
    assert isinstance(noticias["news"], list)
    assert len(noticias["news"]) > 0
    assert all("title" in noticia and "link" in noticia for noticia in noticias["news"])
