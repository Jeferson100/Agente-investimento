import pandas as pd
from coleta_dados import DadosFundamentalistas


def test_dados_dre() -> None:
    df = DadosFundamentalistas("PETR4").dados_dre()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_capex() -> None:
    df = DadosFundamentalistas("PETR4").dados_capex()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_fluxo_caixa() -> None:
    df = DadosFundamentalistas("PETR4").dados_fluxo_caixa()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_precos_relativos() -> None:
    df = DadosFundamentalistas("PETR4").dados_precos_relativos()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_resumo_balanco() -> None:
    df = DadosFundamentalistas("PETR4").dados_resumo_balanco()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


def test_dados_retornos_margens() -> None:
    df = DadosFundamentalistas("PETR4").dados_retornos_margens()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
