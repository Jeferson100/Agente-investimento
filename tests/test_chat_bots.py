import datetime
import os
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio

import pytest
from agente_investimento import (
    ChatAnaliseTecnicaComparacao,
    ChatFundamentalistasComparacaoAsync,
    ChatSentimentoComparacao,
    ChatValuationComparacao,
)
from langchain.schema import Document
from pydantic import SecretStr


class TestChatBots(unittest.TestCase):
    def setUp(self) -> None:
        """Configuração inicial para os testes."""
        self.api_key_serper = os.getenv("API_KEY_SERPER")
        self.api_secret_groq = os.getenv("GROQ_API_KEY")

        # Verificar se as chaves de API estão disponíveis
        if not self.api_secret_groq:
            pytest.skip(
                "API secret groq não definida. Configure a variável de ambiente GROQ_API_KEY"
            )

        # Dados comuns para testes
        self.ticker = "PETR4"
        self.data_inicio = (
            datetime.datetime.now() - datetime.timedelta(days=360)
        ).strftime("%Y-%m-%d")

        self.dados_fundamentalistas = [
            # Simular os documentos carregados pelo loader
            Document(
                page_content="2023-01-01",
                metadata={"ativo_total": 100000000, "passivo_total": 60000000},
            ),
            Document(
                page_content="2023-04-01",
                metadata={"ativo_total": 110000000, "passivo_total": 65000000},
            ),
            Document(
                page_content="2023-07-01",
                metadata={"ativo_total": 120000000, "passivo_total": 70000000},
            ),
        ]

        # Configurar mocks
        self.dados_indicadores = [
            Document(
                page_content="2023-01-01", metadata={"media_movel_21": 20.5, "rsi": 55}
            ),
            Document(
                page_content="2023-01-02", metadata={"media_movel_21": 21.0, "rsi": 60}
            ),
            Document(
                page_content="2023-01-03", metadata={"media_movel_21": 21.5, "rsi": 65}
            ),
        ]

        
        self.valuation_metodo_gordon = {'AMER3.SA': ('|    | ticker   |   dividendo_mediano |   g_sust |   juros_livre |   beta |   capm |   valuation_acao |   preco_atual |   diferenca |\n|---:|:---------|--------------------:|---------:|--------------:|-------:|-------:|-----------------:|--------------:|------------:|\n|  0 | AMER3.SA |              11.591 |        0 |        0.1473 | -0.301 | 0.1653 |            70.13 |          5.26 |     1233.22 |',
        70.13)}
        
        self.valution_metodo_fluxo_caixa = {'AMER3.SA': ('|    |   data |   receita_ano |     ebit_ano |   imposto_ano |   capex_ano |   depreciacao_ano |   ebit_ajustado |   fluxo_caixa |   valor_presente_fluxo |\n|---:|-------:|--------------:|-------------:|--------------:|------------:|------------------:|----------------:|--------------:|-----------------------:|\n|  0 |   2025 |   1.33076e+10 | -2.67217e+09 |  -7.64776e+08 | 5.15005e+08 |       4.29901e+09 |     2.39161e+09 |   1.87661e+09 |            1.35887e+09 |\n|  1 |   2026 |   1.23418e+10 | -2.47824e+09 |  -7.09273e+08 | 4.77629e+08 |       3.98701e+09 |     2.21804e+09 |   1.74041e+09 |            9.12567e+08 |\n|  2 |   2027 |   1.14461e+10 | -2.29838e+09 |  -6.57798e+08 | 4.42966e+08 |       3.69765e+09 |     2.05707e+09 |   1.6141e+09  |            6.12844e+08 |\n|  3 |   2028 |   1.06154e+10 | -2.13158e+09 |  -6.10058e+08 | 4.10818e+08 |       3.4293e+09  |     1.90778e+09 |   1.49696e+09 |            4.11562e+08 |\n|  4 |   2029 |   9.84503e+09 | -1.97688e+09 |  -5.65784e+08 | 3.81003e+08 |       3.18042e+09 |     1.76932e+09 |   1.38832e+09 |            2.76389e+08 |',
        {'Preco do fluxo de caixa para AMER3.SA': 17.12})}
        

        self.dados_sentimento = """
         
            \nNew notice\nPetrobras anuncia novos investimentos
            \nNew notice\nResultados trimestrais superam expectativas
            \nNew notice\nPetrobras tem queda de 20% nos lucros
            \nNew notice\nGoverno brasileiro aprova aumento de 10% nos combustíveis
        
        """

        self.dados_tradutor = """
        Petrobras explores, produces, and sells oil and gas in Brazil and internationally. The company operates through three segments: Exploration and Production; Refining, 
        Transportation and Marketing; and Gas and Power. The Exploration and Production segment explores, develops, and produces crude oil, natural gas liquids, and natural gas primarily for 
        supplies to the domestic refineries. The Refining, Transportation and Marketing segment engages in the refining, logistics, transport, acquisition, and exports of crude oil; and production of fertilizers, 
        as well as holding interests in petrochemical companies. The Gas and Power segment is involved in the logistic and trading of natural gas and electricity; transportation and trading of LNG; 
        generation of electricity through thermoelectric power plants; renewable energy businesses; low carbon services; and natural gas processing business, as well as production of biodiesel and its co-products. 
        The company also engages in prospecting, drilling, refining, processing, trading, and transporting crude oil from producing onshore and offshore oil fields, and shale or other rocks, as well as oil products,
        natural gas

        """

        # Exemplo de notícia para teste
        self.exemplo_noticia = """Petrobras (PETR4) vê oportunidades na Argentina devido ao gás de Vaca
Ela acrescentou que a empresa também poderia procurar oportunidades de petróleo na Argentina
11/03/2025 12h45  • Atualizado 4 horas atrás
Publicidade
A Petrobras (PETR3; PETR4) está analisando oportunidades potenciais na Argentina, enquanto avança em projetos na Colômbia e na África, disse a diretora de exploração e produção Sylvia dos Anjos nesta terça-feira.
O gás da região de Vaca Muerta seria interessante para a Petrobras, já que um gasoduto que contecta Argentina, Bolívia e Brasil poderia ser usado para transportá-lo, afirmou a executiva, nos bastidores da conferência CERAWeek, em Houston.
Ela acrescentou que a empresa também poderia procurar oportunidades de petróleo na Argentina, já que a Petrobras busca ativamente reabastecer suas reservas de petróleo e enfreta dificuldades para obter licenças ambientais para perfurar em novas fronteiras no Brasil.
BAIXAR AGORA
Na Colômbia, a empresa está atualmente elaborando o plano de desenvolvimento de um projeto maritimo onde foram descobertos 6 trilhões de pés cúbicos de gás, enquanto aguarda uma licença do governo.
Cerca de 13 milhões de metros cúbicos por dia de gás do projeto seriam fornecidos à Colômbia por meio de um gasoduto, disse Anjos.
Na África, a empresa espera que poços exploratórios sejam perfurados entre julho e agosto em um bloco no qual tem participação em São Tomé e Príncipe.
Outra área na África do Sul deve ser perfurada no segundo semestre, acrescentou a executiva.
## Tópicos relacionados
© 2000-2025 InfoMoney. Todos os direitos reservados.
O InfoMoney preza a qualidade da informação e atesta a apuração de todo o conteúdo produzido por sua equipe, ressaltando, no entanto, que não faz qualquer tipo de recomendação de investimento, não se responsabilizando por perdas, danos (diretos, indiretos e incidentais), custos e lucros cessantes."""


    async def test_chat_fundamentalistas_sync(self) -> None:
        """Testa a função ChatFundamentalistas de forma síncrona."""
        # Mock para simular resposta
        with patch("agente_investimento.ChatFundamentalistas") as mock_chat:
            mock_chat.return_value = "Resposta simulada"
            
            query = f"Como está a saúde financeira da {self.ticker}"
            result = await ChatFundamentalistasComparacaoAsync(
                query=query,
                dados=[doc.page_content for doc in self.dados_fundamentalistas],
                api_secret=SecretStr(self.api_secret_groq or ""),
            )
            
            # Como é uma coroutine, precisamos aguardar
            result = asyncio.run(result)
            
            # Verificações
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)

    async def test_chat_analise_tecnica_sync(self) -> None:
        """Testa a função ChatAnaliseTecnica de forma síncrona."""
        with patch("agente_investimento.tratando_dados.TratandoDadosIndicadores") as mock_tratando:
            with patch("agente_investimento.ChatAnaliseTecnica") as mock_chat:
                mock_tratando.return_value = self.dados_indicadores
                mock_chat.return_value = "Resposta limpa de análise técnica"

                query = f"Faça uma análise técnica da {self.ticker}"
                result = await ChatAnaliseTecnicaComparacao( 
                    query=query,
                    dados=[doc.page_content for doc in self.dados_indicadores],
                    api_secret=SecretStr(self.api_secret_groq or ""),
                )

                # Verificações
                self.assertIsNotNone(result)
                self.assertIsInstance(result, str)
                

    async def test_chat_valuation_sync(self) -> None:
        """Testa a função ChatValuation de forma síncrona."""
        with patch("agente_investimento.tratando_dados.TratandoDadosValuation") as mock_tratando:
            with patch("agente_investimento.ChatValuation") as mock_chat:
                mock_tratando.return_value = self.valuation_metodo_gordon
                mock_chat.return_value = "Resposta limpa de valuation"
                
                query = f"Qual o valor de mercado da {self.ticker}"
                result = await ChatValuationComparacao(
                    query=query,
                    valuation_metodo_gordon=self.valuation_metodo_gordon,
                    valuation_fluxo_caixa=self.valution_metodo_fluxo_caixa,
                    api_secret=SecretStr(self.api_secret_groq or ""),
                )

                # Verificações
                self.assertIsNotNone(result)
                self.assertIsInstance(result, str)

    async def test_chat_sentimento_sync(self) -> None:
        """Testa a função ChatSentimento de forma síncrona."""
        with patch("agente_investimento.tratando_dados.TratarDadosNoticias") as mock_tratando:
            with patch("agente_investimento.ChatSentimento") as mock_chat:
                mock_tratando.return_value = self.dados_sentimento
                mock_chat.return_value = "Resposta limpa de sentimento"

                query = f"Qual o sentimento das notícias sobre a {self.ticker}"
                result = await ChatSentimentoComparacao(
                    query=query,
                    noticia=self.dados_sentimento,
                    api_secret=SecretStr(self.api_secret_groq or ""),
                )

                # Verificações
                self.assertIsNotNone(result)
                self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()

