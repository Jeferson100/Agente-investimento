import pandas as pd
from typing import List


class VerificadorTicks:
    def __init__(self, tic: str):
        self.tic = tic

    def obtendo_ticks(self) -> List[str]:
        list_tic = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/setor.csv"
        )
        return list_tic["tic"].to_list()

    def verificando_ticks(self) -> bool:
        if self.tic in self.obtendo_ticks():
            return True
        else:
            return False
