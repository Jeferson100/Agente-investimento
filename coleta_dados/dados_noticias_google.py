from typing import Dict, List
from chat_bots import get_secret_key
import requests
from pydantic import SecretStr

try:
    api_secret_serper = get_secret_key("API_KEY_SERPER")
except KeyError as exc:
    raise ValueError("API key serper inválida ou não definida") from exc


class DadosNoticiasGoogle:
    def __init__(self, acao: str, api_serper: SecretStr | None = None) -> None:
        self.acao = acao
        self.api_serper = api_serper

    def get_news(self) -> Dict[str, Dict[str, List[str]]]:
        if api_secret_serper is not None:
            api_serper_serper = api_secret_serper.get_secret_value()
            url = f"https://google.serper.dev/news?q={self.acao}&hl=pt-br&apiKey={api_serper_serper}"
        elif self.api_serper is not None:
            api_serper = self.api_serper.get_secret_value()
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
