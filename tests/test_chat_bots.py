import unittest
from unittest.mock import patch, MagicMock
import pytest
import datetime
import os
from pydantic import SecretStr
from langchain.schema import Document


from chat_bots import (
    ChatAnaliseTecnica,
    ChatFundamentalistas,
    ChatLimpaResposta,
    ChatValuation,
    ChatSentimento,
    ChatTradutor,
)


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

        self.dados_valuation = {
            "precos_atual_valuations": "40.0",
            "indicadores_valuation_fluxo": "50.0",
            "valuation_metodo_gordon": "20.0",
            "valuation_fluxo_caixa": "30.0",
        }

        self.dados_sentimento = """"
         
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

    @patch("chat_bots.ChatFundamentalistas")
    def test_chat_fundamentalistas(self, mock_chat_fundamentalistas: MagicMock) -> None:
        """Testa a função ChatFundamentalistas com diferentes queries."""
        mock_chat_fundamentalistas.return_value = "Resposta simulada"
        for query in [
            f"Como está a saúde financeira da {self.ticker}",
            f"Qual a tendência dos resultados da {self.ticker}",
            f"Análise dos indicadores fundamentalistas da {self.ticker}",
        ]:
            result = ChatFundamentalistas(
                query=query,
                dados=[doc.page_content for doc in self.dados_fundamentalistas],
                api_secret=SecretStr(self.api_secret_groq or ""),
                modelo_llm="qwen-qwq-32b",
            )

            # Verificações
            self.assertIsNotNone(result)
            self.assertIsInstance(result, str)

    @patch("chat_bots.ChatLimpaResposta")
    def test_chat_limpa_resposta(self, mock_limpa_resposta: MagicMock) -> None:
        """Testa a função ChatLimpaResposta com diferentes entradas."""
        # Definir comportamento do mock

        mock_limpa_resposta.return_value = (
            "Notícia resumida sobre Petrobras e oportunidades na Argentina."
        )

        # Testar função
        result = ChatLimpaResposta(
            query=self.exemplo_noticia,
            ticke=self.ticker,
            api_secret=SecretStr(self.api_secret_groq or ""),
        )

        # Verificações
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertLess(len(result), len(self.exemplo_noticia))
        self.assertTrue("Petrobras" in mock_limpa_resposta.return_value)

    @patch("tratando_dados.TratandoDadosIndicadores")
    @patch("chat_bots.ChatAnaliseTecnica")
    def test_chat_analise_tecnica(
        self, mock_limpa_resposta: MagicMock, mock_tratando_dados_indicadores: MagicMock
    ) -> None:
        """Testa a função ChatAnaliseTecnica."""
        mock_tratando_dados_indicadores.return_value = self.dados_indicadores
        mock_limpa_resposta.return_value = "Resposta limpa de análise técnica"

        query = f"Faça uma análise técnica da {self.ticker}"
        result = ChatAnaliseTecnica(
            query=query,
            dados=[doc.page_content for doc in self.dados_indicadores],
            api_secret=SecretStr(self.api_secret_groq or ""),
            modelo_llm="qwen-qwq-32b",
        )

        # Verificações
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    @patch("tratando_dados.TratandoDadosValuation")
    @patch("chat_bots.ChatValuation")
    def test_chat_valuation(
        self, mock_chat_valuation: MagicMock, mock_tratando_dados_valuation: MagicMock
    ) -> None:
        """Testa a função ChatValuation."""
        # Configurar mocks
        mock_tratando_dados_valuation.return_value = self.dados_valuation
        mock_chat_valuation.return_value = "Resposta limpa de valuation"
        query = f"Qual o valor de mercado da {self.ticker}"
        result = ChatValuation(
            query=query,
            precos_atual_valuations=self.dados_valuation["precos_atual_valuations"],
            indicadores_valuation_fluxo=self.dados_valuation[
                "indicadores_valuation_fluxo"
            ],
            valuation_metodo_gordon=self.dados_valuation["valuation_metodo_gordon"],
            valuation_fluxo_caixa=self.dados_valuation["valuation_fluxo_caixa"],
            api_secret=SecretStr(self.api_secret_groq or ""),
            modelo_llm="qwen-qwq-32b",
        )

        # Verificações
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    @patch("tratando_dados.TratarDadosNoticias")
    @patch("chat_bots.ChatSentimento")
    def test_chat_sentimento(
        self, mock_chat_sentimento: MagicMock, mock_tratar_dados_noticias: MagicMock
    ) -> None:
        """Testa a função ChatSentimento."""
        # Configurar mocks
        mock_tratar_dados_noticias.return_value = self.dados_sentimento
        mock_chat_sentimento.return_value = "Resposta limpa de sentimento"

        query = f"Qual o sentimento das notícias sobre a {self.ticker}"
        result = ChatSentimento(
            query=query,
            noticia=self.dados_sentimento,
            api_secret=SecretStr(self.api_secret_groq or ""),
            modelo_llm="qwen-qwq-32b",
        )

        # Verificações
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

    @patch("chat_bots.ChatTradutor")
    def test_chat_tradutor(self, mock_chat_tradutor: MagicMock) -> None:
        """Testa a função ChatTradutor."""
        # Configurar mock
        mock_chat_tradutor.return_value = "Translated text"

        result = ChatTradutor(
            query=self.dados_tradutor,
            api_secret=SecretStr(self.api_secret_groq or ""),
            modelo_llm="qwen-qwq-32b",
        )

        # Verificações
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
