from typing import Dict, List
from chat_bots import get_secret_key
import requests

try:
    api_secret_serper = get_secret_key("API_KEY_SERPER")
except KeyError as exc:
    raise ValueError("API key serper inválida ou não definida") from exc


class DadosNoticiasGoogle:
    def __init__(self, acao: str) -> None:
        self.acao = acao

    def get_news(self) -> Dict[str, Dict[str, List[str]]]:
        if api_secret_serper is not None:
            api_serper = api_secret_serper.get_secret_value()
            url = f"https://google.serper.dev/news?q={self.acao}&hl=pt-br&apiKey={api_serper}"
        else:
            raise ValueError("API key serper inválida ou não definida")

        payload: Dict[str, str] = {}
        headers: Dict[str, str] = {}

        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=20
        )

        data_serper: Dict[str, Dict[str, List[str]]] = response.json()

        return data_serper
