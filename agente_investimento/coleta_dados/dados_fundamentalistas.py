import asyncio
import io
import warnings
from typing import Optional

import aiohttp
import pandas as pd

from .verificador_ticks import VerificadorTicks

warnings.filterwarnings("ignore")


class DadosFundamentalistas:
    def __init__(
        self,
        tic: str,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
    ):
        if VerificadorTicks(tic).verificando_ticks():
            self.tic = tic
        else:
            raise ValueError(
                f"O ticker {tic} não existe ou não está disponível em nossa base."
            )

        self.data_inicio = data_inicio
        self.data_fim = data_fim

    async def dados_dre(self) -> pd.DataFrame:
        url = "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/dre.csv"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()

        try:
            dados_dre: pd.DataFrame = pd.read_csv(io.StringIO(content))
        except pd.errors.EmptyDataError:
            print("Erro ao ler {}".format(url))
            return pd.DataFrame()

        # Filtra pelos dados do ticker
        dados_tic = dados_dre[dados_dre["tic"] == self.tic].copy()

        # Converte a coluna "datas" para datetime
        dados_tic["datas"] = pd.to_datetime(dados_tic["datas"], format="%d/%m/%Y")

        # Remove coluna "Unnamed: 0", se existir
        if "Unnamed: 0" in dados_tic.columns:
            dados_tic = dados_tic.drop(columns="Unnamed: 0")

        # Aplica os filtros de data, se definidos
        if self.data_inicio:
            dados_tic = dados_tic[dados_tic["datas"] >= self.data_inicio]
        if self.data_fim:
            dados_tic = dados_tic[dados_tic["datas"] <= self.data_fim]

        return dados_tic

    async def dados_capex(self) -> pd.DataFrame:
        url = "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/capex.csv"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        try:
            dados_capex = pd.read_csv(io.StringIO(content))
        except pd.errors.EmptyDataError: 
            print("Erro ao ler {}".format(url))
            return pd.DataFrame()
        dados_capex_tic = dados_capex[dados_capex["tic"] == self.tic].copy()
        dados_capex_tic["datas"] = pd.to_datetime(
            dados_capex_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_capex_tic.columns:
            dados_capex_tic = dados_capex_tic.drop(columns="Unnamed: 0")
        if self.data_inicio:
            dados_capex_tic = dados_capex_tic[
                dados_capex_tic["datas"] >= self.data_inicio
            ]
        if self.data_fim:
            dados_capex_tic = dados_capex_tic[dados_capex_tic["datas"] <= self.data_fim]
        return dados_capex_tic

    async def dados_fluxo_caixa(self) -> pd.DataFrame:
        url = "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/fluxo_caixa.csv"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        try:
            dados_fluxo_caixa = pd.read_csv(io.StringIO(content))
        except pd.errors.EmptyDataError:
            print("Erro ao ler {}".format(url))
            return pd.DataFrame()

        dados_fluxo_caixa_tic = dados_fluxo_caixa[
            dados_fluxo_caixa["tic"] == self.tic
        ].copy()
        dados_fluxo_caixa_tic["datas"] = pd.to_datetime(
            dados_fluxo_caixa_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_fluxo_caixa_tic.columns:
            dados_fluxo_caixa_tic = dados_fluxo_caixa_tic.drop(columns="Unnamed: 0")
        if self.data_inicio:
            dados_fluxo_caixa_tic = dados_fluxo_caixa_tic[
                dados_fluxo_caixa_tic["datas"] >= self.data_inicio
            ]
        if self.data_fim:
            dados_fluxo_caixa_tic = dados_fluxo_caixa_tic[
                dados_fluxo_caixa_tic["datas"] <= self.data_fim
            ]
        return dados_fluxo_caixa_tic

    async def dados_precos_relativos(self) -> pd.DataFrame:
        url = "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/precos_relativos.csv"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        try:
            dados_precos_relativos = pd.read_csv(io.StringIO(content))
        except pd.errors.EmptyDataError:
            print("Erro ao ler {}".format(url))
            return pd.DataFrame()

        dados_precos_relativos_tic = dados_precos_relativos[
            dados_precos_relativos["tic"] == self.tic
        ][1:].copy()
        dados_precos_relativos_tic["datas"] = pd.to_datetime(
            dados_precos_relativos_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_precos_relativos_tic.columns:
            dados_precos_relativos_tic = dados_precos_relativos_tic.drop(
                columns="Unnamed: 0"
            )
        if self.data_inicio:
            dados_precos_relativos_tic = dados_precos_relativos_tic[
                dados_precos_relativos_tic["datas"] >= self.data_inicio
            ]
        if self.data_fim:
            dados_precos_relativos_tic = dados_precos_relativos_tic[
                dados_precos_relativos_tic["datas"] <= self.data_fim
            ]
        return dados_precos_relativos_tic

    async def dados_resumo_balanco(self) -> pd.DataFrame:
        url = "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/resumo_balanco.csv"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        try:
            dados_resumo_balanco = pd.read_csv(io.StringIO(content))
        except pd.errors.EmptyDataError:
            print("Erro ao ler {}".format(url))
            return pd.DataFrame()

        dados_resumo_balanco_tic = dados_resumo_balanco[
            dados_resumo_balanco["tic"] == self.tic
        ].copy()
        dados_resumo_balanco_tic["datas"] = pd.to_datetime(
            dados_resumo_balanco_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_resumo_balanco_tic.columns:
            dados_resumo_balanco_tic = dados_resumo_balanco_tic.drop(
                columns="Unnamed: 0"
            )
        if self.data_inicio:
            dados_resumo_balanco_tic = dados_resumo_balanco_tic[
                dados_resumo_balanco_tic["datas"] >= self.data_inicio
            ]
        if self.data_fim:
            dados_resumo_balanco_tic = dados_resumo_balanco_tic[
                dados_resumo_balanco_tic["datas"] <= self.data_fim
            ]
        return dados_resumo_balanco_tic

    async def dados_retornos_margens(self) -> pd.DataFrame:
        url = "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/retornos_margens.csv"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        try:
            dados_retornos_margens = pd.read_csv(io.StringIO(content))
        except pd.errors.EmptyDataError:
            print("Erro ao ler {}".format(url))
            return pd.DataFrame()

        dados_retornos_margens_tic = dados_retornos_margens[
            dados_retornos_margens["tic"] == self.tic
        ].copy()
        dados_retornos_margens_tic["datas"] = pd.to_datetime(
            dados_retornos_margens_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_retornos_margens_tic.columns:
            dados_retornos_margens_tic = dados_retornos_margens_tic.drop(
                columns="Unnamed: 0"
            )
        if self.data_inicio:
            dados_retornos_margens_tic = dados_retornos_margens_tic[
                dados_retornos_margens_tic["datas"] >= self.data_inicio
            ]
        if self.data_fim:
            dados_retornos_margens_tic = dados_retornos_margens_tic[
                dados_retornos_margens_tic["datas"] <= self.data_fim
            ]
        return dados_retornos_margens_tic

    async def dados_fundamentalistas_completo(self) -> pd.DataFrame:
        resultados = await asyncio.gather(
            self.dados_dre(),
            self.dados_capex(),
            self.dados_fluxo_caixa(),
            self.dados_precos_relativos(),
            self.dados_resumo_balanco(),
            self.dados_retornos_margens(),
        )
        dataframes = {
        'dados_dre': resultados[0],
        'dados_capex': resultados[1],
        'dados_fluxo_caixa': resultados[2],
        'dados_precos_relativos': resultados[3],
        'dados_resumo_balanco': resultados[4],
        'dados_retornos_margens': resultados[5]
    }
    
        dataframes_validos = {nome: df for nome, df in dataframes.items() if not df.empty}
    
        if not dataframes_validos:
            print("Aviso: Todos os DataFrames estão vazios")
            return pd.DataFrame()

        try:
            resultado = list(dataframes_validos.values())[0]
            
            for df in list(dataframes_validos.values())[1:]:
                resultado = resultado.merge(df, on=["datas", "tic"], how='outer')
            
            resultado = resultado.loc[:, ~resultado.columns.duplicated()]
            return resultado
        
        except Exception as e:
            print(f"Erro ao realizar merge dos dados: {str(e)}")
            return pd.DataFrame()
