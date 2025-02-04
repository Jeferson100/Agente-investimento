import yfinance as yf
from finta import TA
import pandas as pd
from typing import Dict


class DadosIndicadoresTecnicos:
    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    def tratando_ticker(self) -> str:
        ticker_tratado = self.ticker.upper() + ".SA"
        return ticker_tratado

    def cotacoes_ticker(self) -> pd.DataFrame:
        cotacoes: pd.DataFrame = yf.Ticker(self.tratando_ticker()).history(
            period="5Y", interval="1d"
        )
        return cotacoes

    def indicadores_tecnicos(self, historico: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        dic_indicadores = {}
        dic_indicadores["media_20"] = TA.SMA(historico, 20)
        dic_indicadores["media_100"] = TA.SMA(historico, 100)
        dic_indicadores["media_200"] = TA.SMA(historico, 200)
        dic_indicadores["rsi"] = TA.RSI(historico)
        dic_indicadores["macd"] = TA.MACD(historico)
        dic_indicadores["bands"] = TA.BBANDS(historico)
        dic_indicadores["pivots"] = TA.PIVOT(historico)
        dic_indicadores["vwap"] = TA.VWAP(historico)
        dic_indicadores["adx"] = TA.ADX(historico)
        dic_indicadores["sar"] = TA.SAR(historico)
        return dic_indicadores

    def pegando_indicadores_tecnicos(self) -> pd.DataFrame:
        cotacoes = self.cotacoes_ticker()
        indicadores = self.indicadores_tecnicos(cotacoes)
        return pd.concat(
            [indicadores[key] for key in indicadores.keys()], axis=1
        ).dropna()
