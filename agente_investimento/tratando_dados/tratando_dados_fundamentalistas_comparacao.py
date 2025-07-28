import asyncio
from ..coleta_dados import DadosFundamentalistas
from langchain_community.document_loaders import DataFrameLoader
from typing import List, Optional
import pandas as pd


class TratatandoDadosFundamentalistasComparacao:
    def __init__(
        self,
        tics: List[str],
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        colunas_drop: Optional[List[str]] = None,
    ) -> None:
        self.tics = tics
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.colunas_drop = colunas_drop

    async def dados_fundamentalistas(self, tic: str) -> pd.DataFrame:
        df = DadosFundamentalistas(
            tic=tic, data_inicio=self.data_inicio, data_fim=self.data_fim
        )
        df_dados = await df.dados_fundamentalistas_completo()
        if self.data_inicio:
            return df_dados
        data_inicio = df_dados["datas"].iloc[-4].strftime("%Y-%m-%d")
        df_data_inicio = df_dados.loc[df_dados.datas >= data_inicio]
        return df_data_inicio

    async def drop_columns(self, tic: str) -> pd.DataFrame:
        colunas_drop = [
            "acoes_ordinarias",
            "acoes_preferenciais",
            "total",
            "capex_doze_meses",
            "fluxo_caixa_livre_doze_meses",
            "retorno_sobre_capital_tangivel_inicial",
            "retorno_sobre_capital_tangivel_inicial_pre_impostos",
            "retorno_sobre_capital_investido_inicial_pre_impostos",
            "preço_ncav",
            "margem_ebitda",
            "divida_liquida_ebitda",
            "ev_ebitda",
            "ev_receita_líquida",
            "ev_fco",
            "ev_fcf",
            "ev_ativo_total",
            "preço_vpa",
            "preço_capital_giro",
            "preço_fcf",
            "caixa_equivalentes_caixa",
            "giro_do_ativo_inicial",
            "retorno_sobre_patrimonio_liquido_inicial",
            "retorno_sobre_capital_investido_inicial",
            "fluxo_caixa_financiamento",
            "fluxo_caixa_investimento",
            "fluxo_caixa_operacional",
            "fluxo_caixa_livre_tres_meses",
        ]
        df = await self.dados_fundamentalistas(tic=tic)

        df_cleaned = df.copy()

        df_cleaned.drop(columns=colunas_drop, inplace=True, errors="ignore")

        df_cleaned["datas"] = df_cleaned["datas"].astype(str)

        df_cleaned.dropna(axis=1, how="all", inplace=True)

        return df_cleaned

    async def transformer_loader(self, tic: str):

        dados_drop = await self.drop_columns(tic=tic)

        loader = DataFrameLoader(dados_drop, page_content_column="datas")

        dados_load = loader.load()

        return dados_load

    async def coletando_dados_tickers(self):

        resutado_ticks = await asyncio.gather(
            *[self.transformer_loader(tic=tic) for tic in self.tics]
        )

        return resutado_ticks
