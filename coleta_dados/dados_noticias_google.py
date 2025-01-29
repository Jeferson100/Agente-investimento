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

        url = f"https://google.serper.dev/news?q={self.acao}&hl=pt-br&apiKey={api_secret_serper.get_secret_value()}"

        payload = {}
        headers = {}

        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=10
        )

        data_serper = response.json()

        return data_serper
