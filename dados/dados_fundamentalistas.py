import pandas as pd


class DadosFundamentalistas:
    def __init__(
        self, tic: str, data_inicio: str | None = None, data_fim: str | None = None
    ):
        self.tic = tic
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def dados_dre(
        self, tic: str, data_inicio: str | None = None, data_fim: str | None = None
    ) -> pd.DataFrame:
        
        dados_dre = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/dre.csv"
        )

        dados_tic = dados_dre[dados_dre["tic"] == tic].copy()

        dados_tic["datas"] = pd.to_datetime(dados_tic["datas"], format="%d/%m/%Y")

        if "Unnamed: 0" in dados_tic.columns:

            dados_tic = dados_tic.drop(columns="Unnamed: 0")

        if data_inicio:
            dados_tic = dados_tic[dados_tic["datas"] >= data_inicio]
        if data_fim:
            dados_tic = dados_tic[dados_tic["datas"] <= data_fim]
        return dados_tic

    def dados_capex(
        self, tic: str, data_inicio: str | None = None, data_fim: str | None = None
    ) -> pd.DataFrame:
        dados_capex = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/capex.csv"
        )
        dados_capex_tic = dados_capex[dados_capex["tic"] == tic].copy()
        dados_capex_tic["datas"] = pd.to_datetime(
            dados_capex_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_capex_tic.columns:
            dados_capex_tic = dados_capex_tic.drop(columns="Unnamed: 0")
        if data_inicio:
            dados_capex_tic = dados_capex_tic[dados_capex_tic["datas"] >= data_inicio]
        if data_fim:
            dados_capex_tic = dados_capex_tic[dados_capex_tic["datas"] <= data_fim]
        return dados_capex_tic

    def dados_fluxo_caixa(
        self, tic: str, data_inicio: str | None = None, data_fim: str | None = None
    ) -> pd.DataFrame:
        dados_fluxo_caixa = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/fluxo_caixa.csv"
        )
        dados_fluxo_caixa_tic = dados_fluxo_caixa[
            dados_fluxo_caixa["tic"] == tic
        ].copy()
        dados_fluxo_caixa_tic["datas"] = pd.to_datetime(
            dados_fluxo_caixa_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_fluxo_caixa_tic.columns:
            dados_fluxo_caixa_tic = dados_fluxo_caixa_tic.drop(columns="Unnamed: 0")
        if data_inicio:
            dados_fluxo_caixa_tic = dados_fluxo_caixa_tic[
                dados_fluxo_caixa_tic["datas"] >= data_inicio
            ]
        if data_fim:
            dados_fluxo_caixa_tic = dados_fluxo_caixa_tic[
                dados_fluxo_caixa_tic["datas"] <= data_fim
            ]
        return dados_fluxo_caixa_tic

    def dados_precos_relativos(
        self, tic: str, data_inicio: str | None = None, data_fim: str | None = None
    ) -> pd.DataFrame:
        dados_precos_relativos = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/precos_relativos.csv"
        )
        dados_precos_relativos_tic = dados_precos_relativos[
            dados_precos_relativos["tic"] == tic
        ][1:].copy()
        dados_precos_relativos_tic["datas"] = pd.to_datetime(
            dados_precos_relativos_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_precos_relativos_tic.columns:
            dados_precos_relativos_tic = dados_precos_relativos_tic.drop(
                columns="Unnamed: 0"
            )
        if data_inicio:
            dados_precos_relativos_tic = dados_precos_relativos_tic[
                dados_precos_relativos_tic["datas"] >= data_inicio
            ]
        if data_fim:
            dados_precos_relativos_tic = dados_precos_relativos_tic[
                dados_precos_relativos_tic["datas"] <= data_fim
            ]
        return dados_precos_relativos_tic

    def dados_resumo_balanco(
        self, tic: str, data_inicio: str | None = None, data_fim: str | None = None
    ) -> pd.DataFrame:
        dados_resumo_balanco = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/resumo_balanco.csv"
        )
        dados_resumo_balanco_tic = dados_resumo_balanco[
            dados_resumo_balanco["tic"] == tic
        ].copy()
        dados_resumo_balanco_tic["datas"] = pd.to_datetime(
            dados_resumo_balanco_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_resumo_balanco_tic.columns:
            dados_resumo_balanco_tic = dados_resumo_balanco_tic.drop(
                columns="Unnamed: 0"
            )
        if data_inicio:
            dados_resumo_balanco_tic = dados_resumo_balanco_tic[
                dados_resumo_balanco_tic["datas"] >= data_inicio
            ]
        if data_fim:
            dados_resumo_balanco_tic = dados_resumo_balanco_tic[
                dados_resumo_balanco_tic["datas"] <= data_fim
            ]
        return dados_resumo_balanco_tic

    def dados_retornos_margens(
        self, tic: str, data_inicio: str | None = None, data_fim: str | None = None
    ) -> pd.DataFrame:
        dados_retornos_margens = pd.read_csv(
            "https://raw.githubusercontent.com/Jeferson100/fundamentalist-stock-brazil/main/dados/retornos_margens.csv"
        )
        dados_retornos_margens_tic = dados_retornos_margens[
            dados_retornos_margens["tic"] == tic
        ].copy()
        dados_retornos_margens_tic["datas"] = pd.to_datetime(
            dados_retornos_margens_tic["datas"], format="%d/%m/%Y"
        )

        if "Unnamed: 0" in dados_retornos_margens_tic.columns:
            dados_retornos_margens_tic = dados_retornos_margens_tic.drop(
                columns="Unnamed: 0"
            )
        if data_inicio:
            dados_retornos_margens_tic = dados_retornos_margens_tic[
                dados_retornos_margens_tic["datas"] >= data_inicio
            ]
        if data_fim:
            dados_retornos_margens_tic = dados_retornos_margens_tic[
                dados_retornos_margens_tic["datas"] <= data_fim
            ]
        return dados_retornos_margens_tic

    def dados_fundamentalistas_completo(self) -> pd.DataFrame:
        dados_dre = self.dados_dre(self.tic, self.data_inicio, self.data_fim)
        dados_capex = self.dados_capex(self.tic, self.data_inicio, self.data_fim)
        dados_fluxo_caixa = self.dados_fluxo_caixa(
            self.tic, self.data_inicio, self.data_fim
        )
        dados_precos_relativos = self.dados_precos_relativos(
            self.tic, self.data_inicio, self.data_fim
        )
        dados_resumo_balanco = self.dados_resumo_balanco(
            self.tic, self.data_inicio, self.data_fim
        )
        dados_retornos_margens = self.dados_retornos_margens(
            self.tic, self.data_inicio, self.data_fim
        )
        dados_completo = pd.concat(
            [
                dados_dre,
                dados_capex,
                dados_fluxo_caixa,
                dados_precos_relativos,
                dados_resumo_balanco,
                dados_retornos_margens,
            ],
            axis=1,
        )
        dados_completo = dados_completo.loc[:, ~dados_completo.columns.duplicated()]
        return dados_completo
