import numpy as np
from typing import Dict
import yfinance as yf
import pandas as pd
from .calculo_wacc import CalculoWACC 
from .variacao_receita import VariacaoReceita
from .outros_ativos_nao_operecionais import OutrosAtivosNaoOperacionais
from .passivos_menos_divida import PassivoTotalMenosDivida
from .necessidade_capital_giro import NecessidadeCapitalGiro
from typing import Union

class IndicadoresFinanceiros:
    def __init__(self, ticker: str, margem_ebit_mediana: bool = True, deflacionar_receita: bool = True, percentual_imposto_mediana: bool = True, depreciacao_capex_mediana: bool = True, capex_receita_mediana: bool = True):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker=self.ticker)
        self.financials = self.stock.financials
        self.balance_sheet = self.stock.balance_sheet
        self.cashflow = self.stock.cashflow
        self.margem_ebit_mediana =  margem_ebit_mediana
        self.deflacionar_receita = deflacionar_receita
        self.percentual_imposto_mediana = percentual_imposto_mediana
        self.depreciacao_capex_mediana = depreciacao_capex_mediana
        self.capex_receita_mediana = capex_receita_mediana
       
    def ultima_receita(self) -> float:
        receita_ano = self.financials
        if isinstance(receita_ano, pd.DataFrame):
            if 'Total Revenue' in receita_ano.index:
                receita_ano = receita_ano.loc['Total Revenue'].iloc[0]
            else:
                receita_ano = 0
            if isinstance(receita_ano, pd.Series):
                return float(receita_ano.iloc[0])
            return float(receita_ano)
        return 0.0
    
    def variacao_receita_ultimos_anos(self) -> Dict[str, float]:
        variacao_receita = VariacaoReceita(ticker=self.ticker, deflacionar_receita=self.deflacionar_receita)   
        porcentagem_receita = variacao_receita.receita_crescimento_metricas()
        return porcentagem_receita
    
    def ebit(self) -> Union[pd.Series[float], pd.DataFrame]:
        ebit_ultimos_anos = self.financials
        
        if isinstance(ebit_ultimos_anos, pd.DataFrame):
            if 'EBIT' in ebit_ultimos_anos.index:
                return ebit_ultimos_anos.loc['EBIT']
            elif 'Pretax Income' in ebit_ultimos_anos.index:
                return ebit_ultimos_anos.loc['Pretax Income']
            else:
                # Caso não haja a chave 'EBIT', retornamos uma Series vazia (ou com outro valor padrão)
                return pd.Series(dtype=float)
        
        elif isinstance(ebit_ultimos_anos, pd.Series):
            return ebit_ultimos_anos
        
        # Se self.financials não for DataFrame nem Series, retorne uma Series vazia
        return pd.Series(dtype=float)
    
    def receita(self) -> Union[pd.Series[float], pd.DataFrame]:
        receita_ultimos_anos = self.financials
        
        if isinstance(receita_ultimos_anos, pd.DataFrame):
            if 'Total Revenue' in receita_ultimos_anos.index:
                return receita_ultimos_anos.loc['Total Revenue']
            else:
                # Caso não haja a chave 'Total Revenue', retornamos uma Series vazia (ou com outro valor padrão)
                return pd.Series(dtype=float)
        
        elif isinstance(receita_ultimos_anos, pd.Series):
            return receita_ultimos_anos
        
        # Se self.financials não for DataFrame nem Series, retorne uma Series vazia
        return pd.Series(dtype=float)
         
    def margem_ebit(self) -> float:
        ebit_ultimos_anos: Union[pd.Series[float], pd.DataFrame] = self.ebit()
        receita_ultimos_anos: Union[pd.Series[float], pd.DataFrame] = self.receita()
        try:
            margem_ebit = ebit_ultimos_anos / receita_ultimos_anos
            if self.margem_ebit_mediana:
                margem_ebit = round(margem_ebit.median(),2)
            else:
                margem_ebit = round(margem_ebit.mean(),2) 
            if isinstance(margem_ebit, pd.Series):
                return float(margem_ebit.iloc[0])
            return float(margem_ebit)
        except ZeroDivisionError:
            return 0.0
        
    def imposto(self) -> Union[pd.Series[float], pd.DataFrame]:
        imposto_ultimos_anos = self.financials
        if isinstance(imposto_ultimos_anos, pd.DataFrame):
            if 'Tax Provision' in imposto_ultimos_anos.index:
                return imposto_ultimos_anos.loc['Tax Provision']
            else:
                return pd.Series(dtype=float)
        elif isinstance(imposto_ultimos_anos, pd.Series):
            return imposto_ultimos_anos
        return pd.Series(dtype=float)
    
    
    def percentual_imposto(self) -> float:
        ebit_ultimos_anos: Union[pd.Series[float], pd.DataFrame] = self.ebit()
        imposto_ultimos_anos: Union[pd.Series[float], pd.DataFrame] = self.imposto()
        
        tax_ebit = imposto_ultimos_anos / ebit_ultimos_anos

        # Se for DataFrame, tenta reduzir para Series
        if isinstance(tax_ebit, pd.DataFrame):
            tax_ebit = tax_ebit.squeeze()  # Converte DataFrame em Series, se possível

        # Se for Series, aplique os filtros e agregue o valor
        if isinstance(tax_ebit, pd.Series):
            # Filtra para valores positivos
            tax_ebit = tax_ebit[tax_ebit > 0]
            # Se a Series estiver vazia, podemos definir como 0.0 ou outro valor padrão
            if tax_ebit.empty:
                resultado = 0.30
            else:
                # Escolhe mediana ou média conforme a flag percentual_imposto_mediana
                resultado = tax_ebit.median() if self.percentual_imposto_mediana else tax_ebit.mean()
            return round(float(resultado), 4)
        
        # Caso tax_ebit já seja um float (ou outro tipo numérico)
        return round(float(tax_ebit), 4)

    def depreciacao_amortizacao(self) -> Union[pd.Series[float], pd.DataFrame]:
        depreciacao_amortizacao = self.cashflow
        if isinstance(depreciacao_amortizacao, pd.DataFrame):
            if 'Depreciation And Amortization' in depreciacao_amortizacao.index:
                return depreciacao_amortizacao.loc['Depreciation And Amortization']
            else:
                return pd.Series(dtype=float)
        elif isinstance(depreciacao_amortizacao, pd.Series):
            return depreciacao_amortizacao
        return pd.Series(dtype=float)
    
    def capex(self) -> Union[pd.Series[float], pd.DataFrame]:
        capex = self.cashflow
        if isinstance(capex, pd.DataFrame):
            if 'Capital Expenditure' in capex.index:
                return capex.loc['Capital Expenditure']
            else:
                return pd.Series(dtype=float)
        elif isinstance(capex, pd.Series):
            return capex
        return pd.Series(dtype=float)
        
    
    def depreciacao_capex(self) -> float:
        depreciacao_amortizacao: Union[pd.Series[float], pd.DataFrame] = self.depreciacao_amortizacao()
        capex: Union[pd.Series[float], pd.DataFrame] = self.capex()
        
        depre_capex = depreciacao_amortizacao/capex
        
        if isinstance(depre_capex, pd.DataFrame):
            depre_capex = depre_capex.squeeze()
        
        if self.depreciacao_capex_mediana:
            return abs(depre_capex.median())
        else:
            return abs(depre_capex.mean())
        
    def capex_receita(self) -> float:
        capex = self.capex()
        receita = self.receita()
        
        capex_recei = capex / receita
        
        if isinstance(capex_recei, pd.DataFrame):
            capex_recei = capex_recei.squeeze()
        
        if self.capex_receita_mediana:
            return abs(capex_recei.median())
        else:
            return abs(capex_recei.mean())
    
    def wacc(self) -> float:
        wac = CalculoWACC(ticker=self.ticker)
        valor_wacc = wac.wacc()
        return valor_wacc
    
    def quantidade_acoes(self) -> float:
        quantida_acoe = self.stock.quarterly_balance_sheet
        if isinstance(quantida_acoe, pd.DataFrame):
            quantida_acoe = quantida_acoe.squeeze()
        if 'Share Issued' in quantida_acoe.index:
            quantida_acoe = quantida_acoe.loc['Share Issued'][0]
        else:
            quantida_acoe = 0.0
        return quantida_acoe
    
    def divida_total(self) -> float:
        divida_total = self.stock.get_balancesheet(freq='yearly')
        if isinstance(divida_total, pd.DataFrame):
            if 'TotalDebt' in divida_total.index:
                divida_total = divida_total.loc['TotalDebt'][0]
            else:
                divida_total = 0.0
            if isinstance(divida_total, pd.Series):
                    return float(divida_total.iloc[0])
            return float(divida_total)
        return 0.0
            
    
    def caixa_equivalentes_caixa(self) -> float:
        caixa = self.stock.get_balancesheet(freq='yearly')
        if isinstance(caixa, pd.DataFrame):
            if 'CashCashEquivalentsAndShortTermInvestments' in caixa.index:
                caixa = caixa.loc['CashCashEquivalentsAndShortTermInvestments'][0]
            else:
                caixa = 0.0
            if isinstance(caixa, pd.Series):
                return float(caixa.iloc[0])
            return float(caixa)
        return 0.0
    
    def outros_ativos_nao_operacionais(self) -> float:
        outros_nao_ope = OutrosAtivosNaoOperacionais(self.ticker)
        valor_outros = outros_nao_ope.valor_outros_ativos_nao_operacionais()
        return valor_outros
    
    
    def passivos_totais_divida(self) -> float:
        passivo_nao_circulante = PassivoTotalMenosDivida(self.ticker)
        valor_passivo_nao_circulante = passivo_nao_circulante.valor_total_passivo_menos_divida()
        return valor_passivo_nao_circulante
    
    def necessidade_capital_giro(self) -> float:
        necessidade_capital = NecessidadeCapitalGiro(self.ticker)
        valor_necesseidade_capital = necessidade_capital.valor_necessidade_capital_giro()
        return valor_necesseidade_capital
                
    