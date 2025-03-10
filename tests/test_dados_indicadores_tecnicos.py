import pandas as pd
from coleta_dados import DadosIndicadoresTecnicos


def test_tratando_ticker() -> None:
    obj = DadosIndicadoresTecnicos("PETR4")
    assert obj.tratando_ticker() == "PETR4.SA"


def test_cotacoes_ticker() -> None:
    obj = DadosIndicadoresTecnicos("PETR4")
    df = obj.cotacoes_ticker()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert set(["Open", "High", "Low", "Close", "Volume"]).issubset(df.columns)


def test_indicadores_tecnicos() -> None:
    obj = DadosIndicadoresTecnicos("PETR4")
    df = obj.cotacoes_ticker()
    indicadores = obj.indicadores_tecnicos(df)
    assert isinstance(indicadores, dict)
    assert all(
        isinstance(indicadores[key], pd.Series)
        or isinstance(indicadores[key], pd.DataFrame)
        for key in indicadores
    )


def test_pegando_indicadores_tecnicos() -> None:
    obj = DadosIndicadoresTecnicos("PETR4")
    df = obj.pegando_indicadores_tecnicos()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] <= 30
