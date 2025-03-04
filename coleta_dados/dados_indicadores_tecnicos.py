import yfinance as yf
from finta import TA
import pandas as pd
from typing import Dict


class DadosIndicadoresTecnicos:
    def __init__(
        self, ticker: str, periodo: str = "5Y", intervalo: str = "1wk"
    ) -> None:
        self.ticker = ticker
        self.periodo = periodo
        self.intervalo = intervalo

    def tratando_ticker(self) -> str:
        ticker_tratado = self.ticker.upper() + ".SA"
        return ticker_tratado

    def cotacoes_ticker(self) -> pd.DataFrame:
        cotacoes: pd.DataFrame = yf.Ticker(self.tratando_ticker()).history(
            period=self.periodo, interval=self.intervalo
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
        pd_indicadores = pd.concat(
            [indicadores[key] for key in indicadores.keys()], axis=1
        )
        list_colunas_total_nan = pd_indicadores.columns[
            pd_indicadores.isnull().all()
        ].tolist()
        returno = pd_indicadores.drop(columns=list_colunas_total_nan).dropna()
        if returno.shape[0] >= 30:
            returno = returno[-30:]
        return returno
